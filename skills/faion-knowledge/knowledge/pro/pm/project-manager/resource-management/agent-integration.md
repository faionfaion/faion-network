# Agent Integration — Resource Management

## When to use
- Multi-team programs where same engineers are claimed by 2+ projects
- Onboarding/offboarding wave that shifts skill mix in 30-60 days
- Agency/consulting context billing by utilization
- Mid-project resource crisis (key person quit, contractor delayed)
- Capacity planning ahead of quarterly OKR commitments

## When NOT to use
- Stable single team < 8 people — informal allocation works, formal plans add overhead
- Pure agile teams committed to whole-team ownership — utilization tracking erodes psychological safety
- One-week sprint of throwaway research — over-planning waste
- When the org culture treats utilization % as a performance metric (creates burnout, gaming)

## Where it fails / limitations
- 100% utilization plans always slip; ignoring slack is the #1 failure mode
- Skill matrices encoded once go stale fast; people grow, you do not re-survey
- Resource leveling assumes interchangeable engineers — false for staff-level / specialist roles
- Static plans collapse on first holiday or sick week
- Rate cards mix billable/cost rates, leading to wrong CPI in EVM
- Agency utilization games: marking internal training as "non-billable busy" hides bench time

## Agentic workflow
A capacity-planner subagent ingests calendars (PTO, holidays), current Jira/Linear assignments, and skill tags from an HR system; produces a weekly availability matrix capped at 75% effective capacity. A second leveling agent compares demand (committed work) vs supply, surfaces overload weeks, and proposes options (delay, split, add, cut scope). Human PM picks; agent updates plan and notifies affected leads. Re-runs weekly on cron.

### Recommended subagents
- `capacity-planner` — pulls PTO, ceremonies, current load → effective capacity per person/week
- `skill-matcher` — matches required skills (from WBS) to people with skill-level scoring
- `leveler` — detects overload, proposes mitigations with cost impact
- `utilization-monitor` — weekly delta vs plan, flags drift > 15%

### Prompt pattern
```
You are a capacity-planner. Given calendar events {ical}, sprint commitments
{jira_issues}, recurring meetings {meetings}, return per-person weekly hours
available for project work. Cap at 32h/week (80% of 40). Subtract:
- PTO/holidays (full)
- Recurring meetings (sum)
- Reserve 4h/week for "interruption buffer"
Output JSON {person, week, available_h, committed_h, free_h}.
```

```
You are a skill-matcher. Given task {task} requiring {skills} at {level},
return ranked candidates from {team_roster.yaml}. Score = skill_match * 0.6
+ availability * 0.3 + cost_fit * 0.1. Reject < 0.5.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gcalcli` | Read Google Calendar events for capacity | https://github.com/insanum/gcalcli |
| `khal` | CalDAV calendar queries | https://github.com/pimutils/khal |
| `jira` (CLI) | Pull current assignments + estimates | https://github.com/ankitpokhrel/jira-cli |
| `linear-cli` | Linear capacity/load by user | npm |
| `tempo` (Jira plugin API) | Worklog + capacity | https://apidocs.tempo.io |
| `harvest` API | Time tracking + capacity | https://help.getharvest.com/api-v2 |
| `clockify` API | Free time tracking | https://docs.clockify.me/api |
| `bamboohr` API | HR data, PTO, headcount | https://documentation.bamboohr.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Float | SaaS | Yes | Resource scheduling, REST API |
| Resource Guru | SaaS | Yes | Bookings + leave, REST API |
| Forecast.it | SaaS | Yes | AI scheduling, GraphQL |
| Runn | SaaS | Yes | Capacity planning, rich API |
| Tempo Planner | SaaS (Jira) | Partial | Jira-tied, plugin permissioning |
| Smartsheet | SaaS | Yes | Resource view + API |
| Microsoft Project for Web | SaaS | Yes | Graph API, Azure AD |
| OpenProject | OSS | Yes | Self-host, REST API, Gantt |
| Toggl Plan | SaaS | Yes | Lightweight planning + API |

## Templates & scripts
See templates.md for resource plan and request form. Inline capacity calc:

```python
# capacity.py — effective hours per person per week
from datetime import date, timedelta
import yaml, json
roster = yaml.safe_load(open("roster.yaml"))   # {alice: {hours_week: 40, role: be}}
pto = yaml.safe_load(open("pto.yaml"))         # {alice: ["2025-06-10", ...]}
meetings = yaml.safe_load(open("meetings.yaml"))  # {alice: 6}  weekly hours
BUFFER, EFFECTIVE = 4, 0.80
def week_hours(person, monday):
    days_off = sum(1 for d in [monday + timedelta(i) for i in range(5)]
                   if d.isoformat() in pto.get(person, []))
    base = roster[person]["hours_week"] * (5 - days_off) / 5
    return max(0, base * EFFECTIVE - meetings.get(person, 0) - BUFFER)
out = {p: week_hours(p, date.fromisoformat("2025-06-09")) for p in roster}
print(json.dumps(out, indent=2))
```

## Best practices
- Plan to 75-80% effective capacity, never 100% — meetings + interruptions burn 20%+
- Track skills with three levels (learning, proficient, mentor) and last-used date
- Cross-train one backup per critical skill; bus factor < 2 is a P1 risk
- Keep a "stretch bench" — people with 10-20% slack who can absorb spikes
- For contractors, bake in 2-week ramp-up at 50% productivity, not 100% from day 1
- Resource plan must reconcile to schedule (CPM) and budget (EVM); update all three together
- Surface utilization with trend, not snapshot — point-in-time leads to harassment

## AI-agent gotchas
- Calendar APIs miss informal meetings, pair sessions, debugging deep dives — always ask owner to confirm
- Skill self-assessments inflate; use last-shipped-feature as ground truth
- Allocation agents will pack the calendar to 100% if uncapped; hard-cap at 80% effective
- Pulling PTO from HR systems often hits permissioning issues; have a fallback "ask the EM" loop
- Auto-rebalancing sounds good until it reassigns work mid-sprint and breaks WIP — schedule rebalance only at sprint boundary
- Hourly-rate fields in HR systems mix loaded/unloaded cost; document which one EVM uses
- Privacy: agents reading calendars expose meeting subjects with sensitive titles ("layoff prep") — redact subject lines before LLM input

## References
- PMBoK 7th: Team Performance Domain
- DeMarco & Lister, *Peopleware* (slack chapter)
- Allen Ward, *Lean Product and Process Development* (capacity utilization paradox)
- Float blog, "The 70% rule for resource planning"
