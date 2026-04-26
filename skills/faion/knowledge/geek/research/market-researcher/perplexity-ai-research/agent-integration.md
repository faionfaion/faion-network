# Agent Integration — Perplexity AI for Research

## When to use
- Fast, cited multi-source synthesis where manual source collection would take hours
- Market sizing queries that need recent (< 6 months) data with traceable URLs
- Competitive landscape sweeps producing a first-pass list of players, funding events, and feature sets
- Trend research where breadth matters more than depth in the first pass
- Validating or cross-checking a specific claim with multiple independent sources

## When NOT to use
- Deep primary-source research: Perplexity aggregates web content, not proprietary data
- When citations must be peer-reviewed or from specific databases (PubMed, SSRN, SEC EDGAR)
- Real-time streaming data (stock prices, live social signals) — Perplexity crawls on delay
- Tasks requiring Perplexity to retain context across multiple sessions (no persistent memory)
- When the research question is too ambiguous: vague queries produce authoritative-sounding but unreliable results

## Where it fails / limitations
- Pro Search has a query-per-day cap on the API tier; high-volume agent loops hit the cap within hours
- Perplexity can cite a URL that has since changed or been removed — the agent must verify links before recording
- Results for very recent events (< 48h) are inconsistent; the crawl delay creates coverage gaps
- Long-form synthesis across 10+ sources degrades quality; break into sub-queries and merge results
- The API response format differs from the web UI (no "Pro Search" toggle exists in API v1; use `search_recency_filter` instead)

## Agentic workflow
A Claude Sonnet agent acts as orchestrator: it decomposes a research question into 3-5 targeted Perplexity queries, dispatches each via the Perplexity REST API, collects cited results, de-duplicates overlapping sources, and produces a consolidated markdown synthesis with a source registry. Each query should target one specific sub-question (e.g., market size, key players, recent funding) rather than the full research question at once.

### Recommended subagents
- `faion-sdd-executor-agent` — executes Perplexity-based research tasks defined in SDD specs

### Prompt pattern
```
<perplexity_research>
  <main_question>What is the TAM for AI-native research tools for knowledge workers in 2026?</main_question>
  <sub_queries>
    <query>Global knowledge worker software market size 2025 2026 sources</query>
    <query>AI research tool vendors market share funding 2025</query>
    <query>Perplexity Elicit Consensus user base revenue estimates 2026</query>
  </sub_queries>
  <recency>month</recency>
  <output>Markdown with inline citations. Flag any claim with a single source.</output>
</perplexity_research>
```

```python
# Minimal Perplexity API dispatcher
import requests, os

def perplexity_query(question: str, recency: str = "month") -> dict:
    """recency: 'hour', 'day', 'week', 'month', 'year'"""
    headers = {
        "Authorization": f"Bearer {os.environ['PERPLEXITY_API_KEY']}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.1-sonar-large-128k-online",
        "messages": [{"role": "user", "content": question}],
        "search_recency_filter": recency,
        "return_citations": True
    }
    r = requests.post("https://api.perplexity.ai/chat/completions",
                      json=payload, headers=headers)
    r.raise_for_status()
    data = r.json()
    return {
        "answer": data["choices"][0]["message"]["content"],
        "citations": data.get("citations", [])
    }
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `requests` | Call Perplexity REST API | stdlib-adjacent, no install |
| `anthropic` SDK | Orchestrate query decomposition and synthesis | `pip install anthropic` |
| `httpx` | Async Perplexity calls for parallel sub-queries | `pip install httpx` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Perplexity API | SaaS | Yes — REST | Models: `sonar-small`, `sonar-large`, `sonar-huge`; `return_citations=true` |
| Perplexity Spaces | SaaS | No | Web-only; no API access to Spaces |
| Perplexity Pro Search (UI) | SaaS | No | UI feature only; use `sonar-large` model in API as equivalent |

## Templates & scripts
See `templates.md` for full query-decomposition and synthesis templates. The inline dispatcher above covers the core API call. For parallel sub-queries:

```python
import asyncio, httpx, os

async def parallel_queries(questions: list[str], recency: str = "month") -> list[dict]:
    headers = {
        "Authorization": f"Bearer {os.environ['PERPLEXITY_API_KEY']}",
        "Content-Type": "application/json"
    }
    async with httpx.AsyncClient(timeout=30) as client:
        tasks = [
            client.post(
                "https://api.perplexity.ai/chat/completions",
                json={
                    "model": "llama-3.1-sonar-large-128k-online",
                    "messages": [{"role": "user", "content": q}],
                    "search_recency_filter": recency,
                    "return_citations": True
                },
                headers=headers
            )
            for q in questions
        ]
        responses = await asyncio.gather(*tasks)
    return [r.json() for r in responses]
```

## Best practices
- Decompose research questions into 3-5 narrow sub-queries; broad single queries produce shallow coverage
- Set `search_recency_filter` explicitly — default "any" pulls stale content for fast-moving markets
- Record `citations` alongside each answer; never pass Perplexity output downstream without the source list
- Validate at least 2 citations per critical claim by following the URL — Perplexity links decay within days for news sources
- Use `sonar-huge` only for final synthesis steps; `sonar-small` or `sonar-large` for exploratory queries to control cost
- Export Spaces (web) for long-running projects where human researchers also contribute — but do not rely on Spaces in agent pipelines

## AI-agent gotchas
- The API does not expose Perplexity Spaces; any Space-based context must be manually copied into the agent's prompt
- `return_citations` in the API returns URL strings, not structured metadata; the agent must parse source domains to assess credibility
- Query-per-minute rate limits are stricter than the daily cap; add 1-2 second delays between parallel sub-queries
- Perplexity will confidently synthesize from low-authority sources (forums, SEO blogs) alongside reputable ones; source filtering is the agent's responsibility
- Models available via API change without notice; pin the model name and add a fallback

## References
- [Perplexity API Docs](https://docs.perplexity.ai/)
- [Perplexity AI Statistics 2025](https://seoprofy.com/blog/perplexity-ai-statistics/)
- [Perplexity Models Reference](https://docs.perplexity.ai/guides/model-cards)
- [Anthropic Claude API](https://docs.anthropic.com/en/api/getting-started)
