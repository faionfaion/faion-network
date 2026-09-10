"""
purpose: CSV→JSONL builder with schema validation.
consumes: see AGENTS.md ## Prerequisites
produces: spec
depends-on: content/02-output-contract.xml schema for fine-tuning-openai-data-prep
token-budget-impact: ≤500 tokens to fill
"""
# Usage:
#   python openai-jsonl-builder.py --csv tickets.csv --user-col customer_message \
#       --assistant-col agent_reply --system "You are a support agent." \
#       --label-col tone_label --out-dir data/
# Add --rejected-col <column> to emit OpenAI DPO rows instead of chat rows.
# Output: data/train.jsonl + data/val.jsonl, hash-disjoint split, PII scrubbed.

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import random
import re
from collections import Counter
from pathlib import Path

# r6-no-pii: scrub before anything is written to disk.
PII_PATTERNS = {  # phone first: an email's hash token must never be re-read as digits
    "phone": re.compile(r"\+?\d[\d\s().-]{7,}\d"),
    "email": re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"),
}


def scrub_pii(text: str, counts: Counter) -> str:
    for name, pattern in PII_PATTERNS.items():
        def _hash(m: re.Match) -> str:
            counts[name] += 1
            return f"<{name}:{hashlib.sha256(m.group(0).encode()).hexdigest()[:10]}>"
        text = pattern.sub(_hash, text)
    return text


def build_row(system: str, user: str, assistant: str, rejected: str | None) -> dict:
    # r5-deterministic-system-prompt: `system` is the same constant for every row.
    messages = [{"role": "system", "content": system}, {"role": "user", "content": user}]
    if rejected is None:  # r1-jsonl-schema: chat format
        return {"messages": messages + [{"role": "assistant", "content": assistant}]}
    return {  # r1-jsonl-schema: DPO format (preferred vs non-preferred)
        "input": {"messages": messages},
        "preferred_output": [{"role": "assistant", "content": assistant}],
        "non_preferred_output": [{"role": "assistant", "content": rejected}],
    }


def balance(rows: list[tuple[str, dict]], max_ratio: float, rng: random.Random) -> list[dict]:
    """r4-balanced-classes: downsample majority classes to within max_ratio of the smallest."""
    by_label: dict[str, list[dict]] = {}
    for label, row in rows:
        by_label.setdefault(label, []).append(row)
    floor = min(len(v) for v in by_label.values())
    cap = int(floor * max_ratio)
    out: list[dict] = []
    for label, items in by_label.items():
        if len(items) > cap:
            print(f"balance: {label} {len(items)} -> {cap} (cap {max_ratio}x of {floor})")
            items = rng.sample(items, cap)
        out.extend(items)
    return out


def split(rows: list[dict], val_pct: int) -> tuple[list[dict], list[dict]]:
    """r3-train-val-split: hash-disjoint on the user turn, so near-duplicates never straddle."""
    train, val = [], []
    for row in rows:
        user_text = (row.get("messages") or row["input"]["messages"])[1]["content"]
        bucket = int(hashlib.sha1(user_text.encode()).hexdigest(), 16) % 100
        (val if bucket < val_pct else train).append(row)
    return train, val


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True)
    ap.add_argument("--system", required=True, help="canonical system prompt, one string")
    ap.add_argument("--user-col", required=True)
    ap.add_argument("--assistant-col", required=True)
    ap.add_argument("--rejected-col", help="non-preferred reply column; switches output to DPO")
    ap.add_argument("--label-col", help="class label column; enables 1.5x balancing")
    ap.add_argument("--out-dir", default="data")
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    rng = random.Random(args.seed)
    pii = Counter()
    seen: set[str] = set()
    labelled: list[tuple[str, dict]] = []
    with open(args.csv, newline="", encoding="utf-8") as fh:
        for rec in csv.DictReader(fh):
            user = scrub_pii(rec[args.user_col].strip(), pii)
            assistant = scrub_pii(rec[args.assistant_col].strip(), pii)
            rejected = scrub_pii(rec[args.rejected_col].strip(), pii) if args.rejected_col else None
            if not user or not assistant or (args.rejected_col and not rejected):
                continue
            key = hashlib.sha1(f"{user}\x00{assistant}".encode()).hexdigest()
            if key in seen:
                continue
            seen.add(key)
            labelled.append((rec[args.label_col] if args.label_col else "_", build_row(args.system, user, assistant, rejected)))

    rows = balance(labelled, 1.5, rng) if args.label_col else [r for _, r in labelled]
    if len(rows) < 10:
        raise SystemExit(f"only {len(rows)} usable rows; OpenAI rejects uploads under 10")
    val_pct = 30 if len(rows) < 500 else 20
    train, val = split(rows, val_pct)

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    for name, chunk in (("train", train), ("val", val)):
        with open(out / f"{name}.jsonl", "w", encoding="utf-8") as fh:
            for row in chunk:
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(json.dumps({"train_count": len(train), "val_count": len(val), "val_pct": val_pct,
                      "pii_matches": dict(pii), "format": "dpo" if args.rejected_col else "chat"}))


if __name__ == "__main__":
    main()
