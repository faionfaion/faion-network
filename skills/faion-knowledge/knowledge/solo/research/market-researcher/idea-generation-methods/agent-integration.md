# Agent Integration — Idea Generation Methods

## When to use
- Earliest exploratory stage: solopreneur or founder with no concrete product target.
- After a project shutdown / pivot, regenerating a fresh idea pool grounded in current pains.
- Refilling the funnel — the methodology is a pre-validation step (idea → niche-evaluation → problem-validation).
- Periodic side-project ideation; the 7P framework + Paul Graham questions + pain mining gives complementary angles.

## When NOT to use
- After committing to a niche; switch to feature-discovery and problem-validation.
- For agency/consulting work where the "idea" is set by the client.
- For incremental optimization on an existing product — wrong scope.
- When you cannot dedicate a week to ideation and follow-up; one-shot brainstorms decay.

## Where it fails / limitations
- Self-generated ideas over-index on personal pain; missing pains affecting larger but unfamiliar segments.
- Paul Graham's "what would you pay for that doesn't exist" is reflexive — most answers are categories, not products.
- Pain mining via complaint audit is biased toward articulate, online users.
- Niche scoring without research data turns into a vibes exercise; agents fabricate scores readily.
- The bundled methodologies overlap in places (pain-point-research vs niche-evaluation); pick a sequence, don't run all in parallel.

## Agentic workflow
This methodology covers four sub-methods (idea-generation, paul-graham-questions, pain-point-research, niche-evaluation) bundled in one file. Drive them as a sequenced pipeline: (1) divergent ideation across 7P + PG questions, (2) pain audit refines candidates, (3) niche scoring filters to top 3. Each step uses structured-output JSON. Final output is 3 candidate niches with research/validation plan.

### Recommended subagents
- `divergent-ideator` (sonnet, high-temperature) — runs 7P framework and PG questions per founder profile.
- `pain-miner` (haiku) — extracts complaints/workarounds/tool-stack gaps from a journal or chat history corpus.
- `convergence-scorer` (sonnet) — applies the 5-dimension scorecard (market/competition/barriers/monetization/fit).
- `faion-brainstorm` skill — already exists in the workspace and pairs perfectly: diverge/converge/review cycles.
- `faion-research-agent` (referenced in README, mode: ideas / niche).

### Prompt pattern
```
Role: divergent-ideator.
Input: founder_profile.md (skills, networks, daily routine), constraints.md (time, capital).
Output JSON: {pain:[5 ideas], passion:[5], profession:[5], process:[5], platform:[5], people:[5], product:[5]}.
Constraint: each idea must reference a concrete trigger from founder_profile, not generic startup tropes.
Temperature: 0.9 (force diversity).
```

```
Role: convergence-scorer.
Input: ideas.json (35 candidates).
Task: score on 5 dimensions {market_size, competition, barriers, monetization, fit} (1-5 each).
Output JSON: {scored:[{idea, scores, total, rationale, missing_data:[fields needing research]}]}.
Constraint: any score ≥4 requires a citation OR "missing_data" flag — no unsupported scores.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `searx` (self-hosted) | Multi-engine search for problem signals | https://docs.searxng.org |
| `pup` / `htmlq` | Scrape Reddit/HN/IH for pain-point patterns | https://github.com/EricChiang/pup |
| `pytrends` | Google Trends interest curves | https://github.com/GeneralMills/pytrends |
| `gh search` | Mine GitHub issues for unsolved problems | https://cli.github.com |
| `nb` | Personal pain journal corpus management | https://github.com/xwmx/nb |
| `obsidian-export` | Pull structured notes from Obsidian vault | https://github.com/zoni/obsidian-export |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Reddit / HN / IndieHackers | OSS web | Yes (read-only APIs) | Highest-density pain mining sources. |
| Exploding Topics | SaaS | Limited (paid API) | Trending niche surfacing; pairs with PG question 4. |
| Glasp / Readwise | SaaS | Yes (API) | Highlight history → recurring themes. |
| Trends.vc / Trends.co | SaaS | Manual | Curated trend reports for inspiration. |
| ProductHunt | SaaS | Yes (GraphQL) | Recent launches → competitor gap analysis. |
| AlternativeTo | SaaS | Manual | "Replace X" opportunities surface niches. |
| Listen Notes | SaaS | Yes (API) | Podcast presence in candidate niche. |
| Twitter/X advanced search | SaaS | Limited (paid API) | Pain mining via complaint queries. |
| Crunchbase | SaaS | Yes (API, paid) | Funded competitors signal market validation. |

## Templates & scripts
See `templates.md` for the Ideation Worksheet, PG Questions Journal, Pain Point Log, and Scoring Matrix.

Inline pain audit → idea suggester (Python, ≤45 lines):
```python
import csv, sys, json
from collections import Counter
# csv columns: date, complaint, category, freq, intensity
rows = list(csv.DictReader(open(sys.argv[1])))
weights = {"daily": 5, "weekly": 3, "monthly": 1}
score = []
for r in rows:
    f = weights.get(r["freq"].strip().lower(), 1)
    i = int(r.get("intensity", 0))
    score.append((r["complaint"], f * i, r["category"]))
score.sort(key=lambda x: -x[1])
for c, s, cat in score[:15]:
    print(f"{s:>5}  [{cat:<10}]  {c}")
cats = Counter([r["category"] for r in rows])
print("\nCategory distribution:", dict(cats))
```

## Best practices
- Run divergent ideation BEFORE looking at trending lists — external trends bias output toward "AI for X" tropes.
- Time-box: 30 minutes per PG question, no editing during. Convergence comes later.
- Pair self-generated pain audit with at least 5 cold conversations; otherwise you're solving for yourself only.
- Score ideas in batches of 10+; absolute scores are meaningless without comparison context.
- Kill ideas aggressively — keep top 3 per cycle. The methodology is filtration, not collection.
- Re-run quarterly; markets move and your skill set evolves, so the input changes.

## AI-agent gotchas
- LLMs revert to generic startup tropes ("AI scheduler", "task tracker") under default temperature; raise to 0.8-0.9 for divergence.
- The agent will conflate "passion" ideas with "profession" ideas — provide a strict definition prompt-side.
- PG question 3 ("what do you find yourself building for yourself") needs personal context; without it, the agent produces dropbox/notion clones.
- Niche scoring is the highest fabrication-risk step; require missing_data flags rather than fabricated numbers.
- Idea de-duplication is unreliable across batches; keep a master list with semantic-search dedupe.
- Human-in-loop checkpoints: (1) founder profile accuracy before ideation, (2) shortlist of 10 before scoring, (3) top-3 sanity check before validation.

## References
- Paul Graham, "How to Get Startup Ideas" (paulgraham.com/startupideas.html, 2012, still definitive).
- Pat Flynn, "Will It Fly?" — solopreneur idea validation framework.
- Rob Walling, "Start Small, Stay Small" — bootstrap idea generation.
- Daniel Vassallo, "Just F***ing Ship" — counter-bias toward action.
- IndieHackers podcast archives — case studies of validated solopreneur ideas.
- "The Mom Test" by Rob Fitzpatrick — feeds into the next stage (problem-validation).
- Trends.co / Exploding Topics newsletters — niche-emergence inspiration (use sparingly to avoid trope bias).
