#!/usr/bin/env python3
"""Validate a stripe-payment-links-no-backend spec against the embedded schema.

Usage:
    validate-stripe-payment-links-no-backend.py <file.json>
    validate-stripe-payment-links-no-backend.py --self-test
    validate-stripe-payment-links-no-backend.py --help

Exit codes:
    0 = valid
    1 = invalid (violations to stderr)
    2 = bad invocation
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SLUG = "stripe-payment-links-no-backend"
DECISION_REQUIRED = [
    "mode",
    "links",
    "webhook_endpoint",
    "signature_strategy",
    "idempotency_store",
    "fulfillment_channels",
]
DRIVERS_REQUIRED = ["billing_model", "custom_amount_per_buyer", "connect_required", "catalog_size"]
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
RULE = re.compile(r"^r[0-9a-z-]+$")
FORBIDDEN_OWNER = re.compile(r"^(team|we|us|engineering|support|the (team|squad|group))$", re.IGNORECASE)
ALLOWED_MODES = {"payment-link", "checkout-session", "reject-connect"}
ALLOWED_SIG = {"hmac-sha256-stripe-sdk", "hmac-sha256-manual"}


def _violations(rec: dict) -> list[str]:
    v: list[str] = []
    if rec.get("slug") != SLUG:
        v.append(f"slug must equal '{SLUG}'")
    if not SEMVER.match(str(rec.get("version", ""))):
        v.append("version must be semver")
    owner = str(rec.get("owner", ""))
    if not owner or FORBIDDEN_OWNER.match(owner):
        v.append("owner must be a named human/role; plural owners ('team','we','us') rejected")
    d = rec.get("decision") or {}
    if not isinstance(d, dict):
        v.append("decision must be object")
    else:
        for k in DECISION_REQUIRED:
            if k not in d:
                v.append(f"decision.{k} required")
        if d.get("mode") and d["mode"] not in ALLOWED_MODES:
            v.append(f"decision.mode must be one of {sorted(ALLOWED_MODES)}")
        if d.get("signature_strategy") and d["signature_strategy"] not in ALLOWED_SIG:
            v.append(f"decision.signature_strategy must be one of {sorted(ALLOWED_SIG)}")
        if isinstance(d.get("fulfillment_channels"), list) and not d["fulfillment_channels"]:
            v.append("decision.fulfillment_channels must be non-empty")
    dr = rec.get("drivers") or {}
    if not isinstance(dr, dict):
        v.append("drivers must be object")
    else:
        for k in DRIVERS_REQUIRED:
            if k not in dr:
                v.append(f"drivers.{k} required")
    refs = (rec.get("audit") or {}).get("rule_refs") or []
    if not refs:
        v.append("audit.rule_refs must be non-empty array")
    for r in refs:
        if not RULE.match(str(r)):
            v.append(f"audit.rule_refs entry '{r}' must match ^r[0-9a-z-]+$")
    return v


def _self_test() -> int:
    good = {
        "slug": SLUG,
        "version": "2.0.0",
        "owner": "ruslan@faion.net",
        "decision": {
            "mode": "payment-link",
            "links": [{"sku": "ltd", "url": "https://buy.stripe.com/x", "price_cents": 2900, "currency": "usd"}],
            "webhook_endpoint": "https://hooks.zapier.com/x",
            "signature_strategy": "hmac-sha256-stripe-sdk",
            "idempotency_store": "https://docs.google.com/x",
            "fulfillment_channels": [{"channel": "email", "address": "x@x.x"}],
        },
        "drivers": {"billing_model": "one-off", "custom_amount_per_buyer": False, "connect_required": False, "catalog_size": 1},
        "audit": {"rule_refs": ["r1-verify-signature", "r-payment-link"]},
    }
    if _violations(good):
        return 1
    bad = json.loads(json.dumps(good))
    bad["owner"] = "team"
    bad["audit"]["rule_refs"] = []
    vs = _violations(bad)
    return 0 if vs else 1


def main(argv: list[str]) -> int:
    if "--help" in argv or "-h" in argv:
        sys.stdout.write(__doc__ or "")
        return 0
    if "--self-test" in argv:
        return _self_test()
    if len(argv) < 2:
        sys.stderr.write(f"usage: validate-{SLUG}.py <file.json>\n")
        return 2
    p = Path(argv[1])
    if not p.exists():
        sys.stderr.write(f"missing: {p}\n")
        return 2
    try:
        rec = json.loads(p.read_text())
    except json.JSONDecodeError as e:
        sys.stderr.write(f"bad json: {e}\n")
        return 2
    vs = _violations(rec)
    if vs:
        for x in vs:
            sys.stderr.write(f"VIOLATION: {x}\n")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
