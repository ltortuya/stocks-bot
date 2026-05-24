//! Simulated transport. No I/O, no latency, no failure modes.
//!
//! Echoes whatever joint state is sent and stores spindle state. Used as
//! the default backend so the rest of the app can be developed against
//! the same `Transport` trait that real hardware will implement.

use anyhow::{anyhow, Result};

use super::{Transport, TransportKind};

pub struct SimTransport {
    connected: bool,
    estopped: bool,
    q: [f64; 6],
    spindle_on: bool,
    spindle_rpm: u32,
}

impl SimTransport {
    pub fn new() -> Self {
        Self {
            connected: false,
            estopped: false,
            q: [0.0; 6],
            spindle_on: false,
            spindle_rpm: 0,
        }
    }

    fn require_armed(&self) -> Result<()> {
        if !self.connected {
            return Err(anyhow!("transport not connected"));
        }
        if self.estopped {
            return Err(anyhow!("e-stopped — reconnect to clear"));
        }
        Ok(())
    }
}

impl Transport for SimTransport {
    fn kind(&self) -> TransportKind {
        TransportKind::Sim
    }
    fn is_connected(&self) -> bool {
        self.connected
    }
    fn is_estopped(&self) -> bool {
        self.estopped
    }

    fn connect(&mut self) -> Result<()> {
        self.connected = true;
        self.estopped = false;
        Ok(())
    }
    fn disconnect(&mut self) -> Result<()> {
        self.connected = false;
        Ok(())
    }

    fn send_joint_state(&mut self, q: [f64; 6]) -> Result<()> {
        self.require_armed()?;
        self.q = q;
        Ok(())
    }
    fn read_joint_state(&self) -> Result<[f64; 6]> {
        Ok(self.q)
    }

    fn set_spindle(&mut self, on: bool, rpm: Option<u32>) -> Result<()> {
        self.require_armed()?;
        self.spindle_on = on;
        if let Some(r) = rpm {
            self.spindle_rpm = r;
        }
        Ok(())
    }
    fn spindle_state(&self) -> (bool, u32) {
        (self.spindle_on, self.spindle_rpm)
    }

    fn estop(&mut self) -> Result<()> {
        self.estopped = true;
        self.spindle_on = false;
        Ok(())
    }
}
