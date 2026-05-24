mod sidecar;

use serde::Serialize;
use tauri::Manager;

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

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .setup(|app| {
            let handle = app.handle().clone();
            let sidecar = sidecar::SidecarState::spawn(&handle)
                .expect("failed to spawn sidecar");
            app.manage(sidecar);
            Ok(())
        })
        .invoke_handler(tauri::generate_handler![sidecar_health, sidecar_call])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
