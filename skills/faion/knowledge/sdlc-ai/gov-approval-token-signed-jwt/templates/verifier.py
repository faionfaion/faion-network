# purpose: Reference JWT verifier implementation
# consumes: see content/02-output-contract.xml inputs
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200-500 tokens when loaded as context

#!/usr/bin/env python3
# purpose: reference JWT approval verifier
# consumes: signed JWT + verifier config
# produces: allow/deny decision + audit entry
# depends-on: cryptography stdlib
# token-budget-impact: ~250 tokens
"""Minimal reference verifier; production uses pyjwt or jose."""
from __future__ import annotations
import json


def verify(token: str, public_jwk: dict, expected_aud: str, nonce_seen: set) -> tuple[bool, str]:
    """Return (allowed, reason). Production: replace with pyjwt."""
    header_b64, payload_b64, sig_b64 = token.split(".")
    payload = json.loads(_b64url_decode(payload_b64).decode())
    if payload.get("aud") != expected_aud:
        return False, "aud mismatch"
    if payload.get("scope", "").endswith(":*") or payload["scope"] == "*":
        return False, "wildcard scope"
    if payload.get("exp", 0) - payload.get("iat", 0) > 900:
        return False, "expiry too long"
    jti = payload.get("jti")
    if not jti or jti in nonce_seen:
        return False, "replay or missing jti"
    nonce_seen.add(jti)
    return True, "ok"


def _b64url_decode(s: str) -> bytes:
    import base64
    pad = "=" * (-len(s) % 4)
    return base64.urlsafe_b64decode(s + pad)
