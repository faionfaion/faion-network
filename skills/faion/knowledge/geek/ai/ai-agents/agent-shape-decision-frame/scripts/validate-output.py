#!/usr/bin/env python3
"""validate-output.py — validate an agent-shape-decision-frame record.

Inputs: path to JSON record. Exit 0 if valid; 1 with violations on stderr.
Exit codes: 0=valid, 1=violations, 2=usage, 3=load.
"""

from __future__ import annotations
import json, re, sys
from pathlib import Path

ALLOWED_SHAPES = {"single-turn-single-agent", "single-turn-with-human-gate",
                  "multi-turn-single-agent", "multi-agent", "hosted-only", "escalate"}

def validate(p: dict) -> list[str]:
    v = []
    for k in ["shape_id", "chosen_shape", "framing", "rejected_shapes", "owner", "version", "produced_at"]:
        if k not in p:
            v.append(f"missing {k}")
    if v: return v
    if p["chosen_shape"] not in ALLOWED_SHAPES:
        v.append(f"chosen_shape must be in {sorted(ALLOWED_SHAPES)}")
    f = p["framing"]
    for fk in ["turn_count", "agent_count", "tool_surface", "deployment_surface", "eval_available"]:
        if fk not in f:
            v.append(f"framing.{fk} missing")
    ts = f.get("tool_surface", {})
    for tk in ["read", "scratch", "prod_mutating"]:
        if not isinstance(ts.get(tk), int) or ts[tk] < 0:
            v.append(f"framing.tool_surface.{tk} must be non-negative int")
    if not isinstance(p["rejected_shapes"], list) or not p["rejected_shapes"]:
        v.append("rejected_shapes must be non-empty")
    if str(p["owner"]).strip().lower() in {"team", "we", "us", "tbd", ""}:
        v.append("owner must be named individual")
    if not re.fullmatch(r"\d+\.\d+\.\d+", p["version"]):
        v.append("version must be semver")
    return v

def main(argv):
    if "--help" in argv or "-h" in argv:
        sys.stdout.write(__doc__); return 0
    if "--self-test" in argv:
        good = {"shape_id":"x","chosen_shape":"multi-turn-single-agent",
                "framing":{"turn_count":"multi","agent_count":"single",
                           "tool_surface":{"read":2,"scratch":2,"prod_mutating":0},
                           "deployment_surface":"custom","eval_available":True},
                "rejected_shapes":[{"shape":"multi-agent","reason":"one domain"}],
                "owner":"a@b","version":"1.0.0","produced_at":"2026-05-22T12:00:00Z"}
        vs = validate(good)
        if vs: sys.stderr.write(f"self-test FAILED: {vs}\n"); return 1
        sys.stdout.write("self-test passed\n"); return 0
    if len(argv) < 2:
        sys.stderr.write("usage: validate-output.py <record.json> [--self-test] [--help]\n"); return 2
    try:
        payload = json.loads(Path(argv[1]).read_text())
    except Exception as exc:
        sys.stderr.write(f"load error: {exc}\n"); return 3
    vs = validate(payload)
    if vs:
        for x in vs: sys.stderr.write(f"VIOLATION: {x}\n")
        return 1
    sys.stdout.write("OK\n"); return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
