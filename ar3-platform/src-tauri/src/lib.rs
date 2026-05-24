mod sidecar;
mod transport;

use std::sync::Arc;

use serde::Serialize;
use tauri::Manager;
use tokio::sync::Mutex;

use transport::{sim::SimTransport, Transport, TransportStatus};

/// Type-erased transport behind a tokio Mutex. Lets us swap SimTransport for
/// a real SerialTransport at runtime (M6) without changing call sites.
pub type SharedTransport = Arc<Mutex<Box<dyn Transport>>>;

pub struct TransportState(pub SharedTransport);

#[derive(Debug, Serialize)]
pub struct Health {
    pub ok: bool,
    pub version: String,
}

#[tauri::command]
async fn sidecar_health(
    state: tauri::State<'_, sidecar::SidecarState>,
) -> Result<Health, String> {
    let result: serde_json::Value = state
        .call("health", serde_json::json!({}))
        .await
        .map_err(|e| e.to_string())?;

    Ok(Health {
        ok: result
            .get("ok")
            .and_then(|v| v.as_bool())
            .unwrap_or(false),
        version: result
            .get("version")
            .and_then(|v| v.as_str())
            .unwrap_or("unknown")
            .to_string(),
    })
}

/// Generic passthrough: frontend calls any sidecar method by name.
#[tauri::command]
async fn sidecar_call(
    state: tauri::State<'_, sidecar::SidecarState>,
    method: String,
    params: serde_json::Value,
) -> Result<serde_json::Value, String> {
    state.call(&method, params).await.map_err(|e| e.to_string())
}

// ---- Transport commands ----------------------------------------------------

#[tauri::command]
async fn transport_status(
    state: tauri::State<'_, TransportState>,
) -> Result<TransportStatus, String> {
    Ok(state.0.lock().await.status())
}

#[tauri::command]
async fn transport_connect(
    state: tauri::State<'_, TransportState>,
) -> Result<TransportStatus, String> {
    let mut t = state.0.lock().await;
    t.connect().map_err(|e| e.to_string())?;
    Ok(t.status())
}

#[tauri::command]
async fn transport_disconnect(
    state: tauri::State<'_, TransportState>,
) -> Result<TransportStatus, String> {
    let mut t = state.0.lock().await;
    t.disconnect().map_err(|e| e.to_string())?;
    Ok(t.status())
}

#[tauri::command]
async fn transport_send_joints(
    state: tauri::State<'_, TransportState>,
    q: [f64; 6],
) -> Result<(), String> {
    state
        .0
        .lock()
        .await
        .send_joint_state(q)
        .map_err(|e| e.to_string())
}

#[tauri::command]
async fn transport_set_spindle(
    state: tauri::State<'_, TransportState>,
    on: bool,
    rpm: Option<u32>,
) -> Result<TransportStatus, String> {
    let mut t = state.0.lock().await;
    t.set_spindle(on, rpm).map_err(|e| e.to_string())?;
    Ok(t.status())
}

#[tauri::command]
async fn transport_estop(
    state: tauri::State<'_, TransportState>,
) -> Result<TransportStatus, String> {
    let mut t = state.0.lock().await;
    t.estop().map_err(|e| e.to_string())?;
    Ok(t.status())
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .setup(|app| {
            let handle = app.handle().clone();

            let sidecar = sidecar::SidecarState::spawn(&handle)
                .expect("failed to spawn sidecar");
            app.manage(sidecar);

            // Auto-connect the simulated transport so the UI lights up.
            let mut sim = SimTransport::new();
            let _ = sim.connect();
            let transport: SharedTransport = Arc::new(Mutex::new(Box::new(sim)));
            app.manage(TransportState(transport));

            Ok(())
        })
        .invoke_handler(tauri::generate_handler![
            sidecar_health,
            sidecar_call,
            transport_status,
            transport_connect,
            transport_disconnect,
            transport_send_joints,
            transport_set_spindle,
            transport_estop,
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
