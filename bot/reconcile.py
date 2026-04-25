"""Reconcile local SQLite state with Alpaca positions on startup + each cycle."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Protocol

from bot.state import State


class _ExecutorLike(Protocol):
    def list_positions(self) -> dict[str, dict]: ...


@dataclass
class ReconcileReport:
    closed_locally: list[str] = field(default_factory=list)
    discovered_externally: list[str] = field(default_factory=list)


def reconcile_positions(
    state: State, executor: _ExecutorLike, now: datetime,
) -> ReconcileReport:
    """Truth source = Alpaca's `/v2/positions`.

    - Local-open + Alpaca-not-held → close locally with reason='reconcile'.
    - Alpaca-held + local-not-tracked → report discovery (operator must investigate;
      we do NOT auto-adopt these because we don't know entry context).
    """
    report = ReconcileReport()
    alpaca = executor.list_positions()
    local = {p.symbol: p for p in state.open_positions()}

    for symbol, pos in local.items():
        if symbol not in alpaca:
            # Position was closed externally (TP/SL filled, or operator action)
            state.close_position(
                pos_id=pos.id, exit_time=now.isoformat(),
                exit_price=pos.current_stop or pos.entry_price or 0.0,
                exit_reason="reconcile",
                realized_pnl=0.0,  # unknown without fill history; reporter can recompute later
            )
            report.closed_locally.append(symbol)

    for symbol in alpaca:
        if symbol not in local:
            report.discovered_externally.append(symbol)

    return report
