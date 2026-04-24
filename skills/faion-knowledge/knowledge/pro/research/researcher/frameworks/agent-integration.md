# Agent Integration — Research Frameworks (7Ps, PG Questions, Niche, JTBD, TAM/SAM/SOM, Competitive, VPC)

This is a meta-methodology: a toolbox of eight named frameworks rather than one pipeline. Agentic value comes from picking the right one for the question and chaining several without re-asking the user for the same inputs.

## When to use
- Founder is at the "what should I build?" stage and needs a structured idea funnel (7Ps + Paul Graham → niche scoring → JTBD).
- Investor pitch in 7-14 days requires TAM/SAM/SOM plus a competitive table — both are framework rows here.
- Pivot review: re-score current niche against the same 50-point matrix to make stay/pivot defensible.
- GTM repositioning: rebuild the Value Proposition Canvas before rewriting the homepage.
- Multi-idea triage: the agent applies niche evaluation to N ideas in parallel and ranks by score.
- Pre-spec sanity check before writing a `spec.md` — every framework here outputs an artifact a `faion-sdd` agent can ingest.

## When NOT to use
- Already shipping with paying customers — switch to cohort analysis, retention curves, real revenue. Frameworks here are pre-revenue tools.
- Single-question clarifications ("should I charge $19 or $29?") — over-frameworks the answer; use a pricing experiment instead.
- Pure technical scoping (architecture, API design) — wrong layer; use SDD `design.md`, not VPC.
- Hobby projects, internal tools, OSS side projects — the matrices add zero signal where revenue is not the goal.
- When the user wants speed, not rigor — the framework drag is the point; do not invoke for back-of-napkin chats.
- Two-sided marketplaces in pre-launch — supply/demand dynamics dominate; TAM/SAM/SOM is misleading.

## Where it fails / limitations
- Framework theatre: producing a 50/50 niche score with zero primary research is worse than no score. The matrix legitimizes guesses.
- 7Ps overlap heavily — Pain/Profession/People all collapse into "user X has problem Y". Agents tend to duplicate ideas across cells.
- Paul Graham questions reward introspection, not aggregation; LLMs cannot honestly answer "what do you find yourself building for yourself?" — they will invent a project.
- Niche scoring's 1-10 scale is anchored by whoever scores first; two agents on the same idea diverge by 15+ points.
- TAM/SAM/SOM compounds error across four multipliers — see `../market-research-tam-sam-som/agent-integration.md` for the divergence-flag pattern.
- JTBD statements drift into wishful copywriting ("…so I can feel empowered") instead of measurable outcomes.
- Competitive intelligence is biased toward funded/visible competitors; the long tail is invisible to agents.
- VPC fit-check ("do gain creators fulfill desired gains?") is binary in the canvas but always partial in reality — agents over-claim fit.

## Agentic workflow
The agent treats this as a router: it asks the user which decision is being made (idea generation, validation, sizing, positioning) and only loads the relevant frameworks instead of running all eight. Each framework writes one artifact to `.aidocs/product_docs/`; downstream frameworks read upstream artifacts so the user is never re-prompted for ICP, pain, or pricing tier. Numerical frameworks (niche scoring, TAM/SAM/SOM) require a confidence column per row and a cited source for every external number; LLM-only cells are explicitly tagged "estimate".

Concrete pipeline (idea → spec):
1. Discovery — apply 7Ps + Paul Graham in parallel; output `idea-candidates.md` with 10-20 raw ideas.
2. Triage — score each candidate on the 50-point niche matrix; cull anything < 30.
3. Validation — pick top 3, run the validation criteria (frequency, intensity, WTP, search, competition) with primary research (5+ interviews, Google Trends, Reddit search).
4. Jobs — write JTBD statements (functional + emotional + social) for the survivor; use the `When/I want/So I can` template verbatim.
5. Sizing — TAM/SAM/SOM via three-method triangulation (top-down, bottom-up, competitor); flag spread > 2x; do not average.
6. Competition — fill the 6-dimension table (features, pricing, positioning, tech, feedback, GTM); rank competitors by SWOT.
7. Positioning — Value Proposition Canvas; check pain-relievers cover top-3 pains and gain-creators cover top-3 gains.
8. Handoff — write `executive-summary.md` linking all artifacts; pass to `faion-sdd` to draft `spec.md`.

### Recommended subagents
- `faion-research-agent` — orchestrator, 9 modes (`ideas`, `niche`, `market`, `competitors`, `pricing`, `personas`, `pains`, `validate`, `names`); routes to the right framework.
- `faion-market-researcher-agent` — owns sizing, competitor table, pricing, trend analysis frameworks.
- `faion-user-researcher-agent` — owns JTBD, VPC customer side, pains, personas, validation interviews.
- `faion-domain-checker-agent` — pairs with positioning output when a name shortlist is generated.
- General `web-research` / `WebSearch` subagent — required for niche-evaluation market-size column and competitor sweep.
- Sibling methodologies under `../../researcher/`: `niche-evaluation`, `market-research-tam-sam-som`, `competitor-analysis`, `pricing-research`, `problem-validation` — each has its own `agent-integration.md` with deeper detail.

