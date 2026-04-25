# Agent Integration — AI-Powered PM Tools 2026 (Agile)

## When to use
- In Agile/Scrum contexts: automating sprint planning, backlog grooming, and retrospective action item extraction using PM tool AI
- Setting up Jira Rovo agents or ClickUp Autopilot agents to handle routine Agile ceremonies (daily standup summaries, blocker detection)
- Evaluating AI-assisted sprint velocity prediction and capacity planning tools before adopting them for team use
- Integrating Claude subagents with Jira or Linear to automate user story creation from product briefs
- When Agile teams experience repetitive overhead (writing acceptance criteria, formatting stories, creating sub-tasks) that AI work breakdown can eliminate

## When NOT to use
- When the Agile team is still forming — introducing AI PM tooling before stable team dynamics are established disrupts trust-building
- For complex dependency management across multiple squads — AI work breakdown tools are single-project focused; cross-squad dependency graphs require human planning
- When the team's retrospective process is already healthy and ceremonies are lightweight — adding AI tooling to working processes adds complexity without benefit
- For regulated Agile delivery (SAFe in healthcare, defense) where AI-generated artifacts need compliance review cycles not supported by current tooling

## Where it fails / limitations
- Jira AI work breakdown suggestions are trained on general software project patterns; niche domains (embedded systems, ML pipelines) get irrelevant subtask suggestions
- ClickUp Autopilot agents and Monday Agent Factory require significant setup and prompt engineering to handle Agile-specific workflows beyond the examples in their docs
- AI sprint velocity prediction tools require 6+ sprints of historical data before predictions approach reliability — new teams get noise, not signal
- AI-generated user stories frequently miss the "so that" benefit clause in "As a [user], I want [action], so that [benefit]" format — the business value context requires human input
- Meeting-to-task AI features (Jira Rewatch, ClickUp AI Notetaker) work well for structured meetings but struggle with informal discussion and implicit decisions

## Agentic workflow
Claude subagents enhance Agile workflows by operating between ceremonies: reading the current sprint board state, identifying blockers and overdue tasks, generating draft user stories from product briefs, and producing retrospective summaries. The key integration pattern is agent-as-ceremony-support: before sprint planning, the agent generates draft story breakdowns for each backlog item; before retrospective, it summarizes completed/incomplete work and extracts patterns. All agent outputs are presented to the Agile team as starting points for discussion, not final decisions. The Scrum Master remains the human-in-the-loop for all ceremony facilitation.

### Recommended subagents
- general Bash/HTTP subagent — Jira/Linear API reads for sprint board state
- `faion-sdd-execution` — quality gate before Agile tasks become implementation tasks in SDD workflow
- `faion-knowledge` — load pm/pm-agile methodology for Agile templates and ceremony guides

### Prompt pattern
```xml
<task>Generate sprint planning input for this backlog.</task>
<backlog>{{backlog_items_json}}</backlog>
<team_capacity>{{story_points_this_sprint}}</team_capacity>
<sprint_goal>{{sprint_goal}}</sprint_goal>
<output>
  For each selected backlog item:
  1. Suggested story points (Fibonacci: 1,2,3,5,8,13)
  2. Sub-tasks with estimated points
  3. Acceptance criteria (Given-When-Then format)
  4. Dependencies on other stories
  5. Definition of Done checklist
  Total must not exceed team capacity.
</output>
```

