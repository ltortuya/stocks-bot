//! Minimal G-code parser sufficient for visualizing CAM output.
//!
//! Supports G0/G1 linear motion, G2/G3 arcs (decomposed to line segments
//! in the XY plane), G20/G21 units, G90/G91 absolute/incremental,
//! M3/M5 spindle on/off, F feedrate, S spindle RPM. Comments using
//! `;...` or `(...)` are stripped.
//!
//! All output positions are in millimetres. Execution semantics (G54
//! workpiece offsets, canned cycles, tool changes, etc.) are intentionally
//! ignored — this is a viewer, not a controller.

export type Vec3 = [number, number, number];
export type MoveType = "rapid" | "feed";

export interface Move {
  type: MoveType;
  from: Vec3;
  to: Vec3;
  feed_mm_per_min: number;
  spindleOn: boolean;
  spindleRpm: number;
  line: number; // 1-based source line number for diagnostics
}

export interface Toolpath {
  moves: Move[];
  units: "mm" | "inch";
  bbox_mm: { min: Vec3; max: Vec3 };
  feedLength_mm: number;
  rapidLength_mm: number;
  estimatedTime_s: number;
  warnings: string[];
}

const ARC_SEGMENTS = 24;
const ASSUMED_RAPID_MM_PER_MIN = 5000;

const TOKEN_RE = /([A-Za-z])\s*(-?\d+(?:\.\d+)?)/g;
const COMMENT_PAREN = /\([^)]*\)/g;

interface State {
  pos: Vec3;
  units: "mm" | "inch";
  absolute: boolean;
  feed_mm_per_min: number;
  spindleOn: boolean;
  spindleRpm: number;
  motion: "G0" | "G1" | "G2" | "G3" | null;
}

const dist = (a: Vec3, b: Vec3): number => {
  const dx = b[0] - a[0], dy = b[1] - a[1], dz = b[2] - a[2];
  return Math.sqrt(dx * dx + dy * dy + dz * dz);
};

