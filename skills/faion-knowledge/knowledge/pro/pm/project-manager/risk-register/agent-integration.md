# Agent Integration — Risk Register

## When to use
- Standing up a new project's uncertainty domain artefact: identify, score, plan, assign, track.
- Weekly risk review: agent diffs the live register against telemetry (issue tracker, monitoring, schedule) and proposes additions / status changes.
- Pre-gate / steering-committee snapshot: top-N risks with response status, drives the readiness decision.
- Vendor / supplier onboarding: replicate the register pattern with category=External and contract clauses as triggers.
- Solopreneur "what would kill this project" ritual at every milestone — a 10-row register beats a 0-row one.

## When NOT to use
- Pure-Scrum teams that already track risks as backlog items / "risks-and-impediments" board — duplicating here splits attention.
- Tasks of < 1 week with one owner: a cycle of "what could go wrong before Friday" in standup is enough.
- Pre-discovery / R&D where uncertainty *is* the work; you want a learning log, not a risk register.
- Risks that map to existing controls (security, GDPR) already managed in a separate risk system; do not reinvent.

## Where it fails / limitations
- Probability and impact are notoriously biased; LLMs anchor on the user's framing and produce overconfident scores.
- 5×5 matrix gives a false sense of precision — risk score 12 vs 15 is mostly noise, but it drives prioritisation.
- "Accept" is over-used by both humans and agents to clear the register without doing real work.
- Static registers go stale fast; the methodology ages well only with weekly review.
- Positive risks (opportunities) are routinely dropped; agents focus on threats by default.
- Triggers / leading indicators are vague ("if customer is unhappy"); agents need concrete sensors (NPS drop, ticket volume, missed milestone).
- Risks without a single owner are not managed — they are observed.

## Agentic workflow
Two-phase. Phase 1: a `risk-identifier` reads the project context (charter, WBS, stakeholder register, recent incidents) and brainstorms candidate risks in each PMBoK category, with explicit triggers and owners. Phase 2: a `risk-scorer` assigns probability × impact with rationale and proposes a strategy + response plan. Human review between phases. Weekly the agent diffs telemetry against the register and emits a CHANGES file (new risks, escalations, closures).

### Recommended subagents
- `risk-identifier` (define inline) — input: project artefacts; output: candidate risks YAML.
- `risk-scorer` (define inline) — input: candidate risks; output: scored risks with strategy + response.
- `risk-monitor` (define inline) — input: live register + telemetry feeds; output: CHANGES.md with deltas.
- `faion-brainstorm` — for the initial threat / opportunity list when context is thin.
- `faion-sdd-executor` — once a mitigation becomes a code task, drives implementation through quality gates.

