import { useEffect, useRef } from "react";
import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { TransformControls } from "three/addons/controls/TransformControls.js";
import URDFLoader, { URDFRobot } from "urdf-loader";
import { JointVec, useStore } from "../state/store";
import { kin } from "../rpc/kinematics";

// Minimal debug logger — keep it on while we hunt the IK freeze.
const dbg = (...args: unknown[]) => console.log("[ar3]", ...args);

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
    camera.position.set(1.0, 0.9, 1.0);

    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(window.devicePixelRatio);
    container.appendChild(renderer.domElement);

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.target.set(0, 0.4, 0);
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

    scene.add(new THREE.GridHelper(2, 20, 0x3a4257, 0x232838));
    scene.add(new THREE.AxesHelper(0.12));

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

    // We track dragging state ourselves — three.js's `dragging` property has
    // been unreliable across versions.
    let isDragging = false;
    tcontrols.addEventListener("dragging-changed", (e: any) => {
      isDragging = !!e.value;
      controls.enabled = !isDragging;
      dbg("dragging-changed", { isDragging });
      if (!isDragging) snapGizmoToTcp();
    });

    // ---- IK dispatch -----------------------------------------------------
    let ikInFlight = false;
    let ikPending: THREE.Vector3 | null = null;
    let ikSeq = 0;
    const tmpVec = new THREE.Vector3();
    const REACH_TOL = 0.05;

    const dispatchIK = async () => {
      const robot = robotRef.current;
      if (!robot) {
        dbg("dispatchIK: no robot yet");
        return;
      }
      if (ikInFlight) {
        dbg("dispatchIK: already in flight, will retry");
        return;
      }
      if (!ikPending) return;

      ikInFlight = true;
      const seq = ++ikSeq;
      const targetWorld = ikPending;
      ikPending = null;

      try {
        const local = robot.worldToLocal(tmpVec.copy(targetWorld));
        const seed = useStore.getState().q;
        dbg(`IK #${seq} → local`, [local.x.toFixed(3), local.y.toFixed(3), local.z.toFixed(3)]);
        // Safety net: if the sidecar dies entirely the await would never
        // resolve, jamming `ikInFlight` forever. The sidecar already has its
        // own 400ms guard; this 1.5s race only fires if Python crashed.
        const timeout = new Promise<never>((_, rej) =>
          setTimeout(() => rej(new Error("sidecar unresponsive")), 1500)
        );
        const result = await Promise.race([kin.ik([local.x, local.y, local.z], seed), timeout]);
        dbg(`IK #${seq} ✓`, {
          residual_mm: (result.residual * 1000).toFixed(1),
          ok: result.ok,
          clamped: result.clamped,
          applied: result.residual < REACH_TOL,
        });
        if (result.residual < REACH_TOL) {
          useStore.getState().setAllJoints(result.q as JointVec);
        }
        useStore.getState().setIkStatus({
          residual: result.residual,
          ok: result.ok,
          clamped: result.clamped,
        });
      } catch (err) {
        dbg(`IK #${seq} ✗`, String(err));
        useStore.getState().setIkStatus({
          residual: NaN,
          ok: false,
          clamped: false,
          error: String(err),
        });
      } finally {
        ikInFlight = false;
        if (ikPending) {
          dbg("dispatchIK: chaining next");
          dispatchIK();
        }
      }
    };

    tcontrols.addEventListener("objectChange", () => {
      ikPending = gizmoProxy.position.clone();
      dispatchIK();
    });

    // ---- URDF load --------------------------------------------------------
    const loader = new URDFLoader();
    loader.load("/ar3.urdf", (robot: URDFRobot) => {
      robot.rotation.x = -Math.PI / 2;
      scene.add(robot);
      robotRef.current = robot;
      dbg("URDF loaded; joints:", Object.keys(robot.joints || {}));

      const tcp = robot.links?.["link6"];
      if (tcp) tcp.add(new THREE.AxesHelper(0.08));

      useStore
        .getState()
        .q.forEach((v, i) => robot.setJointValue(`joint${i + 1}`, v));
      snapGizmoToTcp();
      gizmoProxy.visible = true;
    });

    const snapGizmoToTcp = () => {
      const robot = robotRef.current;
      if (!robot) return;
      const tcp = robot.links?.["link6"];
      if (!tcp) return;
      tcp.updateMatrixWorld(true);
      tcp.getWorldPosition(gizmoProxy.position);
    };

    const unsub = useStore.subscribe((state) => {
      const robot = robotRef.current;
      if (!robot) return;
      state.q.forEach((v, i) => robot.setJointValue(`joint${i + 1}`, v));
      if (!isDragging) snapGizmoToTcp();
    });

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

  return <div ref={containerRef} className="viewer" />;
}
