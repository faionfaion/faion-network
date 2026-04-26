"""OpenRouter chat-completions call with primary model + fallback chain.

Input  → list of messages, primary model id, ordered fallback ids.
Output → completion text plus the model id that actually served it.

Defaults configure ANTHROPIC primary, OPENAI fallback, GOOGLE second
fallback — three different upstream providers so a vendor-wide outage in
any one of them does not take the call down.

See content/01-gateway-fallback.xml for fallback semantics.
"""

import os
from dataclasses import dataclass

from openai import OpenAI


@dataclass
class GatewayResult:
    text: str
    used_model: str
    fallback_count: int


def call_with_fallback(
    messages: list[dict],
    primary: str = "anthropic/claude-opus-4",
    fallbacks: tuple[str, ...] = (
        "openai/gpt-5",
        "google/gemini-2.5-pro",
    ),
) -> GatewayResult:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.environ["OPENROUTER_API_KEY"],
    )
    chain = [primary, *fallbacks]
    resp = client.chat.completions.create(
        model=primary,
        messages=messages,
        extra_body={"models": chain, "route": "fallback"},
    )
    used = getattr(resp, "model", primary)
    return GatewayResult(
        text=resp.choices[0].message.content,
        used_model=used,
        fallback_count=chain.index(used) if used in chain else 0,
    )
