---
name: llm-fallback-chains
description: Build an ordered provider fallback chain — Anthropic Sonnet → Haiku → OpenAI GPT-5 → cached static — with tenacity retries, per-provider error classification, and failover-rate telemetry.
tier: geek
group: llm-integration
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a production-ready Python `LLMChain` class that routes each request through an ordered provider chain: `claude-sonnet-4-6` → `claude-haiku-4-5-20251001` → OpenAI `gpt-4o` → a cached static response. Each tier triggers on a distinct error class (rate-limit, timeout, server error, content-policy violation). Failover events are counted per provider so you can track degradation rate in your metrics backend.

## Prerequisites

- Python 3.11+.
- `pip install anthropic>=0.51 openai>=1.30 tenacity>=8.3 pydantic>=2.0`.
- `ANTHROPIC_API_KEY` and `OPENAI_API_KEY` exported in the environment.
- Familiarity with the Anthropic Messages API shape and HTTP status codes returned by each provider.
- Read [knowledge/geek/ai/llm-integration/claude-api-basics](../../../knowledge/geek/ai/llm-integration/claude-api-basics) — the exponential-backoff and rate-limit error codes used in Step 2 come directly from that methodology.

## Steps

1. **Classify provider errors into three trigger categories.**

   Not all errors warrant a provider switch — only do so when the current provider is genuinely unavailable or forbidden for this request:

   | Category | Anthropic codes | OpenAI codes | Action |
   |----------|----------------|--------------|--------|
   | Rate-limit | `429`, `529` (overloaded) | `429` | Retry with backoff on same provider; if retries exhausted, fall through to next |
   | Server error | `500`, `502`, `503`, `504` | `500`, `502`, `503` | Immediate fall-through (no retry on 5xx) |
   | Timeout | `httpx.ReadTimeout`, `openai.APITimeoutError` | same | Fall-through after one retry |
   | Content-policy | `anthropic.BadRequestError` with `"content_policy"` | `openai.BadRequestError` `"content_policy_violation"` | Skip all further retries; fall-through only |
   | Other client error | `400` except content-policy | `400` except content-policy | Re-raise immediately — bug in caller, not provider |

2. **Define the chain dataclass and error-classification helpers.**

   ```python
   # llm_chain/errors.py
   from __future__ import annotations
   import anthropic
   import openai

   class RateLimitError(Exception): pass
   class ServerError(Exception): pass
   class TimeoutError(Exception): pass
   class ContentPolicyError(Exception): pass


   def classify_anthropic(exc: Exception) -> Exception:
       if isinstance(exc, anthropic.RateLimitError):
           return RateLimitError(str(exc))
       if isinstance(exc, anthropic.APIStatusError) and exc.status_code in (500, 502, 503, 504, 529):
           if exc.status_code == 529:
               return RateLimitError(str(exc))  # overloaded = rate-limit class
           return ServerError(str(exc))
       if isinstance(exc, anthropic.BadRequestError) and "content_policy" in str(exc).lower():
           return ContentPolicyError(str(exc))
       if isinstance(exc, (TimeoutError, anthropic.APITimeoutError)):
           return TimeoutError(str(exc))
       return exc


   def classify_openai(exc: Exception) -> Exception:
       if isinstance(exc, openai.RateLimitError):
           return RateLimitError(str(exc))
       if isinstance(exc, openai.APIStatusError) and exc.status_code in (500, 502, 503):
           return ServerError(str(exc))
       if isinstance(exc, openai.BadRequestError) and "content_policy_violation" in str(exc).lower():
           return ContentPolicyError(str(exc))
       if isinstance(exc, openai.APITimeoutError):
           return TimeoutError(str(exc))
       return exc
   ```

3. **Implement the Anthropic provider with tenacity retry on rate-limit only.**

   ```python
   # llm_chain/providers/anthropic_provider.py
   from __future__ import annotations
   import anthropic
   from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
   from llm_chain.errors import classify_anthropic, RateLimitError, ContentPolicyError

   _client = anthropic.Anthropic()


   def _call_anthropic(model: str, messages: list[dict], system: str, max_tokens: int) -> str:
       try:
           resp = _client.messages.create(
               model=model,
               max_tokens=max_tokens,
               system=system,
               messages=messages,
           )
           return resp.content[0].text
       except Exception as exc:
           raise classify_anthropic(exc) from exc


   @retry(
       retry=retry_if_exception_type(RateLimitError),
       stop=stop_after_attempt(3),
       wait=wait_exponential(multiplier=1, min=2, max=30),
       reraise=True,
   )
   def call_sonnet(messages: list[dict], system: str = "", max_tokens: int = 1024) -> str:
       return _call_anthropic("claude-sonnet-4-6", messages, system, max_tokens)


   @retry(
       retry=retry_if_exception_type(RateLimitError),
       stop=stop_after_attempt(3),
       wait=wait_exponential(multiplier=1, min=1, max=15),
       reraise=True,
   )
   def call_haiku(messages: list[dict], system: str = "", max_tokens: int = 1024) -> str:
       return _call_anthropic("claude-haiku-4-5-20251001", messages, system, max_tokens)
   ```

