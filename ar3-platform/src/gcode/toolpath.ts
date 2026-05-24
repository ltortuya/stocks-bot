//! Turn a parsed Toolpath into a Three.js LineSegments object for the scene.
//!
//! Coloring: rapids orange, feed moves green, cutting moves (spindle on
//! during a feed) red. G-code mm are scaled to meters; the caller is
//! responsible for placing the group at the workpiece origin and applying
//! any URDF / world frame rotation.

import * as THREE from "three";
import type { Toolpath } from "./parser";

const COLOR_RAPID = new THREE.Color(0xf0a050);
const COLOR_FEED = new THREE.Color(0x6fd58b);
const COLOR_CUTTING = new THREE.Color(0xf06060);

export function buildToolpathLines(toolpath: Toolpath): THREE.LineSegments {
  const n = toolpath.moves.length;
  const positions = new Float32Array(n * 6);
  const colors = new Float32Array(n * 6);

  for (let i = 0; i < n; i++) {
    const move = toolpath.moves[i];
    const color =
      move.spindleOn && move.type === "feed"
        ? COLOR_CUTTING
        : move.type === "rapid"
        ? COLOR_RAPID
        : COLOR_FEED;
    const o = i * 6;
    positions[o + 0] = move.from[0] / 1000;
    positions[o + 1] = move.from[1] / 1000;
    positions[o + 2] = move.from[2] / 1000;
    positions[o + 3] = move.to[0] / 1000;
    positions[o + 4] = move.to[1] / 1000;
    positions[o + 5] = move.to[2] / 1000;
    colors[o + 0] = color.r;
    colors[o + 1] = color.g;
    colors[o + 2] = color.b;
    colors[o + 3] = color.r;
    colors[o + 4] = color.g;
    colors[o + 5] = color.b;
  }

  const geom = new THREE.BufferGeometry();
  geom.setAttribute("position", new THREE.BufferAttribute(positions, 3));
  geom.setAttribute("color", new THREE.BufferAttribute(colors, 3));

  const mat = new THREE.LineBasicMaterial({
    vertexColors: true,
    transparent: true,
    opacity: 0.95,
  });
  return new THREE.LineSegments(geom, mat);
}
