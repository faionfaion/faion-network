# Agent Integration — Market Sizing with AI

## When to use
- Early-stage validation of TAM/SAM/SOM before investor deck or strategic decision
- Triangulating conflicting market estimates from multiple sources
- Quickly generating a bottom-up model from known unit economics
- Stress-testing existing market assumptions when entering a new segment
- Supplementing a market researcher's draft with AI-fetched data points

## When NOT to use
- As the sole input for a fundraising pitch without primary source validation — LLMs hallucinate market figures
- When the market is nascent (< 3 years old) and no industry reports exist; AI-synthesized data will lack grounding
- When regulatory or geographic nuance is critical (e.g., healthcare TAM per country); AI estimates are too coarse
- When precision matters more than speed — hire a research analyst for high-stakes M&A diligence

## Where it fails / limitations
- LLMs frequently confuse TAM/SAM/SOM definitions and produce figures without citing the report; always demand source URLs
- Top-down figures from Statista, CB Insights, or similar are often paywalled — the agent sees a summary, not raw data
- Bottom-up models require accurate unit economic inputs (ACV, churn, conversion rates); agents will guess if not provided
- Triangulation only increases confidence when both approaches use independent data sources; agents often reuse the same underlying report for both paths
- Market sizing is a point-in-time snapshot; AI tools do not flag when a figure is stale (e.g., 2022 data presented as current)

## Agentic workflow
Run a two-pass workflow: Haiku fetches numerical data from Statista/CB Insights summaries and industry reports; Sonnet constructs both top-down and bottom-up models in parallel; Opus performs triangulation, stress-tests assumptions, and flags low-confidence inputs. The final output is a structured spreadsheet-ready table with explicit assumption documentation and confidence ratings per data point.

### Recommended subagents
- `faion-sdd-executor-agent` — orchestrates multi-step research pipelines with quality gates per stage
- General Claude subagent (Haiku) — bulk data extraction from reports, calculates simple formulas
- General Claude subagent (Opus) — scenario modeling, sensitivity analysis, triangulation validation

### Prompt pattern
```
You are a market sizing analyst. Produce a TAM/SAM/SOM estimate for [market].

Step 1 — Top-down:
Find a credible industry report figure for the total market size.
State the source, year, and geography. Apply [segment %] to get SAM.
Apply [our realistic share %] to get SOM.

Step 2 — Bottom-up:
Estimate: # of potential buyers = [describe ICP].
Average annual contract value = $[X].
Bottom-up TAM = buyers × ACV.

Step 3 — Triangulate:
Compare top-down vs bottom-up. If within 2x, report the midpoint.
If divergent, explain why and flag as low confidence.
Output: markdown table with columns: Metric | Value | Source | Confidence (H/M/L).
```

```
Stress-test this market sizing model: [paste model].
Identify the 3 assumptions with the highest sensitivity.
For each, show what happens if it is 50% lower than assumed.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| perplexity-mcp (MCP) | Fetches cited web search results; useful for report summaries | MCP server, see perplexity.ai/api |
| jq | Parse JSON responses from Statista/CB Insights APIs | `apt install jq` / stedolan.github.io/jq |
| Python + pandas | Bottom-up model calculation and sensitivity tables | `pip install pandas` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Perplexity Pro | SaaS | Yes (API) | Best for synthesized multi-source estimates with citations |
| Statista | SaaS | Partial | Summaries free; raw data paywalled; API for enterprise |
| CB Insights | SaaS | Partial | API available for enterprise; agents get summaries |
| AlphaSense | SaaS | Partial | Filings search; strong for public company benchmarks |
| SimilarWeb | SaaS | Yes (API) | Traffic/user estimates for digital market sizing |
| PitchBook | SaaS | No | No public API; data quality high but human-only access |

## Templates & scripts
See `templates.md` for the market sizing worksheet template.

Bottom-up calculation script (Python, inline):
```python
# bottom_up_tam.py
def calc_market(
    icp_companies: int,
    adoption_rate: float,     # 0.0-1.0
    acv_usd: float,
    growth_rate_yoy: float,   # 0.0-1.0, for 3-yr projection
) -> dict:
    buyers = icp_companies * adoption_rate
    tam = buyers * acv_usd
    return {
        "buyers": int(buyers),
        "tam_year1": tam,
        "tam_year3": tam * ((1 + growth_rate_yoy) ** 3),
    }

# Example
result = calc_market(
    icp_companies=500_000,
    adoption_rate=0.05,
    acv_usd=10_000,
    growth_rate_yoy=0.25,
)
print(result)
# {'buyers': 25000, 'tam_year1': 250000000, 'tam_year3': 488281250}
```

## Best practices
- Always run both top-down and bottom-up; accept the result only when they are within 2-3x of each other
- Document every assumption explicitly — "ICP = 500K companies" must cite a source or be flagged as an estimate
- Use Perplexity Pro Search over ChatGPT for market data — Perplexity cites sources; ChatGPT often fabricates figures
- Include confidence ratings (H/M/L) per data point; investors will ask, and it forces honest calibration
- For SOM, use realistic 3-5 year capture rates based on comparable early-stage companies, not wishful thinking
- Refresh quarterly — market data older than 18 months in fast-moving sectors should be flagged as stale

## AI-agent gotchas
- Agents frequently omit the year of market data; always require the agent to state the publication year explicitly
- Haiku/Sonnet will invent a plausible-sounding figure if no real data is found; add "if no credible source found, return NULL" to the prompt
- Top-down and bottom-up agents may both cite the same underlying Gartner/IDC estimate presented differently — triangulation is false confidence; require independent data paths
- Sensitivity analysis requires the agent to vary one assumption at a time while holding others fixed; without that instruction, agents vary multiple simultaneously and produce noise
- Human checkpoint required before any market size is presented externally; agent output is directional, not quotable

## References
- https://www.nngroup.com/articles/market-sizing/ (framing, not AI-specific)
- https://www.sequoiacap.com/article/writing-a-business-plan/ (TAM/SAM/SOM framing)
- Perplexity AI Pro Search — https://www.perplexity.ai/
- CB Insights — https://www.cbinsights.com/
- AlphaSense — https://www.alpha-sense.com/
- SimilarWeb API — https://developers.similarweb.com/
