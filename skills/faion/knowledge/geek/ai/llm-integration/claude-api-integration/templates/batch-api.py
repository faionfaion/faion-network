"""
Anthropic Batch API helpers — create batch jobs and poll for results.

Batch API provides 50% cost reduction. Processing time: up to 24 hours.
Not suitable for real-time workflows; use for offline enrichment only.

Usage:
    requests = [
        {"id": "r1", "messages": [{"role": "user", "content": "Hello"}]},
        {"id": "r2", "messages": [{"role": "user", "content": "World"}]},
    ]
    batch_id = create_batch(client, requests)
    results = poll_batch(client, batch_id)  # blocks until done
"""
import time
import anthropic


def create_batch(client: anthropic.Anthropic, requests: list[dict]) -> str:
    """Submit requests to Claude Batch API. Returns batch ID."""
    batch = client.beta.messages.batches.create(
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


def poll_batch(
    client: anthropic.Anthropic,
    batch_id: str,
    poll_interval: int = 30,
) -> list[dict]:
    """Poll until batch is done. Returns list of {id, text} for succeeded results."""
    while True:
        batch = client.beta.messages.batches.retrieve(batch_id)
        if batch.processing_status == "ended":
            return [
                {
                    "id": r.custom_id,
                    "text": r.result.message.content[0].text,
                }
                for r in client.beta.messages.batches.results(batch_id)
                if r.result.type == "succeeded"
            ]
        time.sleep(poll_interval)
