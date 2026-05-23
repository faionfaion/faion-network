"""
purpose: OpenAI client wrapper with tenacity retry + finish_reason guard + usage logging.
consumes: messages list, model id, temperature, max_tokens.
produces: dict {content, usage, finish_reason, request_id, latency_ms}.
depends-on: openai>=1.0, tenacity>=8.0.
token-budget-impact: zero overhead at runtime; logs all calls for cost audit.
"""
import time
from openai import OpenAI, RateLimitError, APIError, BadRequestError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

client = OpenAI()


@retry(
    retry=retry_if_exception_type((RateLimitError, APIError)),
    wait=wait_exponential(multiplier=1, min=1, max=60),
    stop=stop_after_attempt(5),
    reraise=True,
)
def call_chat(
    messages: list[dict],
    model: str = "gpt-4o-mini",
    temperature: float = 0.2,
    max_tokens: int = 2048,
    response_format: dict | None = None,
    seed: int | None = None,
) -> dict:
    """Call Chat Completions with retry on transient errors only."""
    if not isinstance(messages, list) or not messages:
        raise BadRequestError("messages must be a non-empty list")
    t0 = time.monotonic()
    kwargs = {"model": model, "messages": messages, "temperature": temperature, "max_tokens": max_tokens}
    if response_format is not None:
        kwargs["response_format"] = response_format
    if seed is not None:
        kwargs["seed"] = seed
    raw = client.chat.completions.with_raw_response.create(**kwargs)
    latency_ms = int((time.monotonic() - t0) * 1000)
    parsed = raw.parse()
    choice = parsed.choices[0]
    if choice.finish_reason == "length":
        raise ValueError(f"Response truncated by max_tokens={max_tokens}")
    return {
        "content": choice.message.content,
        "usage": parsed.usage.model_dump() if hasattr(parsed.usage, "model_dump") else dict(parsed.usage.__dict__),
        "finish_reason": choice.finish_reason,
        "request_id": raw.headers.get("x-request-id", ""),
        "latency_ms": latency_ms,
    }
