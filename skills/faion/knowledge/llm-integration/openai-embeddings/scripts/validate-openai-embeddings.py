#!/usr/bin/env python3
"""validate-openai-embeddings.py — Validate an embed-record JSON file.

Inputs:
  - <record.json>  Path to a JSON record matching content/02-output-contract.xml schema.

Outputs:
  - stdout: PASS / FAIL with violation list.

Exit codes:
  0 - record validates.
  1 - record violates schema.
  2 - usage error.

Flags:
  --help        Show this message.
  --self-test   Run against built-in valid + invalid fixtures.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MODELS = {"text-embedding-3-small", "text-embedding-3-large", "text-embedding-ada-002"}
CID_RE = re.compile(r"^[a-zA-Z0-9_\-:]+$")
HASH_RE = re.compile(r"^[a-f0-9]{16,64}$")

VALID_FIXTURE = {
    "custom_id": "doc_42_chunk_3",
    "model": "text-embedding-3-small",
    "dimensions": 1536,
    "vector_len": 1536,
    "source_hash": "9a8b7c6d5e4f3210",
    "chunk_text": "Embeddings encode semantic meaning into dense vectors of fixed dimensionality.",
    "embedded_at": "2026-05-22T12:34:56Z",
}
INVALID_FIXTURE = {
    "custom_id": "doc_42",
    "model": "text-embedding-3-small",
    "dimensions": 1536,
    "vector_len": 3072,
    "source_hash": "",
    "chunk_text": "",
}


def validate(rec: dict) -> list[str]:
    out: list[str] = []
    for k in ("custom_id", "model", "dimensions", "vector_len", "source_hash", "chunk_text", "embedded_at"):
        if k not in rec:
            out.append(f"missing field: {k}")
    if "custom_id" in rec and (not isinstance(rec["custom_id"], str) or not CID_RE.match(rec["custom_id"]) or len(rec["custom_id"]) < 4):
        out.append("custom_id must match ^[a-zA-Z0-9_\\-:]+$ and len >= 4")
    if "model" in rec and rec["model"] not in MODELS:
        out.append(f"model must be one of {sorted(MODELS)}")
    if "dimensions" in rec and (not isinstance(rec["dimensions"], int) or not 1 <= rec["dimensions"] <= 3072):
        out.append("dimensions must be int in [1, 3072]")
    if "vector_len" in rec and (not isinstance(rec["vector_len"], int) or not 1 <= rec["vector_len"] <= 3072):
        out.append("vector_len must be int in [1, 3072]")
    if rec.get("vector_len") and rec.get("dimensions") and rec["vector_len"] != rec["dimensions"]:
        out.append(f"vector_len ({rec['vector_len']}) != dimensions ({rec['dimensions']})")
    if "source_hash" in rec and not HASH_RE.match(str(rec.get("source_hash", ""))):
        out.append("source_hash must be hex 16-64 chars")
    if "chunk_text" in rec and (not isinstance(rec["chunk_text"], str) or not rec["chunk_text"].strip()):
        out.append("chunk_text must be non-empty string")
    return out


def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[1] in ("--help", "-h"):
        sys.stdout.write(__doc__ or "")
        return 0 if any(a in ("--help", "-h") for a in argv) else 2
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
        rec = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        sys.stderr.write(f"invalid JSON: {exc}\n")
        return 1
    v = validate(rec)
    if v:
        sys.stdout.write("FAIL\n")
        for x in v:
            sys.stdout.write(f"  - {x}\n")
        return 1
    sys.stdout.write("PASS\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
