"""Telegram alert wrapper."""
from __future__ import annotations

import requests


class TelegramAlerts:
    def __init__(self, token: str, chat_id: str, timeout_sec: float = 5.0) -> None:
        self._token = token
        self._chat_id = chat_id
        self._timeout = timeout_sec

    def send(self, text: str) -> bool:
        url = f"https://api.telegram.org/bot{self._token}/sendMessage"
        try:
            resp = requests.post(
                url,
                data={"chat_id": self._chat_id, "text": text, "parse_mode": "HTML"},
                timeout=self._timeout,
            )
            return resp.status_code == 200
        except Exception:
            return False

    @staticmethod
    def format_signal(
        symbol: str, qty: int, entry: float, stop: float, target: float, rvol: float,
    ) -> str:
        return (
            f"<b>{symbol}</b> entry triggered\n"
            f"qty={qty}  entry={entry:.2f}\n"
            f"stop={stop:.2f}  target={target:.2f}\n"
            f"rvol={rvol:.2f}"
        )

    @staticmethod
    def format_close(
        symbol: str, qty: int, exit_price: float, entry: float, pnl: float, reason: str,
    ) -> str:
        sign = "+" if pnl >= 0 else "-"
        return (
            f"<b>{symbol}</b> closed ({reason})\n"
            f"qty={qty}  entry={entry:.2f}  exit={exit_price:.2f}\n"
            f"pnl={sign}${abs(pnl):.2f}"
        )

    @staticmethod
    def format_halt(reason: str) -> str:
        return f"<b>HALT</b> activated: {reason}"
