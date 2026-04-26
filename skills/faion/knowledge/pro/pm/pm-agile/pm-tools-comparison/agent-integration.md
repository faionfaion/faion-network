# Agent Integration — PM Tools Comparison

## When to use
- Selecting an initial PM tool for a new team or product.
- Re-evaluating an existing tool when pain points (speed, cost, integrations) accumulate.
- Building an ADR for a board/leadership review with quantitative scoring.
- Mid-migration sanity check: confirm the chosen tool actually scores higher on what mattered.

## When NOT to use
- Single-person projects — overhead exceeds gain; pick whatever the user already has.
- When the org has a mandated tool (Jira via enterprise contract) and switching is not on the table.
- Hot fix / firefighting periods — tool selection should not be the response to delivery problems.

## Where it fails / limitations
- Scoring is anchor-biased: whichever tool the evaluator already knows scores higher.
- TCO calculations almost always under-estimate migration + custom-reporting cost.
- "Feature coverage" matrices ignore that 80% of value comes from 20% of features.
- 2-week PoCs are too short to surface scaling pain (Jira's slowness only appears at >10k issues).
- Vendor-stability risk hard to quantify; small tools can fold or pivot mid-contract.

## Agentic workflow
Use a Claude subagent to fill the scoring matrix from public data + the team's stated requirements, then render a draft ADR. Humans run the live PoC and only feed the agent measured scores (setup time, daily-flow time, satisfaction). Keep the agent away from the final recommendation — it's a synthesis assistant, not a decision-maker.

### Recommended subagents
- `faion-pm-agent` — produces the comparison matrix + ADR draft from research.
- General-purpose Claude subagent — runs the WebSearch sweep on each tool's pricing, integrations, recent changes.
- `faion-sdd-executor-agent` — once a tool is chosen, generates the migration task tree.

### Prompt pattern
```
For tools <A,B,C>, fill the scoring matrix in templates.md.
Score each cell 1–10 with one citation (URL or vendor doc).
Mark any cell where evidence is older than 12 months as STALE.
```

```
Given the matrix totals and our team's top 3 requirements (X,Y,Z),
draft an ADR recommending <tool>. Include: context, decision,
3 alternatives considered, key risks, migration effort estimate
in tokens (not days), and a 6-month review date.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh` | Compare GitHub Projects directly via CLI | `brew install gh` |
| `linear-cli` | Linear ops (issue export, automation) | https://github.com/evangodon/lr |
| `jira-cli` | Jira issue export, scripting | `brew install ankitpokhrel/jira-cli/jira-cli` |
| `glab` | GitLab Boards via CLI | `brew install glab` |
| `notion-cli` | Notion content export | `npm i -g notion-cli` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Jira | SaaS | REST + Webhooks | Most powerful; slow, complex permissions |
| Linear | SaaS | GraphQL + Webhooks | Fastest UX; smallest ecosystem |
| ClickUp | SaaS | REST | Most features; risk of bloat |
| GitHub Projects | SaaS | GraphQL (Projects v2) | Best when code+issues live together |
| GitLab Boards | SaaS/OSS | REST | Same, with self-host option |
| Azure DevOps Boards | SaaS | REST | Strong in regulated/Microsoft shops |
| Notion | SaaS | API | Better for docs+light tracking |
| Trello | SaaS | REST | Solo/small-team kanban |
| Asana | SaaS | REST | Marketing/cross-functional teams |

## Templates & scripts
See `templates.md` for the scoring matrix, evaluation scorecard, TCO calculator, and ADR. Inline weighted-score helper:

```python
#!/usr/bin/env python3
# weighted-score.py — compute weighted totals from a YAML scorecard.
import sys, yaml
data = yaml.safe_load(open(sys.argv[1]))
for tool, cats in data["tools"].items():
    total = sum(cats[c]["score"] * data["weights"][c] / 100 for c in cats)
    print(f"{tool}: {total:.2f}")
```

## Best practices
- Define the top 3 must-have requirements BEFORE looking at any tool — anchors the weights.
- Score from team-measured PoC data, not vendor marketing.
- Pre-commit to a reversible decision: "we'll re-evaluate in 6 months, here's the rollback plan."
- Cap evaluated tools at 4–5; more turns into analysis paralysis.
- Always include an "incumbent + zero-change" baseline as one of the options.
- Capture migration cost at item-count granularity (#issues, #automations, #integrations) before signing.

## AI-agent gotchas
- Agents tend to favor newer / more-mentioned-online tools (recency bias from training data).
- Pricing scraped from sites is frequently outdated; require live citations and check the URL date.
- Agents will hallucinate integrations that don't exist; require a vendor-docs URL per claimed integration.
- "Score 10/10" claims appear when the agent is anchored — force a forced-rank step (rank A>B>C, no ties).
- Do not let the agent run the comparison and write the recommendation in one prompt; separate steps.

## References
- ADR template: https://adr.github.io/
- Jira evaluation guides — Atlassian pricing pages.
- "Information Dashboard Design" by Stephen Few (for evaluating reporting strength).
- Linear "How we built Linear" engineering blog (vendor-stability data point).
- Gartner Magic Quadrant for Agile Planning Tools (annual).