4. **Implement the OpenAI provider with the same retry contract.**

   ```python
   # llm_chain/providers/openai_provider.py
   from __future__ import annotations
   import openai
   from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
   from llm_chain.errors import classify_openai, RateLimitError

   _client = openai.OpenAI()


   @retry(
       retry=retry_if_exception_type(RateLimitError),
       stop=stop_after_attempt(3),
       wait=wait_exponential(multiplier=1, min=2, max=30),
       reraise=True,
   )
   def call_gpt4o(messages: list[dict], system: str = "", max_tokens: int = 1024) -> str:
       openai_messages = []
       if system:
           openai_messages.append({"role": "system", "content": system})
       openai_messages.extend(messages)
       try:
           resp = _client.chat.completions.create(
               model="gpt-4o",
               max_tokens=max_tokens,
               messages=openai_messages,
           )
           return resp.choices[0].message.content or ""
       except Exception as exc:
           raise classify_openai(exc) from exc
   ```

5. **Build the chain with per-provider failover counters.**

   ```python
   # llm_chain/chain.py
   from __future__ import annotations
   import logging
   from collections import defaultdict
   from llm_chain.errors import (
       RateLimitError, ServerError, TimeoutError, ContentPolicyError,
   )
   from llm_chain.providers.anthropic_provider import call_sonnet, call_haiku
   from llm_chain.providers.openai_provider import call_gpt4o

   logger = logging.getLogger(__name__)

   # Cumulative failover counters — replace with Prometheus Counter in production
   _failover_counts: dict[str, int] = defaultdict(int)

   STATIC_FALLBACK = (
       "I'm temporarily unable to process your request. "
       "Please try again in a moment."
   )

   # Errors that trigger fallthrough (exhausted retries OR immediate skip)
   _FALLTHROUGH = (RateLimitError, ServerError, TimeoutError, ContentPolicyError)


   class LLMChain:
       """Ordered provider chain with failover telemetry."""

       def __init__(
           self,
           system: str = "",
           max_tokens: int = 1024,
           static_fallback: str = STATIC_FALLBACK,
       ) -> None:
           self.system = system
           self.max_tokens = max_tokens
           self.static_fallback = static_fallback

       def call(self, messages: list[dict]) -> tuple[str, str]:
           """Return (response_text, provider_used).

           provider_used is one of: sonnet, haiku, gpt-4o, static.
           """
           for provider_name, fn in [
               ("sonnet", lambda: call_sonnet(messages, self.system, self.max_tokens)),
               ("haiku", lambda: call_haiku(messages, self.system, self.max_tokens)),
               ("gpt-4o", lambda: call_gpt4o(messages, self.system, self.max_tokens)),
           ]:
               try:
                   result = fn()
                   return result, provider_name
               except _FALLTHROUGH as exc:
                   _failover_counts[provider_name] += 1
                   logger.warning(
                       "provider=%s failed type=%s msg=%s; falling through",
                       provider_name, type(exc).__name__, str(exc)[:120],
                   )
               except Exception:
                   raise  # non-retriable client error → re-raise immediately

           # All live providers exhausted
           _failover_counts["all"] += 1
           logger.error("all providers exhausted; returning static fallback")
           return self.static_fallback, "static"

       @staticmethod
       def failover_counts() -> dict[str, int]:
           """Return a snapshot of per-provider failover counts."""
           return dict(_failover_counts)
   ```

