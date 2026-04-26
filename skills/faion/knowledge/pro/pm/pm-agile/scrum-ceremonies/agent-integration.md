# Agent Integration — Scrum Ceremonies

## When to use
- Bootstrapping Scrum for a new team and wiring ceremonies into a PM tool (Jira, Linear, GitHub Projects, Azure DevOps).
- Replacing free-form standups with disciplined cadence after onboarding new joiners or merging two teams.
- Optimizing a remote/distributed Scrum team — async standups, retro tools, recorded reviews.
- Reducing ceremony time-tax (e.g., halve planning by pre-refining stories with an agent the day before).
- Evidence collection for transformations (capture sprint goal achievement, retro action follow-through, velocity stability).
- Pair with `jira-workflow-management/` (board setup), `pm-tools-overview/` (tool fit), `value-stream-management/` (flow metrics overlay).

## When NOT to use
- Solo developer or pair-of-two — Scrum overhead exceeds value; use Kanban + lightweight reviews.
- Pure research / discovery teams with no incremental delivery — switch to Lean Startup or Discovery Kanban.
- Crisis/incident periods — break glass, run incident process, restart Scrum after.
- Hardware-heavy programs where 2-week sprints do not match material lead times — use Kanban or hybrid (`hybrid-delivery/`).
- Teams that already have working ceremonies and good outcomes — do not redesign for novelty.

## Where it fails / limitations
- "Ceremony theatre": team runs the events but the underlying refinement / DoR / DoD discipline is missing — agents reinforce theatre if they only schedule and notify.
- Standups become status reports to a manager — design for team-to-team flow, not boss reporting.
- Retros without action follow-through; same actions appear sprint after sprint — agents must enforce that previous-sprint actions are reviewed before new ones added.
- Sprint reviews without real stakeholders — turns into engineering show-and-tell. Agents cannot fix attendance, only flag risk.
- Estimation drift: planning poker degrades into "PO says it's a 5". Agents should detect convergence-too-fast (everyone votes the same on first round) and prompt re-discussion.
- Async standups: bots lull teams into never talking; blockers stay unresolved in threads. Hard limit: blocker > 24h escalates to a sync.
- Global remote teams across >5 timezones cannot run effective live ceremonies; rotate inconvenience or accept async-by-design.

## Agentic workflow
A `ceremony-orchestrator` agent owns the sprint clock: schedules each event in the team calendar, posts pre-reads (refined backlog, capacity, prior-sprint metrics), drafts agendas, and posts post-event summaries with action items linked to issues. A `refinement-coach` agent runs against the backlog mid-sprint: flags stories without acceptance criteria, oversized stories, missing estimates, hidden dependencies, then opens a refinement-ready list for the PO. A `retro-synthesizer` clusters retro contributions, surfaces themes, and writes a 1-page summary with new action items + status of previous ones. A `standup-bot` collects async updates, computes blocker age, and pages a Scrum Master after thresholds. Humans facilitate live; agents do prep + capture, never replace conversation.

### Recommended subagents
- `ceremony-orchestrator` (haiku) — schedule + agenda + summary; touches calendar, PM tool, chat.
- `refinement-coach` (sonnet) — backlog quality checks, story splitting suggestions, INVEST scoring.
- `estimation-helper` (sonnet) — proposes story-point estimates from historical reference issues; never auto-applies.
- `retro-synthesizer` (sonnet) — clusters retro inputs, drafts summary, links actions to backlog.
- `standup-bot` (haiku) — async question prompts, thread-summary, blocker-age escalation.
- `velocity-watcher` (haiku) — alerts on velocity outliers, commitment ratio drift, scope creep.

### Prompt pattern
```
You are refinement-coach. Inputs: a list of backlog items (id, title, body,
acceptance_criteria, estimate, dependencies). For each, return STRICT JSON:
{ "id": "...", "ready": true|false,
  "issues": ["missing AC", "oversized: split suggestion", "no estimate", ...],
  "split_suggestion": "...|null", "estimate_hint": "S|M|L|null" }
Rules: never invent AC. Apply INVEST. Flag any story estimated >8 points.
```

