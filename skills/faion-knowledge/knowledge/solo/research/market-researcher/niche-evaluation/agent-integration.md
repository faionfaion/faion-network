# Agent Integration — Niche Evaluation

## When to use
- After `idea-generation` produces 5-10 candidate niches; need to score and short-list.
- Pivoting from current niche; need to benchmark new candidate against current performance.
- Investor/board ask: "why this niche over X" with defensible numbers.
- Product-line expansion: should our second product target the same niche or adjacent?

## When NOT to use
- You're already shipping with paying customers in the niche — your churn data beats any agent score.
- Pure curiosity research; the framework is decision-forcing, not exploratory.
- Hyper-local services (plumber, dentist) — TAM/SAM/SOM doesn't translate; use catchment-area metrics.

## Where it fails / limitations
- TAM/SAM/SOM numbers are the most-fabricated outputs in product agents. Without explicit data sources (Statista, IBISWorld, gov stats), agents anchor on round-number priors ($1B, $100M, $10M).
- "Competitor mapping" via LLM lists 5 well-known names; misses the long tail (Indie Hackers, Etsy shops, Discord servers) where real competition lives.
- Audience-accessibility scoring is gameable — agents score 4-5 for any niche with a Reddit subreddit, regardless of the sub's actual engagement.
- Personal-fit can't be evaluated by agent; must be founder self-report, never delegated.
- The 4.0+ "proceed immediately" threshold is a folk number; calibrate against your past wins/losses, not the framework's defaults.

## Agentic workflow
Two-phase: (1) `niche-researcher` agent gathers evidence — TAM via Statista WebFetch, competitors via Crunchbase + Indie Hackers + G2, audience signals via Reddit/Twitter API. Outputs an evidence file with citations. (2) `niche-scorer` agent applies the 5-criterion matrix using ONLY evidence from phase 1; refuses to score without source. Final personal-fit score entered by human. Compare 3-5 niches side-by-side, decide top 1-2 for problem-validation phase. Run on quarterly cadence as market shifts.

### Recommended subagents
- `niche-researcher` — sonnet + WebFetch + Reddit API, evidence-collection phase. Outputs JSON with citations.
- `niche-scorer` — sonnet, applies scorecard with refuse-without-source rule.
- `competitor-mapper` — haiku, maps competitors onto Quality × Players quadrant from raw list.
- Personal-fit: NO agent. Founder fills directly.

### Prompt pattern
```
Niche definition: {[Product Type] for [Audience] who [Problem]}
Phase 1 — Evidence gathering. Do NOT score yet. Return:
- TAM: $X cite source URL
- SAM: $X cite source URL
- SOM: $X show calculation
- Competitors: [{name, url, pricing, strength, weakness, source}]
- Communities: [{platform, name, members, activity_level, source_url}]
- Search volume: from Google Trends / Ahrefs free tier
Refuse to fabricate. If unknown, return "unknown" — better than guess.
```

```
Evidence: {phase1.json}
Score 4 of 5 criteria (Market, Competition, Accessibility, Monetization)
1-5, citing evidence row. Do NOT score Personal Fit. Return scorecard +
weighted total + decision band. Flag any score with weak evidence.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pytrends` | Google Trends programmatic | `pip install pytrends` |
| `ahrefs-api` (paid) | Keyword volume, domain authority | https://ahrefs.com/api |
| `praw` | Reddit API for community sizing | `pip install praw` |
| `crunchbase-cli` (community) | Competitor funding/team data | https://www.crunchbase.com/data |
| `claude` + WebFetch | Statista, IBIS, G2 page fetching | https://docs.anthropic.com/en/docs/claude-code |
| `jq` + `csvkit` | Niche-comparison matrix | system |
| `datasette` | Visualize multi-niche scorecards | `pip install datasette` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Statista | SaaS, paid | WebFetch (limited) | Authoritative TAM; most reports paywalled. Free abstracts citable. |
| IBISWorld | SaaS, paid | Limited | Industry reports; library card free access often available. |
| US Census BFS / SBA | Free gov | Yes | Small-business demographics, business formation; cite-quality source. |
| Eurostat | Free gov | Yes | EU-side TAM data. |
| Google Trends | Free | Yes (`pytrends`) | Direction, not magnitude. |
| Ahrefs / SEMrush | SaaS | API yes | Keyword volume; free tier limited. |
| Reddit (`praw`) | Free | Yes | Community size, post velocity, sentiment. |
| Twitter/X API | SaaS | Paid only post-2023 | Niche conversations; expensive for hobbyist. |
| Crunchbase | SaaS | Limited | Competitor funding/headcount; gated. |
| G2 / Capterra | SaaS | Scrape | Competitor reviews → weakness mining. |
| Indie Hackers | Free | Scrape | Solopreneur-scale competitor revenue self-disclosure. |
| Discord / Circle / Slack | Various | Manual | Community-of-practice signal; rarely API-accessible. |

