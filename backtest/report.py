"""Write trade log CSV + summary JSON to backtest/results/<run_id>/."""
from __future__ import annotations

import csv
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from backtest.engine import BacktestTrade


def write_trades_csv(trades: list[BacktestTrade], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not trades:
        path.write_text("symbol,entry_time,entry_price,qty,exit_time,exit_price,exit_reason,realized_pnl\n")
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "symbol", "entry_time", "entry_price", "qty",
            "exit_time", "exit_price", "exit_reason", "realized_pnl",
        ])
        writer.writeheader()
        for t in trades:
            row = asdict(t)
            row["entry_time"] = t.entry_time.isoformat()
            row["exit_time"] = t.exit_time.isoformat()
            writer.writerow(row)


def write_summary_json(summary: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(summary, indent=2, default=str))