export function parseGcode(text: string): Toolpath {
  const state: State = {
    pos: [0, 0, 0],
    units: "mm",
    absolute: true,
    feed_mm_per_min: 600,
    spindleOn: false,
    spindleRpm: 0,
    motion: null,
  };
  const moves: Move[] = [];
  const warnings: string[] = [];

  let minX = Infinity, minY = Infinity, minZ = Infinity;
  let maxX = -Infinity, maxY = -Infinity, maxZ = -Infinity;
  let feedLen = 0;
  let rapidLen = 0;

  const grow = (p: Vec3) => {
    if (p[0] < minX) minX = p[0]; if (p[0] > maxX) maxX = p[0];
    if (p[1] < minY) minY = p[1]; if (p[1] > maxY) maxY = p[1];
    if (p[2] < minZ) minZ = p[2]; if (p[2] > maxZ) maxZ = p[2];
  };
  grow(state.pos);

  const lines = text.split(/\r?\n/);
  for (let li = 0; li < lines.length; li++) {
    let raw = lines[li];
    // strip comments
    raw = raw.replace(COMMENT_PAREN, "");
    const semi = raw.indexOf(";");
    if (semi >= 0) raw = raw.slice(0, semi);
    raw = raw.trim();
    if (!raw) continue;

    const codes: string[] = [];
    const args: Record<string, number> = {};
    TOKEN_RE.lastIndex = 0;
    let m: RegExpExecArray | null;
    while ((m = TOKEN_RE.exec(raw)) !== null) {
      const letter = m[1].toUpperCase();
      const num = parseFloat(m[2]);
      if (letter === "G" || letter === "M") {
        codes.push(`${letter}${Math.floor(num)}`);
      } else {
        args[letter] = num;
      }
    }

    // Non-motion G / M codes
    for (const code of codes) {
      switch (code) {
        case "G20": state.units = "inch"; break;
        case "G21": state.units = "mm"; break;
        case "G90": state.absolute = true; break;
        case "G91": state.absolute = false; break;
        case "G0":
        case "G1":
        case "G2":
        case "G3":
          state.motion = code as State["motion"];
          break;
        case "M3":
        case "M03": state.spindleOn = true; break;
        case "M5":
        case "M05": state.spindleOn = false; break;
        case "M2":
        case "M02":
        case "M30": break; // end of program — fine to ignore here
        case "M6":
        case "M06":
          warnings.push(`line ${li + 1}: tool change (M6) ignored`);
          break;
        case "G17":
        case "G54":
        case "G40":
        case "G49":
          // Common defaults — silently accept.
          break;
        default:
          if (code.startsWith("G") || code.startsWith("M")) {
            warnings.push(`line ${li + 1}: ${code} not supported, ignoring`);
          }
      }
    }

    if ("F" in args) state.feed_mm_per_min = args.F;
    if ("S" in args) state.spindleRpm = args.S;

    // Emit motion if a motion modal is active and any axis word was given.
    if (
      state.motion &&
      ("X" in args || "Y" in args || "Z" in args ||
       "I" in args || "J" in args || "K" in args)
    ) {
      const scale = state.units === "inch" ? 25.4 : 1;
      const from: Vec3 = [state.pos[0], state.pos[1], state.pos[2]];
      const to: Vec3 = [from[0], from[1], from[2]];

      if (state.absolute) {
        if ("X" in args) to[0] = args.X * scale;
        if ("Y" in args) to[1] = args.Y * scale;
        if ("Z" in args) to[2] = args.Z * scale;
      } else {
        if ("X" in args) to[0] += args.X * scale;
        if ("Y" in args) to[1] += args.Y * scale;
        if ("Z" in args) to[2] += args.Z * scale;
      }

      const isArc = state.motion === "G2" || state.motion === "G3";
      const moveType: MoveType = state.motion === "G0" ? "rapid" : "feed";

      const emit = (a: Vec3, b: Vec3) => {
        if (a[0] === b[0] && a[1] === b[1] && a[2] === b[2]) return;
        moves.push({
          type: moveType,
          from: a,
          to: b,
          feed_mm_per_min: state.feed_mm_per_min,
          spindleOn: state.spindleOn,
          spindleRpm: state.spindleRpm,
          line: li + 1,
        });
        grow(b);
        const d = dist(a, b);
        if (moveType === "rapid") rapidLen += d;
        else feedLen += d;
      };

      if (isArc) {
        // I/J/K are center offsets from start. K (Z) is unusual for an
        // XY-plane arc; we'd need G18/G19 plane select for proper support.
        const cx = from[0] + (args.I ?? 0) * scale;
        const cy = from[1] + (args.J ?? 0) * scale;
        const cw = state.motion === "G2";
        const r = Math.hypot(from[0] - cx, from[1] - cy);
        if (!isFinite(r) || r === 0) {
          warnings.push(`line ${li + 1}: zero-radius arc, drawing chord`);
          emit(from, to);
        } else {
          const a0 = Math.atan2(from[1] - cy, from[0] - cx);
          const a1 = Math.atan2(to[1] - cy, to[0] - cx);
          let sweep = a1 - a0;
          if (cw) {
            if (sweep > 0) sweep -= 2 * Math.PI;
            if (sweep === 0) sweep = -2 * Math.PI;
          } else {
            if (sweep < 0) sweep += 2 * Math.PI;
            if (sweep === 0) sweep = 2 * Math.PI;
          }
          let prev: Vec3 = from;
          for (let s = 1; s <= ARC_SEGMENTS; s++) {
            const t = s / ARC_SEGMENTS;
            const ang = a0 + sweep * t;
            const next: Vec3 = [
              cx + r * Math.cos(ang),
              cy + r * Math.sin(ang),
              from[2] + (to[2] - from[2]) * t,
            ];
            emit(prev, next);
            prev = next;
          }
        }
      } else {
        emit(from, to);
      }
      state.pos = to;
    }
  }

  if (moves.length === 0) {
    minX = minY = minZ = 0;
    maxX = maxY = maxZ = 0;
  }

  const feedTime = state.feed_mm_per_min > 0
    ? (feedLen / state.feed_mm_per_min) * 60
    : 0;
  const rapidTime = (rapidLen / ASSUMED_RAPID_MM_PER_MIN) * 60;

  return {
    moves,
    units: state.units,
    bbox_mm: { min: [minX, minY, minZ], max: [maxX, maxY, maxZ] },
    feedLength_mm: feedLen,
    rapidLength_mm: rapidLen,
    estimatedTime_s: feedTime + rapidTime,
    warnings,
  };
}
