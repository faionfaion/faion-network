# purpose: Batch API submit + poll + errored-resubmit loop.
# consumes: list[{id, prompt}] (id == DB primary key).
# produces: list[{id, text}] or list[{id, error}]; errored items are re-emitted for resubmission.
# depends-on: rules r5 + r6 in content/01-core-rules.xml.
# token-budget-impact: 50% discount on input + output for batched calls (24h SLA).
"""Batch API submit + poll + errored-resubmit loop."""
from __future__ import annotations

import time

import anthropic

client = anthropic.Anthropic()

MODEL_ID = "claude-sonnet-4-20250514"
POLL_INTERVAL_SECONDS = 60  # rule r5: ≥60s polling cadence.


def submit_batch(prompts: list[dict]) -> str:
    """Submit a batch. `prompts` items must each have `id` (db pk) and `prompt`."""
    if not prompts:
        raise ValueError("Empty batch refused.")
    reqs = [
        {
            "custom_id": p["id"],
            "params": {
                "model": MODEL_ID,
                "max_tokens": 1024,
                "messages": [{"role": "user", "content": p["prompt"]}],
            },
        }
        for p in prompts
    ]
    return client.messages.batches.create(requests=reqs).id


def poll_and_collect(batch_id: str, poll_interval: int = POLL_INTERVAL_SECONDS) -> list[dict]:
    """Poll until `processing_status == "ended"`; errored items returned for resubmit (rule r6)."""
    if poll_interval < 60:
        raise ValueError("Poll interval below 60 violates rule r5.")
    while True:
        batch = client.messages.batches.retrieve(batch_id)
        if batch.processing_status == "ended":
            out: list[dict] = []
            for r in client.messages.batches.results(batch_id):
                if r.result.type == "succeeded":
                    out.append({"id": r.custom_id, "text": r.result.message.content[0].text})
                else:
                    out.append({"id": r.custom_id, "error": str(r.result.error), "resubmit": True})
            return out
        time.sleep(poll_interval)