### Prompt pattern
```
You are a research-framework router. Decision being made: <idea | sizing | positioning | pivot>.
Inputs available: <ICP, pain hypothesis, prior artifacts in .aidocs/product_docs/>.
Pick the SMALLEST set of frameworks from frameworks/README.md that answers the decision.
Do NOT run frameworks whose inputs are missing — request them or skip with a note.
For every numeric cell, cite a URL + retrieval date or tag "estimate".
Output: one artifact per framework, plus a one-paragraph rationale for the chosen subset.
```
```
Score these N ideas on the niche-evaluation 50-point matrix.
Rule: each criterion 1-10 with a one-line justification AND a source URL for market-size and competition columns.
Reject any score that lacks a justification. Output: ranked table, then top-3 rationale.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh` (GitHub CLI) | Competitor stars, contributors, issue volume — proxy for traction | `brew install gh` / cli.github.com |
| `pytrends` | Google Trends CAGR signal for validation + niche scoring | pypi.org/project/pytrends |
| `crunchbase-api` | Funding/headcount/founded-year for competitor table | data.crunchbase.com/docs |
| `similarweb-api` | Traffic estimates for competitor-based sizing | developers.similarweb.com |
| `serpapi` / `serper.dev` | Programmatic Google search — search-volume column in validation | serpapi.com / serper.dev |
| `apollo-api` / `clearbit-api` | Firmographic ICP counts for bottom-up TAM | apollo.io/api · clearbit.com/docs |
| `census-bureau-api` (free) | NAICS establishment counts for top-down anchor | api.census.gov |
| `eurostat-api` (free) | NACE establishment counts (EU) | ec.europa.eu/eurostat/api |
| `g2-api` / `capterra` scrape | Review counts — competitor traction proxy | partner.g2.com |
| `producthunt-api` (GraphQL) | Recent launches, upvote velocity for trend signal | api.producthunt.com/v2/docs |
| `whois` / `domainsdb.info` | Domain availability after positioning round | domainsdb.info |
| `waybackpack` | Pin paywalled report URLs to retrieval date | github.com/jsvine/waybackpack |
| `pandoc` + `csvkit` | Convert framework tables between md/csv/xlsx | csvkit.rtfd.io |
| `claude` (Anthropic CLI) | Run framework prompts in batch | docs.anthropic.com |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Crunchbase | Funding/competitor DB | Yes — REST API, paid | Ground truth for competitive table |
| PitchBook | Private market data | Partial — enterprise API | Better than Crunchbase for late-stage |
| Statista | Market reports | Partial — HTML scrape | Best single source for TAM headline |
| IBISWorld | Industry reports | Partial — login scrape | Strong for US/AU verticals |
| SimilarWeb | Traffic estimates | Yes — REST API, paid | Bottom-up reach for SOM |
| Semrush / Ahrefs | SEO + keyword volume | Yes — REST API | Validation "search" column |
| Google Trends | Demand signal | Yes — `pytrends` | Free CAGR sanity check |
| Reddit (`praw`) | Pain-point mining | Yes — REST API | Strong for validating intensity (7+/10) |
| Dovetail / Notably | Interview tagging | Yes — REST API | JTBD synthesis from raw transcripts |
| Maze / UserTesting | Remote user testing | Yes — REST API | Validation criteria evidence |
| Typeform / Tally | Survey collection | Yes — REST API | Quantify WTP, frequency |
| LinkedIn Sales Nav | ICP count | Hostile — ToS-blocked scraping | Manual one-offs only |
| G2 / Capterra | Software reviews | Partial — scrape | Competitor weakness mining |
| Product Hunt | Launch traction | Yes — GraphQL API | Discover long-tail competitors |
| Owler / Owletter | Competitor news | Yes — RSS/email | Cheap competitor-watch layer |
| ChatGPT/Claude with web | Synthesis | Yes — Anthropic/OpenAI APIs | Use ONLY for synthesis, never for primary numbers |

## Templates & scripts
See `templates.md` for the canonical 50-point niche matrix, JTBD statement template, TAM/SAM/SOM math blocks, and competitor output template. Inline router helper:

