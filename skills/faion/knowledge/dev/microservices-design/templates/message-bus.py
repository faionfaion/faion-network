"""
purpose: Async message bus for inter-service events (publish + subscribe).
consumes: see content/02-output-contract.xml inputs
produces: artefact conforming to content/02-output-contract.xml (microservices-design)
depends-on: content/01-core-rules.xml
token-budget-impact: small (template is loaded only when an artefact is being authored)
"""
from typing import Awaitable, Callable, Dict, List


Handler = Callable[[dict], Awaitable[None]]


class MessageBus:
    def __init__(self) -> None:
        self._subs: Dict[str, List[Handler]] = {}

    def subscribe(self, topic: str, handler: Handler) -> None:
        self._subs.setdefault(topic, []).append(handler)

    async def publish(self, topic: str, payload: dict) -> None:
        for h in self._subs.get(topic, []):
            await h(payload)
