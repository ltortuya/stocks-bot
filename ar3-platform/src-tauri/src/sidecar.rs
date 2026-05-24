//! JSON-RPC over stdio client for the Python kinematics sidecar.
//!
//! The sidecar is a Python process launched as a child of this Tauri app.
//! Communication is newline-delimited JSON-RPC 2.0 on stdin/stdout.

use anyhow::{anyhow, Context, Result};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::process::Stdio;
use std::sync::atomic::{AtomicU64, Ordering};
use std::sync::Arc;
use tauri::{AppHandle, Manager};
use tokio::io::{AsyncBufReadExt, AsyncWriteExt, BufReader};
use tokio::process::{Child, ChildStdin, Command};
use tokio::sync::{oneshot, Mutex};

#[derive(Debug, Serialize)]
struct Request<'a> {
    jsonrpc: &'a str,
    id: u64,
    method: &'a str,
    params: serde_json::Value,
}

#[derive(Debug, Deserialize)]
struct Response {
    #[allow(dead_code)]
    jsonrpc: Option<String>,
    id: Option<u64>,
    #[serde(default)]
    result: Option<serde_json::Value>,
    #[serde(default)]
    error: Option<RpcError>,
}

#[derive(Debug, Deserialize)]
struct RpcError {
    code: i32,
    message: String,
}

/// Resolves a project-relative path. Used to find sidecar/server.py and
/// public/ar3.urdf. Tries dev-mode locations first, then bundled resources.
fn resolve_project_file(app: &AppHandle, rel: &str) -> Result<std::path::PathBuf> {
    let cwd = std::env::current_dir().context("current_dir")?;

    let candidates = [
        cwd.join("..").join(rel), // pnpm tauri dev: cwd is src-tauri/
        cwd.join(rel),
        app.path()
            .resource_dir()
            .ok()
            .map(|p| p.join(rel))
            .unwrap_or_default(),
    ];

    for path in candidates.iter() {
        if path.exists() {
            return Ok(path.clone());
        }
    }
    Err(anyhow!(
        "{} not found (looked relative to cwd={:?})",
        rel,
        cwd
    ))
}

pub struct SidecarState {
    inner: Arc<Inner>,
}

struct Inner {
    next_id: AtomicU64,
    pending: Mutex<HashMap<u64, oneshot::Sender<Response>>>,
    stdin: Mutex<ChildStdin>,
    _child: Mutex<Child>,
}

impl SidecarState {
    pub fn spawn(app: &AppHandle) -> Result<Self> {
        let script = resolve_project_file(app, "sidecar/server.py")?;
        let urdf = resolve_project_file(app, "public/ar3.urdf").ok();
        let python = std::env::var("AR3_PYTHON").unwrap_or_else(|_| {
            // On Windows, the canonical command is `python`; elsewhere `python3`.
            if cfg!(windows) {
                "python".to_string()
            } else {
                "python3".to_string()
            }
        });

        let mut cmd = Command::new(&python);
        cmd.arg("-u").arg(&script);
        if let Some(p) = &urdf {
            cmd.arg("--urdf").arg(p);
        }
        let mut child = cmd
            .stdin(Stdio::piped())
            .stdout(Stdio::piped())
            .stderr(Stdio::inherit())
            .spawn()
            .with_context(|| format!("spawn {} {}", python, script.display()))?;

        let stdin = child.stdin.take().ok_or_else(|| anyhow!("no stdin"))?;
        let stdout = child.stdout.take().ok_or_else(|| anyhow!("no stdout"))?;

        let inner = Arc::new(Inner {
            next_id: AtomicU64::new(1),
            pending: Mutex::new(HashMap::new()),
            stdin: Mutex::new(stdin),
            _child: Mutex::new(child),
        });

        // Reader task: split lines, dispatch responses to waiting callers.
        let reader_inner = inner.clone();
        tauri::async_runtime::spawn(async move {
            let mut lines = BufReader::new(stdout).lines();
            while let Ok(Some(line)) = lines.next_line().await {
                let resp: Response = match serde_json::from_str(&line) {
                    Ok(r) => r,
                    Err(e) => {
                        eprintln!("[sidecar] bad JSON: {e}: {line}");
                        continue;
                    }
                };
                if let Some(id) = resp.id {
                    if let Some(tx) = reader_inner.pending.lock().await.remove(&id) {
                        let _ = tx.send(resp);
                    }
                }
            }
            eprintln!("[sidecar] stdout closed");
        });

        Ok(SidecarState { inner })
    }

    pub async fn call(
        &self,
        method: &str,
        params: serde_json::Value,
    ) -> Result<serde_json::Value> {
        let id = self.inner.next_id.fetch_add(1, Ordering::Relaxed);
        let (tx, rx) = oneshot::channel();
        self.inner.pending.lock().await.insert(id, tx);

        let req = Request {
            jsonrpc: "2.0",
            id,
            method,
            params,
        };
        let mut line = serde_json::to_string(&req)?;
        line.push('\n');

        {
            let mut stdin = self.inner.stdin.lock().await;
            stdin.write_all(line.as_bytes()).await?;
            stdin.flush().await?;
        }

        let resp = rx.await.context("sidecar reader dropped")?;
        if let Some(err) = resp.error {
            return Err(anyhow!("sidecar error {}: {}", err.code, err.message));
        }
        resp.result.ok_or_else(|| anyhow!("empty result"))
    }
}
