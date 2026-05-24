import { useEffect, useRef } from "react";
import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { TransformControls } from "three/addons/controls/TransformControls.js";
import URDFLoader, { URDFRobot } from "urdf-loader";
import { JointVec, useStore } from "../state/store";
import { kin } from "../rpc/kinematics";

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

    // Floor grid + world axes
    const grid = new THREE.GridHelper(2, 20, 0x3a4257, 0x232838);
    scene.add(grid);
    const worldAxes = new THREE.AxesHelper(0.12);
    scene.add(worldAxes);

    // TCP gizmo — a small sphere with a TransformControls handle. The user
    // drags the colored arrows to move it; we run IK on each new position.
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
    // In three.js >= r163 TransformControls no longer extends Object3D;
    // its visual handles live in a separate root accessed via getHelper().
    const gizmoHelper = tcontrols.getHelper();
    scene.add(gizmoHelper);

    // Track dragging ourselves — the new TransformControls' `dragging`
    // property is unreliable across versions.
    let isDragging = false;
    tcontrols.addEventListener("dragging-changed", (e: any) => {
      isDragging = !!e.value;
      controls.enabled = !isDragging;
      if (!isDragging) {
        // On release, snap the gizmo to wherever the arm actually ended up,
        // so subsequent drags start from a real TCP position.
        snapGizmoToTcp();
      }
    });

    // ---- IK dispatch (single in-flight, last write wins) -----------------
    let ikInFlight = false;
    let ikPending: THREE.Vector3 | null = null;

    const tmpVec = new THREE.Vector3();
    const REACH_TOL = 0.05; // 50 mm — don't move the arm into a clamped pose

    const dispatchIK = async () => {
      const robot = robotRef.current;
      if (!robot || ikInFlight || !ikPending) return;

      ikInFlight = true;
      const targetWorld = ikPending;
      ikPending = null;

      try {
        const local = robot.worldToLocal(tmpVec.copy(targetWorld));
        const seed = useStore.getState().q;
        const result = await kin.ik([local.x, local.y, local.z], seed);

        // Only follow the cursor when the arm can plausibly reach it.
        // Otherwise we'd lock the joints at a limit and the next drag would
        // use a degenerate seed and the arm would appear "frozen".
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

    // ---- Load URDF --------------------------------------------------------
    const loader = new URDFLoader();
    loader.load("/ar3.urdf", (robot: URDFRobot) => {
      robot.rotation.x = -Math.PI / 2; // Z-up → Y-up
      scene.add(robot);
      robotRef.current = robot;

      const tcp = robot.links?.["link6"];
      if (tcp) tcp.add(new THREE.AxesHelper(0.08));

      const q = useStore.getState().q;
      q.forEach((v, i) => robot.setJointValue(`joint${i + 1}`, v));

      // Place gizmo on TCP and reveal it.
      snapGizmoToTcp();
      gizmoProxy.visible = true;
    });

    // Place the gizmo proxy on the current TCP world position.
    const snapGizmoToTcp = () => {
      const robot = robotRef.current;
      if (!robot) return;
      const tcp = robot.links?.["link6"];
      if (!tcp) return;
      tcp.updateMatrixWorld(true);
      tcp.getWorldPosition(gizmoProxy.position);
    };

    // React to joint changes from sliders, Home button, or IK results.
    // After every joint update, if we're not actively dragging, also pull
    // the gizmo to the new TCP — keeps the two visually locked together.
    const unsub = useStore.subscribe((state) => {
      const robot = robotRef.current;
      if (!robot) return;
      state.q.forEach((v, i) => robot.setJointValue(`joint${i + 1}`, v));
      if (!isDragging) snapGizmoToTcp();
    });

    // Animation
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
      // tcontrols.dispose() in three r163+ calls this.traverse() which doesn't
      // exist on the refactored class — skip it; the GC handles memory.
      renderer.dispose();
      if (renderer.domElement.parentNode === container) {
        container.removeChild(renderer.domElement);
      }
    };
  }, []);

  return <div ref={containerRef} className="viewer" />;
}
