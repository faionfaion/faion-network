#!/usr/bin/env python3
"""validate-vui-market-context.py

Validate vui_market_brief.json against the schema in 02-output-contract.xml.

Inputs:
    --file PATH       path to brief JSON
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid
    1 = invalid (violations printed to stderr)
    2 = usage / unreadable input
"""
from __future__ import annotations

import argparse
import datetime
import json
import sys
from pathlib import Path
from urllib.parse import urlparse

TRUSTED = {"statista.com", "voicebot.ai", "edisonresearch.com",
           "nngroup.com", "pewresearch.org", "gartner.com"}
DENOMS = {"smart-speaker-households", "voice-assistant-users", "voice-search-query-share"}
PLATFORMS = {"Alexa", "Google Assistant", "Siri", "Bixby", "Custom LLM-VUI"}
ROW_KEYS = ("metric", "value", "year", "source_url", "geo", "denominator")
MAX_AGE_DAYS = 90


def host_of(url: str) -> str:
    try:
        host = urlparse(url).hostname or ""
    except ValueError:
        return ""
    return host.lower().lstrip("www.")


def in_trusted(host: str) -> bool:
    return any(host == t or host.endswith("." + t) for t in TRUSTED)


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in ("refreshed_at", "model", "data", "platforms"):
        if k not in obj:
            errs.append(f"missing top-level key: {k}")
    if errs:
        return errs
    try:
        ref = datetime.date.fromisoformat(obj["refreshed_at"])
        if (datetime.date.today() - ref).days > MAX_AGE_DAYS:
            errs.append(f"brief older than {MAX_AGE_DAYS} days: {obj['refreshed_at']}")
    except (TypeError, ValueError):
        errs.append(f"refreshed_at not ISO date: {obj['refreshed_at']!r}")
    data = obj.get("data", [])
    if not isinstance(data, list) or len(data) < 4:
        errs.append("data must be array with >=4 items")
    else:
        for i, row in enumerate(data):
            for k in ROW_KEYS:
                if k not in row or row[k] in (None, ""):
                    errs.append(f"data[{i}] missing field: {k}")
            if row.get("denominator") not in DENOMS:
                errs.append(f"data[{i}].denominator not in enum: {row.get('denominator')}")
            host = host_of(row.get("source_url", ""))
            if not in_trusted(host):
                errs.append(f"data[{i}].source_url host not trusted: {host}")
    plats = obj.get("platforms", [])
    seen = {p.get("name") for p in plats if isinstance(p, dict)}
    missing = PLATFORMS - seen
    if missing:
        errs.append(f"platforms missing entries: {sorted(missing)}")
    return errs


OK = {
    "refreshed_at": datetime.date.today().isoformat(),
    "model": "claude-opus-4-7",
    "data": [
        {"metric": "smart-speaker household penetration", "value": "55%", "year": 2025,
         "source_url": "https://www.edisonresearch.com/infinite-dial-2025/",
         "geo": "US", "denominator": "smart-speaker-households", "confidence": "high"},
        {"metric": "voice-search share", "value": "20%", "year": 2025,
         "source_url": "https://www.statista.com/topics/4642/voice-assistants/",
         "geo": "global", "denominator": "voice-search-query-share", "confidence": "medium"},
        {"metric": "US adults using voice assistant", "value": "62%", "year": 2025,
         "source_url": "https://www.pewresearch.org/internet/fact-sheet/mobile/",
         "geo": "US", "denominator": "voice-assistant-users", "confidence": "high"},
        {"metric": "voice assistants globally", "value": "8.4B", "year": 2025,
         "source_url": "https://www.voicebot.ai/voice-assistant-statistics/",
         "geo": "global", "denominator": "voice-assistant-users", "confidence": "medium"},
    ],
    "platforms": [
        {"name": "Alexa", "reach_by_geo": {"US": 0.7}, "sdk_health": "maintained"},
        {"name": "Google Assistant", "reach_by_geo": {"global": 0.6}, "sdk_health": "maintained"},
        {"name": "Siri", "reach_by_geo": {"iOS": 0.95}, "sdk_health": "maintained"},
        {"name": "Bixby", "reach_by_geo": {"KR": 0.4}, "sdk_health": "maintained"},
        {"name": "Custom LLM-VUI", "reach_by_geo": {"any": 1.0}, "sdk_health": "active"},
    ],
}
BAD = {"data": [{"metric": "voice usage", "value": "62%", "year": 2025}]}


def self_test() -> int:
    if validate(OK):
        sys.stderr.write("ok rejected\n")
        return 1
    if not validate(BAD):
        sys.stderr.write("bad accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--file", type=str)
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
