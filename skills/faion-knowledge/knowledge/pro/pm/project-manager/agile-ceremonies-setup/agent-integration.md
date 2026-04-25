# Agent Integration — Agile Ceremonies Setup

## When to use
- Bootstrapping Scrum (or Scrum-of-Scrums) for a new team: defining cadence, agendas, time-boxes, tool wiring.
- Migrating waterfall / ad-hoc team to a structured ceremony rhythm.
- Tuning ceremonies that have decayed (silent retros, status-report standups, drifting reviews).
- Setting up async / hybrid ceremonies for distributed teams (timezone-aware standups, async demos).
- Configuring PM tools (Jira / Linear / Azure DevOps Boards) to mirror the ceremony cadence.

## When NOT to use
- Solo / 2-person teams — overhead exceeds value; lightweight async check-ins suffice.
- Continuous-delivery teams running flow-based Kanban with WIP limits and SLA dashboards; ceremonies become anti-patterns.
- Teams with zero psychological safety — retros become blame sessions and make things worse before they help. Fix safety first.

## Where it fails / limitations
- Time-box discipline collapses without an active facilitator; ceremonies bloat 2-3x and the team blames "agile" rather than facilitation.
- Async standups become status reports nobody reads; lose the point of the event.
- Sprint reviews drift into "demo theatre" instead of real stakeholder feedback.
- Retros that don't track action-item completion = same complaints every sprint, then team gives up.
- Tool-driven ceremonies (Jira-only) miss the conversational value; tool is record, not the event.
- Ceremony rituals get re-imported even when the team has moved to flow-based delivery; org-level cargo culting.

## Agentic workflow
Three useful agent surfaces: (1) one-time setup — generate ceremony cadence, agendas, tool config (Jira board, Linear cycle, ADO sprint) from team profile (size, timezone spread, sprint length). (2) Ongoing facilitation — async standup bot prompts (Geekbot / Standuply / Slack workflow), retro board templates per sprint, agenda generation tied to sprint metrics. (3) Continuous improvement — post-sprint analysis: did the team meet sprint goal? velocity trend? action-item closure rate? Then propose ceremony tweaks. Keep agents away from authoring sprint goals or assigning work — those are PO / team decisions.

### Recommended subagents
- A `ceremony-bootstrapper` subagent (define inline) — emits agendas + tool configs from team profile.
- A `retro-facilitator` subagent — generates retro board template per sprint, seeds prompts based on metrics, never owns actions.
- An `async-standup-bot` (Geekbot-equivalent) — collects responses, formats summary, escalates blockers older than 24h.
- A `ceremony-health-auditor` — quarterly: ratio of completed retro actions, velocity stability, sprint-goal-met rate.

### Prompt pattern
```
Inputs: team_size=7, sprint_length=2w, timezone_spread="UTC-5 to UTC+3",
delivery_model="scrum", tool="jira", remote_pct=80.

Output Markdown bundle:
- ceremony_cadence (table: event, time-box, day, mode sync/async).
- per_event_agenda (sprint-planning, daily, review, retro, refinement).
- jira_config (sprint dates, board columns, quick filters, dashboard widgets).
- standup_bot_config (Geekbot YAML).
- definition_of_ready, definition_of_done starter.

Hard constraints: total ceremony overhead per person ≤ 8% of sprint capacity.
Do NOT propose more than 2 sync ceremonies for high timezone spread.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `jira-cli` (ankitpokhrel) | Sprint CRUD, issue queries, board ops | https://github.com/ankitpokhrel/jira-cli |
| `linear-cli` / `lr` | Linear cycle ops | https://github.com/evangodon/lr |
| `az boards` (Azure DevOps CLI) | Sprint / iteration / work-item CRUD | https://learn.microsoft.com/en-us/azure/devops/cli/ |
| `gh project` | GitHub Projects (Iterations) | https://cli.github.com/manual/gh_project |
| `slack-cli` / Slack API | Standup bot integration, reminders | https://api.slack.com/apis |
| Geekbot CLI / API | Async standup automation | https://geekbot.com/ |
| `mural-cli` / `miro-cli` | Retro board provisioning | https://developers.miro.com/ |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Jira (Cloud + Server) | SaaS / on-prem | Yes — REST | Sprint, board, dashboard APIs |
| Linear | SaaS | Yes — GraphQL | Cycles map cleanly to sprints |
| Azure DevOps Boards | SaaS / on-prem | Yes — REST | Iteration paths, queries |
| GitHub Projects (v2) | SaaS | Yes — GraphQL | Iterations, automation |
| ClickUp | SaaS | Yes — REST | Sprints + Goals |
| Notion | SaaS | Yes — REST | Retro DB, agenda pages |
| Geekbot / Standuply / Daily.bot | SaaS | Yes — REST | Async standups |
| Parabol / Retrium / EasyRetro / Metro Retro | SaaS | Yes (varies) | Retrospective platforms |
| Miro / Mural / FigJam | SaaS | Yes — REST | Visual retro / planning |
| Plandex / Planning Poker apps | SaaS | Yes (mostly) | Estimation events |

## Templates & scripts
See `templates.md` and `examples.md` for full sprint-planning, retro, and standup templates. Inline: create a 2-week sprint with capacity-aware backlog selection (Jira CLI).

```bash
#!/usr/bin/env bash
set -euo pipefail
PROJECT="${1:?project key}"
GOAL="${2:?sprint goal}"
START="${3:-$(date -u +%F)}"
END="${4:-$(date -u -d '+14 days' +%F)}"
BOARD_ID=$(jira board --project "$PROJECT" --plain --no-headers --type scrum | awk 'NR==1{print $1}')
SPRINT_ID=$(jira sprint create -b "$BOARD_ID" -n "Sprint $(date -u +%G-W%V)" \
              -s "${START}T09:00" -e "${END}T17:00" --plain | awk '{print $NF}')
