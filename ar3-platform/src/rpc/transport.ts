import { invoke } from "@tauri-apps/api/core";
import type { JointVec } from "../state/store";

export type TransportKind = "disconnected" | "sim" | "serial";

export interface TransportStatus {
  kind: TransportKind;
  connected: boolean;
  commanded_q: JointVec | null;
  spindle_on: boolean;
  spindle_rpm: number;
  estopped: boolean;
}

export const transport = {
  status: () => invoke<TransportStatus>("transport_status"),
  connect: () => invoke<TransportStatus>("transport_connect"),
  disconnect: () => invoke<TransportStatus>("transport_disconnect"),
  sendJoints: (q: JointVec) => invoke<void>("transport_send_joints", { q }),
  setSpindle: (on: boolean, rpm?: number) =>
    invoke<TransportStatus>("transport_set_spindle", { on, rpm }),
  estop: () => invoke<TransportStatus>("transport_estop"),
};