### Prompt pattern
```
You are scoring project risks against PMBoK risk taxonomy.
For each candidate risk emit:
{ "id": "R-XX",
  "title": "...",
  "category": "Technical|External|Organizational|PM",
  "probability": "VL|L|M|H|VH",
  "impact":      "VL|L|M|H|VH",
  "score": int,                # P*I on 1-25 scale
  "strategy": "Avoid|Transfer|Mitigate|Accept|Exploit|Share|Enhance",
  "response_plan": "imperative sentence",
  "trigger": "concrete observable signal",
  "owner": "name or UNASSIGNED",
  "is_opportunity": bool,
  "rationale": "≤2 sentences" }
Constraints:
- "Accept" requires a contingency_amount or contingency_plan.
- Trigger must be observable (metric, event, date), not subjective.
- Owners cannot be "the team" — name an individual.
- Always include at least 1 opportunity per 10 risks.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `yq` | Validate / mutate risk-register YAML in CI | https://github.com/mikefarah/yq |
| `jq` | Filter / query risk JSON for dashboards | https://stedolan.github.io/jq/ |
| `pandoc` | Render risk register markdown → DOCX / PDF | https://pandoc.org/ |
| `mermaid-cli` | Render heatmap or risk-network diagrams | https://github.com/mermaid-js/mermaid-cli |
| `montecarlo-cli` (`mcli`) | Monte Carlo on risk-driven contingency reserves | https://github.com/cetra3/mcli |
| `gh` / `jira-cli` / `linear` | Sync risks ↔ issues for tracking | https://cli.github.com/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Jira (Risk Management plugins, e.g. Risk Register for Jira) | SaaS | Yes — REST | Risks as issues, custom fields for P/I |
| Smartsheet | SaaS | Yes — REST | Pre-built risk register templates |
| Monday.com | SaaS | Yes — GraphQL | Risk boards with automations |
| ClickUp | SaaS | Yes — REST | Custom-field heatmap |
| Risk Management Studio | SaaS | Partial — REST | ISO 31000 aligned tooling |
| Active Risk Manager | SaaS | Partial | Enterprise / regulated industry |
| Notion | SaaS | Yes — REST | Lightweight register; good for solopreneur |
| Power BI / Tableau | SaaS | Yes — SQL | Cross-portfolio heatmaps and trends |

## Templates & scripts
See `templates.md` for the register and risk-card markdown. Inline scorer + heatmap (Python, ≤50 lines):

```python
#!/usr/bin/env python3
"""Validate a risk register YAML and emit a heatmap markdown."""
import sys, yaml
LEVELS = {"VL": 1, "L": 2, "M": 3, "H": 4, "VH": 5}
def main(path):
    risks = yaml.safe_load(open(path))["risks"]
    grid = [[[] for _ in range(5)] for _ in range(5)]
    for r in risks:
        p = LEVELS[r["probability"]] - 1
        i = LEVELS[r["impact"]]      - 1
        s = (p + 1) * (i + 1)
        if s != r.get("score"):
            sys.exit(f"score mismatch on {r['id']}: stored {r.get('score')} computed {s}")
        if r["strategy"] == "Accept" and not (r.get("contingency_amount")
                                              or r.get("contingency_plan")):
            sys.exit(f"{r['id']}: Accept without contingency")
        grid[i][p].append(r["id"])
    print("| P\\I | VL | L | M | H | VH |")
    print("|-----|----|---|---|---|----|")
    for pi, row in enumerate(grid):
        cells = " | ".join(",".join(c) or "-" for c in row)
        print(f"| {list(LEVELS.keys())[pi]} | {cells} |")
if __name__ == "__main__":
    main(sys.argv[1])
```

## Best practices
- Every risk has exactly one named owner; never "the team".
- Triggers must be observable (metric, log event, date); reject "if it gets bad".
- Calibrate P/I scales with at least one historical reference: e.g. "H impact = > $50k or > 1 month delay".
- Risk-driven contingency: sum (P × I × cost) for open risks; beats flat 15% reserve.
- Weekly review is a ritual, not optional; missed weeks → register goes stale.
- Track top-5 risks at every steering committee; if the same five appear month after month, the responses are not working.
- Capture opportunities (positive risks) — sponsor approval rates rise when you show upside.
- For agile teams, surface high-score risks into the sprint backlog as risk-mitigation stories.

## AI-agent gotchas
- LLMs love brainstorming risks but score them all "Medium / Medium" — force a normal-ish distribution and reject outputs where > 70% are M/M.
- "Communication breakdown" appears in 90% of LLM-generated registers — treat as a smell and replace with project-specific risks.
- Agents drop opportunities; require a positive-risk quota.
- Triggers default to "if it happens" — strip and require concrete signals.
- Currency / units missing on impact ("major" with no $ or days); force a `quantitative_impact` field.
- "Accept" gets used as a junk drawer; require contingency on every Accept.
- LLMs invent risk-management ISO codes; verify any cited standard.
- For very large registers (> 50 risks), context windows truncate — chunk by category and stitch.

## References
- PMI — Practice Standard for Project Risk Management: https://www.pmi.org/standards/risk
- PMI — A Guide to the PMBOK 7th Edition, Uncertainty Performance Domain: https://www.pmi.org/standards/pmbok
- ISO 31000 — Risk Management Guidelines: https://www.iso.org/iso-31000-risk-management.html
- COSO ERM — Enterprise Risk Management framework: https://www.coso.org/
- Douglas Hubbard — "The Failure of Risk Management" (2009)
- Steve McConnell — "Software Estimation: Demystifying the Black Art" (chapters on uncertainty)
- Risk Doctor (David Hillson) — https://www.risk-doctor.com/
