"""
OpenAI client wrapper with tenacity retry on RateLimitError and APIError.

Usage:
    content, usage = call_chat(messages, model="gpt-4o-mini")
"""
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from openai import OpenAI, RateLimitError, APIError

client = OpenAI()


@retry(
    retry=retry_if_exception_type((RateLimitError, APIError)),
    wait=wait_exponential(multiplier=1, min=1, max=60),
    stop=stop_after_attempt(5),
)
def call_chat(
    messages: list[dict],
    model: str = "gpt-4o-mini",
    temperature: float = 0.2,
    max_tokens: int = 2048,
) -> tuple[str, object]:
    """Make a chat completion call with automatic retry. Returns (content, usage)."""
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    choice = response.choices[0]
    if choice.finish_reason == "length":
        raise ValueError(f"Response truncated by max_tokens={max_tokens}")
    return choice.message.content, response.usage
