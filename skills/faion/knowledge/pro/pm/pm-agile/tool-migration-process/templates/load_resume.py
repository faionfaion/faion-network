#!/usr/bin/env python3
"""Load JSONL of target-shaped issues; resumes from .checkpoint on rerun.

Usage:
    cat transformed.jsonl | TARGET_API_URL=https://... TARGET_TOKEN=tok_... python load_resume.py

Input:  JSONL on stdin; each record must have a `_source_id` field.
Output: prints OK <source_id> -> <target_id> per successful record.
        Writes completed source IDs to .load_checkpoint.
        Exits non-zero on unrecoverable error.
"""
import json
import os
import sys
import time

import requests

CHECKPOINT = ".load_checkpoint"
done = set(open(CHECKPOINT).read().split()) if os.path.exists(CHECKPOINT) else set()
URL = os.environ["TARGET_API_URL"]
TOK = os.environ["TARGET_TOKEN"]

with open(CHECKPOINT, "a") as ck:
    for line in sys.stdin:
        rec = json.loads(line)
        sid = rec["_source_id"]
        if sid in done:
            continue
        for attempt in range(5):
            r = requests.post(URL, json=rec, headers={"Authorization": TOK})
            if r.status_code < 300:
                break
            if r.status_code == 429:
                time.sleep(2**attempt)
                continue
            sys.exit(f"FAIL {sid}: {r.status_code} {r.text[:200]}")
        ck.write(sid + "\n")
        ck.flush()
        print(f"OK {sid} -> {r.json()['id']}")
