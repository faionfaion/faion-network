# purpose: OpenAI Batch API submitter: serialises JSONL, uploads file, polls completion
# consumes: list of request dicts + endpoint
# produces: batch id + output JSONL once Batch completes
# depends-on: content/04-procedure.xml
# token-budget-impact: small

"""
Batch API: build JSONL, upload, submit job, poll for results.
50% cost discount; up to 24h completion window.
Do NOT wait synchronously — use a completion-handler or cron to poll.
"""
import json
import time
import openai


def build_batch_jsonl(texts: list[str], model: str = "gpt-4o-mini") -> bytes:
    """Build JSONL payload for Batch API."""
    requests = [
        {
            "custom_id": f"item-{i}",
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": {
                "model": model,
                "messages": [{"role": "user", "content": text}],
                "max_tokens": 512,
            },
        }
        for i, text in enumerate(texts)
    ]
    return "\n".join(json.dumps(r) for r in requests).encode()


def submit_batch(texts: list[str]) -> str:
    """Submit a batch job. Returns batch_id for polling."""
    client = openai.OpenAI()
    file_obj = client.files.create(
        file=("batch.jsonl", build_batch_jsonl(texts), "application/jsonl"),
        purpose="batch",
    )
    batch = client.batches.create(
        input_file_id=file_obj.id,
        endpoint="/v1/chat/completions",
        completion_window="24h",
    )
    return batch.id


def poll_batch(batch_id: str, poll_interval: int = 60) -> list[dict]:
    """Poll batch until complete. Returns list of result dicts."""
    client = openai.OpenAI()
    while True:
        batch = client.batches.retrieve(batch_id)
        if batch.status == "completed":
            content = client.files.content(batch.output_file_id)
            return [json.loads(line) for line in content.text.strip().splitlines()]
        if batch.status in ("failed", "cancelled", "expired"):
            raise RuntimeError(f"Batch {batch_id} ended with status: {batch.status}")
        time.sleep(poll_interval)
