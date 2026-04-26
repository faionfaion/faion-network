# Agent Integration — Feature Discovery

## When to use
- Pre-roadmap planning when feature backlog has more than ~30 candidates and effort/impact is unclear.
- After a noticeable churn or activation drop, to prioritize between fixing existing flows and adding new capability.
- When stakeholders push competing feature requests and you need a defensible ranking (RICE / Kano / ODI).
- When validating a new feature idea before committing engineering — fake-door, prototype, or wizard-of-oz.

## When NOT to use
- Pre-PMF: ignore feature discovery and run problem-validation first; you don't have a stable user base to score reach against.
- Single-feature decisions where the cost of building is smaller than the cost of running RICE.
- When you already have <5 features in scope; prioritization overhead exceeds value.
- When telemetry is missing — RICE on guessed Reach is theatrical.

## Where it fails / limitations
- RICE confidence numbers (50/80/100%) become noise without a written rubric — agents will fabricate plausible scores.
- Kano survey requires N≥30 paying users; below that, classification is unreliable.
- Opportunity Scoring (ODI) needs paired importance + satisfaction questions on the same respondents — splitting them invalidates the math.
- Discovery from support tickets over-weights vocal users; weight by ARR or segment.
- Competitor feature parity is not a real signal — copying without understanding the underlying job leads to bloat.

## Agentic workflow
Drive feature discovery as a four-stage pipeline: collect (analytics/tickets/interviews), categorize (Kano), score (RICE+ODI), validate (fake-door/prototype). Each stage is a separate subagent run with structured-output JSON so the next stage can consume it. Keep the human in the loop at two checkpoints: confidence values before RICE, and the validation method choice. Persist the feature-request log as a single markdown table the agent can append to over weeks.

### Recommended subagents
- `faion-sdd-executor-agent` — drive the discovery board template through SDD lifecycle and emit structured outputs per step.
- `nero-sdd-executor-agent` — same workflow inside NERO context for internal tooling features.
- A custom `feature-discovery-analyst` subagent (sonnet) for ticket clustering and pattern extraction; haiku for filling RICE rows once Reach/Effort are pinned by humans.

### Prompt pattern
```
Role: feature-discovery-analyst.
Input: support_tickets.jsonl (1k rows), analytics_summary.md, interviews.md.
Task: cluster tickets by underlying job; output JSON {clusters:[{job, count, severity, sample_ticket_ids}]}.
Constraint: do not propose solutions, only surface jobs. Min cluster size: 5 tickets.
```

```
Role: rice-scorer.
Input: candidate_features.json (with confirmed Reach + Effort), product context.
Task: assign Impact (0.25/0.5/1/2/3) and Confidence (50/80/100); output JSON with rationale per row.
Constraint: cite a metric or interview quote per row; refuse to score without evidence.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh` | Pull GitHub issues/discussions as feature-request input | https://cli.github.com |
| `linear-cli` | Export Linear issues to JSON for clustering | https://github.com/evangodon/linear-cli |
| `jq` | Slice analytics dumps; group ticket exports by tag | https://jqlang.github.io/jq/ |
| `posthog` CLI / API | Pull funnel + feature-flag adoption data | https://posthog.com/docs/api |
| `mixpanel-api` | Cohort + retention pulls for Reach estimation | https://developer.mixpanel.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| ProductBoard | SaaS | Yes (REST API) | Native feature backlog + RICE; agent can sync ideas in/out. |
| Productlift | SaaS | Yes (API) | Public roadmap + voting; agent reads vote counts as Reach proxy. |
| Canny | SaaS | Yes (API + webhooks) | Aggregates feature requests by user segment and ARR weight. |
| Aha! | SaaS | Partial (REST API, rate-limited) | Strong on Kano + scorecards; clunky for high-frequency agent writes. |
| Savio | SaaS | Yes (API) | B2B feedback aggregation; pulls Intercom/Slack/HubSpot. |
| PostHog | OSS+Cloud | Yes (API) | Feature flags for fake-door tests + cohort Reach. |
| Statsig | SaaS | Yes (API) | A/B + holdout for prototype validation. |
| Maze | SaaS | Yes (API) | Prototype + tree tests; agent can pull conversion. |

## Templates & scripts
See `templates.md` for Feature Discovery Board, Feature Request Log, RICE table.

Inline RICE scorer (Python, ≤50 lines):
```python
import csv, sys
# rows: feature, reach, impact, confidence, effort
with open(sys.argv[1]) as f:
    rows = list(csv.DictReader(f))
scored = []
for r in rows:
    reach = float(r["reach"])
    impact = float(r["impact"])
    conf = float(r["confidence"]) / 100
    effort = max(float(r["effort"]), 0.1)
    rice = (reach * impact * conf) / effort
    scored.append((r["feature"], round(rice, 1)))
scored.sort(key=lambda x: -x[1])
for name, score in scored:
    print(f"{score:>8}  {name}")
```

## Best practices
- Lock the Effort estimate via a separate eng-only review BEFORE the agent runs RICE; otherwise eng inflates effort to kill features they dislike.
- Reach must come from telemetry, not interviews. If you cannot measure it, drop the feature back to discovery.
- Validate top-3 RICE features with fake-door before committing — empirical CTR beats Confidence%.
- Run Kano per segment, not on the whole base — the same feature is a Must-have for one segment and Indifferent for another.
- Keep the discovery board immutable per quarter; new ideas wait for next cycle. Prevents agent thrash on re-scoring.
- Track "Rejected" with reason — saves re-litigating the same idea every quarter.

## AI-agent gotchas
- LLMs hallucinate Reach values when telemetry is missing. Force `null` Reach when there's no source link in the row.
- Agents will collapse distinct jobs ("export PDF" + "share PDF") into one cluster. Require sample IDs per cluster so a human can audit.
- Confidence% is the most-faked field; require a citation (interview ID, metric URL) per Confidence>=80.
- Kano classification from LLM-only data is unreliable; use it for shortlisting but require survey data for the final call.
- Opus-grade trade-off reasoning is wasted on filling in the RICE table; reserve it for "which segment do we cut" decisions.
- Human-in-loop checkpoints: (1) cluster review before scoring, (2) Effort sign-off, (3) validation method per top feature.

## References
- Sean McBride, "RICE: Simple prioritization for product managers" — Intercom blog.
- Anthony Ulwick, "What Customers Want" (Outcome-Driven Innovation / ODI).
- Noriaki Kano, "Attractive quality and must-be quality" (1984).
- Marty Cagan, "Inspired" (chapters 18-22 on discovery).
- Teresa Torres, "Continuous Discovery Habits" (opportunity solution trees).
