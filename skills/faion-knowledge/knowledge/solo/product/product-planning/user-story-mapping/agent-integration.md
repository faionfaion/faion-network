# Agent Integration — User Story Mapping

## When to use
- Designing an end-to-end user journey across multiple activities (sign-up → onboarding → first value → retention).
- Slicing a backlog into shippable releases when a flat list lost the journey context.
- Cross-functional alignment workshop where eng / design / PM need a shared picture before sprint planning.
- Identifying the walking skeleton for an MVP (pairs with mvp-scoping).

## When NOT to use
- Pure technical work (infra, refactors, platform changes) — there's no user-facing backbone.
- Tiny single-flow features — direct user stories suffice.
- Teams without shared journey understanding yet — do user-journey-mapping or JTBD interviews first.

## Where it fails / limitations
- ASCII / 2D map representation is poor for agents to read; structured JSON is required for agentic work.
- Story mapping in isolation produces brittle assumptions; pair with discovery interviews.
- Backbone over-detail ("happy-path-only") hides errors and edge cases.
- Map drift: gets built once, never updated. Treat as a living artifact tied to roadmap reviews.
- LLMs love adding "tasks" without grouping; output looks rich but lacks the vertical-priority discipline.

## Agentic workflow
A backbone subagent emits the high-level user activities (5–10 verbs) given a persona and journey scope. A task-decomposer subagent produces per-activity tasks with priority rank within column. A skeleton subagent picks the minimal task per activity to make an end-to-end working flow. A release-slicer subagent partitions remaining tasks into release rows aligned to the roadmap. A reviewer subagent checks: every activity has a task, walking skeleton is end-to-end, no release is empty, no task is orphaned. Persist as JSON `{backbone[], tasks[{activity, task, rank, release}], skeleton[task_ids], releases[{id, name, goal}]}` and render to markdown table per release.

### Recommended subagents
- `faion-mlp-spec-analyzer-agent` — story-map agent named in this methodology's metadata.
- `faion-mvp-scope-analyzer-agent` — validates the walking skeleton matches MVP scope.
- `faion-mlp-feature-proposer-agent` — feeds candidate tasks per activity.
- `faion-spec-reviewer-agent` — promotes each release-bound task into a story with acceptance criteria.

### Prompt pattern
```
Given persona=<p>, goal=<g>, scope=<from..to>:
1) Emit backbone (5-10 verb-phrase activities, ordered left-to-right).
2) For each activity, emit tasks ordered by importance, max 6 per column.
3) Mark exactly one task per column as walking_skeleton=true (must be end-to-end).
4) Assign each remaining task a release in {R1,R2,R3,backlog}.
Output JSON only. Reject any release with zero tasks across the backbone.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| Miro REST API | Create/read story-map boards | https://developers.miro.com |
| FigJam (Figma API) | Read sticky-note exports | https://www.figma.com/developers/api |
| Mural API | Story-map boards | https://developers.mural.co |
| `mermaid-cli` | Render journey/skeleton diagrams from JSON | https://github.com/mermaid-js/mermaid-cli |
| Linear API + GitHub Projects | Materialize each task as an issue with release label | https://developers.linear.app, https://cli.github.com |
| Notion API | Database with `activity` + `release` properties | https://developers.notion.com |
| `pandoc` | Convert markdown story-map to stakeholder doc | https://pandoc.org |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| StoriesOnBoard | SaaS | Yes (REST) | Purpose-built story mapping, integrates with Jira/Trello |
| Avion | SaaS | Yes (REST) | Story mapping + spec linkage |
| Easy Agile (Jira app) | SaaS | Yes (Jira API) | Native Jira story mapping |
| FeatureMap | SaaS | Yes (REST) | Lightweight, exports to Trello/Jira |
| Miro / FigJam / Mural | SaaS | Partial | Workshop-first; agents read board exports |
| Linear projects | SaaS | Yes (GraphQL) | Use cycles as releases, custom field as activity |
| Plain markdown + Notion / Obsidian | OSS-ish | Yes | File-based, agent-writable, no SaaS lock-in |

## Templates & scripts
See `templates.md` for the story-map and story-card layouts. Skeleton/release validator (≤ 30 lines):

```python
# storymap_check.py — validate skeleton coverage and release balance
import json, sys
m = json.load(sys.stdin)  # {backbone, tasks: [{activity, task, rank, release, walking_skeleton}]}

activities = set(m["backbone"])
skeleton = [t for t in m["tasks"] if t.get("walking_skeleton")]
skeleton_acts = {t["activity"] for t in skeleton}

problems = []
missing = activities - skeleton_acts
if missing:
    problems.append(f"Walking skeleton missing activities: {sorted(missing)}")
if len(skeleton) != len(activities):
    problems.append("Skeleton must have exactly one task per activity")

by_release = {}
for t in m["tasks"]:
    if t["release"] not in (None, "backlog"):
        by_release.setdefault(t["release"], set()).add(t["activity"])
for r, covered in by_release.items():
    if covered != activities and r != "backlog":
        problems.append(f"Release {r} doesn't span all activities (missing {sorted(activities - covered)})")

print(json.dumps({"ok": not problems, "problems": problems}, indent=2))
```

## Best practices
- Build the backbone first with verbs in user-journey order; then add tasks. Reverse order produces noise.
- Walking skeleton is non-negotiable: exactly one task per backbone activity and end-to-end working flow.
- Each release slice must span the full backbone, not just one column. Otherwise users can't complete the journey.
- Include error/edge tasks in the columns, not just happy path.
- Update the map at every quarterly review; treat it as living, not a deliverable.
- Pair the map with the spec: each release-bound task gets a story-card with acceptance criteria.
- For solo dev work, drop the workshop ceremony but keep the structure: backbone + skeleton + 2 release slices.

## AI-agent gotchas
- LLMs collapse activities into nouns ("Dashboard") instead of verbs ("View Dashboard"). Force verb-phrase format.
- Without a walking-skeleton constraint, agents produce a maximalist Release 1. Enforce "one task per column for skeleton" in the schema.
- Agents tend to omit error / empty-state / failure tasks. Add a "include 1+ error path per activity" rule.
- Story maps are 2D; ASCII rendering is fragile. Keep authoritative source as JSON, render markdown tables per release for human readers.
- Human-in-loop checkpoints: (a) backbone approval, (b) walking-skeleton selection, (c) release-slice lock-in.
- Don't let the same agent produce backbone + tasks + slices in one shot — quality drops sharply. Run as a 3-stage pipeline.

## References
- Jeff Patton, "User Story Mapping: Discover the Whole Story, Build the Right Product" (O'Reilly, 2014) — canonical text.
- Jeff Patton's blog https://www.jpattonassociates.com/the-new-backlog/
- Aha! glossary — "User Story Mapping" https://www.aha.io/roadmapping/guide/templates/user-story-map
- Atlassian — "User story mapping for agile product owners" https://www.atlassian.com/agile/project-management/user-stories
- Henrik Kniberg — story mapping examples in the Spotify product engineering posts.
