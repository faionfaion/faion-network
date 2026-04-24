# Agent Integration — Business Model Planning

Methodology covers four linked frameworks: niche-viability-scoring (5-criteria),
business-model-research (Blue Ocean / Four Actions), value-proposition-design
(Strategyzer canvas), pricing-research (model selection + Van Westendorp).

## When to use

- Pre-spec phase of a new product/SaaS where TAM/SAM/SOM exists but no model decision yet.
- Niche short-list arrives from `idea-generation-methods` and needs ranking before a `spec.md`.
- Re-pricing an existing SaaS after churn or competitor shift; need defensible tier cuts.
- Pivoting into a "blue ocean" adjacency — must justify which factors to eliminate/raise.
- Founder asks "is this niche worth pursuing?" and needs a number, not an opinion.
- Solopreneur on faion-net stack needs a value-proposition canvas wired to a `persona-building` doc before launch.

## When NOT to use

- Pure market sizing — use `market-research-tam-sam-som` first.
- Competitor feature/pricing scrape — use `competitor-analysis` and pipe its output here.
- Already-priced product with PMF; tweak via `conversion-optimizer`, not a re-canvas.
- B2C consumer apps with ad-only revenue — pricing-research framework assumes paid value capture.
- Funded startup with VC pressure for hyper-growth; Blue Ocean discipline often loses to land-grab tactics.
- Internal tools, hobby projects, or commissioned client work with fixed scope/budget.

## Where it fails / limitations

- **Subjective scores look quantitative.** A 7.30 weighted total feels precise; the inputs are gut calls. Treat outputs as relative rankings across niches, not absolute go/no-go.
- **Blue Ocean post-hoc bias.** Cirque, Yellow Tail, NetJets are always-cited because they worked. Survivorship masks the failure rate of "create new factor" bets.
- **Value Proposition Canvas decays.** Pains/gains shift quarterly in early markets; a 6-month-old canvas is fiction.
- **Van Westendorp on synthetic personas.** LLM-simulated WTP surveys produce regression-to-mean prices ($19/$49/$99) regardless of niche — agents must be told to stay out of pricing surveys.
- **Tiered pricing complexity.** "Tiered subscription" is the default LLM answer for any SaaS; usage-based or hybrid often dominates real economics.
- **Five-criteria weights are fixed.** 25/20/20/20/15 was tuned for indie SaaS; enterprise sales, hardware, marketplaces need different weightings.

## Agentic workflow

Drive this methodology as a four-phase pipeline where each phase writes a structured artifact the next phase consumes. Phase 1 (niche-viability) produces a scorecard from up to 5 candidate niches; phase 2 (business-model) takes the top niche and runs the Four Actions against scraped competitor data; phase 3 (value-proposition) joins customer-jobs from `persona-building` with phase-2 output to produce a fit score; phase 4 (pricing) ingests `competitor-analysis` pricing tables plus phase-3 value estimate and emits tier definitions. Each phase writes Markdown + a sidecar JSON with the same structure so a downstream `product-manager` agent can consume it without re-parsing prose.

### Recommended subagents

- `faion-research-agent` (mode `niche`) — owns phases 1-2; the existing methodology already binds to it (see README "Agent" lines).
- `faion-research-agent` (mode `personas`) — owns phase 3; pulls or builds `persona-building` artifacts before scoring fit.
- `faion-research-agent` (mode `pricing`) — owns phase 4; restricted to WebSearch + Read on competitor docs.
- `faion-sdd-executor-agent` (in this repo: `agents/faion-sdd-executor-agent.md`) — wraps the four phases as four SDD tasks under one feature, enforcing quality gates between them.
- `faion-brainstorm` skill — invoke between phases 1 and 2 when only one niche scores ≥6.0 and you need 5+ Blue Ocean ideas to choose from.

### Prompt pattern

Phase 1 (scoring):

```
Score niche "{niche}" using the 5-criteria model in
knowledge/pro/research/market-researcher/business-model-planning/README.md.
Use WebSearch for market size + competitor count. Output: Markdown table
matching the README "Niche Viability Scorecard" template AND a JSON sidecar
{niche, criteria:[{name, score, weight, justification, sources:[url]}], total, decision}.
Do NOT invent sources. If a criterion cannot be sourced, set score=null and
flag it in justification.
```

Phase 4 (pricing), constrained:

```
Given competitors.json (from competitor-analysis) and value_map.json (from phase 3),
recommend ONE pricing model from the 6 in the README. Reject "tiered subscription"
unless you can name 3 distinct WTP segments with different jobs-to-be-done.
Output: justification (≤150 words) + tiers table + the rejection reasons for the
other 5 models.
```

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `strategyzer-cli` (community wrappers, not official) | VPC + BMC scaffolding as Markdown | `npm i -g strategyzer-md` (third-party) |
| `flowchart-cli` / `mermaid-cli` | Render Strategy Canvas as line plot from CSV | `npm i -g @mermaid-js/mermaid-cli` |
| `pandas` + `scipy` | Van Westendorp PSM analysis (4 question intersect) | `pip install pandas scipy` |
| `pricingsaas-cli` (unofficial scraper) | Pull competitor pricing pages | github.com/pricingsaas/scraper (verify ToS) |
| `gh` | Pull README pricing/business-model docs from competitor OSS repos | `gh repo view <org>/<repo> --json description,homepageUrl` |
| `curl` + `jq` | Hit Crunchbase/Producthunt unofficial JSON endpoints for competitor lists | preinstalled |
| `perplexity` MCP / `tavily` | Sourceable WebSearch with citations (better than raw WebSearch for criterion justification) | tavily.com, perplexity.ai |

