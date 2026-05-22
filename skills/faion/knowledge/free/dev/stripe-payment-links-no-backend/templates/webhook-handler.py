# purpose: reference HMAC-SHA256 webhook verifier for Stripe (Zapier Code-step or serverless)
# consumes: raw_body bytes + Stripe-Signature header + STRIPE_WEBHOOK_SECRET env
# produces: verified event dict OR raises SignatureVerificationError
# depends-on: nothing (stdlib only — keeps Zapier Code step dependency-free)
# token-budget-impact: ~200 tokens
"""Reference snippet — copy into Zapier Code (Python) step or serverless handler."""
from __future__ import annotations

import hashlib
import hmac
import json
import time


class SignatureVerificationError(Exception):
    """Raised when Stripe-Signature header fails HMAC verification."""


def verify_stripe_signature(raw_body: bytes, sig_header: str, secret: str, tolerance_seconds: int = 300) -> dict:
    """Verify Stripe webhook payload and return the parsed event.

    raw_body must be the exact bytes Stripe sent — no framework re-serialisation.
    """
    if not isinstance(raw_body, (bytes, bytearray)):
        raise SignatureVerificationError("raw_body must be bytes — preserve raw request body")
    parts = dict(p.split("=", 1) for p in sig_header.split(","))
    ts = int(parts["t"])
    sig = parts["v1"]
    if abs(time.time() - ts) > tolerance_seconds:
        raise SignatureVerificationError("timestamp outside tolerance — possible replay")
    signed_payload = f"{ts}.".encode() + raw_body
    expected = hmac.new(secret.encode(), signed_payload, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, sig):
        raise SignatureVerificationError("HMAC mismatch — payload forged or secret wrong")
    return json.loads(raw_body)


if __name__ == "__main__":
    import sys
    if "--help" in sys.argv:
        print(__doc__)
