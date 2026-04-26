"""Performance metrics for backtest trade lists."""
from __future__ import annotations

import math
from datetime import datetime
from typing import Any

from backtest.engine import BacktestTrade


def equity_curve(trades: list[BacktestTrade], starting_equity: float) -> list[tuple[datetime, float]]:
    eq = starting_equity
    out: list[tuple[datetime, float]] = []
    for t in sorted(trades, key=lambda x: x.exit_time):
        eq += t.realized_pnl
        out.append((t.exit_time, eq))
    return out


def max_drawdown(values: list[float]) -> float:
    """Returns max drawdown as a NEGATIVE fraction (e.g. -0.25 = -25%)."""
    if not values:
        return 0.0
    peak = values[0]
    worst = 0.0
    for v in values:
        peak = max(peak, v)
        if peak > 0:
            dd = (v - peak) / peak
            worst = min(worst, dd)
    return worst


def compute_summary(trades: list[BacktestTrade], starting_equity: float) -> dict[str, Any]:
    if not trades:
        return {"trade_count": 0, "starting_equity": starting_equity,
                "ending_equity": starting_equity, "total_pnl": 0.0,
                "total_return_pct": 0.0, "max_drawdown_pct": 0.0,
                "win_count": 0, "loss_count": 0, "win_rate": 0.0,
                "avg_win": 0.0, "avg_loss": 0.0, "profit_factor": 0.0,
                "sharpe_daily": 0.0}
    wins = [t.realized_pnl for t in trades if t.realized_pnl > 0]
    losses = [t.realized_pnl for t in trades if t.realized_pnl < 0]
    total_pnl = sum(t.realized_pnl for t in trades)
    ending = starting_equity + total_pnl
    curve = [v for _, v in equity_curve(trades, starting_equity)]

    # Daily returns from equity curve (simple approximation)
    rets = []
    if len(curve) >= 2:
        for i in range(1, len(curve)):
            if curve[i - 1] > 0:
                rets.append((curve[i] - curve[i - 1]) / curve[i - 1])
    sharpe = 0.0
    if len(rets) >= 2:
        mean = sum(rets) / len(rets)
        var = sum((r - mean) ** 2 for r in rets) / (len(rets) - 1)
        std = math.sqrt(var)
        sharpe = (mean / std * math.sqrt(252)) if std > 0 else 0.0

    return {
        "trade_count": len(trades),
        "starting_equity": starting_equity,
        "ending_equity": ending,
        "total_pnl": total_pnl,
        "total_return_pct": total_pnl / starting_equity if starting_equity > 0 else 0.0,
        "max_drawdown_pct": max_drawdown(curve),
        "win_count": len(wins),
        "loss_count": len(losses),
        "win_rate": len(wins) / len(trades) if trades else 0.0,
        "avg_win": sum(wins) / len(wins) if wins else 0.0,
        "avg_loss": sum(losses) / len(losses) if losses else 0.0,
        "profit_factor": (sum(wins) / abs(sum(losses))) if losses else float("inf"),
        "sharpe_daily": sharpe,
    }
