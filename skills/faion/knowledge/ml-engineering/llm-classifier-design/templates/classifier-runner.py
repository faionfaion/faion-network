# purpose: Template fixture for llm-classifier-design: classifier-runner.py
# consumes: content/01-core-rules.xml
# produces: executable script
# depends-on: content/02-output-contract.xml
# token-budget-impact: small
"""Batch classifier runner: JSONL in, one forced tool call per batch, verdicts JSONL out.

Usage:
    python classifier-runner.py --config classifier-config.json \
        --system-prefix system-prefix.md --items items.jsonl --out verdicts.jsonl

classifier-config.json follows content/02-output-contract.xml
(model, batch_size, tool_schema{name,input_schema}, kappa_min, cache_system_prefix).
items.jsonl rows: {"id": "<external-id>", "text": "<item text>"}.
Requires: pip install anthropic   (sync Anthropic client; ANTHROPIC_API_KEY in the environment)
"""
from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

from anthropic import Anthropic

logger = logging.getLogger("classifier-runner")


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def build_user_message(chunk: list[dict]) -> str:
    # r3: numeric ids 1..N inside the message; the external id never reaches the model
    return "\n\n".join(f'<item id="{i + 1}">\n{row["text"]}\n</item>' for i, row in enumerate(chunk))


def classify_batch(client: Anthropic, cfg: dict, system_prefix: str, chunk: list[dict]) -> dict[str, str]:
    tool = cfg["tool_schema"]
    resp = client.messages.create(
        model=cfg["model"],  # r2: smallest model that cleared kappa_min, pinned in config
        max_tokens=16 * len(chunk) + 64,
        # r4: byte-identical prefix on every batch; cache_control makes it a cache hit from batch 2 on
        system=[{"type": "text", "text": system_prefix, "cache_control": {"type": "ephemeral"}}],
        tools=[{"name": tool["name"], "description": tool.get("description", "Report one verdict per item id."),
                "input_schema": tool["input_schema"]}],
        # r1: single forced tool call. On models that reject forced tool_choice
        # (claude-fable-5-1) switch to {"type": "auto"} plus strict=True on the tool.
        tool_choice={"type": "tool", "name": tool["name"]},
        messages=[{"role": "user", "content": build_user_message(chunk)}],
    )
    blocks = [b for b in resp.content if b.type == "tool_use"]
    if len(blocks) != 1:
        raise RuntimeError(f"expected exactly one tool_use block, got {len(blocks)} (r1)")
    verdicts: dict = blocks[0].input["verdicts"]  # r5: fixed shape, keyed by numeric id as string
    if set(verdicts) != {str(i + 1) for i in range(len(chunk))}:
        # procedure step 4 gate: count mismatch aborts the batch, never a partial write
        raise RuntimeError(f"verdict ids {sorted(verdicts)} != 1..{len(chunk)}; batch aborted")
    u = resp.usage
    cache_read = u.cache_read_input_tokens or 0
    cache_write = u.cache_creation_input_tokens or 0
    logger.info("batch=%d items input=%d cache_read=%d cache_write=%d",
                len(chunk), u.input_tokens, cache_read, cache_write)
    return {row["id"]: verdicts[str(i + 1)] for i, row in enumerate(chunk)}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", type=Path, required=True)
    ap.add_argument("--system-prefix", type=Path, required=True)
    ap.add_argument("--items", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    cfg = json.loads(args.config.read_text())
    if not cfg.get("cache_system_prefix", False):
        raise SystemExit("cache_system_prefix must be true (r4)")
    system_prefix = args.system_prefix.read_text()  # never f-string this; any byte change misses the cache
    items = load_jsonl(args.items)
    batch_size = int(cfg["batch_size"])
    client = Anthropic()

    n_ok, n_batches = 0, 0
    with args.out.open("w") as out:
        for start in range(0, len(items), batch_size):
            chunk = items[start:start + batch_size]
            try:
                results = classify_batch(client, cfg, system_prefix, chunk)
            except RuntimeError as exc:
                logger.error("batch at offset %d failed: %s", start, exc)
                continue
            for item_id, verdict in results.items():
                out.write(json.dumps({"id": item_id, "verdict": verdict}) + "\n")
            n_ok += len(results)
            n_batches += 1
    logger.info("done: %d/%d items in %d batches -> %s", n_ok, len(items), n_batches, args.out)
    # r4 check: cache_read should be non-zero on every batch after the first; if it stays 0
    # the prefix is under the model's minimum cacheable size or something varies between calls.
    return 0 if n_ok == len(items) else 1


if __name__ == "__main__":
    sys.exit(main())
