# __faion_header_v1__
# purpose: FastAPI ConnectionManager with channel subscriptions and graceful disconnect
# consumes: see content/02-output-contract.xml
# produces: spec
# depends-on: content/04-procedure.xml + content/01-core-rules.xml#redis-pubsub-fanout
# token-budget-impact: ~300 tokens when loaded as context
# faion_header_json: {"__faion_header__":{"purpose":"FastAPI ConnectionManager with channel subscriptions and graceful disconnect","consumes":"see content/02-output-contract.xml","produces":"spec","depends_on":"content/04-procedure.xml + content/01-core-rules.xml#redis-pubsub-fanout","token_budget_impact":"~300 tokens when loaded as context"}}
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active: dict[str, list[WebSocket]] = {}

    async def connect(self, channel: str, ws: WebSocket) -> None:
        await ws.accept()
        self.active.setdefault(channel, []).append(ws)

    async def disconnect(self, channel: str, ws: WebSocket) -> None:
        self.active.get(channel, []).remove(ws)

    async def broadcast(self, channel: str, message: dict) -> None:
        for ws in list(self.active.get(channel, [])):
            try:
                await ws.send_json(message)
            except Exception:
                self.active[channel].remove(ws)
