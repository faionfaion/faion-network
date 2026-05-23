#!/usr/bin/env python3
"""validate-vision-basics.py — Validate extract() output JSON.

Inputs:
  - <result.json>  ImageResult JSON per 02-output-contract.xml.

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
CONFIDENCES = {"high", "low"}
STATUSES = {"ok", "error"}
REQUIRED = ["status", "description", "text_content", "confidence", "provider",
            "model", "cache_key", "cached"]
PLACEHOLDERS = {"see image", "as shown", "n/a", "tbd"}
BOILERPLATE = re.compile(r"^the image (shows|displays|contains)\s*\.?$", re.IGNORECASE)

VALID = {
    "status": "ok",
    "description": "An invoice from Acme Co dated 2026-04-15 totaling $1,247.50.",
    "text_content": "Acme Co\nInvoice #4421",
    "confidence": "high",
    "provider": "anthropic",
    "model": "claude-sonnet-4-5",
    "cache_key": "9f4a7c3e8d2b1a5f6e9c0d3b2a1f4e8d7c9b6a5d4e3c2b1a0f9e8d7c6b5a4f3e",
    "cached": False,
}
INVALID = {"status":"ok","description":"The image shows.","text_content":"see image",
           "confidence":"high","provider":"openai","model":"gpt-4o","cache_key":"abc","cached":False}

def validate(r):
    out = []
    for k in REQUIRED:
        if k not in r: out.append(f"missing field: {k}")
    if "status" in r and r["status"] not in STATUSES:
        out.append(f"status not in {STATUSES}")
    if "provider" in r and r["provider"] not in PROVIDERS:
        out.append(f"provider not in {PROVIDERS}")
    if "confidence" in r and r["confidence"] not in CONFIDENCES:
        out.append(f"confidence not in {CONFIDENCES}")
    if "cache_key" in r and not SHA256_RE.match(str(r["cache_key"])):
        out.append("cache_key must be 64-char sha256 hex")
    if r.get("status") == "ok":
        d = str(r.get("description",""))
        if len(d) < 10: out.append("description < 10 chars")
        if BOILERPLATE.match(d.strip()): out.append("description matches boilerplate")
        tc = r.get("text_content")
        if isinstance(tc, str) and tc.strip().lower() in PLACEHOLDERS:
            out.append(f"text_content is placeholder: {tc}")
        if (r.get("confidence") == "high" and isinstance(tc, str)
                and tc.strip().lower() in PLACEHOLDERS):
            out.append("confidence=high with placeholder text_content")
    return out

def main(a):
    if len(a) < 2 or a[1] in ("--help","-h"):
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

if __name__ == "__main__": sys.exit(main(sys.argv))
