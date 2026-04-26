"""Reference verifier for an approval JWT.

Checks: signature, audience, expiry, scope match, single-use (jti).
Self-approval is rejected. Replays raise an alert before raising.
"""

from __future__ import annotations

import hashlib
import json
import time
from typing import Any

import jwt  # PyJWT


class ApprovalDenied(Exception):
    pass


def _canonical(args: dict[str, Any]) -> str:
    return json.dumps(args, sort_keys=True, separators=(",", ":"))


def verify(
    token: str,
    *,
    public_key: str,
    audience: str,
    expected_tool: str,
    expected_target: str,
    expected_args: dict[str, Any],
    seen_jti_store,
) -> dict[str, Any]:
    try:
        claims = jwt.decode(
            token,
            key=public_key,
            algorithms=["EdDSA", "RS256"],
            audience=audience,
            options={"require": ["exp", "iat", "sub", "jti", "iss"]},
        )
    except jwt.PyJWTError as e:
        raise ApprovalDenied(f"signature/decode: {e}") from e

    if claims.get("sub") == audience:
        raise ApprovalDenied("self-approval forbidden")

    if claims["exp"] - claims["iat"] > 300:
        raise ApprovalDenied("ttl exceeds 300s")

    if time.time() > claims["exp"]:
        raise ApprovalDenied("expired")

    scope = claims.get("scope") or {}
    if scope.get("tool") != expected_tool:
        raise ApprovalDenied("tool mismatch")
    if scope.get("target") != expected_target:
        raise ApprovalDenied("target mismatch")

    expected_hash = "sha256:" + hashlib.sha256(
        _canonical(expected_args).encode()
    ).hexdigest()
    if scope.get("args_hash") != expected_hash:
        raise ApprovalDenied("args hash mismatch")

    if seen_jti_store.exists(claims["jti"]):
        seen_jti_store.alert_replay(claims["jti"])
        raise ApprovalDenied("replay detected")
    seen_jti_store.record(claims["jti"], claims["exp"])

    return claims