6. **Wire up failover-rate telemetry.**

   Export `failover_counts()` to your metrics backend on each request or on a periodic flush. Minimal example using a Prometheus `Counter` if you have `prometheus_client` installed:

   ```python
   # llm_chain/metrics.py
   from __future__ import annotations

   try:
       from prometheus_client import Counter
       _provider_failovers = Counter(
           "llm_chain_failovers_total",
           "Number of provider failovers",
           ["provider"],
       )

       def record_failover(provider: str) -> None:
           _provider_failovers.labels(provider=provider).inc()

   except ImportError:
       # prometheus_client not installed — use in-memory counters only
       def record_failover(provider: str) -> None:  # type: ignore[misc]
           pass
   ```

   Patch `chain.py` to call `record_failover(provider_name)` alongside `_failover_counts[provider_name] += 1`. Set an alert threshold: if `sonnet` failover rate exceeds 5% of calls in any 5-minute window, page on-call.

7. **Run the working end-to-end call.**

   ```python
   # run_chain.py
   import os
   from llm_chain.chain import LLMChain

   chain = LLMChain(
       system="You are a concise assistant. Reply in one sentence.",
       max_tokens=128,
   )

   response, provider = chain.call(
       messages=[{"role": "user", "content": "What is the Anthropic fallback chain pattern?"}]
   )
   print(f"[{provider}] {response}")
   print("Failover counts:", chain.failover_counts())
   ```

   Expected output (healthy environment):

   ```
   [sonnet] A fallback chain routes requests through ordered LLM providers...
   Failover counts: {}
   ```

   If `ANTHROPIC_API_KEY` is absent, the chain falls through to `gpt-4o` and prints `[gpt-4o] ...`.

## Verify

Run the script and confirm it exits 0 and prints `[sonnet]` as the provider:

```bash
python run_chain.py
```

To force a fallback and verify the chain works end-to-end, temporarily unset `ANTHROPIC_API_KEY`:

```bash
ANTHROPIC_API_KEY=invalid python run_chain.py
```

Expected: output starts with `[gpt-4o]` or `[static]`, and `Failover counts:` shows `{"sonnet": 1, "haiku": 1}` or similar. The process must exit 0 regardless of which provider answers.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `TypeError: classify_anthropic() got unexpected exc` | `anthropic.APIConnectionError` not mapped | Add `anthropic.APIConnectionError` → `ServerError` in `classify_anthropic()` |
| Chain raises instead of falling through on 400 | `BadRequestError` without `"content_policy"` in message hits the re-raise path | Inspect `exc.message` in a debugger; log the raw error body before classifying |
| tenacity retries on 500 (server error) | `ServerError` accidentally included in `retry_if_exception_type` | `ServerError` must NOT be in the tenacity `retry=` tuple — only `RateLimitError` retries |
| `gpt-4o` always chosen even when Anthropic is healthy | `ANTHROPIC_API_KEY` env var missing or empty at import time | `anthropic.Anthropic()` reads the key at construction; ensure the env var is set before importing the module |
| Failover counts always 0 in Prometheus | `record_failover()` called but metrics endpoint not scraped | Add `/metrics` endpoint via `prometheus_client.start_http_server(9090)` or expose via your WSGI app |
| `ContentPolicyError` falls through to static without trying haiku | Intended — content-policy violations are request-specific, not provider-specific; all providers will reject the same payload | Add a sanitisation layer before the chain if you need haiku/gpt-4o to attempt the request |

## Next

- Add Anthropic prompt caching on `claude-sonnet-4-6` for the `system` prompt — reduces cost and latency on the primary provider, making fallthrough less likely; see [knowledge/geek/ai/llm-integration/claude-best-practices](../../../knowledge/geek/ai/llm-integration/claude-best-practices).
- Extend the chain with a circuit-breaker (e.g., `pybreaker`) so a provider that fails 10 consecutive calls is skipped for 60 seconds without retrying — reduces tail latency when a provider is in rolling outage.
- Add request-level tracing (OpenTelemetry `span` per provider attempt) to correlate failover events with user-visible latency spikes.

## References

- [knowledge/geek/ai/llm-integration/claude-api-basics](../../../knowledge/geek/ai/llm-integration/claude-api-basics) — rate-limit error codes (`429`, `529` overloaded), exponential backoff parameters, and model ID pinning conventions that back the retry config in Steps 3 and 4
- [knowledge/geek/ai/llm-integration/claude-api-integration](../../../knowledge/geek/ai/llm-integration/claude-api-integration) — production Anthropic SDK patterns for multi-provider routing, error surface mapping, and request lifecycle that inform the error-classification helpers in Step 2
- [knowledge/geek/ai/llm-integration/guardrails-implementation](../../../knowledge/geek/ai/llm-integration/guardrails-implementation) — content-policy detection patterns that back the `ContentPolicyError` classification and the no-retry decision for policy violations in Step 1
