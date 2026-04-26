# Agent Integration — Risk Management

## When to use
- Multi-month delivery where surprises cost real money (>$10k or >2 weeks).
- Regulated, safety-critical, or contractual work where audit trail is required.
- Cross-team programs with technical, vendor, and resource interdependencies.
- Initiatives where a quantitative reserve (contingency) must be defended to finance.

## When NOT to use
- Pure exploratory R&D / spike work — fail-fast learning beats register hygiene.
- Single-developer hobby project; an issue tracker `risk` label is enough.
- Sub-2-week features where ceremony cost > expected loss.
- Pure-Scrum teams already running impediment + retro loops with adequate coverage.

## Where it fails / limitations
- Probability×Impact scoring is anchoring-prone; teams converge on "Medium" defaults and lose discrimination.
- EMV summed without correlation overstates contingency for correlated risks.
- "Set-and-forget" registers stale within 2-3 sprints; without trigger reviews the doc is theatre.
- Black-swan / unknown-unknown events are by definition outside the register.
- Opportunity-side risks are systematically under-managed — most teams only log threats.

## Agentic workflow
A Claude subagent works well for the mechanical parts of risk hygiene: extracting candidate risks from project artefacts, normalizing entries, detecting drift between register and reality, and drafting response plans. The human PM keeps ownership of probability/impact judgement, EMV defensibility, and Change-Control-Board escalations. Run the agent on a weekly cadence against the live register (Markdown, Jira, or Notion) and surface a delta diff for human review — never let the agent silently mutate scores.

### Recommended subagents
- `faion-pm-agent` (declared in README front-matter) — owns the methodology; drafts register entries from charter, scope, and meeting notes.
- `faion-sdd-execution` quality-gate agent — feed it the register so AC reviews check for risk coverage.
- `faion-brainstorm` diverge/converge — run a "what could go wrong" diverge round at kickoff and at each phase gate.

### Prompt pattern
```
You are a risk-identification assistant. Read the attached charter + WBS.
Output JSON: [{id, category, description, probability(VL/L/M/H/VH),
impact(VL/L/M/H/VH), trigger, suggested_strategy, rationale}].
Mark every score with a one-line rationale citing source text.
Do NOT invent owners. Flag any risk with score >=15 as "needs_review=true".
```

```
Diff the prior register vs the current one. Output: NEW, CHANGED_SCORE,
CLOSED, STALE (>14 days no update). Never mutate fields — emit the diff only.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pmbok-risk-register` (Excel/CSV templates from PMI) | Canonical register layout | https://www.pmi.org |
| `riskman` (npm) | Markdown-driven risk register with CLI scoring | https://www.npmjs.com/package/riskman |
| `risk-cli` (Python) | Monte Carlo on EMV inputs | `pipx install risk-cli` |
| `jira` CLI (`go-jira`, `jira-cli`) | Sync risks as issues with `risk` issue-type | https://github.com/ankitpokhrel/jira-cli |
| `gh` CLI | Sync risks as labelled issues for solo/light projects | https://cli.github.com |
| `pandoc` | Render `risks.md` to PDF for steering reports | https://pandoc.org |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Jira (Risk Management for Jira, RMsis) | SaaS | Yes — REST API + JQL | First-class risk issue type, P×I custom fields. |
| Monday.com risk template | SaaS | Yes — GraphQL API | Easy for non-PMOs; weak EMV math. |
| Smartsheet RAID log | SaaS | Yes — REST API | Strong for regulated/PMO orgs. |
| Notion + database | SaaS | Yes — REST API | Best for solo/small; agent can fully drive it. |
| @riskmgmt/risk-register (OSS, GitHub) | OSS | Yes — Markdown | Fits SDD repos; diff-friendly. |
| Palisade @RISK / ModelRisk | Desktop | Limited | Quantitative Monte Carlo when EMV alone underflows. |
| ServiceNow GRC | Enterprise SaaS | Yes — REST API | Heavyweight; only for regulated programs. |

## Templates & scripts
See `templates.md` for register and response-plan layouts. Minimal helper to compute EMV and flag P×I crit cells:

```python
# emv.py — score a Markdown risk register, exit non-zero on critical untriaged risks.
import re, sys, pathlib
P = {"VL":0.05,"L":0.20,"M":0.40,"H":0.60,"VH":0.85}
I = {"VL":0.025,"L":0.075,"M":0.15,"H":0.30,"VH":0.50}
text = pathlib.Path(sys.argv[1]).read_text()
crit = []
for row in re.findall(r"\|\s*(R-\d+)\s*\|.*?\|\s*([A-Z]{1,2})\s*\|\s*([A-Z]{1,2})\s*\|", text):
    rid, p, i = row
    if p in P and i in I:
        score = P[p]*I[i]
        if score >= 0.15:
            crit.append((rid, score))
sys.exit(1 if crit else 0)
```

## Best practices
- Pair every risk with a trigger condition you can observe (metric, calendar event, signal) — risks without triggers are wishes.
- Calibrate the team once per quarter on probability buckets using base-rate exercises; otherwise everyone defaults to "Medium".
- Track opportunity risks in the same register, color-coded — forces parity of attention.
- Roll EMV into a single contingency line, not per-risk reserves; finance only funds aggregates.
- Keep the top-5 risks visible on the status report; everything else goes in the appendix.
- Close risks explicitly with outcome ("materialized", "passed", "merged into R-XX") — never delete.

## AI-agent gotchas
- Agents will happily auto-score every risk Medium-Medium; require explicit rationale per score in the output schema.
- LLMs hallucinate plausible-but-wrong risk owners — leave `owner` blank and have a human assign.
- Agent-generated registers tend toward generic ("vendor delay", "scope creep"); seed with project-specific artefacts (charter, ADRs, vendor SOWs) before running.
- Don't let the agent close risks autonomously; require human signoff because closure has audit consequences.
- Token budget: a 50-risk register is ~3-5k tokens; reading it on every turn wastes context. Pass only the top-N by score plus changed rows.
- Human-in-loop checkpoints: (1) initial calibration, (2) any score change >= 2 levels, (3) any new "High/Crit" entry, (4) any contingency-budget impact.

## References
- PMI, *PMBOK Guide* 7th ed., Uncertainty Performance Domain.
- ISO 31000:2018 — Risk management guidelines.
- D. Hubbard, *The Failure of Risk Management* (2009) — on why P×I matrices mislead.
- D. Vose, *Risk Analysis: A Quantitative Guide* (3rd ed.).
