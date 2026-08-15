# __faion_header_v1__
# purpose: FastAPI ConnectionManager with channel subscriptions, presence map and graceful disconnect
# consumes: see content/02-output-contract.xml
# produces: spec
# depends-on: content/01-core-rules.xml#versioned-envelope + content/01-core-rules.xml#close-code-truthful
# token-budget-impact: ~400 tokens when loaded as context
# faion_header_json: {"__faion_header__":{"purpose":"FastAPI ConnectionManager with channel subscriptions, presence map and graceful disconnect","consumes":"see content/02-output-contract.xml","produces":"spec","depends_on":"content/01-core-rules.xml#versioned-envelope + content/01-core-rules.xml#close-code-truthful","token_budget_impact":"~400 tokens when loaded as context"}}
import asyncio
import logging

from fastapi import WebSocket
from fastapi.websockets import WebSocketState

# RFC 6455 close codes this manager emits (rule close-code-truthful).
CLOSE_NORMAL = 1000
CLOSE_GOING_AWAY = 1001
CLOSE_POLICY_VIOLATION = 1008


class ConnectionManager:
    """Per-process. Cross-node fan-out belongs on Redis Pub/Sub, not here."""

    def __init__(self) -> None:
        self.connections: dict[str, WebSocket] = {}          # user_id -> socket
        self.subscribers: dict[str, set[str]] = {}           # channel -> user_ids
        self.user_channels: dict[str, set[str]] = {}         # user_id -> channels

    async def connect(self, user_id: str, ws: WebSocket) -> None:
        await ws.accept()
        if user_id in self.connections:
            await self.disconnect(user_id, code=CLOSE_GOING_AWAY)
        self.connections[user_id] = ws
        self.user_channels[user_id] = set()
        logging.info("ws connect user=%s", user_id)

    async def disconnect(self, user_id: str, code: int = CLOSE_NORMAL) -> None:
        for channel in list(self.user_channels.get(user_id, ())):
            self.unsubscribe(user_id, channel)
        ws = self.connections.pop(user_id, None)
        self.user_channels.pop(user_id, None)
        if ws and ws.client_state == WebSocketState.CONNECTED:
            await ws.close(code=code)
        logging.info("ws disconnect user=%s code=%s", user_id, code)

    def subscribe(self, user_id: str, channel: str) -> None:
        self.subscribers.setdefault(channel, set()).add(user_id)
        self.user_channels.setdefault(user_id, set()).add(channel)

    def unsubscribe(self, user_id: str, channel: str) -> None:
        subs = self.subscribers.get(channel)
        if subs:
            subs.discard(user_id)
            if not subs:
                del self.subscribers[channel]
        self.user_channels.get(user_id, set()).discard(channel)

    async def send_to_user(self, user_id: str, envelope: dict) -> None:
        ws = self.connections.get(user_id)
        if not ws or ws.client_state != WebSocketState.CONNECTED:
            return
        try:
            await ws.send_json(envelope)
        except Exception as exc:  # noqa: BLE001 — a dead socket must not kill the loop
            logging.error("ws send failed user=%s: %s", user_id, exc)
            await self.disconnect(user_id, code=CLOSE_POLICY_VIOLATION)

    async def broadcast(self, channel: str, envelope: dict) -> None:
        targets = list(self.subscribers.get(channel, ()))
        await asyncio.gather(
            *(self.send_to_user(uid, envelope) for uid in targets),
            return_exceptions=True,
        )