## Services & apps

| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Strategyzer.com | SaaS | No public API | Manual export only; parse PDFs server-side. |
| Miro / FigJam | SaaS | Partial (Miro REST v2) | Can create/read sticky notes; not designed for batch canvas generation. |
| Notion | SaaS | Yes (REST API) | Best target for writing canvases — DB schema per phase. |
| Airtable | SaaS | Yes (REST + MCP) | Good for niche-scorecard as a sortable base. |
| ProductHunt API | SaaS | Yes (GraphQL, OAuth) | Niche competitor discovery; rate-limited. |
| Crunchbase API | SaaS (paid) | Yes | TAM/competitor signals; pricing prohibitive for solo. |
| ProfitWell / Paddle Price Intelligence | SaaS | Limited | Pricing benchmarks per category — public reports only without contract. |
| OpenVC / SimilarWeb | SaaS | Partial | Useful for SAM estimation inputs. |
| Conjointly | SaaS | Yes (API) | Real Van Westendorp / conjoint with real respondents — never use LLM-simulated WTP instead. |
| `awesome-business-models` (GitHub lists) | OSS | Yes (raw md) | Pattern library for Four Actions ideation. |

## Templates & scripts

The README ships four Markdown templates (scorecard, Blue Ocean canvas, VPC, pricing strategy). Use them as-is.

Inline helper — weighted niche score from a JSON sidecar (run after phase 1):

```bash
#!/usr/bin/env bash
# score-niche.sh <scorecard.json>
# Validates weights sum to 1.0 and recomputes weighted total.
set -euo pipefail
F="${1:?scorecard.json required}"

jq -e '
  . as $c
  | (.criteria | map(.weight) | add) as $w
  | (.criteria | map(.score * .weight) | add) as $t
  | if ($w - 1.0 | fabs) > 0.001
      then error("weights sum to \($w), not 1.0")
    elif (.criteria | any(.score == null))
      then error("null score in: \([.criteria[] | select(.score==null) | .name] | join(\",\"))")
    else
      {niche, total: ($t|.*100|round/100),
       decision: (if $t >= 7.5 then "STRONG" elif $t >= 5.5 then "CAUTION"
                  elif $t >= 3.5 then "RISK" else "PASS" end),
       criteria: .criteria}
    end
' "$F"
```

For Van Westendorp PSM, use a real survey tool (Conjointly, Pollfish). Do NOT generate synthetic respondents with an LLM — the README pricing-research step 3 explicitly demands real users.

## Best practices

- Score 3-5 niches in parallel, never one in isolation; the framework's value is comparative ranking.
- Always cite a URL per criterion score. "Market size: 7" with no link is noise an agent can fabricate.
- Run phase 2 (Four Actions) only after a `competitor-analysis` doc exists — otherwise "eliminate" lacks a baseline.
- Bind VPC pains to interview transcript IDs from `user-interviews-methods`; un-cited pains decay fastest.
- For pricing, default-reject "tiered subscription" and force the agent to argue for it (defeats LLM bias toward $9/$19/$49).
- Keep weighted-criteria weights under version control; if you adjust them mid-comparison, restart the entire batch.
- Treat the four phases as gated SDD tasks — each must produce a JSON sidecar that validates against a stored schema before next phase runs.
- Re-run niche-viability quarterly on shipped products; turning the score into a trend line catches creeping red-ocean drift.

## AI-agent gotchas

- **Hallucinated TAM.** Agents will confidently state "$200M market" with no source. Require `sources: [url]` in JSON sidecar; reject empty arrays.
- **Default scoring.** LLMs anchor everything to 6/7. Force the agent to assign at least one ≤4 and at least one ≥8 across the 5 criteria, or rerun with chain-of-thought.
- **Cirque-du-Soleil syndrome.** Asked for Blue Ocean examples, agents quote the same 5-7 textbook cases. Require examples post-2018 and reject Cirque/Yellow Tail/NetJets/iTunes/Wii citations.
- **Pain inflation.** Customer-profile pains all come back as 8-9/10 unless capped. Cap: at most 2 pains may exceed 7/10 per persona.
- **Pricing regression to mean.** WTP estimates collapse to $19/$49/$99. Pin to an external benchmark (ProfitWell category report, competitor scrape) before letting the agent suggest tiers.
- **HITL gates:** before phase 2 (niche commitment), before phase 4 (pricing publication), and before any external-facing canvas. Pricing in particular must never auto-publish — single typo can tank revenue.
- **Survivorship bias in canvases.** Strategy Canvas curves drawn by an LLM tend to look like the winning case. Force plotting against ≥3 real competitor data points pulled from competitor-analysis JSON.
- **Stale canvases.** Add `valid_until` (90 days) to every VPC sidecar; expire and force regeneration in CI.

## References

- Osterwalder & Pigneur, *Business Model Generation* (2010) — BMC + VPC origin.
- Osterwalder et al., *Value Proposition Design* (2014) — VPC mechanics and FIT.
- Kim & Mauborgne, *Blue Ocean Strategy* (2005, expanded 2015) — Four Actions, Strategy Canvas.
- Van Westendorp (1976), "NSS-Price Sensitivity Meter" — original PSM paper.
- Patrick Campbell / ProfitWell pricing studies — pricing model selection benchmarks.
- Strategyzer.com canvas downloads (free PDFs) — printable templates.
- Sibling methodologies in this skill: `competitor-analysis/`, `market-research-tam-sam-som/`, `persona-building/` (in `pro/research/researcher/`).