## Templates & scripts
See `templates.md` for Niche Evaluation Scorecard. Multi-niche side-by-side runner:

```bash
#!/usr/bin/env bash
# evaluate-niches.sh — pass file with one niche definition per line
set -euo pipefail
NICHES=${1:?niches.txt required}
RUN=~/niches/$(date +%F)
mkdir -p "$RUN"

while IFS= read -r niche; do
  slug=$(echo "$niche" | tr ' /' '_-' | head -c 40)
  claude -p "$(cat ~/prompts/niche-research.txt)" \
    --input "Niche: $niche" > "$RUN/$slug.evidence.json"
  claude -p "$(cat ~/prompts/niche-score.txt)" \
    --input-file "$RUN/$slug.evidence.json" > "$RUN/$slug.score.json"
done < "$NICHES"

# Comparison table
jq -s '[.[] | {niche: .niche, score: .total, band: .decision}]' \
  "$RUN"/*.score.json | csvkit -f json > "$RUN/comparison.csv"
```

## Best practices
- **One sentence niche definition mandatory**: `[Product] for [Audience] who [Problem]`. If you can't, agent output is worthless.
- **Evidence-before-score discipline**: never let the same agent gather + score; bias compounds.
- **Long-tail competitor scan**: agents miss IH/Etsy/Discord competitors. Force a "what would a $1k MRR solo developer build here" prompt as separate pass.
- **Calibrate thresholds against your wins**: if your last winning niche scored 3.7, your "proceed" band is 3.5+, not 4.0.
- **Re-evaluate quarterly**: market direction (Trends arrow) matters more than absolute size for early-stage.
- **Personal fit overrides**: any niche where founder excitement < 3 fails, regardless of score. Hard-code this gate.
- **Buyer ≠ user**: niches where buyer (e.g., manager) differs from user (e.g., engineer) need both columns scored separately. Agents collapse them; force split.

## AI-agent gotchas
- TAM hallucination is the #1 failure. Reject any number without `source_url`. Better "unknown" than fabricated.
- Agents over-rate "blue ocean" — they don't know what they don't see. Probability of zero competitors ≈ probability of zero demand. Score caution.
- Reddit member count is vanity; weight by 30-day post velocity instead. Force agent to fetch both.
- Monetization scoring biases toward SaaS (training data dominance). Course/template/services niches systematically under-score; correct manually.
- **Human-in-loop checkpoint**: personal-fit row + final go/no-go always human.
- Currency: TAM in USD, but if niche is non-US, agents miss FX/PPP. Mark currency explicitly.
- "Few competitors" can mean either blue ocean or no demand — forces a problem-validation step before commit.
- Agents conflate niche size with founder addressable market; the 1-3% SOM is on a multi-year horizon, not Year 1.

## References
- Pat Flynn — "Will It Fly?" (niche viability framework)
- Sam Altman — "How to Start a Startup" lecture series (market sizing)
- Steve Blank — "The Four Steps to the Epiphany" (customer development)
- Eric Ries — "The Lean Startup" (validation discipline)
- Statista, IBISWorld, US Census BFS — TAM/SAM evidence sources
- "Indie Hackers Podcast" — long-tail competitor revenue signal
