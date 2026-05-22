# purpose: batch + cache stack reference for an Anthropic-style pipeline
# consumes: workload jsonl, frozen system prompt
# produces: batch submission with cache_control marker on stable prefix
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~5% of sync-uncached on cached portion (50% batch × 90% cache read)
"""Anthropic Messages Batches with prompt caching — canonical stack.

Effective input cost on cached tokens: 0.5 (batch) * 0.1 (cache read) = 0.05x of
synchronous-uncached price. The first item pays cache-write (1.25x) once.

Required for the stack to fire:
1. system + tools are byte-identical across all items in the batch
2. cache_control sits on the LAST static block (system here)
3. variable content lives only in the user message at the end
"""
from __future__ import annotations

import hashlib
import json

from anthropic import Anthropic
from anthropic.types.beta.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.messages.batch_create_params import Request

client = Anthropic()

SYSTEM_PROMPT = (
    "You are a precise document analyst. "
    "Return JSON matching the schema in the user message."
)

TOOLS: list[dict] = []  # populate with static tool defs; do not sort at runtime


def _prefix_hash(system: str, tools: list[dict]) -> str:
    payload = json.dumps({"system": system, "tools": tools}, sort_keys=True)
    return hashlib.sha256(payload.encode()).hexdigest()


def submit_batch(docs: list[dict]) -> str:
    expected = _prefix_hash(SYSTEM_PROMPT, TOOLS)
    requests: list[Request] = []
    for i, doc in enumerate(docs):
        params = MessageCreateParamsNonStreaming(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system=[
                {
                    "type": "text",
                    "text": SYSTEM_PROMPT,
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            tools=TOOLS,
            messages=[{"role": "user", "content": doc["text"]}],
        )
        assert _prefix_hash(SYSTEM_PROMPT, TOOLS) == expected
        requests.append(Request(custom_id=f"doc-{i}", params=params))

    batch = client.messages.batches.create(requests=requests)
    return batch.id
