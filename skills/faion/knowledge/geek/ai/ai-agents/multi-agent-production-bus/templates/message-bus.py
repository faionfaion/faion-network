# purpose: production MessageBus skeleton emitted by multi-agent-production-bus methodology
# consumes: asyncio + structured Message dataclass + handler subscribers
# produces: importable MessageBus + Message + CommunicationType
# depends-on: r1-structured-message, r2-handler-timeout, r3-broadcast-excludes-sender
# token-budget-impact: ~300 tokens
"""Reference MessageBus implementation. Drop into your agent system."""
from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List


class CommunicationType(Enum):
    DIRECT = "direct"
    BROADCAST = "broadcast"
    REQUEST = "request"


@dataclass
class Message:
    sender: str
    receiver: str
    content: dict
    msg_type: CommunicationType
    correlation_id: str = ""
    metadata: dict = field(default_factory=dict)


class MessageBus:
    def __init__(self, handler_timeout_seconds: int = 60):
        self.subscribers: Dict[str, List[Callable]] = {}
        self.history: List[Message] = []
        self.timeout = handler_timeout_seconds

    def subscribe(self, name: str, handler: Callable) -> None:
        self.subscribers.setdefault(name, []).append(handler)

    async def send(self, msg: Message) -> List[Any]:
        if not isinstance(msg.content, dict):
            raise TypeError("Message.content must be dict — r1-structured-message")
        self.history.append(msg)
        targets = (
            [n for n in self.subscribers if n != msg.sender]
            if msg.msg_type is CommunicationType.BROADCAST
            else [msg.receiver]
        )
        out: List[Any] = []
        for name in targets:
            for h in self.subscribers.get(name, []):
                out.append(await asyncio.wait_for(h(msg), timeout=self.timeout))
        return out


def _self_test() -> int:
    bus = MessageBus(handler_timeout_seconds=1)
    received: List[Message] = []

    async def h(m: Message):
        received.append(m)
        return "ok"

    bus.subscribe("worker", h)
    asyncio.run(bus.send(Message(sender="planner", receiver="worker", content={"x": 1}, msg_type=CommunicationType.DIRECT)))
    return 0 if len(received) == 1 else 1


if __name__ == "__main__":
    import sys
    if "--self-test" in sys.argv:
        raise SystemExit(_self_test())
    if "--help" in sys.argv:
        print(__doc__)
