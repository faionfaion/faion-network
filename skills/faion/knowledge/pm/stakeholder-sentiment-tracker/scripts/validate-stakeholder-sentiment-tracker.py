#!/usr/bin/env python3
"""validate-stakeholder-sentiment-tracker.py — Validate a weekly sentiment-tracker run.

Inputs:
  - <run.json>  Path to the weekly run JSON.

Outputs:
  - stdout: PASS / FAIL with violation list.

Exit codes:
  0 - run validates.
  1 - run violates schema / consent / alarm rules.
  2 - usage error.

Flags:
  --help        Show this message.
  --self-test   Run against a built-in fixture.
"""
from __future__ import annotations

import datetime as dt
import json
import sys
from pathlib import Path

ALLOWED_CLASSES = {"supportive", "cautious", "hostile", "no-signal"}
MIN_TREND_WEEKS = 4

VALID_FIXTURE = {
    "run_date": dt.date.today().isoformat(),
    "stakeholders": [
        {
            "name": "Maria",
            "consent_date": "2026-01-10",
            "class": "cautious",
            "trend": ["supportive", "supportive", "supportive", "cautious"],
            "alarm": {"fired": False, "reason": ""},
        }
    ],
}
INVALID_FIXTURE = {"run_date": "x", "stakeholders": [{"name": "Maria", "score": 4}]}


def validate(spec: dict) -> list[str]:
    out: list[str] = []
    try:
        dt.date.fromisoformat(str(spec.get("run_date", "")))
    except ValueError:
        out.append("run_date not ISO date")
    sks = spec.get("stakeholders", [])
    if not isinstance(sks, list) or not sks:
        out.append("stakeholders must be non-empty list")
        return out
    for i, s in enumerate(sks):
        if not isinstance(s, dict):
            out.append(f"stakeholders[{i}] not object")
            continue
        if "name" not in s:
            out.append(f"stakeholders[{i}].name missing")
        if "consent_date" not in s:
            out.append(f"stakeholders[{i}].consent_date missing")
        else:
            try:
                dt.date.fromisoformat(str(s["consent_date"]))
            except ValueError:
                out.append(f"stakeholders[{i}].consent_date not ISO date")
        cls = s.get("class")
        if cls not in ALLOWED_CLASSES:
            out.append(f"stakeholders[{i}].class must be one of {sorted(ALLOWED_CLASSES)}")
        tr = s.get("trend", [])
        if not isinstance(tr, list) or len(tr) < MIN_TREND_WEEKS:
            out.append(f"stakeholders[{i}].trend must have >= {MIN_TREND_WEEKS} weeks")
        else:
            for j, t in enumerate(tr):
                if t not in ALLOWED_CLASSES:
                    out.append(f"stakeholders[{i}].trend[{j}] invalid class {t}")
        if "score" in s:
            out.append(f"stakeholders[{i}].score forbidden (numeric scores not allowed)")
        alarm = s.get("alarm", {})
        if isinstance(alarm, dict) and alarm.get("fired"):
            ap = alarm.get("action_plan")
            if not isinstance(ap, dict) or not all(k in ap for k in ("hypothesis", "intervention", "deadline")):
                out.append(f"stakeholders[{i}].alarm.action_plan must include hypothesis, intervention, deadline")
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
