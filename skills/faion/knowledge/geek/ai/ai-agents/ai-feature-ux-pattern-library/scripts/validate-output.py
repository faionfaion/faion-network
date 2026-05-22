#!/usr/bin/env python3
"""validate-output.py - validate a ai-feature-ux-pattern-library output."""
from __future__ import annotations
import json, re, sys
from pathlib import Path

PLURAL = {"team","we","us","tbd",""}

def validate(p):
    v = []
    for k in ["artefact_id","owner","version","version_stamp","produced_at","rationale","inputs_used"]:
        if k not in p: v.append(f"missing {k}")
    if v: return v
    if str(p["owner"]).strip().lower() in PLURAL:
        v.append("owner must be a named individual or rotating role")
    if not re.fullmatch(r"\d+\.\d+\.\d+", p["version"]):
        v.append("version must be semver")
    if len(str(p["rationale"])) < 20:
        v.append("rationale too short (<20 chars)")
    if not p["inputs_used"]:
        v.append("inputs_used must be non-empty list")
    return v

def main(argv):
    if "--help" in argv or "-h" in argv:
        sys.stdout.write(__doc__ or ""); return 0
    if "--self-test" in argv:
        good = {"artefact_id":"a1","owner":"alex@faion.net","version":"1.0.0",
                "version_stamp":"x@1.0.0","produced_at":"2026-05-22T10:00:00Z",
                "rationale":"sufficiently long rationale string","inputs_used":["x.md"]}
        vs = validate(good)
        if vs: sys.stderr.write(f"FAIL: {vs}\n"); return 1
        sys.stdout.write("self-test passed\n"); return 0
    if len(argv) < 2:
        sys.stderr.write("usage: validate-output.py <output.json> [--self-test] [--help]\n"); return 2
    try:
        payload = json.loads(Path(argv[1]).read_text())
    except Exception as e:
        sys.stderr.write(f"load error: {e}\n"); return 3
    vs = validate(payload)
    if vs:
        for x in vs: sys.stderr.write(f"VIOLATION: {x}\n")
        return 1
    sys.stdout.write("OK\n"); return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
