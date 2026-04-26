# Agent Integration — AI in Project Management

## When to use
- Assessing where AI can reduce PM overhead in an existing project workflow (risk management, task automation, schedule optimization)
- Implementing PMBOK 8 AI appendix guidance: documenting AI-assisted decisions, establishing human oversight gates
- Detecting bottleneck shifts caused by AI productivity gains at the individual level that haven't translated to org-level delivery improvements (DORA 2025 paradox)
- Building AI-assisted risk identification and probability forecasting into a project's health monitoring system
- Establishing team AI literacy baselines before rolling out AI PM tools

## When NOT to use
- As justification for removing human PM oversight — PMBOK 8 explicitly requires human control for AI-assisted decisions
- When the project is a one-person, short-duration task where PM overhead exceeds coordination benefit
- For projects in regulated industries (medical devices, aerospace) where AI decision documentation requirements are not yet established in the compliance framework
- When the team has not established baseline metrics — AI optimization without baseline measurement cannot demonstrate improvement

## Where it fails / limitations
- The "AI productivity paradox": AI tools boost individual output metrics (21% more tasks completed, 98% more PRs merged) while organizational delivery metrics stay flat because bottlenecks shift to review, integration, and deployment phases (DORA 2025)
- AI risk prediction accuracy (96% claimed by some vendors) applies to specific use cases with sufficient historical data — generalizing to novel projects is unreliable
- AI schedule optimization tools cannot account for human factors (team morale, tacit knowledge dependencies, key person risk) without explicit input
- Resource capacity forecasting AI requires integration with actual time-tracking data — most organizations have poor time-tracking hygiene, which degrades prediction quality
- PMBOK 8 ethical guidance on AI use in PM is principles-based, not prescriptive — implementation requires organizational judgment calls

## Agentic workflow
Claude subagents support AI-in-PM workflows at two levels: decision support (risk analysis, status summarization, bottleneck detection) and execution (automated status updates, meeting summary → action items, sprint report generation). For risk management, an agent reads project status data from the PM tool API, identifies tasks with overdue dependencies, and generates a risk report with probability scores based on historical patterns. Human review of all risk assessments and resource decisions is mandatory before action. The agent records AI-assisted decisions in the project audit log to comply with PMBOK 8 traceability requirements.

### Recommended subagents
- general Bash/HTTP subagent — PM tool API reads for project health data
- `faion` — load pm/project-manager methodology for risk matrix and reporting templates
- `faion-sdd-execution` — quality gate before AI-generated plans are handed to engineering teams

### Prompt pattern
```xml
<task>Generate a project health report with risk assessment.</task>
<project_data>
  <open_issues>{{count}}</open_issues>
  <overdue_tasks>{{list}}</overdue_tasks>
  <blockers>{{list}}</blockers>
  <team_capacity>{{available_hours_this_week}}</team_capacity>
  <deadline>{{target_date}}</deadline>
</project_data>
<output>
  1. RAG status (Red/Amber/Green) with justification
  2. Top 3 risks with probability (High/Medium/Low) and impact
  3. Recommended mitigation for each risk
  4. Flag: are any risks beyond human PM authority to resolve?
</output>
<constraint>Mark all AI-generated risk scores as "AI-estimated" for audit log purposes.</constraint>
```

```xml
<task>Detect bottleneck shifts from this sprint velocity data.</task>
<data>{{sprint_history_json}}</data>
<check>
  Compare individual task completion rate vs. deployment frequency.
  If individual velocity is high but deployment frequency is low,
  identify the phase where work is accumulating (review, staging, QA, deploy).
</check>
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `jira-cli` | Fetch sprint data, open issues, overdue tasks | https://github.com/ankitpokhrel/jira-cli |
| `gh` (GitHub CLI) | Pull request throughput, review cycle time | `apt install gh` / https://cli.github.com/ |
| `linear-cli` | Linear project health queries | https://github.com/linearapp/linear |
| `curl` + `jq` | PM tool REST/GraphQL API calls for health data | system packages |
| `python` + `pandas` | Burn-down analysis, velocity trend calculation | `pip install pandas` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Jira + Atlassian Intelligence | SaaS | Partial | Risk prediction not API-exposed; use standard API for metrics extraction |
| Wrike | SaaS | Partial — REST API | ML risk prediction data viewable in UI but limited API exposure |
| Forecast App | SaaS | Yes — API | Resource matching and project insights available via REST API |
| Epicflow | SaaS | No | Bottleneck detection UI only; no public API |
| DORA Metrics tooling (Faros, LinearB) | SaaS | Yes — API | Deployment frequency, lead time, change failure rate — essential for paradox detection |
| Google Looker Studio | SaaS | Partial | PM data visualization; agent can push data via API connectors |

## Templates & scripts
See `templates.md` for risk matrix and project health report templates.

DORA metrics collector (deployment frequency check):
```bash
#!/bin/bash
# Count deployments in last 30 days from GitHub releases
REPO="${1:?Usage: $0 <owner/repo>}"
THIRTY_DAYS_AGO=$(date -d '30 days ago' --iso-8601=seconds)

gh api "repos/$REPO/releases" \
  --jq "[.[] | select(.created_at > \"$THIRTY_DAYS_AGO\")] | length" \
  --paginate | paste -sd+ | bc

echo " deployments in last 30 days"
```

## Best practices
- Measure end-to-end flow time (idea to production), not just individual task velocity — the AI productivity paradox is invisible when you only measure individual output
- Document every AI-assisted decision in the project log with the format: "AI suggested [X] based on [data]; human PM approved/modified/rejected because [reason]" — this is the PMBOK 8 traceability requirement
- Start AI integration with low-risk, high-value use cases: status report generation, meeting summary to action items, overdue task alerts — these have clear output and easy human verification
- Build team AI literacy incrementally; resistance to AI PM tools often stems from fear of surveillance rather than AI skepticism
- Monitor for ethical AI use: AI scheduling and resource allocation tools must not be used to enforce surveillance-style productivity monitoring without explicit team consent
- Validate AI risk predictions against actual outcomes quarterly and retrain or adjust confidence levels based on prediction accuracy

## AI-agent gotchas
- Agents generating risk assessments from project data will produce confident-sounding probability scores even when data is insufficient — always label AI risk scores as "estimated" and require human validation
- AI-generated status reports from PM tool data can misrepresent project health if the underlying data is stale or incomplete — agents must check data freshness before generating reports
- PMBOK 8 requires "human oversight for decisions" — agents must be configured to surface decisions for human approval rather than acting autonomously on project management actions (reassigning resources, closing issues, changing deadlines)
- The DORA metrics collector and similar tools measure software delivery, not project management effectiveness — conflating the two is a common mistake when interpreting AI PM tool outputs
- Agents cannot detect team morale, interpersonal conflicts, or burnout from project data — these are critical risk factors that only human observation can identify

## References
- https://dora.dev/research/2025/ — DORA 2025: AI productivity paradox, State of DevOps
- https://www.pmi.org/pmbok-guide-standards — PMBOK Guide 8th edition (AI appendix)
- https://developer.atlassian.com/cloud/jira/platform/rest/v3/ — Jira REST API
- https://cli.github.com/manual/ — GitHub CLI for DORA metrics extraction
- https://forecast.app/api — Forecast App REST API
- https://linearb.io/ — LinearB DORA metrics (engineering intelligence)
