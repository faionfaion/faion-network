"""
purpose: Context cache create + reuse pattern.
consumes: see AGENTS.md ## Prerequisites
produces: code
depends-on: content/02-output-contract.xml schema for gemini-api
token-budget-impact: ≤500 tokens to fill
"""

# Context cache: create once per (model, content) key, reuse across calls, refresh TTL.
# Requires: pip install "google-genai>=1.0"  (google.genai API, stable since 2025)

from __future__ import annotations

import hashlib
import logging
import os
import time
from typing import Callable, TypeVar

from google import genai
from google.genai import errors, types

logger = logging.getLogger(__name__)
T = TypeVar("T")

MODEL = "gemini-3-flash-001"          # r5: pinned version suffix, never a floating tag
CACHE_TTL_S = 3600                    # output-contract cache_ttl_s
MIN_CACHE_TOKENS = 1024               # r3: below this the API rejects the cache anyway
BACKOFF_BASE_S, BACKOFF_CAP_S = 5, 60  # r1

# r4: one explicit threshold per harm category; defaults drift between model versions
SAFETY_SETTINGS = [
    types.SafetySetting(category=c, threshold="BLOCK_MEDIUM_AND_ABOVE")
    for c in (
        "HARM_CATEGORY_HARASSMENT",
        "HARM_CATEGORY_HATE_SPEECH",
        "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "HARM_CATEGORY_DANGEROUS_CONTENT",
    )
]

client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])


def with_backoff(call: Callable[[], T], max_retries: int = 5) -> T:
    """r1: exponential backoff 5s -> 60s; a 429 Retry-After header wins over the schedule."""
    for attempt in range(max_retries):
        try:
            return call()
        except errors.APIError as exc:
            if exc.code not in (429, 500, 503) or attempt == max_retries - 1:
                raise
            wait = min(BACKOFF_BASE_S * 2**attempt, BACKOFF_CAP_S)
            headers = getattr(getattr(exc, "response", None), "headers", None) or {}
            if exc.code == 429 and headers.get("retry-after"):
                wait = max(wait, float(headers["retry-after"]))
            logger.warning("Gemini %s; retry %d/%d in %.0fs", exc.code, attempt + 1, max_retries, wait)
            time.sleep(wait)
    raise AssertionError("unreachable")


def cache_key(system_instruction: str, reference_docs: list[str]) -> str:
    """Deterministic display_name: identical content maps to one cache across processes."""
    h = hashlib.sha256(MODEL.encode())
    h.update(system_instruction.encode())
    for doc in reference_docs:
        h.update(b"\x00" + doc.encode())
    return f"ctx-{h.hexdigest()[:24]}"


def get_or_create_cache(system_instruction: str, reference_docs: list[str]) -> types.CachedContent | None:
    """Return the cache for this content, creating it on first use.

    None means the context is under MIN_CACHE_TOKENS (r3); the caller sends it inline.
    """
    key = cache_key(system_instruction, reference_docs)
    for existing in client.caches.list():
        if existing.display_name == key:
            client.caches.update(name=existing.name, config=types.UpdateCachedContentConfig(ttl=f"{CACHE_TTL_S}s"))
            return existing
    contents = [types.Content(role="user", parts=[types.Part.from_text(text=d) for d in reference_docs])]
    total = client.models.count_tokens(model=MODEL, contents=contents).total_tokens or 0
    if total < MIN_CACHE_TOKENS:
        logger.info("context is %d tokens (< %d); not caching", total, MIN_CACHE_TOKENS)
        return None
    return with_backoff(lambda: client.caches.create(
        model=MODEL,
        config=types.CreateCachedContentConfig(
            display_name=key,
            system_instruction=system_instruction,
            contents=contents,
            ttl=f"{CACHE_TTL_S}s",
        ),
    ))


def generate(prompt: str, cache: types.CachedContent | None,
             system_instruction: str, reference_docs: list[str]) -> str:
    """One call against the cache; inline fallback when there is no cache."""
    if cache is not None:
        # system_instruction and contents live in the cache; passing them again is a 400
        config = types.GenerateContentConfig(cached_content=cache.name, safety_settings=SAFETY_SETTINGS)
        contents: list[str] = [prompt]
    else:
        config = types.GenerateContentConfig(system_instruction=system_instruction, safety_settings=SAFETY_SETTINGS)
        contents = [*reference_docs, prompt]
    response = with_backoff(lambda: client.models.generate_content(model=MODEL, contents=contents, config=config))
    usage = response.usage_metadata
    logger.info("prompt_tokens=%s cached_tokens=%s", usage.prompt_token_count, usage.cached_content_token_count)
    return response.text or ""


# Usage (r3: worth it only when the same context is reused >= 5x within the TTL):
# docs = [open(p).read() for p in ["<reference-doc-1>", "<reference-doc-2>"]]
# cache = get_or_create_cache("<system-instruction>", docs)
# for question in questions:
#     print(generate(question, cache, "<system-instruction>", docs))
# if cache: client.caches.delete(name=cache.name)   # once the batch is done; TTL expiry otherwise
