# Agent Integration — AI in Project Management

## When to use
- Project risk register needs automated scoring and trend analysis across sprint data
- Stakeholder reports require synthesis from multiple sources (Jira, GitHub, budget sheets)
- Schedule variance analysis must run continuously, not just at milestones
- Resource allocation decisions require capacity forecasting across 3+ team members
- Post-mortems need pattern extraction from historical project data

## When NOT to use
- Project has fewer than 3 people — overhead exceeds benefit
- Decisions carry legal or contractual weight — AI recommendations need full human sign-off with audit trail
- Team lacks baseline PM tooling (Jira/Linear/GitHub) — AI has nothing to feed on
- One-off, highly political decisions where stakeholder dynamics dominate data signals

## Where it fails / limitations
- The AI Productivity Paradox applies: AI boosts individual task velocity, but organizational throughput bottlenecks shift to review and deployment — flat delivery metrics persist
- AI risk scoring is only as good as the input data; stale or missing issue updates degrade accuracy significantly
- Schedule predictions drift when external dependencies (vendors, clients) are not tracked in the PM tool
- AI-generated summaries can obscure nuance — a "green" risk status may hide a critical qualitative flag only a human catches
- DORA 2025 shows 96% prediction accuracy requires clean, structured data pipelines — most teams don't have them

## Agentic workflow
A Claude subagent is well-suited to the data-aggregation and synthesis layer of AI-assisted PM: pull structured data from project APIs, run heuristic risk scoring, generate stakeholder digests, and surface anomalies. The agent should never trigger budget reallocations or deadline changes autonomously — those require a human-in-loop confirmation step. Pair a lightweight Haiku agent for routine weekly digest generation with a Sonnet agent for retrospective pattern analysis.

### Recommended subagents
- `faion-sdd-executor-agent` — executes structured SDD tasks including implementation plans; can synthesize task-level progress into a sprint summary
- Custom PM-digest agent — polls Jira/Linear API, computes schedule variance, generates Markdown report; runs on cron

### Prompt pattern
```
You are a project status analyst. Given the following sprint data (JSON):
<sprint_data>{{sprint_data}}</sprint_data>

1. Identify tasks that are behind schedule by >20%.
2. Flag any risks that appeared in the last 7 days.
3. Summarize in ≤200 words for a non-technical stakeholder.
Do not recommend actions — list findings only. A human will decide next steps.
```

```
Analyze this risk register and score each item Low/Medium/High based on:
- Days since last update
- Number of dependent tasks
- Owner response rate
Return JSON: [{id, score, reason}]
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `jira-cli` | Query Jira issues, sprints, boards from terminal | `brew install ankitpokhrel/tap/jira-cli` / github.com/ankitpokhrel/jira-cli |
| `gh` (GitHub CLI) | Pull PR/issue data into agent context | `brew install gh` / cli.github.com |
| `linear` CLI | Linear issue queries (no official CLI; use GraphQL API) | linear.app/docs/graphql |
| `gsheet-cli` | Read/write Google Sheets for budget tracking | github.com/lidaobing/gsheet-cli |
| `mlflow` CLI | Track ML experiment runs if AI models are embedded in delivery pipeline | pip install mlflow |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Jira | SaaS | Yes — REST API v3 | Rich sprint/issue data; webhook support for real-time triggers |
| Linear | SaaS | Yes — GraphQL API | Cleaner API than Jira; good for agent polling |
| GitHub Projects | SaaS | Yes — GraphQL | Useful when dev and PM tracking are unified |
| Notion | SaaS | Partial — REST API | Good for document synthesis; limited structured query |
| Microsoft Project | SaaS/Desktop | Partial — Graph API | Complex auth; useful if org is MS-centric |
| ProjectManager.com | SaaS | Yes — REST API | Predictive analytics built-in; agent can augment |
| Forecast.app | SaaS | Yes — REST API | AI-native PM tool; resource forecasting endpoint |
| Clockify | SaaS | Yes — REST API | Time-tracking data feeds resource capacity models |

## Templates & scripts
See templates.md for sprint digest template and risk register schema.

Inline: minimal risk-scoring script for agent use:
```python
import json, datetime

def score_risk(risk: dict) -> str:
    days_stale = (datetime.date.today() - datetime.date.fromisoformat(risk["last_updated"])).days
    dep_count = risk.get("dependent_tasks", 0)
    if days_stale > 14 or dep_count > 5:
        return "High"
    if days_stale > 7 or dep_count > 2:
        return "Medium"
    return "Low"

risks = json.load(open("risks.json"))
for r in risks:
    r["score"] = score_risk(r)
print(json.dumps(risks, indent=2))
```

## Best practices
- Feed AI only structured, timestamped data — free-text PM notes produce low-quality signals
- Maintain a human decision log separate from AI recommendations; regulatory audits require it
- Run AI risk scoring weekly, not per-commit — daily runs amplify noise
- Validate AI schedule predictions against actuals for at least 3 sprints before trusting them in stakeholder reports
- Use Value Stream Mapping alongside AI tooling to locate post-AI bottlenecks (review, deploy) — the productivity paradox is real
- Scope AI automation to observation and synthesis; keep action triggers human-initiated
- Document each AI-assisted decision with the model version, input data hash, and reviewer name

## AI-agent gotchas
- API rate limits on Jira/Linear can silently truncate data — always log the record count fetched vs. expected
- LLMs hallucinate task IDs and dates when context is long; always validate against source system before including in reports
- An agent that auto-closes risks or auto-updates status fields can corrupt the PM system state — gate all writes behind a confirmation prompt
- Sprint boundary detection is tricky: if the agent runs mid-sprint, partial data skews velocity calculations — timestamp-gate queries
- Stakeholder digest tone varies by model version — pin the model; a Haiku upgrade can change summary style noticeably

## References
- PMI AI in Project Management report 2024 — pmi.org
- DORA 2025 State of DevOps Report — dora.dev
- PMBOK Guide 8th Edition — pmi.org/pmbok-guide-standards
- "AI Productivity Paradox" — Google DORA research, 2025
- Forecast.app AI PM benchmarks — forecast.app/blog
