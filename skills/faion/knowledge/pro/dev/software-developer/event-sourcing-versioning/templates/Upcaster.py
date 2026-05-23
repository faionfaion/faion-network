# purpose: upcaster registry + example v1 -> v2 transform
# consumes: raw event dict + version
# produces: latest-shape event dict
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~250 tokens when loaded as reference

from __future__ import annotations

from typing import Callable

Upcaster = Callable[[dict], dict]

_REGISTRY: dict[tuple[str, int], Upcaster] = {}


def register(event_name: str, from_version: int):
    def decorator(fn: Upcaster) -> Upcaster:
        _REGISTRY[(event_name, from_version)] = fn
        return fn
    return decorator


def upcast(event_name: str, payload: dict, target_version: int) -> dict:
    while payload.get("event_version", 1) < target_version:
        current = payload.get("event_version", 1)
        fn = _REGISTRY.get((event_name, current))
        if fn is None:
            raise RuntimeError(
                f"no upcaster registered for {event_name} v{current} -> v{current + 1}"
            )
        payload = fn(payload)
        payload["event_version"] = current + 1
    return payload


@register("OrderPlaced", from_version=1)
def order_placed_v1_to_v2(v1: dict) -> dict:
    return {
        "order_id": v1["order_id"],
        "buyer_id": v1["customer_id"],
        "total_cents": v1["total_cents"],
    }
