import { useEffect, useRef } from "react";
import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { TransformControls } from "three/addons/controls/TransformControls.js";
import { STLLoader } from "three/addons/loaders/STLLoader.js";
import URDFLoader, { URDFRobot } from "urdf-loader";
import { JointVec, useStore } from "../state/store";
import { kin } from "../rpc/kinematics";

const CAMERA_HOME = new THREE.Vector3(1.1, 0.8, 1.1);
const CAMERA_TARGET = new THREE.Vector3(0, 0.35, 0);

// Approximate work envelope of the AR3 (~720 mm from shoulder per CAD).
// Shoulder height tracks the real base_link height; see public/ar3.urdf.
const REACH_RADIUS = 0.72;
const SHOULDER_HEIGHT = 0.17;

// The community URDF (ongdexter/ar3_core) names joints joint_1..joint_6 and
// the TCP link link_6. urdf-loader exposes them under the same names.
const JOINT_NAMES = ["joint_1", "joint_2", "joint_3", "joint_4", "joint_5", "joint_6"];
const TCP_LINK = "link_6";

export function Viewer() {
  const containerRef = useRef<HTMLDivElement>(null);
  const robotRef = useRef<URDFRobot | null>(null);

  useEffect(() => {
    const container = containerRef.current!;
    const width = container.clientWidth;
    const height = container.clientHeight;

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x0e1117);

    const camera = new THREE.PerspectiveCamera(45, width / height, 0.01, 100);
    camera.position.copy(CAMERA_HOME);

    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(window.devicePixelRatio);
    container.appendChild(renderer.domElement);

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.target.copy(CAMERA_TARGET);
    controls.enableDamping = true;
    controls.dampingFactor = 0.08;
    controls.update();

    // Lighting
    scene.add(new THREE.AmbientLight(0xffffff, 0.55));
    const key = new THREE.DirectionalLight(0xffffff, 1.0);
    key.position.set(3, 5, 4);
    scene.add(key);
    const rim = new THREE.DirectionalLight(0x8aa6ff, 0.35);
    rim.position.set(-3, 2, -3);
    scene.add(rim);

    // Floor grid (toggleable)
    const grid = new THREE.GridHelper(2, 20, 0x3a4257, 0x232838);
    scene.add(grid);
    scene.add(new THREE.AxesHelper(0.12));

    // Workspace reach dome — translucent hemisphere centered at the shoulder.
    // Approximate envelope, not the exact reachable manifold.
    const domeGroup = new THREE.Group();
    const domeMesh = new THREE.Mesh(
      new THREE.SphereGeometry(
        REACH_RADIUS,
        32,
        16,
        0,
        Math.PI * 2,
        0,
        Math.PI / 2
      ),
      new THREE.MeshBasicMaterial({
        color: 0x4c9aff,
        transparent: true,
        opacity: 0.06,
        side: THREE.DoubleSide,
        depthWrite: false,
      })
    );
    const domeWire = new THREE.Mesh(
      new THREE.SphereGeometry(
        REACH_RADIUS,
        16,
        8,
        0,
        Math.PI * 2,
        0,
        Math.PI / 2
      ),
      new THREE.MeshBasicMaterial({
        color: 0x4c9aff,
        wireframe: true,
        transparent: true,
        opacity: 0.18,
      })
    );
    domeGroup.add(domeMesh);
    domeGroup.add(domeWire);
    domeGroup.position.y = SHOULDER_HEIGHT;
    scene.add(domeGroup);

    // TCP proxy + TransformControls (drag the colored arrows).
    const gizmoProxy = new THREE.Mesh(
      new THREE.SphereGeometry(0.022, 20, 20),
      new THREE.MeshStandardMaterial({
        color: 0xf0a050,
        emissive: 0xf0a050,
        emissiveIntensity: 0.25,
        roughness: 0.4,
      })
    );
    gizmoProxy.visible = false;
    scene.add(gizmoProxy);

    const tcontrols = new TransformControls(camera, renderer.domElement);
    tcontrols.setMode("translate");
    tcontrols.setSize(0.85);
    tcontrols.attach(gizmoProxy);
    const gizmoHelper = tcontrols.getHelper();
    scene.add(gizmoHelper);

    let isDragging = false;
    tcontrols.addEventListener("dragging-changed", (e: any) => {
      isDragging = !!e.value;
      controls.enabled = !isDragging;
      if (!isDragging) snapGizmoToTcp();
    });

    // ---- IK dispatch -----------------------------------------------------
    let ikInFlight = false;
    let ikPending: THREE.Vector3 | null = null;
    const tmpVec = new THREE.Vector3();
    const REACH_TOL = 0.05;

    const dispatchIK = async () => {
      const robot = robotRef.current;
      if (!robot || ikInFlight || !ikPending) return;

      ikInFlight = true;
      const targetWorld = ikPending;
      ikPending = null;

      try {
        const local = robot.worldToLocal(tmpVec.copy(targetWorld));
        const seed = useStore.getState().q;
        const timeout = new Promise<never>((_, rej) =>
          setTimeout(() => rej(new Error("sidecar unresponsive")), 1500)
        );
        const result = await Promise.race([
          kin.ik([local.x, local.y, local.z], seed),
          timeout,
        ]);
        if (result.residual < REACH_TOL) {
          useStore.getState().setAllJoints(result.q as JointVec);
        }
        useStore.getState().setIkStatus({
          residual: result.residual,
          ok: result.ok,
          clamped: result.clamped,
        });
      } catch (err) {
        useStore.getState().setIkStatus({
          residual: NaN,
          ok: false,
          clamped: false,
          error: String(err),
        });
      } finally {
        ikInFlight = false;
        if (ikPending) dispatchIK();
      }
    };

    tcontrols.addEventListener("objectChange", () => {
      ikPending = gizmoProxy.position.clone();
      dispatchIK();
    });

    // ---- URDF load --------------------------------------------------------
    const loader = new URDFLoader();
    // urdf-loader's default mesh callback uses dynamic imports for STLLoader
    // that don't always resolve under Vite. Wire STL explicitly so the
    // ar3_core meshes are guaranteed to load.
    loader.loadMeshCb = (path, manager, done) => {
      const ext = path.split(".").pop()?.toLowerCase();
      if (ext === "stl") {
        new STLLoader(manager).load(
          path,
          (geom) => {
            geom.computeVertexNormals();
            const mesh = new THREE.Mesh(geom);
            done(mesh);
          },
          undefined,
          (err) => {
            console.error("[ar3] STL load failed:", path, err);
            done(null as unknown as THREE.Object3D, err as Error);
          }
        );
      } else {
        console.warn("[ar3] no loader for mesh extension:", path);
        done(new THREE.Object3D());
      }
    };
    loader.load("/ar3.urdf", (robot: URDFRobot) => {
      robot.rotation.x = -Math.PI / 2;
      scene.add(robot);
      robotRef.current = robot;

      const tcpLink = robot.links?.[TCP_LINK];
      if (tcpLink) tcpLink.add(new THREE.AxesHelper(0.08));

      useStore
        .getState()
        .q.forEach((v, i) => robot.setJointValue(JOINT_NAMES[i], v));

      snapGizmoToTcp();
      pushTcpToStore();
      gizmoProxy.visible = true;
    });

    const snapGizmoToTcp = () => {
      const robot = robotRef.current;
      if (!robot) return;
      const tcp = robot.links?.[TCP_LINK];
      if (!tcp) return;
      tcp.updateMatrixWorld(true);
      tcp.getWorldPosition(gizmoProxy.position);
    };

    // Push TCP position in URDF coords to the store so panels can display it.
    const tcpWorld = new THREE.Vector3();
    const tcpLocal = new THREE.Vector3();
    const pushTcpToStore = () => {
      const robot = robotRef.current;
      if (!robot) return;
      const tcp = robot.links?.[TCP_LINK];
      if (!tcp) return;
      tcp.updateMatrixWorld(true);
      tcp.getWorldPosition(tcpWorld);
      tcpLocal.copy(tcpWorld);
      robot.worldToLocal(tcpLocal);
      const prev = useStore.getState().tcp;
      const next: [number, number, number] = [tcpLocal.x, tcpLocal.y, tcpLocal.z];
      if (
        !prev ||
        Math.abs(prev[0] - next[0]) > 1e-5 ||
        Math.abs(prev[1] - next[1]) > 1e-5 ||
        Math.abs(prev[2] - next[2]) > 1e-5
      ) {
        useStore.getState().setTcp(next);
      }
    };

    // ---- React to store changes ------------------------------------------
    let lastQ = useStore.getState().q;
    let lastViewer = useStore.getState().viewer;
    const unsub = useStore.subscribe((state) => {
      const robot = robotRef.current;
      if (robot && state.q !== lastQ) {
        lastQ = state.q;
        state.q.forEach((v, i) => robot.setJointValue(JOINT_NAMES[i], v));
        pushTcpToStore();
        if (!isDragging) snapGizmoToTcp();
      }
      if (state.viewer !== lastViewer) {
        if (state.viewer.showGrid !== lastViewer.showGrid) {
          grid.visible = state.viewer.showGrid;
        }
        if (state.viewer.showWorkspace !== lastViewer.showWorkspace) {
          domeGroup.visible = state.viewer.showWorkspace;
        }
        if (state.viewer.resetViewTick !== lastViewer.resetViewTick) {
          camera.position.copy(CAMERA_HOME);
          controls.target.copy(CAMERA_TARGET);
          controls.update();
        }
        lastViewer = state.viewer;
      }
    });

    // Initial viewer settings sync (in case persisted state differs).
    grid.visible = lastViewer.showGrid;
    domeGroup.visible = lastViewer.showWorkspace;

    // Animate
    let raf = 0;
    const animate = () => {
      raf = requestAnimationFrame(animate);
      controls.update();
      if (!isDragging) snapGizmoToTcp();
      renderer.render(scene, camera);
    };
    animate();

    // Resize
    const ro = new ResizeObserver(() => {
      const w = container.clientWidth;
      const h = container.clientHeight;
      if (w === 0 || h === 0) return;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    });
    ro.observe(container);

    return () => {
      cancelAnimationFrame(raf);
      ro.disconnect();
      unsub();
      try { tcontrols.detach(); } catch {}
      try { scene.remove(gizmoHelper); } catch {}
      renderer.dispose();
      if (renderer.domElement.parentNode === container) {
        container.removeChild(renderer.domElement);
      }
    };
  }, []);

  return (
    <div ref={containerRef} className="viewer">
      <ViewerToolbar />
    </div>
  );
}

function ViewerToolbar() {
  const showGrid = useStore((s) => s.viewer.showGrid);
  const showWorkspace = useStore((s) => s.viewer.showWorkspace);
  const toggleGrid = useStore((s) => s.toggleGrid);
  const toggleWorkspace = useStore((s) => s.toggleWorkspace);
  const requestResetView = useStore((s) => s.requestResetView);

  return (
    <div className="viewer-toolbar">
      <button
        className={`vt ${showGrid ? "vt-on" : ""}`}
        onClick={toggleGrid}
        title="Toggle floor grid"
      >
        grid
      </button>
      <button
        className={`vt ${showWorkspace ? "vt-on" : ""}`}
        onClick={toggleWorkspace}
        title="Toggle workspace reach dome"
      >
        reach
      </button>
      <button className="vt" onClick={requestResetView} title="Reset camera">
        reset view
      </button>
    </div>
  );
}
