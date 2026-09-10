"""
purpose: Langfuse client init.
consumes: see AGENTS.md ## Prerequisites
produces: spec
depends-on: content/02-output-contract.xml schema for llm-observability
token-budget-impact: ≤500 tokens to fill
"""
# langfuse>=3.0 (OTel-based v3 client). Env vars read here:
#   LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY  - project keys
#   LANGFUSE_HOST                             - self-host URL; default keeps
#                                               traces on-prem (rule r6)
#   LANGFUSE_SAMPLE_RATE                      - 1.0 for the first N days (rule r5)
#   APP_ENV, APP_RELEASE                      - tags every trace
from __future__ import annotations

import os
import re
import time
from typing import Any

from langfuse import Langfuse, get_client

# Rule r4: PII is redacted client-side before export; never rely on the vendor.
_PII_PATTERNS = (
    re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"),                 # email
    re.compile(r"\+?\d[\d\s().-]{7,}\d"),                    # phone
    re.compile(r"\b[A-Z]{2}\d{6,9}\b"),                      # passport / ID
)


def redact_pii(data: Any) -> Any:
    if isinstance(data, str):
        for pat in _PII_PATTERNS:
            data = pat.sub("<redacted>", data)
        return data
    if isinstance(data, dict):
        return {k: redact_pii(v) for k, v in data.items()}
    if isinstance(data, list):
        return [redact_pii(v) for v in data]
    return data


def init_langfuse() -> Langfuse:
    """Create the singleton; later code uses langfuse.get_client()."""
    return Langfuse(
        public_key=os.environ["LANGFUSE_PUBLIC_KEY"],
        secret_key=os.environ["LANGFUSE_SECRET_KEY"],
        host=os.environ.get("LANGFUSE_HOST", "http://localhost:3000"),
        environment=os.environ.get("APP_ENV", "production"),
        release=os.environ.get("APP_RELEASE", "<git-sha>"),
        sample_rate=float(os.environ.get("LANGFUSE_SAMPLE_RATE", "1.0")),
        mask=redact_pii,
        flush_at=15,
        flush_interval=5.0,
    )


# Provider price book, USD per 1M tokens; extend per <model-id> in use.
PRICE_PER_1M = {"<model-id>": {"input": 3.0, "output": 15.0}}


def cost_usd(model: str, tokens_in: int, tokens_out: int) -> float:
    price = PRICE_PER_1M.get(model, {"input": 0.0, "output": 0.0})
    return (tokens_in * price["input"] + tokens_out * price["output"]) / 1_000_000


def traced_completion(model: str, messages: list[dict[str, str]], call_provider) -> str:
    """Rule r1: every LLM call records input, output, tokens, latency, cost.

    `call_provider(model, messages)` must return
    (text, tokens_in, tokens_out); wrap the vendor SDK call there.
    """
    langfuse = get_client()
    with langfuse.start_as_current_generation(
        name="llm.completion", model=model, input=messages
    ) as gen:
        started = time.perf_counter()
        text, tokens_in, tokens_out = call_provider(model, messages)
        latency_ms = (time.perf_counter() - started) * 1000
        gen.update(
            output=text,
            usage_details={"input": tokens_in, "output": tokens_out},
            cost_details={"total": cost_usd(model, tokens_in, tokens_out)},
            metadata={"latency_ms": round(latency_ms, 1)},
        )
    return text


if __name__ == "__main__":
    client = init_langfuse()
    assert client.auth_check(), "Langfuse credentials rejected"
    client.flush()
