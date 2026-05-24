import { useEffect, useRef } from "react";
import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
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
    const canvas = renderer.domElement;
    container.appendChild(canvas);

    const controls = new OrbitControls(camera, canvas);
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
    scene.add(new THREE.GridHelper(2, 20, 0x3a4257, 0x232838));
    scene.add(new THREE.AxesHelper(0.12));

    // ---- Drag handle ------------------------------------------------------
    // A sphere positioned at the TCP. Click + drag to move the arm. We avoid
    // three.js' TransformControls because its dispose / dragging-state APIs
    // have been unstable across recent releases.
    const handle = new THREE.Mesh(
      new THREE.SphereGeometry(0.028, 24, 24),
      new THREE.MeshStandardMaterial({
        color: 0xf0a050,
        emissive: 0xf0a050,
        emissiveIntensity: 0.22,
        roughness: 0.35,
      })
    );
    handle.visible = false;
    scene.add(handle);

    // ---- IK dispatch (single in-flight, last write wins) -----------------
    let ikInFlight = false;
    let ikPending: THREE.Vector3 | null = null;
    const tmpVec = new THREE.Vector3();
    const REACH_TOL = 0.05; // 50 mm — don't lock arm at a joint limit

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

    // ---- Pointer handling on the handle ----------------------------------
    const raycaster = new THREE.Raycaster();
    const pointer = new THREE.Vector2();
    const dragPlane = new THREE.Plane();
    const intersection = new THREE.Vector3();
    const camDir = new THREE.Vector3();

    let isDragging = false;
    let isHovering = false;

    const updatePointer = (e: PointerEvent) => {
      const rect = canvas.getBoundingClientRect();
      pointer.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
      pointer.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;
    };

    const handleHit = (): boolean => {
      raycaster.setFromCamera(pointer, camera);
      return raycaster.intersectObject(handle, false).length > 0;
    };

    const setHover = (on: boolean) => {
      if (on === isHovering) return;
      isHovering = on;
      canvas.style.cursor = on ? "grab" : "";
      (handle.material as THREE.MeshStandardMaterial).emissiveIntensity =
        on ? 0.55 : 0.22;
    };

    const onPointerDown = (e: PointerEvent) => {
      if (e.button !== 0) return; // left click only
      updatePointer(e);
      if (!handleHit()) return;

      isDragging = true;
      controls.enabled = false;
      canvas.style.cursor = "grabbing";
      try { canvas.setPointerCapture(e.pointerId); } catch {}

      // Drag in a plane parallel to the camera, through the handle.
      camera.getWorldDirection(camDir);
      dragPlane.setFromNormalAndCoplanarPoint(camDir, handle.position);
    };

    const onPointerMove = (e: PointerEvent) => {
      updatePointer(e);

      if (!isDragging) {
        setHover(handleHit());
        return;
      }

      raycaster.setFromCamera(pointer, camera);
      if (raycaster.ray.intersectPlane(dragPlane, intersection)) {
        ikPending = intersection.clone();
        dispatchIK();
      }
    };

    const endDrag = (e?: PointerEvent) => {
      if (!isDragging) return;
      isDragging = false;
      controls.enabled = true;
      canvas.style.cursor = isHovering ? "grab" : "";
      if (e) {
        try { canvas.releasePointerCapture(e.pointerId); } catch {}
      }
      snapHandleToTcp();
    };

    canvas.addEventListener("pointerdown", onPointerDown);
    canvas.addEventListener("pointermove", onPointerMove);
    canvas.addEventListener("pointerup", endDrag);
    canvas.addEventListener("pointercancel", endDrag);
    // Catch the case where the pointer is released outside the window.
    window.addEventListener("blur", () => endDrag());

    // ---- URDF load --------------------------------------------------------
    const loader = new URDFLoader();
    loader.load("/ar3.urdf", (robot: URDFRobot) => {
      robot.rotation.x = -Math.PI / 2; // Z-up → Y-up
      scene.add(robot);
      robotRef.current = robot;

      const tcp = robot.links?.["link6"];
      if (tcp) tcp.add(new THREE.AxesHelper(0.08));

      useStore
        .getState()
        .q.forEach((v, i) => robot.setJointValue(`joint${i + 1}`, v));

      snapHandleToTcp();
      handle.visible = true;
    });

    const snapHandleToTcp = () => {
      const robot = robotRef.current;
      if (!robot) return;
      const tcp = robot.links?.["link6"];
      if (!tcp) return;
      tcp.updateMatrixWorld(true);
      tcp.getWorldPosition(handle.position);
    };

    // React to joint changes from sliders, Home, or IK results.
    const unsub = useStore.subscribe((state) => {
      const robot = robotRef.current;
      if (!robot) return;
      state.q.forEach((v, i) => robot.setJointValue(`joint${i + 1}`, v));
      if (!isDragging) snapHandleToTcp();
    });

    // Animate
    let raf = 0;
    const animate = () => {
      raf = requestAnimationFrame(animate);
      controls.update();
      if (!isDragging) snapHandleToTcp();
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
      canvas.removeEventListener("pointerdown", onPointerDown);
      canvas.removeEventListener("pointermove", onPointerMove);
      canvas.removeEventListener("pointerup", endDrag);
      canvas.removeEventListener("pointercancel", endDrag);
      renderer.dispose();
      if (canvas.parentNode === container) container.removeChild(canvas);
    };
  }, []);

  return <div ref={containerRef} className="viewer" />;
}
