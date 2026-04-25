# Agent Integration — Backlog Grooming & Roadmapping

## When to use
- Sprint kickoff: need to pick top N items from backlog for next cycle
- Product review: prioritize incoming requests from users/stakeholders
- Quarterly planning: produce a theme-based roadmap from raw backlog data
- Backlog has grown past 20+ items without recent triage
- New team member needs product direction context

## When NOT to use
- Single-task execution sessions where direction is already clear
- Greenfield projects with no backlog yet (use spec-requirements first)
- Real-time stakeholder negotiations (async agent output won't substitute for live discussion)
- When RICE inputs (reach, impact, confidence) are pure guesses with no data backing

## Where it fails / limitations
- RICE scoring requires real user/traffic data; agent-generated numbers are illustrative only — always flag as estimates
- Roadmaps output by agents need human sign-off before communicating to stakeholders
- "Won't do" lists require product authority; agent cannot know undocumented business constraints
- Agent cannot detect political blockers or team morale issues that shift priorities

## Agentic workflow
A subagent reads the backlog directory (`.aidocs/backlog/`), applies RICE scoring to each item using provided data points, and outputs a ranked priority list with MoSCoW classification. A second pass generates a Now/Next/Later roadmap grouped by strategic themes. Human reviews and approves before the roadmap is finalized. The `faion-sdd-executor-agent` can then execute items from the "Now" bucket sequentially.

### Recommended subagents
- `faion-sdd-executor-agent` — executes implementation tasks for items promoted from backlog to in-progress
- General planning subagent (claude-opus-4-5 or claude-opus-4-7) — strategic roadmap generation, dependency chain analysis

### Prompt pattern
```
Read all files in .aidocs/backlog/ideas/. For each item, compute RICE score using:
Reach={provided_reach}, Impact={provided_impact}, Confidence={confidence}%, Effort={effort_months}.
Output a ranked table (highest score first) with MoSCoW column.
Flag any item lacking data for Reach or Impact as "estimate-needed".
```

```
Given the ranked backlog above, group items into a Now/Next/Later roadmap.
Now = Must items scoring >5 RICE. Next = Should items scoring 2-5. Later = rest.
Output roadmap.md following the template in templates.md.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh` (GitHub CLI) | Manage GitHub Issues as backlog items, add labels, milestones | `brew install gh` / https://cli.github.com |
| `jq` | Parse/filter JSON from PM APIs | `apt install jq` / https://stedolan.github.io/jq/ |
| `roadmap-cli` (OSS) | Generate terminal roadmap charts from JSON | `npm i -g roadmap-cli` / https://github.com/nickvdyck/roadmap |
| `linear` CLI | Query/update Linear issues from shell | `npm i -g @linear/sdk` / https://developers.linear.app/docs/sdk/getting-started |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Linear | SaaS | Yes — REST + GraphQL API | Best API for agent-driven backlog reads; webhooks for triggers |
| GitHub Projects | SaaS | Yes — GraphQL API | Native if codebase is on GitHub; see github-projects methodology |
| Productboard | SaaS | Partial — REST API, limited write | Good for input aggregation; agents can read feature requests |
| Notion | SaaS | Yes — REST API | Flexible but unstructured; agent must parse free-form content |
| Trello | SaaS | Yes — REST API | Simple; see trello-kanban methodology |
| Coda | SaaS | Yes — REST API | Tables work well for RICE scoring sheets |

## Templates & scripts
Backlog item template, grooming session template, and roadmap template are in `templates.md`.

Inline helper — dump backlog items from GitHub Issues to a RICE-ready CSV:
```bash
#!/usr/bin/env bash
# gh-backlog-export.sh — requires `gh` and `jq`
REPO="${1:?Usage: $0 owner/repo}"
gh issue list --repo "$REPO" --label "backlog" --limit 100 --json number,title,labels,assignees \
  | jq -r '["ID","Title","Labels"] , (.[] | [.number, .title, ([.labels[].name] | join(","))]) | @csv' \
  > backlog-export.csv
echo "Exported to backlog-export.csv"
```

## Best practices
- Keep RICE scores in the backlog item file, not in a separate spreadsheet — agents need single-file context
- Add a `## RICE Score` section to every `.aidocs/backlog/*/` item as part of grooming
- Mark roadmap items as `Confidence: High/Medium/Low` — agents must propagate uncertainty, not hide it
- Never let the backlog exceed 40 unscored items; schedule agent-assisted triage when it crosses 20
- Use theme-based roadmaps (not time-based) for solo projects — quarters shift, themes don't
- Document "Won't do" items explicitly; prevents repeated re-prioritization of the same rejected idea
- Separate "ideas/" from "validated/" in `.aidocs/backlog/`; agents only score validated items

## AI-agent gotchas
- Agent RICE scores are hallucinated if Reach/Impact inputs aren't grounded in real data — always supply numbers in the prompt
- Roadmap "Later" bucket items will drift; re-run grooming every 4-6 weeks, not once per quarter
- Agents tend to mark everything "Must" — enforce: Must ≤ 60% of scope rule in the prompt explicitly
- "Human-in-loop" checkpoint required before promoting any item from backlog to spec phase
- Token budget: full backlog read + roadmap write for 40 items ≈ 30-50k tokens; use Sonnet, not Haiku
- If backlog items lack descriptions, agent output will be generic; enforce item template before grooming

## References
- https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers/ — RICE framework original
- https://www.scrum.org/resources/what-is-a-product-backlog — Scrum backlog guide
- https://www.atlassian.com/agile/scrum/backlog-refinement — Atlassian backlog refinement
- https://roadmunk.com/guides/product-roadmap-examples/ — Roadmap patterns
- https://www.agilebusiness.org/page/ProjectFramework_10_MoSCoWPrioritisation — MoSCoW method
