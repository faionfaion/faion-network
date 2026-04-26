# perplexity_research.py — batch Pro Search via Perplexity REST API
# Requires: pip install httpx
# Set PPLX_API_KEY environment variable before running.

import httpx
import json
import os
import time

PPLX_API_KEY = os.environ.get("PPLX_API_KEY", "")
PPLX_URL = "https://api.perplexity.ai/chat/completions"


def pro_search(query: str, retries: int = 3) -> dict:
    """Execute one Pro Search query; returns answer text and citation URLs."""
    headers = {
        "Authorization": f"Bearer {PPLX_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "sonar-pro",
        "messages": [{"role": "user", "content": query}],
        "return_citations": True,
        "search_recency_filter": "year",  # last 12 months — override if broader window needed
    }
    for attempt in range(retries):
        try:
            r = httpx.post(PPLX_URL, headers=headers, json=payload, timeout=30)
            r.raise_for_status()
            data = r.json()
            return {
                "query": query,
                "answer": data["choices"][0]["message"]["content"],
                "citations": data.get("citations", []),
            }
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429 and attempt < retries - 1:
                time.sleep(2 ** attempt)  # exponential backoff
                continue
            raise
    return {"query": query, "answer": None, "citations": [], "error": "max_retries"}


def batch_research(queries: list[str]) -> list[dict]:
    """Run multiple atomic sub-queries sequentially with backoff between calls."""
    results = []
    for q in queries:
        results.append(pro_search(q))
        time.sleep(1)  # polite delay between calls
    return results


# Example:
# results = batch_research([
#     "TAM for AI research tools market 2025 with sources",
#     "Perplexity AI revenue and user growth 2025",
# ])
# print(json.dumps(results, indent=2))
