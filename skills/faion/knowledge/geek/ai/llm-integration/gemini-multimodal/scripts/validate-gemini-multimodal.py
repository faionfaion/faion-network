#!/usr/bin/env python3
"""validate-gemini-multimodal.py — validate a gemini-multimodal-config.json.

Usage:
    validate-gemini-multimodal.py --config <path>
    validate-gemini-multimodal.py --self-test
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

MODALITIES = {"image", "audio", "video", "pdf", "mixed"}


def validate(c: dict) -> list[dict]:
    v: list[dict] = []
    if not (0 < c.get("inline_limit_mb", 0) <= 4):
        v.append({"rule": "r1", "field": "inline_limit_mb", "msg": "must be in (0, 4]"})
    if c.get("modality") not in MODALITIES:
        v.append({"rule": "schema", "field": "modality", "msg": "invalid modality"})
    fa = c.get("files_api") or {}
    if not fa.get("enabled") and c.get("modality") in {"audio", "video", "pdf"}:
        v.append({"rule": "r1", "field": "files_api.enabled", "msg": "must be enabled for audio/video/pdf"})
    if not (1 <= fa.get("ttl_hours", 0) <= 48):
        v.append({"rule": "r3", "field": "files_api.ttl_hours", "msg": "must be in [1, 48]"})
    cc = c.get("context_cache") or {}
    if cc.get("enabled") and cc.get("min_tokens", 0) < 32768:
        v.append({"rule": "r4", "field": "context_cache.min_tokens", "msg": "must be >=32768"})
    return v


def self_test() -> int:
    smoke = json.loads(Path(__file__).parent.parent.joinpath("templates/_smoke-test.json").read_text(encoding="utf-8"))
    for k in list(smoke):
        if k.startswith("_"):
            smoke.pop(k)
    assert validate(smoke) == [], f"smoke must pass: {validate(smoke)}"
    bad = dict(smoke); bad["inline_limit_mb"] = 50
    assert any(x["rule"] == "r1" for x in validate(bad))
    sys.stdout.write("self-test: OK\n")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", type=Path)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    if not args.config:
        ap.error("--config required")
        return 2
    data = json.loads(args.config.read_text(encoding="utf-8"))
    v = validate(data)
    sys.stdout.write(json.dumps({"ok": not v, "violations": v}, indent=2) + "\n")
    return 0 if not v else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
