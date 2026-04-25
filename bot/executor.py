"""Alpaca order placement, cancellation, replacement, and account queries."""
from __future__ import annotations

from typing import Any

import requests


class AlpacaExecutor:
    def __init__(
        self, api_key: str, api_secret: str,
        base_url: str = "https://paper-api.alpaca.markets",
        timeout_sec: float = 10.0,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout_sec
        self._headers = {
            "APCA-API-KEY-ID": api_key,
            "APCA-API-SECRET-KEY": api_secret,
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def _req(self, method: str, path: str, **kw: Any) -> requests.Response:
        return requests.request(
            method, f"{self.base_url}{path}",
            headers=self._headers, timeout=self.timeout, **kw,
        )

    def get_equity(self) -> float:
        r = self._req("GET", "/v2/account")
        r.raise_for_status()
        return float(r.json()["equity"])

    def list_positions(self) -> dict[str, dict[str, Any]]:
        r = self._req("GET", "/v2/positions")
        r.raise_for_status()
        out: dict[str, dict[str, Any]] = {}
        for p in r.json():
            out[p["symbol"]] = {
                "qty": int(float(p["qty"])),
                "avg_entry_price": float(p["avg_entry_price"]),
                "current_price": float(p.get("current_price", 0) or 0),
                "unrealized_pl": float(p.get("unrealized_pl", 0) or 0),
            }
        return out

    def list_orders(self, status: str = "open") -> list[dict[str, Any]]:
        r = self._req("GET", "/v2/orders", params={"status": status, "limit": 500})
        r.raise_for_status()
        return r.json()

    def submit_entry_stop_limit(
        self, symbol: str, qty: int, stop_price: float, limit_price: float,
    ) -> dict[str, Any]:
        body = {
            "symbol": symbol, "qty": str(qty), "side": "buy",
            "type": "stop_limit", "time_in_force": "day",
            "stop_price": f"{stop_price:.2f}", "limit_price": f"{limit_price:.2f}",
        }
        r = self._req("POST", "/v2/orders", json=body)
        r.raise_for_status()
        return r.json()

    def submit_take_profit(
        self, symbol: str, qty: int, limit_price: float,
    ) -> dict[str, Any]:
        body = {
            "symbol": symbol, "qty": str(qty), "side": "sell",
            "type": "limit", "time_in_force": "gtc",
            "limit_price": f"{limit_price:.2f}",
        }
        r = self._req("POST", "/v2/orders", json=body)
        r.raise_for_status()
        return r.json()

    def submit_stop_loss(
        self, symbol: str, qty: int, stop_price: float,
    ) -> dict[str, Any]:
        body = {
            "symbol": symbol, "qty": str(qty), "side": "sell",
            "type": "stop", "time_in_force": "gtc",
            "stop_price": f"{stop_price:.2f}",
        }
        r = self._req("POST", "/v2/orders", json=body)
        r.raise_for_status()
        return r.json()

    def submit_market_sell(self, symbol: str, qty: int) -> dict[str, Any]:
        body = {
            "symbol": symbol, "qty": str(qty), "side": "sell",
            "type": "market", "time_in_force": "day",
        }
        r = self._req("POST", "/v2/orders", json=body)
        r.raise_for_status()
        return r.json()

    def cancel_order(self, order_id: str) -> None:
        r = self._req("DELETE", f"/v2/orders/{order_id}")
        if r.status_code in (204, 404, 422):
            return  # idempotent: order may already be filled/cancelled
        r.raise_for_status()

    def replace_stop_loss(
        self, old_order_id: str, symbol: str, qty: int, new_stop_price: float,
    ) -> dict[str, Any]:
        self.cancel_order(old_order_id)
        return self.submit_stop_loss(symbol=symbol, qty=qty, stop_price=new_stop_price)