```
You are retro-synthesizer. Cluster these N raw retro notes into themes.
Return: { "themes": [{ "name", "notes": [...], "sentiment": "+|0|-" }],
"top_actions": [{ "owner_hint", "action", "linked_theme" }],
"unresolved_from_last_retro": [...] }. Do not invent owners.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `jira-cli` | Sprint create/start/close, JQL for review/retro queries | https://github.com/ankitpokhrel/jira-cli |
| `gh project` | GitHub Projects fields, iteration management | https://cli.github.com |
| `glab` | GitLab iterations + boards | https://gitlab.com/gitlab-org/cli |
| `linear` (community CLI) / GraphQL | Cycle CRUD, issue moves | https://developers.linear.app/docs/sdk |
| `slack-cli` / `slack-sdk` | Async standup channel, retro voting | https://api.slack.com |
| `geekbot` / `standuply` API | Hosted async standup bots | https://geekbot.com / https://standuply.com |
| `parabol` / `retrium` API | Retro tooling with REST | https://www.parabol.co / https://retrium.com |
| `mermaid-cli` | Render burndown / cumulative-flow diagrams from CSV | `npm i -g @mermaid-js/mermaid-cli` |
| `pandoc` | Convert sprint review notes to PPTX/PDF for stakeholders | https://pandoc.org |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Jira Software | SaaS | REST v3 + JQL | Native Scrum boards, sprint reports, velocity charts. |
| Linear | SaaS | GraphQL | Cycles, fast UI, opinionated workflow. |
| GitHub Projects (v2) | SaaS | GraphQL | Iterations field, integrates with PRs. |
| Azure DevOps Boards | SaaS | REST | Native Scrum + SAFe templates. |
| ClickUp / Monday | SaaS | REST | Scrum modules, weak velocity reporting at scale. |
| Geekbot / Standuply / Daily.bot | SaaS | REST | Async standups in Slack/Teams. |
| Parabol | SaaS/OSS | REST | Retro + standup integrated. |
| Retrium | SaaS | REST | Retro-focused, anonymous voting. |
| Miro / FigJam / Mural | SaaS | REST | Visual retros, sailboat/4Ls templates. |
| Zoom / Meet / Teams | SaaS | REST | Live ceremony delivery + recording. |
| Confluence / Notion | SaaS | REST | Sprint review docs, retro archives, DoD/DoR pages. |

## Templates & scripts
README ships sprint-planning, retro, and standup-bot YAML templates. Inline below: a script that scores a sprint review readiness signal.

```python
#!/usr/bin/env python3
"""sprint_review_readiness.py — gate for "is this sprint ready to demo?" """
from __future__ import annotations
import json, sys

def main(path: str) -> int:
    s = json.load(open(path))
    issues = []
    if s["completed_points"] / max(s["committed_points"], 1) < 0.6:
        issues.append("low completion ratio (<60%)")
    if any(i["status"] != "Done" for i in s["committed"] if i.get("demoable")):
        issues.append("undone demoable items present")
    if not s.get("demo_environment"):
        issues.append("no demo environment URL")
    if not s.get("invited_stakeholders"):
        issues.append("no stakeholders invited")
    if s.get("escaped_bugs", 0) > 3:
        issues.append("too many escaped bugs to demo cleanly")
    if issues:
        print("NOT READY:", *issues, sep="\n  - ")
        return 1
    print("Sprint review ready.")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
```

## Best practices
- Time-box hard. End on time even if unfinished — recurring overruns indicate bad inputs (refinement quality, capacity miscalc).
- Never run planning without a refined-Ready backlog ≥ 1.5× sprint capacity; force a refinement session if missing.
- Walk the board (right-to-left) at standup; prioritize flow over individual status. Agents that surface stale columns help.
- Sprint goal must be falsifiable in one sentence; ban vague goals like "make progress on X". Reject during planning.
- Retro action items have owner + due-date + linked issue or they do not exist; agents enforce.
- Rotate facilitators; standardize ceremony agendas in a runbook so rotation is cheap.
- Async standups: maximum blocker age = 1 working day; auto-escalate.
- Capture sprint review feedback in the backlog with provenance (who said what); never leave it in chat.
- Velocity is for forecasting, not management — never use it as a performance metric per person.

## AI-agent gotchas
- Bots that "summarize standups" to managers turn the ceremony into reporting; restrict standup-bot output to the team channel.
- Estimation suggestions from LLMs anchor humans (anchoring bias) — keep them masked until after first vote, or do not use.
- Auto-clustering retros loses context (sarcasm, sentiment) — always show original notes alongside themes.
- Async standup tools generate vast logs; without rotation/archive, retrieval becomes the bottleneck. Page-summarize weekly.
- Calendar agents schedule across time zones poorly when DST flips — always use IANA tz names, never UTC offsets.
- Reading sprint metrics out-of-context: the same 30-point velocity is "good" or "bad" depending on capacity, holidays, dependencies. Force the agent to include context.
- Auto-closing stale stories at sprint end is a foot-gun; let the team triage spillover, not a rule.
- Permission scope: a standup-bot writing into the issue tracker can create circular notification storms; whitelist target fields.
- Human-in-the-loop checkpoints (mandatory): sprint goal acceptance, story splitting, retro action commitment, sprint-end spillover decision.

## References
- The Scrum Guide (2020), Schwaber & Sutherland — https://scrumguides.org
- Derby & Larsen, "Agile Retrospectives" — https://pragprog.com/titles/dlret/agile-retrospectives/
- Retromat (retro formats) — https://retromat.org
- Cohn, "Agile Estimating and Planning"
- Kniberg, "Scrum and XP from the Trenches"
- Sibling methodologies: `jira-workflow-management/`, `kanban-scaled-agile-ceremonies/`, `pm-tools-overview/`, `value-stream-management/`.
