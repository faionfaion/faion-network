# purpose: Batch API submit + poll + errored-resubmit helpers for ClaudeService.
# consumes: list[{id, messages, [model], [max_tokens]}]; id == DB primary key.
# produces: list[{id, text}] succeeded + list[{id, error, resubmit:True}] errored.
# depends-on: rule r7 in content/01-core-rules.xml.
# token-budget-impact: 50% discount on input + output for batched calls (24h SLA).
"""Anthropic Batch API helpers — create + poll + resubmit-errored."""
from __future__ import annotations

import time

import anthropic

POLL_INTERVAL_SECONDS = 60  # rule r7: ≥60s.


def create_batch(client: anthropic.Anthropic, requests: list[dict]) -> str:
    if not requests:
        raise ValueError("Empty batch refused.")
    batch = client.messages.batches.create(
        requests=[
            {
                "custom_id": r["id"],
                "params": {
                    "model": r.get("model", "claude-sonnet-4-20250514"),
                    "max_tokens": r.get("max_tokens", 1024),
                    "messages": r["messages"],
                },
            }
            for r in requests
        ]
    )
    return batch.id


def poll_batch(client: anthropic.Anthropic, batch_id: str, poll_interval: int = POLL_INTERVAL_SECONDS) -> list[dict]:
    """Poll until `processing_status == "ended"`. Errored items flagged for resubmit."""
    if poll_interval < 60:
        raise ValueError("Poll interval below 60 violates rule r7.")
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
