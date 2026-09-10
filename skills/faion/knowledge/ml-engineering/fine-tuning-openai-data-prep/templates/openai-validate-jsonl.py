"""
purpose: Pre-upload validator (schema + token counts).
consumes: see AGENTS.md ## Prerequisites
produces: spec
depends-on: content/02-output-contract.xml schema for fine-tuning-openai-data-prep
token-budget-impact: ≤500 tokens to fill
"""
# Usage:
#   python openai-validate-jsonl.py data/train.jsonl data/val.jsonl \
#       --model gpt-4o-mini-2024-07-18 --epochs 3
# Exit 0 = safe to upload. Prints a token_budget JSON for data-prep-spec.md.
# Requires: pip install tiktoken (falls back to a 4-chars-per-token estimate).

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter

try:
    import tiktoken
    _ENC = tiktoken.get_encoding("o200k_base")  # gpt-4o / gpt-4.1 family
except ImportError:  # pragma: no cover
    _ENC = None

# r2-token-budget: per-example cap = training context of the base model.
# Values from OpenAI fine-tuning docs (2025); re-check before a new base model.
CONTEXT_CAP = {"gpt-4o-mini": 65536, "gpt-4o": 65536, "gpt-4.1": 65536,
               "gpt-4.1-mini": 65536, "gpt-4.1-nano": 65536, "gpt-3.5-turbo": 16385}
# Training price, USD per 1M tokens (openai.com/pricing, 2025). Verify before quoting.
PRICE_PER_1M = {"gpt-4o-mini": 3.0, "gpt-4o": 25.0, "gpt-4.1": 25.0,
                "gpt-4.1-mini": 5.0, "gpt-4.1-nano": 1.5, "gpt-3.5-turbo": 8.0}
ROLES = {"system", "user", "assistant"}
PII = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+|\+?\d[\d\s().-]{7,}\d")


def family(model: str) -> str:
    return next((k for k in sorted(CONTEXT_CAP, key=len, reverse=True) if model.startswith(k)), "gpt-4o-mini")


def count_tokens(text: str) -> int:
    return len(_ENC.encode(text)) if _ENC else max(1, len(text) // 4)


def messages_of(row: dict) -> list[dict]:
    """r1-jsonl-schema: chat, DPO or legacy completion; anything else is a schema error."""
    if "messages" in row:
        return row["messages"]
    if "input" in row and "preferred_output" in row and "non_preferred_output" in row:
        return row["input"]["messages"] + row["preferred_output"] + row["non_preferred_output"]
    if "prompt" in row and "completion" in row:
        return [{"role": "user", "content": row["prompt"]}, {"role": "assistant", "content": row["completion"]}]
    raise ValueError("no messages / DPO triple / prompt+completion keys")


def check_messages(msgs: list[dict]) -> None:
    roles = [m.get("role") for m in msgs]
    if not set(roles) <= ROLES:
        raise ValueError(f"unknown role in {roles}")
    if "user" not in roles or "assistant" not in roles:
        raise ValueError("needs at least one user and one assistant turn")
    if any(not isinstance(m.get("content"), str) or not m["content"].strip() for m in msgs):
        raise ValueError("empty or non-string content")


def validate(path: str, cap: int) -> dict:
    errors: list[str] = []
    tokens: list[int] = []
    system_prompts: Counter = Counter()
    pii_hits = 0
    with open(path, encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            try:
                row = json.loads(line)
                msgs = messages_of(row)
                check_messages(msgs)
            except (ValueError, KeyError, TypeError) as exc:
                errors.append(f"{path}:{n}: {exc}")
                continue
            total = sum(count_tokens(m["content"]) + 4 for m in msgs)  # +4 per message overhead
            if total > cap:  # r2-token-budget: silent truncation corrupts the signal
                errors.append(f"{path}:{n}: {total} tokens > cap {cap}")
            tokens.append(total)
            for m in msgs:
                if m["role"] == "system":
                    system_prompts[m["content"]] += 1
                pii_hits += len(PII.findall(m["content"]))  # r6-no-pii
    if len(system_prompts) > 1:  # r5-deterministic-system-prompt
        errors.append(f"{path}: {len(system_prompts)} distinct system prompts; expected exactly 1")
    if pii_hits:
        errors.append(f"{path}: {pii_hits} PII-looking matches; scrub before upload")
    if len(tokens) < 10:
        errors.append(f"{path}: {len(tokens)} examples; OpenAI minimum is 10")
    return {"count": len(tokens), "total_tokens": sum(tokens),
            "max_tokens": max(tokens, default=0), "errors": errors}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+", help="train.jsonl [val.jsonl]")
    ap.add_argument("--model", default="gpt-4o-mini-2024-07-18")
    ap.add_argument("--epochs", type=int, default=3)
    ap.add_argument("--max-tokens", type=int, help="override the per-example context cap")
    args = ap.parse_args()

    fam = family(args.model)
    cap = args.max_tokens or CONTEXT_CAP[fam]
    reports = {f: validate(f, cap) for f in args.files}
    errors = [e for r in reports.values() for e in r["errors"]]
    train_tokens = reports[args.files[0]]["total_tokens"]
    summary = {
        "model": args.model, "context_cap": cap,
        "files": {f: {k: v for k, v in r.items() if k != "errors"} for f, r in reports.items()},
        "token_budget": {"total_tokens": train_tokens * args.epochs,
                         "estimated_usd": round(train_tokens * args.epochs / 1e6 * PRICE_PER_1M[fam], 2)},
        "error_count": len(errors),
    }
    print(json.dumps(summary, indent=2))
    for e in errors[:50]:
        print(e, file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
