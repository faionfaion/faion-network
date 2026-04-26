"""Batch API submit + poll loop.

Usage:
    batch_id = submit_batch([{"id": "req-1", "prompt": "Hello"}])
    results = poll_and_collect(batch_id)
    # results: [{"id": "req-1", "text": "..."}, {"id": "req-2", "error": "..."}]
"""
import time
import anthropic

client = anthropic.Anthropic()


def submit_batch(prompts: list[dict]) -> str:
    """Submit list of {id, prompt} dicts to Batch API. Returns batch_id."""
    reqs = [
        {
            "custom_id": p["id"],
            "params": {
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 1024,
                "messages": [{"role": "user", "content": p["prompt"]}],
            },
        }
        for p in prompts
    ]
    return client.beta.messages.batches.create(requests=reqs).id


def poll_and_collect(batch_id: str, poll_interval: int = 60) -> list[dict]:
    """Poll until batch ends. Returns list of {id, text} or {id, error}."""
    while True:
        batch = client.beta.messages.batches.retrieve(batch_id)
        if batch.processing_status == "ended":
            results = []
            for r in client.beta.messages.batches.results(batch_id):
                if r.result.type == "succeeded":
                    results.append({
                        "id": r.custom_id,
                        "text": r.result.message.content[0].text,
                    })
                else:
                    results.append({"id": r.custom_id, "error": str(r.result.error)})
            return results
        time.sleep(poll_interval)