```xml
<task>Summarize this sprint for retrospective input.</task>
<completed>{{completed_stories}}</completed>
<incomplete>{{incomplete_stories_with_reasons}}</incomplete>
<blockers>{{blockers_encountered}}</blockers>
<output>
  1. What went well (infer from completed stories and absence of blockers)
  2. What to improve (infer from blockers and incomplete stories)
  3. Draft action items for each improvement area
  Note: mark all inferences as "AI observation, validate with team"
</output>
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `jira-cli` | Sprint management, issue creation, board queries | https://github.com/ankitpokhrel/jira-cli |
| `linear-cli` | Cycle (sprint) management in Linear | https://github.com/linearapp/linear |
| `gh` | GitHub Projects board management, PR status | https://cli.github.com/ |
| `curl` + `jq` | Direct API calls for sprint data extraction | system packages |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Jira Software + Rovo | SaaS | Partial — REST API v3 | Rovo agents not yet API-composable; standard CRUD via REST for agent use |
| Linear | SaaS | Yes — GraphQL API | Best API for Agile: cycles, projects, issues, labels all queryable |
| ClickUp | SaaS | Yes — REST API v2 | Sprints ("Sprints" feature), tasks, subtasks all accessible via REST |
| GitHub Projects | SaaS | Yes — GraphQL API | Native Agile board; `gh` CLI provides excellent agent interface |
| Shortcut (Clubhouse) | SaaS | Yes — REST API | Stories, epics, iterations API; good for mid-sized Agile teams |
| Notion | SaaS | Yes — API | Lightweight Agile setups; Kanban databases accessible via API |

## Templates & scripts
See `templates.md` for sprint report, retrospective, and user story templates.

Linear sprint board summary (requires LINEAR_API_KEY):
```bash
#!/bin/bash
# Get current active cycle tasks from Linear
TEAM_KEY="${1:?Usage: $0 <team_key>}"

curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"{ team(key: \\\"$TEAM_KEY\\\") { activeCycle { name startsAt endsAt completedScopeHistory scopeHistory issues { nodes { title state { name } assignee { name } priority } } } } }\"}" | \
jq '.data.team.activeCycle | {
  cycle: .name,
  period: "\(.startsAt[:10]) to \(.endsAt[:10])",
  issues: [.issues.nodes[] | {title, state: .state.name, assignee: .assignee.name, priority}]
}'
```

## Best practices
- Use AI work breakdown as a first-draft accelerator for backlog grooming, not as a replacement — team estimation via Planning Poker retains value for shared understanding and commitment
- Configure AI story creation to always include "so that [business value]" enforcement — AI-generated stories without business value context create technical tasks masquerading as user stories
- Track sprint predictability (planned vs. completed story points) before and after introducing AI tools — this reveals whether AI tooling improves or disrupts sprint reliability
- Retrospective AI summaries should be presented without AI attribution in the ceremony — teams that know content is AI-generated engage less critically with it
- For Jira Rovo agent setup, start with a single workflow automation (e.g., "when issue is moved to Done, generate completion summary") before building multi-step agent chains
- AI capacity planning tools need velocity data in story points, not hours — teams using hours for estimation will get poor AI predictions

## AI-agent gotchas
- Agents creating Jira subtasks from AI work breakdown must handle Jira's parent-child link format correctly — subtasks require `"issuetype": {"name": "Subtask"}` and `"parent": {"key": "PROJ-X"}` in the API payload
- Linear GraphQL mutations for sprint (cycle) assignment require the cycle ID, not the cycle name — agents must fetch the current cycle ID before assigning issues
- AI sprint velocity prediction tools embedded in ClickUp Brain and Jira use the vendor's model; Claude agents inferring velocity from raw sprint data use a different model — do not mix predictions from both in the same report without labeling
- Retrospective summaries generated by agents from issue data miss verbal discussion, team sentiment, and interpersonal dynamics — agents should always frame outputs as "data-based observations" not "retrospective conclusions"
- GitHub Projects board state via `gh` CLI reflects PR/issue status but not actual work-in-progress — agents reading GitHub Projects may undercount work that is in progress but not yet linked to issues

## References
- https://developer.atlassian.com/cloud/jira/software/rest/intro/ — Jira Software REST API (Agile endpoints)
- https://developers.linear.app/docs/graphql/working-with-the-graphql-api — Linear GraphQL API
- https://docs.github.com/en/issues/planning-and-tracking-with-projects — GitHub Projects documentation
- https://github.com/ankitpokhrel/jira-cli — jira-cli for terminal-based Agile management
- https://dora.dev/research/2025/ — DORA 2025 research on AI impact on engineering teams
- https://www.atlassian.com/software/jira/guides/rovo — Jira Rovo agent documentation
