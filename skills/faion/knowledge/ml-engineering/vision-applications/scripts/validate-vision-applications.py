#!/usr/bin/env python3
"""validate-vision-applications.py — Validate task-specific VLM output.

Inputs:
  - <result.json>  Output JSON with task ∈ {document, classify, moderate}.

Outputs:
  - stdout: PASS / FAIL with violation list.

Exit codes: 0 valid, 1 invalid, 2 usage.

Flags: --help, --self-test.
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path

SHA256_RE = re.compile(r"^[a-f0-9]{64}$")
PROVIDERS = {"openai", "anthropic", "google"}
SEVERITIES = {"none", "low", "medium", "high"}

VALID = {
    "status": "ok", "task": "moderate", "is_safe": False,
    "flags": ["violence"], "severity": "high",
    "confidence": 0.92, "needs_human_review": True,
    "provider": "openai", "model": "gpt-4o",
    "cache_key": "9f4a7c3e8d2b1a5f6e9c0d3b2a1f4e8d7c9b6a5d4e3c2b1a0f9e8d7c6b5a4f3e",
    "cached": False,
}
INVALID = {
    "status": "ok", "task": "moderate", "is_safe": False, "flags": [],
    "severity": "HIGH", "confidence": 0.45, "needs_human_review": False,
    "provider": "openai", "model": "gpt-4o", "cache_key": "abc", "cached": False,
}


def validate(r: dict) -> list[str]:
    out = []
    common = ["status", "task", "provider", "model", "cache_key", "cached"]
    for k in common:
        if k not in r: out.append(f"missing field: {k}")
    task = r.get("task")
    if task not in {"document", "classify", "moderate"}:
        out.append(f"task not in document|classify|moderate (got {task})")
    if "provider" in r and r["provider"] not in PROVIDERS:
        out.append(f"provider not in {PROVIDERS}")
    if "cache_key" in r and not SHA256_RE.match(str(r["cache_key"])):
        out.append("cache_key must be 64-char sha256 hex")
    if task == "document":
        if "fields" not in r or not isinstance(r["fields"], dict):
            out.append("document task missing fields dict")
    elif task == "classify":
        for k in ("category", "confidence", "reasoning"):
            if k not in r: out.append(f"classify missing {k}")
        if isinstance(r.get("category"), str) and r["category"] != r["category"].lower():
            out.append("category not lowercased (rule r4)")
    elif task == "moderate":
        for k in ("is_safe", "flags", "severity", "confidence", "needs_human_review"):
            if k not in r: out.append(f"moderate missing {k}")
        if isinstance(r.get("severity"), str):
            sev = r["severity"]
            if sev != sev.lower(): out.append("severity not lowercased (rule r4)")
            if sev.lower() not in SEVERITIES: out.append(f"severity not in {SEVERITIES}")
        conf = r.get("confidence")
        if isinstance(conf, (int, float)):
            sev = str(r.get("severity", "")).lower()
            should_review = conf < 0.7 or sev in {"medium", "high"}
            if should_review and not r.get("needs_human_review"):
                out.append("needs_human_review must be true when conf<0.7 or severity≥medium (rule r6)")
    return out


def main(a):
    if len(a) < 2 or a[1] in ("--help", "-h"):
        sys.stdout.write(__doc__ or ""); return 0 if "--help" in a else 2
    if a[1] == "--self-test":
        ok = validate(VALID); bad = validate(INVALID)
        if ok: sys.stderr.write(f"self-test FAIL: valid rejected: {ok}\n"); return 1
        if not bad: sys.stderr.write("self-test FAIL: invalid accepted\n"); return 1
        sys.stdout.write("self-test OK\n"); return 0
    p = Path(a[1])
    if not p.is_file(): sys.stderr.write(f"not a file: {p}\n"); return 2
    try: data = json.loads(p.read_text())
    except json.JSONDecodeError as e: sys.stderr.write(f"invalid JSON: {e}\n"); return 1
    v = validate(data)
    if v:
        sys.stdout.write("FAIL\n")
        for x in v: sys.stdout.write(f"  - {x}\n")
        return 1
    sys.stdout.write("PASS\n"); return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
