//! Turn a parsed Toolpath into a Three.js Object3D for the scene.
//!
//! Uses LineSegments2 / LineMaterial so segments render with a real pixel
//! width — plain LineBasicMaterial ignores linewidth on most browsers and
//! produces 1px hairlines that are virtually invisible at typical zoom.
//!
//! Coloring: rapids orange, feed moves green, cutting moves (spindle on
//! during a feed) red. G-code mm are scaled to meters; the caller positions
//! the wrapping group at the workpiece origin and applies any URDF / world
//! frame rotation.

import * as THREE from "three";
import { LineMaterial } from "three/addons/lines/LineMaterial.js";
import { LineSegments2 } from "three/addons/lines/LineSegments2.js";
import { LineSegmentsGeometry } from "three/addons/lines/LineSegmentsGeometry.js";
import type { Toolpath } from "./parser";

const COLOR_RAPID: [number, number, number] = [0.94, 0.63, 0.31];
const COLOR_FEED: [number, number, number] = [0.44, 0.84, 0.55];
const COLOR_CUTTING: [number, number, number] = [0.95, 0.38, 0.38];

export interface ToolpathLines {
  object: LineSegments2;
  material: LineMaterial;
}

export function buildToolpathLines(
  toolpath: Toolpath,
  pixelLineWidth = 3
): ToolpathLines {
  const n = toolpath.moves.length;
  const positions = new Float32Array(n * 6);
  const colors = new Float32Array(n * 6);

  for (let i = 0; i < n; i++) {
    const move = toolpath.moves[i];
    const c =
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
    colors[o + 0] = c[0]; colors[o + 1] = c[1]; colors[o + 2] = c[2];
    colors[o + 3] = c[0]; colors[o + 4] = c[1]; colors[o + 5] = c[2];
  }

  const geom = new LineSegmentsGeometry();
  geom.setPositions(positions);
  geom.setColors(colors);

  const material = new LineMaterial({
    linewidth: pixelLineWidth, // pixels
    vertexColors: true,
    worldUnits: false,
    resolution: new THREE.Vector2(1, 1), // caller updates on mount + resize
    transparent: true,
    depthTest: true,
  });

  const object = new LineSegments2(geom, material);
  object.computeLineDistances();
  return { object, material };
}

