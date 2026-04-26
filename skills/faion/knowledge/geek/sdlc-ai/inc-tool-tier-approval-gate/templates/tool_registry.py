"""Reference tool-tier registry and executor for SRE agents.

The agent invokes `executor.call(name, args, approval=...)`. The executor
looks up the tier, audits the call, and refuses T2 without a verified
approval token. Unknown tools default to T2.
"""

from __future__ import annotations

import enum
import time
from collections.abc import Callable
from dataclasses import dataclass


class Tier(enum.Enum):
    T0 = "read_only"
    T1 = "safe_mutation"
    T2 = "destructive"


@dataclass
class ToolSpec:
    fn: Callable[..., object]
    tier: Tier


REGISTRY: dict[str, ToolSpec] = {}


def register(name: str, tier: Tier) -> Callable[[Callable[..., object]], Callable[..., object]]:
    def decorator(fn: Callable[..., object]) -> Callable[..., object]:
        REGISTRY[name] = ToolSpec(fn=fn, tier=tier)
        return fn

    return decorator


def call(name: str, args: dict, *, approval: str | None = None) -> object:
    spec = REGISTRY.get(name)
    tier = spec.tier if spec else Tier.T2  # unknown -> most-restrictive
    if tier is Tier.T2 and not _verify(approval, name=name, target=args.get("target")):
        raise PermissionError(f"{name} requires human approval")
    _audit(name=name, args=args, tier=tier, approval=approval)
    if spec is None:
        raise KeyError(f"tool not registered: {name}")
    return spec.fn(**args)


def _verify(token: str | None, *, name: str, target: object) -> bool:
    if token is None:
        return False
    claims = _decode_signed_jwt(token)  # raises on bad sig
    if claims["tool"] != name or claims["target"] != target:
        return False
    if claims["exp"] - claims["iat"] > 300:
        return False
    if not _consume_jti(claims["jti"]):  # single-use
        return False
    return claims["exp"] > int(time.time())


def _decode_signed_jwt(token: str) -> dict:
    raise NotImplementedError("wire your jwt library here")


def _consume_jti(jti: str) -> bool:
    raise NotImplementedError("wire your replay-cache (redis SETNX with TTL) here")


def _audit(**record: object) -> None:
    raise NotImplementedError("wire append-only audit log here")
