import { useEffect, useRef } from "react";
import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import URDFLoader, { URDFRobot } from "urdf-loader";
import { useStore } from "../state/store";

export function Viewer() {
  const containerRef = useRef<HTMLDivElement>(null);
  const robotRef = useRef<URDFRobot | null>(null);

  useEffect(() => {
    const container = containerRef.current!;
    const width = container.clientWidth;
    const height = container.clientHeight;

    // Scene
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

    // Load URDF
    const loader = new URDFLoader();
    loader.load("/ar3.urdf", (robot: URDFRobot) => {
      // URDF uses Z-up; Three.js uses Y-up.
      robot.rotation.x = -Math.PI / 2;
      scene.add(robot);
      robotRef.current = robot;

      // TCP axes on the end-effector
      const tcp = robot.links?.["link6"];
      if (tcp) tcp.add(new THREE.AxesHelper(0.08));

      // Apply current joint state immediately
      const q = useStore.getState().q;
      q.forEach((v, i) => robot.setJointValue(`joint${i + 1}`, v));
    });

    // React to joint state changes
    const unsub = useStore.subscribe((state) => {
      const robot = robotRef.current;
      if (!robot) return;
      state.q.forEach((v, i) => robot.setJointValue(`joint${i + 1}`, v));
    });

    // Animation
    let raf = 0;
    const animate = () => {
      raf = requestAnimationFrame(animate);
      controls.update();
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
      renderer.dispose();
      if (renderer.domElement.parentNode === container) {
        container.removeChild(renderer.domElement);
      }
    };
  }, []);

  return <div ref={containerRef} className="viewer" />;
}
