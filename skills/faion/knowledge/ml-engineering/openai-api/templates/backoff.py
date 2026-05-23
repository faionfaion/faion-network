# purpose: Exponential-backoff wrapper for OpenAI API calls handling 429 + 5xx
# consumes: callable + args/kwargs
# produces: retry-aware wrapper with capped delay
# depends-on: content/03-failure-modes.xml
# token-budget-impact: small

"""
Exponential backoff wrapper for OpenAI API calls.
Handles RateLimitError (429) and server errors (5xx).
Max 6 retries, delay doubles each attempt (1s → 32s), capped at 60s.
"""
import time
import openai
from openai import RateLimitError, APIStatusError


def call_with_backoff(client: openai.OpenAI, **kwargs):
    """
    Call client.chat.completions.create with exponential backoff.
    Pass all create() kwargs directly.
    """
    for attempt in range(6):
        try:
            return client.chat.completions.create(**kwargs)
        except RateLimitError:
            wait = min(2 ** attempt, 60)
            time.sleep(wait)
        except APIStatusError as e:
            if e.status_code >= 500:
                wait = min(2 ** attempt, 60)
                time.sleep(wait)
            else:
                raise  # 4xx errors are not retryable
    raise RuntimeError("Exceeded retry limit (6 attempts)")
