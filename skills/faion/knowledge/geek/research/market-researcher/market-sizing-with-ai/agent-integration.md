# Agent Integration — Market Sizing with AI

## When to use
- Producing TAM/SAM/SOM estimates to support a go/no-go decision or investor deck
- Triangulating market size when no single authoritative report exists
- Stress-testing existing market estimates by running independent top-down and bottom-up paths
- Automating recurring market-size updates as part of a research cadence

## When NOT to use
- When the investor or client requires primary-source analyst reports (Gartner, IDC) by name — AI cannot substitute these
- Highly novel markets with less than 12 months of public data — AI will extrapolate from adjacent, unreliable proxies
- Regulated contexts (IPO prospectus, SEC filing) where every number needs traceable sourcing
- When the market boundary is contested — AI will anchor to the most common framing without flagging ambiguity

## Where it fails / limitations
- AI tools confuse TAM, SAM, and SOM; prompt must define each explicitly or outputs will be inconsistent
- Bottom-up estimates require accurate counts of target customers; AI will guess if no reliable dataset exists
- Statista and CB Insights data lags 6-18 months; AI-synthesized estimates inherit that lag without disclosure
- Triangulation only improves confidence if the two paths are truly independent — AI often draws from the same underlying sources for both
- Currency and geography scope creep: AI frequently extends a US-market figure to "global" without flagging the assumption

## Agentic workflow
A Claude Sonnet agent handles the full sizing loop: it receives a market definition, generates separate top-down and bottom-up research queries, dispatches them to Perplexity or web-search, collects results, and outputs a structured estimate with confidence ranges and assumption log. The agent must be explicitly instructed to keep the two paths independent and to document every assumption. A human reviews the assumption log before the estimate is used in any deliverable.

### Recommended subagents
- `faion-sdd-executor-agent` — executes a market-sizing task defined in an SDD spec with quality gates

### Prompt pattern
```
<market_sizing_task>
  <market>Cloud-based AI research tools for knowledge workers, global, 2026</market>
  <approach>Run top-down and bottom-up independently. Do not share intermediate results between paths.</approach>
  <top_down>Find total knowledge-worker software market → isolate AI tools segment → apply addressable fraction</top_down>
  <bottom_up>Estimate target companies × seats × annual price</bottom_up>
  <output>
    - TAM, SAM, SOM with confidence range (low/mid/high)
    - Assumption log (one line per assumption)
    - Source list with access date
  </output>
</market_sizing_task>
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pytrends` | Google Trends proxy for demand signal | `pip install pytrends` / [github](https://github.com/GeneralMills/pytrends) |
| `serpapi` | Structured search for market reports | `pip install google-search-results` / [serpapi.com](https://serpapi.com/) |
| `pandas` | Tabulate and triangulate estimates | `pip install pandas` |
| `anthropic` (Python SDK) | Drive Claude for synthesis and calculation | `pip install anthropic` / [docs](https://docs.anthropic.com/) |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Statista | SaaS | No — export only | Market reports; agent must parse downloaded PDFs |
| CB Insights | SaaS | Partial — CSV export | Company counts, funding data useful for bottom-up |
| Perplexity Pro | SaaS | Yes — REST API | Best for synthesizing analyst commentary |
| AlphaSense | SaaS | Partial | Strong for public-company disclosures and earning-call signals |
| Exploding Topics | SaaS | Yes — REST API | Demand signal for emerging markets |
| Google Trends | Free | Yes — `pytrends` | Proxy for consumer demand; not reliable for B2B |

## Templates & scripts
See `templates.md` for the full market-sizing brief template. Inline triangulator:

```python
import anthropic, json

client = anthropic.Anthropic()

def triangulate_market(market_def: str, top_down_data: str, bottom_up_data: str) -> dict:
    prompt = f"""<triangulation>
<market>{market_def}</market>
<top_down_findings>{top_down_data}</top_down_findings>
<bottom_up_findings>{bottom_up_data}</bottom_up_findings>
<instructions>
1. Compute TAM/SAM/SOM for each path independently.
2. If estimates differ by more than 2x, identify which assumption drives the gap.
3. Output JSON: {{
     "tam": {{"low": 0, "mid": 0, "high": 0, "unit": "USD billions"}},
     "sam": {{"low": 0, "mid": 0, "high": 0}},
     "som": {{"low": 0, "mid": 0, "high": 0}},
     "confidence": "low|medium|high",
     "gap_driver": "string or null",
     "assumptions": ["list"]
   }}
</instructions>
</triangulation>"""
    r = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return json.loads(r.content[0].text)
```

## Best practices
- Define market boundaries in the prompt with three constraints: geography, customer type, and minimum deal size
- Always run top-down and bottom-up in separate agent calls to prevent cross-contamination of reasoning
- Include a confidence range (low/mid/high), not a single point estimate — AI cannot produce false precision
- Log every assumption explicitly; reviewers need to challenge assumptions, not numbers
- Re-run sizing every 6 months for fast-moving markets; instruct the agent to flag stale sources (>12 months old)
- Cross-check AI estimates against any available public analyst commentary, even if from a different geography

## AI-agent gotchas
- Agents conflate TAM and SAM without explicit definitions; define both in the system prompt
- LLMs anchor heavily on the first data point encountered; instruct the agent to collect all sources before synthesizing
- Bottom-up paths require a customer count estimate the agent cannot verify; treat this as a human-supplied input, not AI output
- "Similar market" reasoning (e.g., "CRM market is $X, so AI research tools should be Y% of that") is a hallucination risk unless sourced
- Models will omit the confidence range unless explicitly required in the output schema

## References
- [CB Insights Market Sizing Guide](https://www.cbinsights.com/research/report/market-sizing/)
- [Perplexity API](https://docs.perplexity.ai/)
- [Statista](https://www.statista.com/)
- [AlphaSense](https://www.alphasense.com/)
- [Sequoia Market Sizing Framework](https://www.sequoiacap.com/article/how-to-present-to-investors/)
