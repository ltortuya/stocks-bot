"""Tests for bot.executor."""
from __future__ import annotations

import responses

from bot.executor import AlpacaExecutor


def _exec() -> AlpacaExecutor:
    return AlpacaExecutor(api_key="k", api_secret="s",
                          base_url="https://paper-api.alpaca.markets")


@responses.activate
def test_get_account_equity() -> None:
    responses.add(
        responses.GET,
        "https://paper-api.alpaca.markets/v2/account",
        json={"equity": "100000.00", "cash": "100000.00", "buying_power": "200000.00"},
        status=200,
    )
    assert _exec().get_equity() == 100_000.00


@responses.activate
def test_submit_stop_limit_buy_returns_order_id() -> None:
    responses.add(
        responses.POST,
        "https://paper-api.alpaca.markets/v2/orders",
        json={"id": "ord-123", "status": "accepted",
              "symbol": "AAPL", "qty": "10", "type": "stop_limit"},
        status=200,
    )
    order = _exec().submit_entry_stop_limit(
        symbol="AAPL", qty=10, stop_price=215.44, limit_price=216.09,
    )
    assert order["id"] == "ord-123"
    body = responses.calls[0].request.body.decode()
    assert "stop_limit" in body
    assert "AAPL" in body


@responses.activate
def test_submit_market_sell_returns_order_id() -> None:
    responses.add(
        responses.POST,
        "https://paper-api.alpaca.markets/v2/orders",
        json={"id": "ord-456", "status": "accepted"},
        status=200,
    )
    order = _exec().submit_market_sell(symbol="AAPL", qty=10)
    assert order["id"] == "ord-456"


@responses.activate
def test_replace_stop_loss_cancels_then_submits_new() -> None:
    responses.add(
        responses.DELETE,
        "https://paper-api.alpaca.markets/v2/orders/old-stop",
        status=204,
    )
    responses.add(
        responses.POST,
        "https://paper-api.alpaca.markets/v2/orders",
        json={"id": "new-stop"},
        status=200,
    )
    order = _exec().replace_stop_loss(
        old_order_id="old-stop", symbol="AAPL", qty=10, new_stop_price=220.00,
    )
    assert order["id"] == "new-stop"


@responses.activate
def test_cancel_order_tolerates_404() -> None:
    responses.add(
        responses.DELETE,
        "https://paper-api.alpaca.markets/v2/orders/missing",
        status=404,
    )
    # Should not raise
    _exec().cancel_order("missing")


@responses.activate
def test_list_open_positions_returns_dict() -> None:
    responses.add(
        responses.GET,
        "https://paper-api.alpaca.markets/v2/positions",
        json=[
            {"symbol": "AAPL", "qty": "10", "avg_entry_price": "215.42",
             "current_price": "216.10", "unrealized_pl": "6.80"},
        ],
        status=200,
    )
    positions = _exec().list_positions()
    assert "AAPL" in positions
    assert positions["AAPL"]["qty"] == 10
    assert positions["AAPL"]["avg_entry_price"] == 215.42
