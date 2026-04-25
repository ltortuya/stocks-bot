"""Risk: position sizing, daily caps, halt enforcement."""
from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path

from bot.state import State


@dataclass(frozen=True)
class RiskCheck:
    ok: bool
    reason: str | None = None


def position_size(
    equity: float, entry: float, stop: float, per_trade_risk_pct: float = 0.015,
) -> int:
    """Floor((per_trade_risk_pct * equity) / (entry - stop)). Returns 0 if stop >= entry."""
    if stop >= entry:
        return 0
    risk_per_share = entry - stop
    budget = per_trade_risk_pct * equity
    qty = int(math.floor(budget / risk_per_share))
    return max(qty, 0)


def can_open_new_position(
    state: State,
    max_open: int,
    max_daily_new: int,
    daily_new_count: int,
    halt_flag_path: Path | str,
) -> RiskCheck:
    """Combined gate: position cap + daily new cap + halt flag + state halt."""
    if Path(halt_flag_path).exists():
        return RiskCheck(False, "halt flag file present")
    if state.is_halted():
        return RiskCheck(False, "halt active in state")
    open_count = len(state.open_positions())
    if open_count >= max_open:
        return RiskCheck(False, f"at max open positions ({open_count}/{max_open})")
    if daily_new_count >= max_daily_new:
        return RiskCheck(False, f"daily new-entry cap reached ({daily_new_count}/{max_daily_new})")
    return RiskCheck(True)
