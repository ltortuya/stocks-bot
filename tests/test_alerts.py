"""Tests for bot.alerts."""
from __future__ import annotations

import responses

from bot.alerts import TelegramAlerts


@responses.activate
def test_send_posts_to_bot_api() -> None:
    responses.add(
        responses.POST,
        "https://api.telegram.org/botTOKEN/sendMessage",
        json={"ok": True, "result": {"message_id": 1}},
        status=200,
    )
    alerts = TelegramAlerts(token="TOKEN", chat_id="CHAT")
    ok = alerts.send("hello world")
    assert ok is True
    body = responses.calls[0].request.body
    if isinstance(body, bytes):
        body = body.decode()
    assert "chat_id=CHAT" in body
    assert "hello+world" in body or "hello%20world" in body


@responses.activate
def test_send_returns_false_on_http_error() -> None:
    responses.add(
        responses.POST,
        "https://api.telegram.org/botTOKEN/sendMessage",
        status=500,
    )
    alerts = TelegramAlerts(token="TOKEN", chat_id="CHAT")
    ok = alerts.send("oops")
    assert ok is False


def test_format_signal_message() -> None:
    alerts = TelegramAlerts(token="x", chat_id="y")
    msg = alerts.format_signal(
        symbol="AAPL", qty=14, entry=215.42, stop=204.65, target=237.0, rvol=2.4,
    )
    assert "AAPL" in msg
    assert "14" in msg
    assert "215.42" in msg
    assert "204.65" in msg
    assert "237.00" in msg


def test_format_close_message() -> None:
    alerts = TelegramAlerts(token="x", chat_id="y")
    msg = alerts.format_close(
        symbol="AAPL", qty=14, exit_price=237.0, entry=215.42,
        pnl=150.82, reason="target",
    )
    assert "AAPL" in msg
    assert "target" in msg
    assert "+$150.82" in msg or "+150.82" in msg
