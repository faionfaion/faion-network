"""
perplexity-dispatcher.py — Sync and async Perplexity API dispatchers.
Sync: perplexity_query(question, recency) → dict{answer, citations}
Async: parallel_queries(questions, recency) → list[dict]
Requires: PERPLEXITY_API_KEY env var
"""
import asyncio
import os

import httpx
import requests


def perplexity_query(question: str, recency: str = "month") -> dict:
    """Single synchronous Perplexity query.
    recency: 'hour' | 'day' | 'week' | 'month' | 'year'
    """
    headers = {
        "Authorization": f"Bearer {os.environ['PERPLEXITY_API_KEY']}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "llama-3.1-sonar-large-128k-online",
        "messages": [{"role": "user", "content": question}],
        "search_recency_filter": recency,
        "return_citations": True,
    }
    r = requests.post(
        "https://api.perplexity.ai/chat/completions",
        json=payload,
        headers=headers,
    )
    r.raise_for_status()
    data = r.json()
    return {
        "answer": data["choices"][0]["message"]["content"],
        "citations": data.get("citations", []),
    }


async def parallel_queries(
    questions: list[str], recency: str = "month"
) -> list[dict]:
    """Dispatch multiple sub-queries in parallel with 1s delay between requests."""
    headers = {
        "Authorization": f"Bearer {os.environ['PERPLEXITY_API_KEY']}",
        "Content-Type": "application/json",
    }
    async with httpx.AsyncClient(timeout=30) as client:
        tasks = [
            client.post(
                "https://api.perplexity.ai/chat/completions",
                json={
                    "model": "llama-3.1-sonar-large-128k-online",
                    "messages": [{"role": "user", "content": q}],
                    "search_recency_filter": recency,
                    "return_citations": True,
                },
                headers=headers,
            )
            for q in questions
        ]
        responses = await asyncio.gather(*tasks)
    return [r.json() for r in responses]
