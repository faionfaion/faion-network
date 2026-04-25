# Agent Integration — Perplexity AI for Research

## When to use
- Fast synthesis of a research question that requires pulling from 5+ web sources simultaneously
- Market sizing, competitive landscape, or trend research where citations matter
- Fact-checking a specific claim with primary source validation
- Generating a research brief or background document as a starting point for deeper analysis
- When Claude alone is insufficient because the question requires live web data (post-knowledge-cutoff events, current pricing, recent funding rounds)

## When NOT to use
- When primary source documents (PDFs, internal databases, proprietary data) are the required source — Perplexity only searches the public web
- For confidential competitive research where queries themselves leak strategic intent via Perplexity's servers
- When a single authoritative source (an official spec, a government database) is available directly — fetch it with a targeted HTTP call instead
- For qualitative synthesis requiring judgment (strategy, product decisions) — Perplexity retrieves and summarizes, but does not reason about tradeoffs

## Where it fails / limitations
- Citations are URL-level, not page-level; a cited source may support only part of the synthesized claim
- Perplexity's synthesis can merge facts from different time periods without flagging the temporal mismatch
- Pro Search depth is limited by the query; compound or multi-part questions produce shallow answers on secondary threads
- Paywalled sources appear in citation lists but Perplexity cannot read behind the paywall — summary reflects only the abstract or preview
- For rapidly changing data (stock prices, live stats, breaking news), Perplexity's index lags real-time by hours to days

## Agentic workflow
Sonnet formulates optimized search queries from a research brief, breaking compound questions into atomic sub-queries (one fact per query). Haiku executes each Pro Search call and stores raw results with citations. Sonnet synthesizes the retrieved results, cross-checks conflicting claims, and flags low-confidence assertions. A human reviews flagged items and approves the final synthesis before it enters any downstream pipeline.

### Recommended subagents
- `faion-sdd-executor-agent` — can execute multi-step research pipelines with Perplexity as the data source stage
- General Claude subagent (Sonnet) — query formulation, synthesis of Perplexity outputs, conflict resolution
- General Claude subagent (Haiku) — executing individual Pro Search queries, citation extraction

### Prompt pattern
```
You are a research analyst. Break this research question into 3-5 atomic sub-queries
suitable for Perplexity Pro Search:

Research question: [question]

For each sub-query:
- Write the exact Perplexity search string (use year "2025" or "2026" to force recency)
- Specify what fact you expect it to return
- Specify what source type is most credible for this fact (industry report / news / official site / academic)
```

```
Perplexity returned these results for query "[query]": [paste results with citations]

Synthesize the findings:
1. Core finding (one sentence)
2. Supporting data points with source URLs
3. Conflicting claims (if any) and which source to trust
4. Confidence level: H (multiple independent sources agree) / M (partial agreement) / L (single source or paywalled)
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| Perplexity API (REST) | Programmatic Pro Search queries, returns JSON with citations | perplexity.ai/api, `pip install openai` (compatible client) |
| httpx (Python) | Async HTTP client for batching Perplexity API calls | `pip install httpx` |
| jq | Parse and extract citation URLs from Perplexity JSON responses | `apt install jq` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Perplexity Pro | SaaS | Yes (API) | sonar-pro model; best for research; returns citations in JSON |
| Perplexity API (sonar) | SaaS | Yes (API) | Lighter model; faster, cheaper; use for high-volume fact checks |
| Perplexity Spaces | SaaS | Partial | Organize research projects; no API for Spaces management |
| Exa AI | SaaS | Yes (API) | Semantic web search alternative; stronger for academic/technical queries |
| Tavily | SaaS | Yes (API) | Research-optimized search API; often used in LangChain/CrewAI pipelines |
| SerpAPI | SaaS | Yes (API) | Google SERP programmatic access; weaker synthesis but broader index |

## Templates & scripts
Perplexity batch research script (Python, inline):
```python
# perplexity_research.py
import httpx, json

PPLX_API_KEY = "your-api-key"
PPLX_URL = "https://api.perplexity.ai/chat/completions"

def pro_search(query: str) -> dict:
    headers = {
        "Authorization": f"Bearer {PPLX_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "sonar-pro",
        "messages": [{"role": "user", "content": query}],
        "return_citations": True,
        "search_recency_filter": "year",  # last 12 months
    }
    r = httpx.post(PPLX_URL, headers=headers, json=payload, timeout=30)
    r.raise_for_status()
    data = r.json()
    return {
        "answer": data["choices"][0]["message"]["content"],
        "citations": data.get("citations", []),
    }

def batch_research(queries: list[str]) -> list[dict]:
    return [{"query": q, **pro_search(q)} for q in queries]

results = batch_research([
    "TAM for AI research tools market 2025 with sources",
    "Perplexity AI revenue and growth 2025",
])
print(json.dumps(results, indent=2))
```

## Best practices
- Use `search_recency_filter: "year"` to avoid stale data; Perplexity defaults to broader time windows that include outdated figures
- Formulate one atomic fact per query; compound queries ("market size AND competitors AND trends") produce diluted answers across all three
- Always export citations and store them alongside the synthesized finding — the source is as important as the fact for downstream validation
- Use Perplexity Spaces to organize a research project's queries and findings across sessions; prevents duplication and enables audit trails
- Cross-validate high-stakes numbers (TAM, funding rounds, revenue) against at least one additional independent source (AlphaSense, Crunchbase, official press releases)

## AI-agent gotchas
- Perplexity's synthesis sounds authoritative even when it cites a single low-quality source; always check citation count and source quality, not just the answer text
- The API returns citations as URLs, not structured metadata; agents must parse and validate each URL independently if source quality assessment is required
- Rate limits on the Pro API are strict at lower tiers; batch queries need exponential backoff and retry logic
- Perplexity may return a paywalled URL as a citation — the agent cannot verify whether the full article supports the claim; flag paywalled citations as unverified
- Human checkpoint required for any Perplexity-sourced figure that will be presented externally; hallucination risk is lower than pure LLM but not zero

## References
- https://www.perplexity.ai/
- https://docs.perplexity.ai/reference/post_chat_completions
- https://seoprofy.com/blog/perplexity-ai-statistics/ (usage stats)
- Exa AI — https://exa.ai/
- Tavily — https://tavily.com/
