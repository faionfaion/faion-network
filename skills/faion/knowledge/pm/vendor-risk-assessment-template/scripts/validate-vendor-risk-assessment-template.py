#!/usr/bin/env python3
"""validate-vendor-risk-assessment-template.py — Validate a filled vendor-risk assessment.

Inputs:
  - <assessment.json>  Path to the assessment JSON.

Outputs:
  - stdout: PASS / FAIL with violation list.

Exit codes:
  0 - assessment validates.
  1 - assessment violates schema / staleness / ownership rules.
  2 - usage error.

Flags:
  --help        Show this message.
  --self-test   Run against a built-in fixture.
"""
from __future__ import annotations

import datetime as dt
import json
import re
import sys
from pathlib import Path

SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
OWNER_RE = re.compile(r"^[a-zA-Z0-9._-]+:[a-zA-Z0-9._-]+$")
URL_RE = re.compile(r"^https?://[^\s]+$")
STALE_DAYS = 90
ALLOWED_RATING = {"low", "medium", "high", "critical"}

VALID_FIXTURE = {
    "artefact_id": "datadog-risk-assessment",
    "vendor_name": "Datadog",
    "owner": "compliance:alice",
    "version": "1.0.0",
    "last_reviewed": dt.date.today().isoformat(),
    "risk_rating": "medium",
    "status": "active",
    "fields": {
        "dpa_url": "https://www.datadoghq.com/legal/dpa/",
        "subprocessor_list_url": "https://www.datadoghq.com/legal/sub-processors/",
        "data_residency": "EU",
        "encryption_at_rest": True,
        "retention_days": 365,
        "breach_notification_sla_hours": 72,
    },
    "inputs_used": [{"name": "DPA", "source": "https://www.datadoghq.com/legal/dpa/"}],
}
INVALID_FIXTURE = {"owner": "team", "fields": {}}


def validate(spec: dict) -> list[str]:
    out: list[str] = []
    for k in ("artefact_id", "vendor_name", "owner", "version", "last_reviewed", "risk_rating", "fields", "inputs_used"):
        if k not in spec:
            out.append(f"{k} missing")
    if "owner" in spec and (not OWNER_RE.match(str(spec["owner"])) or str(spec["owner"]).lower().startswith(("team", "we", "us"))):
        out.append("owner must be role:person, not team")
    if "version" in spec and not SEMVER_RE.match(str(spec["version"])):
        out.append("version must be semver")
    if "last_reviewed" in spec:
        try:
            d = dt.date.fromisoformat(str(spec["last_reviewed"]))
            age = (dt.date.today() - d).days
            if age > STALE_DAYS:
                out.append(f"last_reviewed stale ({age} days; max {STALE_DAYS})")
        except ValueError:
            out.append("last_reviewed not ISO date")
    if "risk_rating" in spec and spec["risk_rating"] not in ALLOWED_RATING:
        out.append(f"risk_rating must be one of {sorted(ALLOWED_RATING)}")
    fields = spec.get("fields", {})
    for k in ("dpa_url", "subprocessor_list_url", "data_residency", "encryption_at_rest", "retention_days", "breach_notification_sla_hours"):
        if k not in fields:
            out.append(f"fields.{k} missing")
    if "dpa_url" in fields and not URL_RE.match(str(fields["dpa_url"])):
        out.append("fields.dpa_url must be http(s) URL")
    if "subprocessor_list_url" in fields and not URL_RE.match(str(fields["subprocessor_list_url"])):
        out.append("fields.subprocessor_list_url must be http(s) URL")
    if "retention_days" in fields and not isinstance(fields["retention_days"], int):
        out.append("fields.retention_days must be int")
    if "breach_notification_sla_hours" in fields and not isinstance(fields["breach_notification_sla_hours"], int):
        out.append("fields.breach_notification_sla_hours must be int")
    inputs = spec.get("inputs_used", [])
    if not isinstance(inputs, list) or not inputs:
        out.append("inputs_used must be non-empty list")
    return out


def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[1] in ("--help", "-h"):
        sys.stdout.write(__doc__ or "")
        return 0 if "--help" in argv else 2
    if argv[1] == "--self-test":
        ok = validate(VALID_FIXTURE)
        bad = validate(INVALID_FIXTURE)
        if ok:
            sys.stderr.write(f"self-test FAIL: valid fixture rejected: {ok}\n")
            return 1
        if not bad:
            sys.stderr.write("self-test FAIL: invalid fixture accepted\n")
            return 1
        sys.stdout.write("self-test OK\n")
        return 0
    p = Path(argv[1])
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n")
        return 2
    try:
        spec = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        sys.stderr.write(f"invalid JSON: {exc}\n")
        return 1
    v = validate(spec)
    if v:
        sys.stdout.write("FAIL\n")
        for x in v:
            sys.stdout.write(f"  - {x}\n")
        return 1
    sys.stdout.write("PASS\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
