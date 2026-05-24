//! Hardware abstraction. The frontend talks to `Transport`; concrete impls
//! decide whether bytes go to a simulated arm, a real AR3 over USB serial,
//! ROS 2, or something else. M4 ships SimTransport only; M6 adds serial.

use anyhow::Result;
use serde::Serialize;

pub mod sim;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize)]
#[serde(rename_all = "lowercase")]
pub enum TransportKind {
    Disconnected,
    Sim,
    Serial,
}

#[derive(Debug, Clone, Serialize)]
pub struct TransportStatus {
    pub kind: TransportKind,
    pub connected: bool,
    pub commanded_q: Option<[f64; 6]>,
    pub spindle_on: bool,
    pub spindle_rpm: u32,
    pub estopped: bool,
}

pub trait Transport: Send + Sync {
    fn kind(&self) -> TransportKind;
    fn is_connected(&self) -> bool;
    fn connect(&mut self) -> Result<()>;
    fn disconnect(&mut self) -> Result<()>;

    /// Push a commanded joint vector to the transport. Implementations may
    /// stream this at high rate (sculpting jobs do hundreds of times per
    /// second); keep the call cheap.
    fn send_joint_state(&mut self, q: [f64; 6]) -> Result<()>;

    /// Last reported joint state. For sim this is whatever was last sent.
    /// For real hardware it will eventually be the encoder reading.
    fn read_joint_state(&self) -> Result<[f64; 6]>;

    /// Spindle control. v1 SimTransport just stores the values.
    fn set_spindle(&mut self, on: bool, rpm: Option<u32>) -> Result<()>;
    fn spindle_state(&self) -> (bool, u32);

    /// Hard stop. Once estopped the transport refuses motion + spindle
    /// commands until a reconnect.
    fn estop(&mut self) -> Result<()>;
    fn is_estopped(&self) -> bool;

    fn status(&self) -> TransportStatus {
        let (on, rpm) = self.spindle_state();
        TransportStatus {
            kind: self.kind(),
            connected: self.is_connected(),
            commanded_q: if self.is_connected() {
                self.read_joint_state().ok()
            } else {
                None
            },
            spindle_on: on,
            spindle_rpm: rpm,
            estopped: self.is_estopped(),
        }
    }
}