jira sprint move -b "$BOARD_ID" -s "$SPRINT_ID" \
  $(jira issue list -p "$PROJECT" -s 'Ready' --order-by priority --plain --no-headers \
    | awk '{print $1}' | head -8)
jira sprint start -b "$BOARD_ID" -s "$SPRINT_ID" --goal "$GOAL"
echo "Sprint $SPRINT_ID started: $GOAL"
```

## Best practices
- Cap total ceremony time at ≤ 10% of sprint capacity. If the team complains about meetings, audit the time-boxes first.
- One *single* sprint goal per sprint, written before backlog selection. No goal = standup is status reporting.
- Definition of Ready (DoR) at refinement, Definition of Done (DoD) at planning. Without both, sprint scope is mush.
- Track completed retro actions as backlog items with the sprint they came from. < 70% closure rate = retros aren't working.
- Rotate facilitators (standup, retro) — distributes facilitation skill, prevents Scrum-Master single point of failure.
- For distributed teams: maximum one sync ceremony per day (planning + retro can be the same day); use async for standups.
- Sprint Review must include real users / stakeholders, not just the dev team. Internal demo = waste.
- Retro format rotation (Start-Stop-Continue → 4Ls → Sailboat → Mad-Sad-Glad) every 4-6 sprints to keep it fresh.
- Ceremony health survey (1-5 score) every quarter — measure the ceremony, not just the work.

## AI-agent gotchas
- LLM defaults to Scrum vocabulary even when team is on Kanban / flow; it will invent sprints that don't exist. Anchor on `delivery_model` input.
- Generated agendas often exceed time-box (60+45+45 = 150 min for a 2-week sprint review is overkill); enforce sum ≤ time-box.
- Async standup prompts written by LLMs default to status questions ("what did you do yesterday"); push toward goal-progress + blocker focus.
- Retro action items often lack owner / due date / measurable outcome — agent emits "improve communication" not "implement standup template by sprint N+1, owner @x". Force structured output.
- Tool-config generation: Jira / Linear / ADO have rate-limited APIs and irreversible side effects (deleted boards). Always dry-run first; never let agent delete boards.
- Timezone math: agent forgets daylight-saving transitions; standup that worked in March breaks in November. Use tz-aware library, not naive UTC offsets.
- LLMs invent "Scrum guide" rules ("daily must be standing") that aren't in the actual Scrum Guide (2020). Cite version.
- Sprint goal generation by LLM tends to be vacuous ("complete sprint backlog"); reject if it doesn't pass the "what changes for users?" test.

## References
- Scrum Guide 2020 — https://scrumguides.org/scrum-guide.html
- Agile Retrospectives (Derby & Larsen) — https://pragprog.com/titles/dlret/agile-retrospectives/
- Retromat (retro format library) — https://retromat.org/
- Jira REST API — https://developer.atlassian.com/cloud/jira/platform/rest/v3/
- Linear API — https://developers.linear.app/
- Azure DevOps REST — https://learn.microsoft.com/en-us/rest/api/azure/devops/
- Liberating Structures (facilitation patterns) — https://www.liberatingstructures.com/
