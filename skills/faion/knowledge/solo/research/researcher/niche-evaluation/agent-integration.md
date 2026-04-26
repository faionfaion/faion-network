# Agent Integration — Niche Evaluation

## When to use
- Choosing among 3-10 candidate niches before committing to a product direction.
- Solopreneur narrowing-down stage: ideas list → top 3 to validate.
- Re-evaluating an existing niche after market signals shift (new entrants, regulation, AI commoditization).
- Pitching investors / stakeholders and needing a defensible scoring rubric.

## When NOT to use
- After committing — switch to problem-validation, then feature-discovery.
- For very small experiments (one-week tests) where decision overhead exceeds upside.
- When you have only one niche option — score it but don't pretend the comparison is meaningful.
- For commodity markets where the niche is irrelevant (execution speed wins).

## Where it fails / limitations
- Personal-fit weight (20%) is the most-faked dimension; founders inflate it for ideas they like.
- TAM/SAM/SOM numbers from analyst reports are commonly off by an order of magnitude; treat as ranges.
- Competition matrix becomes static the day you build it; refresh quarterly.
- Accessibility scoring (Reddit/Twitter/podcasts) overrates discoverability for B2B niches where decision-makers don't post publicly.
- A high score doesn't survive contact with one bad interview; this method gates exploration, not decisions.

## Agentic workflow
Score each candidate niche through five subagent passes (market, competition, accessibility, monetization, personal fit). Each pass returns JSON with score + 3 evidence citations. A separate aggregator agent computes the weighted total and ranks niches; the human picks based on ranking + qualitative gut. Run the comparison sheet side-by-side, never one niche at a time.

### Recommended subagents
- `market-sizer` (sonnet + WebSearch) — estimates TAM/SAM/SOM with cited sources.
- `competition-mapper` (sonnet) — finds 5-10 competitors per niche, classifies by quadrant.
- `accessibility-scorer` (haiku) — checks subreddits, podcasts, X/LinkedIn presence.
- `monetization-modeler` (sonnet) — evaluates revenue models against segment willingness to pay.
- `personal-fit-prober` (sonnet) — interviews founder via questions, NOT auto-scores.
- `niche-aggregator` (haiku) — fills the weighted scorecard.

### Prompt pattern
```
Role: market-sizer.
Input: niche definition "[product] for [audience] who [problem]".
Output JSON: {tam:{value, range, source_url}, sam:{...}, som:{...}, trend:"growing|flat|declining", evidence:[urls]}.
Rule: cite at least 2 independent sources; if data thin, return {confidence: "low"} not fabricated numbers.
```

```
Role: competition-mapper.
Input: niche definition + 1-page market summary.
Output JSON: {competitors:[{name, url, pricing, positioning, quadrant:"opportunity|premium|crowded|race-to-bottom"}]}.
Rule: minimum 5 competitors; if fewer found, flag "low competition signal" with reasoning.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `searx` (self-hosted) | Privacy-preserving multi-engine search | https://docs.searxng.org |
| `pup` / `htmlq` | Scrape competitor pricing pages | https://github.com/EricChiang/pup |
| `gh` | Mine GitHub topic searches for OSS competitors | https://cli.github.com |
| `pytrends` | Google Trends programmatic access | https://github.com/GeneralMills/pytrends |
| `keyword-tools-cli` (3rd-party) | Pull keyword volume estimates | varies |
| `crunchbase-api` | Funding + competitor data | https://data.crunchbase.com/docs |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Crunchbase | SaaS | Yes (API, paid) | Funding/founders/valuations of competitors. |
| Similarweb | SaaS | Partial (API costly) | Competitor traffic + sources. |
| SEMrush / Ahrefs | SaaS | Yes (API) | Keyword volume, organic traffic, backlink intelligence. |
| BuiltWith | SaaS | Yes (API) | Tech-stack signal of competitor maturity. |
| Statista | SaaS | Manual | TAM/SAM data; rate-limited for agents. |
| G2 / Capterra | SaaS | Limited (scraping) | Competitor reviews → pain mining. |
| Reddit API | OSS | Yes | Community size + post frequency = audience health. |
| Discord / Slack APIs | SaaS | Yes (with consent) | B2B-niche community presence. |
| Listen Notes | SaaS | Yes (API) | Podcast presence in a niche. |

## Templates & scripts
See `templates.md` for the full Niche Evaluation Scorecard.

Inline weighted scorer (Python, ≤30 lines):
```python
import csv, sys
WEIGHTS = {"market":0.25,"competition":0.20,"accessibility":0.15,
           "monetization":0.20,"personal_fit":0.20}
THRESHOLDS = [(4.0,"proceed"),(3.5,"validate"),(3.0,"fix-weak-areas"),(0,"reconsider")]
with open(sys.argv[1]) as f:
    rows = list(csv.DictReader(f))
for r in rows:
    score = sum(float(r[k]) * w for k, w in WEIGHTS.items())
    label = next(l for t, l in THRESHOLDS if score >= t)
    print(f"{r['niche']:<40} {score:.2f}  -> {label}")
```

## Best practices
- Score at least 3 niches in parallel; absolute scores mean little without comparison.
- Lock weights before scoring; tweaking weights to favor a preferred niche is the most common bias.
- Require evidence citations for any score ≥4 — this is the agent's most-fabricated zone.
- Personal fit must come from a self-interview, not an auto-score; LLMs flatter the user.
- Re-score niches every quarter; market entries / regulation can flip the ranking.
- Use Reddit/Discord post frequency as a leading indicator — declining communities = declining niche.

## AI-agent gotchas
- LLMs hallucinate TAM numbers when the niche is narrow (e.g., "AI tools for solo notaries"). Require source URLs or "low confidence".
- "Few competitors" can mean blue ocean OR no demand. Force the agent to distinguish via search-volume + adjacent-product data.
- Agents over-weight high-quality SaaS competitors and miss spreadsheet/Notion-template alternatives — explicitly include "current workarounds" in the competition prompt.
- Personal fit auto-scoring leaks the user's enthusiasm; surface it as a question, never compute it.
- When asked to compare niches, agents pick the one mentioned first; randomize order.

## References
- Eric Ries, "The Lean Startup" (build-measure-learn).
- Pat Flynn / Smart Passive Income — niche evaluation worksheets for solopreneurs.
- Steve Blank, "Customer Development" — niche segmentation and serviceable obtainable market.
- Naval Ravikant, "How to Get Rich" — specific knowledge + leverage angle on niche.
- Rob Walling, "Start Small, Stay Small" — bootstrap niche evaluation.
- Daniel Vassallo, "Just F***ing Ship" — anti-overthinking counterweight.
