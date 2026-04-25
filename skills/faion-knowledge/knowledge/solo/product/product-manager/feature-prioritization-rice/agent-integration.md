# Agent Integration — Feature Prioritization (RICE)

## When to use
- Comparing 5+ candidate features in a single quarter where reach and effort vary widely.
- Killing pet features: a numeric score forces stakeholders to debate inputs, not opinions.
- Triaging a backlog after a discovery sprint produced more validated problems than capacity.
- Deciding between two features that look "obviously valuable" — RICE exposes effort-adjusted ROI.

## When NOT to use
- Solo founder with <3 candidates — overhead exceeds signal; flip a coin or pick by gut and ship.
- Hard-deadline regulatory or compliance work — there is no "score", you ship or get fined.
- Discovery phase before reach and impact data exist — confidence will be 50% across the board, ranking is noise.
- Strategic bets / 0-to-1 features — RICE punishes high-effort, high-confidence-low items even when they are the only path to a moat.

## Where it fails / limitations
- Reach × Impact × Confidence is multiplicative, so one wrong factor (e.g. inflated reach) dominates the score.
- Confidence anchors on the loudest scorer; without a calibration step everyone defaults to 80%.
- Effort estimates from PMs are systematically 2-3× too low; engineers must own the E column.
- Score does not encode dependencies, sequencing, or strategic narrative — top-ranked feature may be useless without #4.
- Cross-team comparison breaks: "Reach = 10K" means different things for free-tier vs paid customers.

## Agentic workflow
Have a discovery agent gather feature candidates with a one-paragraph problem statement each, then run a scoring agent that proposes R/I/C/E with explicit rationale per factor (cite analytics queries or research notes). A second reviewer agent challenges every Confidence ≥ 80% and every Effort ≤ 1 month. Human approves the final ranking before it enters the roadmap. Re-run quarterly with a delta-only pass — only re-score items whose underlying assumptions changed.

### Recommended subagents
- `faion-mlp-feature-proposer-agent` — drafts initial R/I/C/E with rationale per factor (named in the README).
- `faion-sdd-executor-agent` — once a feature wins, hand it to SDD to break into spec/design/tasks.
- A custom `rice-challenger` Sonnet agent — single-purpose: read scores, attack confidence and effort claims, return revised proposal.

### Prompt pattern
```
Given the feature candidates in <backlog>, for each compute RICE.
For Reach cite the analytics query or proxy metric.
For Impact pick from {3, 2, 1, 0.5, 0.25} and state which user-facing metric moves.
For Confidence drop one tier (100->80, 80->50) for each unknown.
For Effort use eng-weeks and add 30% buffer for unknown integrations.
Output as a markdown table sorted by score, plus a 2-line "why this ranks here" per row.
```

```
Review this RICE table. Find every Confidence >=80% with no cited evidence and propose a downgrade.
Find every Effort <1 month and ask the engineer-persona challenge questions.
Return a diff, not a rewrite.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh issue list --json number,title,labels` | Pull candidate features from GitHub issues for scoring | https://cli.github.com/manual/gh_issue_list |
| `linear-cli` | Pull/push backlog from Linear, where RICE fields are first-class | https://github.com/evangodon/lr |
| `csvkit` (`csvsql`) | Quick re-rank: `csvsql --query "select *,(r*i*c)/e as rice from features.csv order by rice desc"` | https://csvkit.readthedocs.io |
| `qsv` | Faster csvkit replacement for >10K-row backlogs | https://github.com/jqnatividad/qsv |
| `mermaid-cli` | Render priority bubble charts from RICE output | https://github.com/mermaid-js/mermaid-cli |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| ProductBoard | SaaS | Yes (REST + webhooks) | Native RICE column; agent can POST score updates via API. |
| Productlift | SaaS | Limited (no public API yet) | Cheap RICE-first board for solo PMs. |
| Airfocus | SaaS | Yes (REST API) | Configurable RICE matrix, supports custom factors. |
| Linear | SaaS | Yes (GraphQL API) | Add R/I/C/E as custom fields; agents update via GraphQL. |
| Aha! | SaaS | Yes (REST + webhooks) | Enterprise; RICE templates built-in. |
| Notion | SaaS | Yes (REST API) | DIY: database with formula column for RICE; cheap and scriptable. |
| OpenProject | OSS | Yes (REST API) | Self-host option for RICE custom fields. |

## Templates & scripts
See `templates.md` for the scoring spreadsheet and decision-record formats. Inline helper for re-ranking a CSV:

```bash
#!/usr/bin/env bash
# rice-rank.sh features.csv → sorted CSV with RICE column appended
# CSV columns: name,reach,impact,confidence,effort
set -euo pipefail
input="${1:?usage: rice-rank.sh features.csv}"

awk -F',' 'NR==1{print $0",rice"; next}
  {
    rice = ($2 * $3 * $4) / ($5 == 0 ? 0.01 : $5);
    printf "%s,%.2f\n", $0, rice
  }' "$input" | (read -r header; echo "$header"; sort -t',' -k6 -gr)
```

## Best practices
- Always store the raw R/I/C/E inputs alongside the score; the score alone is unauditable.
- Cap Confidence at 80% unless there is shipped data on the same surface — 100% is almost always wrong.
- Re-score a feature the moment its prerequisite assumption is invalidated, not at the next quarterly cycle.
- Keep the impact scale (3 / 2 / 1 / 0.5 / 0.25) — adding intermediate values destroys cross-feature comparability.
- Pair RICE with strategic veto: top-3 by score, then PM picks one strategic bet that may rank lower.
- Track post-ship actuals (real reach, real effort) to calibrate next quarter's estimates — this is the only way confidence improves.

## AI-agent gotchas
- LLMs are confident bullshitters about Reach. Force a citation: every Reach value must reference a query, dashboard, or proxy metric, otherwise the agent fabricates numbers that look plausible.
- Effort estimation from an LLM with no access to the codebase is noise. Either feed it `cloc` output and a dependency graph, or have a human engineer fill that column.
- An agent will happily score 50 features in one pass; quality drops sharply after ~10. Batch in chunks of 8-10.
- The model anchors on the first feature it scores. Randomize order per pass and average two passes.
- Human-in-loop checkpoint #1: before any feature with score >2× the median is committed to roadmap, a human must validate Reach and Effort. These are the highest-leverage error sources.
- Human-in-loop checkpoint #2: any feature where the agent assigned Impact = 3 must be co-signed — Impact=3 is reserved for differentiators.
- Don't let the agent re-score retroactively to "explain" why a shipped feature succeeded; that destroys the calibration data.

## References
- Sean McBride / Intercom — original RICE writeup: https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers/
- Roman Pichler, "Strategize" (2nd ed., 2022) — Ch. 6 on prioritization frameworks.
- Productboard's RICE field reference: https://www.productboard.com/glossary/rice-scoring-model/
- Lenny Rachitsky — "How the best PMs prioritize": https://www.lennysnewsletter.com/p/how-the-best-product-managers-prioritize