```bash
#!/usr/bin/env bash
# framework-router.sh — pick frameworks based on the decision being made
# usage: ./framework-router.sh <idea|validate|size|position|pivot>
set -euo pipefail
mode="${1:?mode required: idea|validate|size|position|pivot}"
case "$mode" in
  idea)     echo "7ps paul-graham niche-evaluation" ;;
  validate) echo "validation-criteria jtbd problem-interviews" ;;
  size)     echo "tam-sam-som competitor-analysis" ;;
  position) echo "value-prop-canvas competitor-analysis jtbd" ;;
  pivot)    echo "niche-evaluation tam-sam-som value-prop-canvas" ;;
  *)        echo "unknown mode: $mode" >&2; exit 1 ;;
esac
```

## Best practices
- Pick a subset, not the whole toolbox — running all eight frameworks on one idea is framework theatre.
- Lock the ICP in one sentence before any framework runs; reuse that sentence verbatim across artifacts.
- Cite a URL with retrieval date on every external number; LLM-only cells are explicitly tagged "estimate".
- Niche scoring: require a one-line justification per criterion and force two independent scorers (or two agent runs) — average only if within 2 points.
- TAM/SAM/SOM: triangulate three methods (see sibling methodology); never average if spread > 2x.
- JTBD: write the functional statement first; emotional/social are derivative. Replace adjectives with verbs.
- Validation: 5+ user interviews beats any framework; the matrix is a checklist, not a substitute.
- VPC fit must be checked against actual user quotes, not assumed pains/gains; cite the interview ID per row.
- Competitor table: cap at 5-7 named players plus an explicit "long tail" row — agents tend to over-list.
- Round aggressively: $8.3B is fake precision, $8B is honest; two sig figs max for TAM/SAM.
- Re-score every 6 months; diff the assumptions, not the headlines.
- Frameworks output artifacts in `.aidocs/product_docs/`; downstream agents read these — keep filenames stable.

## AI-agent gotchas
- LLMs hallucinate framework cells fluently; without a citation requirement the niche matrix becomes confidently wrong.
- Confirmation bias: if the user hints "this should be a $1B market" or "I love this idea", the agent reverse-engineers high scores. Pre-commit the scoring rubric before showing the hypothesis.
- 7Ps duplication: the agent fills Pain/Profession/People with restatements of the same idea; require non-overlap by tagging the underlying user-pain-id.
- Paul Graham introspection prompts ("what do you find yourself building?") force the agent to invent a personal project; either skip these for agent runs or pipe in real user history.
- Niche scoring drift: identical inputs to two agent runs produce 15+ point spread. Mitigate by fixing random seed or requiring a justification per cell.
- JTBD wishful copywriting: "feel empowered" is not measurable; require a verifiable outcome ("invoice sent in <90s, paid within 14 days").
- Stale training data: the model "knows" 2023 market sizes and 2022 competitor lists; force fresh web fetches for anything post-cutoff.
- Currency mixing: agents mix USD/EUR/GBP within one TAM report; normalize to USD with a dated FX rate.
- VPC over-fit: the canvas always "fits" if the agent invented both sides; require pains/gains sourced from interviews and pain-relievers from the spec.
- Competitive table over-listing: agents add every adjacent product; cap to direct + 1 indirect tier and tag the rest as "long tail".
- Tier gating: this methodology lives in `pro/`; calling agents on `free`/`solo` tier should abort with a tier-upgrade message instead of approximating.
- Output drift: agents rewrite the template on each pass; lock to the headings in `templates.md` and only fill cells.
- Confusing GMV with revenue, ARR with bookings, MRR with cash — agents add incompatible numbers in competitor tables. Normalize to ARR.

## References
- Methodology files: `README.md`, `checklist.md`, `templates.md`, `examples.md`, `llm-prompts.md` (this directory).
- Sibling deep-dive methodologies: `../market-research-tam-sam-som/`, `../niche-evaluation/`, `../competitor-analysis/`, `../problem-validation/`, `../pricing-research/`.
- Skill orchestrator: `../CLAUDE.md` and `../SKILL.md` — defines `faion-research-agent` modes.
- Paul Graham, "How to Get Startup Ideas" — paulgraham.com/startupideas.html
- Steve Blank, "Market Size: TAM, SAM, SOM" — steveblank.com/2010/01/14/market-size
- Clayton Christensen, "Jobs to Be Done" — christenseninstitute.org/jobs-to-be-done
- Strategyzer, "Value Proposition Canvas" — strategyzer.com/canvas/value-proposition-canvas
- a16z, "16 Startup Metrics" — a16z.com/2015/08/21/16-metrics
- CB Insights, "State of Venture" — cbinsights.com/research
- US Census BDS — census.gov/programs-surveys/bds
- Eurostat SBS — ec.europa.eu/eurostat
- Crunchbase API — data.crunchbase.com/docs
- SimilarWeb API — developers.similarweb.com
- pytrends — github.com/GeneralMills/pytrends
