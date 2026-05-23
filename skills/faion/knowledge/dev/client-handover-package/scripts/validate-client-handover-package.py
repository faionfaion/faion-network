#!/usr/bin/env python3
"""validate-client-handover-package.py

Validate a client-handover-package JSON against schema + rule consistency.

Inputs:
    --file PATH      path to handover JSON
    --self-test      run built-in valid + invalid fixtures
    --help           this message

Exit codes:
    0 = valid
    1 = invalid (violation list printed to stderr)
    2 = usage / unreadable file
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ID_RE = re.compile(r"^chp-[a-z0-9-]{6,}$")
EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
TEAM_ALIASES = {"engineering", "dev", "ops", "team", "platform", "qa", "support"}
SEVERITY = {"high", "medium", "low"}
EFFORT = {"S", "M", "L"}
BLAST = {1, 3, 5}
VERDICTS = {"archive-and-close", "block-missing-sections", "block-secrets-not-transferred", "block-no-successor", "block-no-signoff"}
VER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
MIN_LEN = {"scope_summary": 50, "runbook": 100, "architecture": 100, "ops_surface": 50}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    for k in ("artefact_id", "client", "engagement_end", "sections", "credentials", "open_items", "successor_email", "support_window", "signoff", "verdict", "version", "last_reviewed"):
        if k not in obj:
            errs.append(f"missing required field: {k}")

    if "artefact_id" in obj and not ID_RE.match(str(obj["artefact_id"])):
        errs.append("artefact_id must match ^chp-[a-z0-9-]{6,}$")

    sec = obj.get("sections") or {}
    for s, ml in MIN_LEN.items():
        if s not in sec:
            errs.append(f"sections.{s} missing")
        elif not isinstance(sec.get(s), str) or len(sec[s]) < ml:
            errs.append(f"sections.{s} must be string of length >= {ml}")

    creds = obj.get("credentials") or []
    if not isinstance(creds, list):
        errs.append("credentials must be a list")
    else:
        for i, c in enumerate(creds):
            for sub in ("name", "vault_path", "rotation_date", "acknowledged_by", "acknowledged_at"):
                if sub not in c or not str(c.get(sub, "")).strip():
                    errs.append(f"credentials[{i}].{sub} missing or empty")

    items = obj.get("open_items") or []
    if isinstance(items, list):
        for i, it in enumerate(items):
            for sub in ("title", "severity", "effort", "blast_radius", "next_step"):
                if sub not in it:
                    errs.append(f"open_items[{i}].{sub} missing")
            if it.get("severity") not in SEVERITY:
                errs.append(f"open_items[{i}].severity must be one of {sorted(SEVERITY)}")
            if it.get("effort") not in EFFORT:
                errs.append(f"open_items[{i}].effort must be one of {sorted(EFFORT)}")
            if it.get("blast_radius") not in BLAST:
                errs.append(f"open_items[{i}].blast_radius must be one of {sorted(BLAST)}")

    se = str(obj.get("successor_email", ""))
    if se and not EMAIL_RE.match(se):
        errs.append("successor_email must be valid email")
    if se.split("@", 1)[0].lower() in TEAM_ALIASES:
        errs.append("successor_email is a team alias")

    sw = obj.get("support_window") or {}
    if not isinstance(sw, dict):
        errs.append("support_window missing")
    else:
        days = sw.get("days")
        if not isinstance(days, int) or not (7 <= days <= 90):
            errs.append("support_window.days must be int in [7,90]")
        sla = sw.get("sla_hours")
        if not isinstance(sla, (int, float)) or not (0 < sla <= 168):
            errs.append("support_window.sla_hours must be number in (0, 168]")
        for sub in ("scope", "channel", "after_window"):
            if not str(sw.get(sub, "")).strip():
                errs.append(f"support_window.{sub} must be non-empty")

    so = obj.get("signoff") or {}
    if not isinstance(so, dict):
        errs.append("signoff missing")
    else:
        for sub in ("consultant_signed_by", "consultant_signed_at", "client_signed_by", "client_signed_at"):
            if sub not in so:
                errs.append(f"signoff.{sub} missing")
        for em_key in ("consultant_signed_by", "client_signed_by"):
            em = str(so.get(em_key, ""))
            if em and not EMAIL_RE.match(em):
                errs.append(f"signoff.{em_key} must be valid email")
            if em.split("@", 1)[0].lower() in TEAM_ALIASES:
                errs.append(f"signoff.{em_key} is a team alias")
        for d_key in ("consultant_signed_at", "client_signed_at"):
            if d_key in so and not DATE_RE.match(str(so[d_key])):
                errs.append(f"signoff.{d_key} must be ISO date")

    verdict = obj.get("verdict")
    if verdict and verdict not in VERDICTS:
        errs.append(f"verdict must be one of {sorted(VERDICTS)}")

    if "version" in obj and not VER_RE.match(str(obj["version"])):
        errs.append("version must be semver MAJOR.MINOR.PATCH")
    if "last_reviewed" in obj and not DATE_RE.match(str(obj["last_reviewed"])):
        errs.append("last_reviewed must be ISO date YYYY-MM-DD")
    return errs


VALID_FIXTURE = {
    "artefact_id": "chp-acme-2026-05",
    "client": "ACME",
    "engagement_end": "2026-05-23",
    "sections": {
        "scope_summary": "Built and shipped /v2/quote endpoint with Go shadow router; migrated from Python over 8 weeks.",
        "runbook": "Start: docker compose up. Stop: docker compose down. Debug: tail /var/log/quote.log; rotate flags via LaunchDarkly UI; restart with `systemctl restart quote-go`.",
        "architecture": "Diagram in docs/architecture.png. Go service on :8080, Python remains on :8081 until cutover. Postgres at :5432, Redis at :6379. External integrations: Stripe, Datadog.",
        "ops_surface": "Datadog dashboard ACME-quote; alerts to #ops Slack; logs retained 30 days."
    },
    "credentials": [{"name": "datadog_api_key", "vault_path": "op://faion.net/ACME/datadog", "rotation_date": "2026-05-22", "acknowledged_by": "successor@acme.com", "acknowledged_at": "2026-05-23"}],
    "open_items": [{"title": "Remove Python service", "severity": "medium", "effort": "M", "blast_radius": 3, "next_step": "Schedule for sprint 27"}],
    "successor_email": "successor@acme.com",
    "support_window": {"days": 30, "scope": "bug-fixes only", "sla_hours": 24, "channel": "slack #consultant-handover", "after_window": "hourly billing"},
    "signoff": {"consultant_signed_by": "ruslan@faion.net", "consultant_signed_at": "2026-05-23", "client_signed_by": "successor@acme.com", "client_signed_at": "2026-05-23"},
    "verdict": "archive-and-close",
    "version": "1.0.0",
    "last_reviewed": "2026-05-23",
}

INVALID_FIXTURE = {
    "artefact_id": "handover",
    "client": "ACME",
    "engagement_end": "today",
    "sections": {"scope_summary": "did the thing"},
    "credentials": [],
    "open_items": [{"title": "stuff", "severity": "med", "effort": "X", "blast_radius": 2, "next_step": ""}],
    "successor_email": "team@acme.com",
    "support_window": {"days": 365, "scope": "", "sla_hours": 0, "channel": "", "after_window": ""},
    "signoff": {},
    "verdict": "archive-and-close",
    "version": "1.0",
    "last_reviewed": "today",
}


def self_test() -> int:
    errs = validate(VALID_FIXTURE)
    if errs:
        sys.stderr.write(f"self-test FAILED: valid fixture rejected: {errs}\n")
        return 1
    errs = validate(INVALID_FIXTURE)
    if not errs:
        sys.stderr.write("self-test FAILED: invalid fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str, help="path to handover JSON")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.file:
        ap.print_help()
        return 2
    p = Path(args.file)
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n")
        return 2
    try:
        obj = json.loads(p.read_text())
    except json.JSONDecodeError as e:
        sys.stderr.write(f"invalid JSON: {e}\n")
        return 2
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
