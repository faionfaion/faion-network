# Agent Integration — User Story Mapping

## When to use
- Decomposing a new product or major feature where the user journey spans 3+ steps and the team needs shared mental model.
- Slicing releases out of a large feature backlog by identifying a "walking skeleton" then incremental release slices.
- Onboarding a new contributor who needs to understand the product end-to-end in one diagram.
- Discovery → delivery handoff: turning interview transcripts into structured backbone + tasks before sprint planning.

## When NOT to use
- Single isolated feature with no journey (e.g. "add audit log endpoint") — go directly to a story or spec.
- Maintenance/bug-fix work where the journey is already mapped and stable.
- Linear data-pipeline-style products that have no user-facing journey; technical sequence diagrams serve better.
- When the team will not maintain the map. Stale story maps actively mislead.

## Where it fails / limitations
- Backbone exploding to 15+ activities — the map turns into a Gantt chart and loses strategic clarity.
- Walking skeleton missing one column entirely; the agent or author skipped an activity because nothing felt minimal there. Walking skeleton must be end-to-end.
- Treating the map as static; user behaviour and analytics should rewrite vertical priorities monthly.
- Solo mapping by an agent without user research input produces happy-path-only maps, missing error/recovery flows.
- Confusing the map with a backlog. The map is journey-shaped; the backlog is rank-shaped. Both are needed.

## Agentic workflow
A discovery agent ingests interview notes / journey maps and emits backbone activities (5–10). A task generator expands each activity into user tasks and ranks them vertically by impact. A slicer agent draws the walking skeleton and proposes 2–3 release slices, each with a value statement. A reviewer agent checks for end-to-end completeness (every activity has a skeleton task, no gaps). Human approves the backbone before tasks are generated — getting the backbone wrong propagates errors downward.

### Recommended subagents
- `faion-mlp-spec-analyzer-agent` — referenced in `README.md` for story-map authoring.
- `faion-task-creator-agent` — converts each task card into a backlog story with acceptance criteria.
- `faion-mvp-scope-analyzer-agent` — uses the walking skeleton as MVP boundary.
- `faion-spec-reviewer-agent` — final pass on each generated story for testability.

### Prompt pattern
```
System: You are a story-map author. Output JSON only:
  {persona, goal, backbone:[{id,name,order}],
   tasks:[{id, backbone_id, name, story, acceptance:[], priority:int}],
   slices:[{name, theme, task_ids:[], value_statement}]}
Constraints: 5 <= len(backbone) <= 10. Every backbone item must have at
  least one task in slice "walking_skeleton". priority 1 = highest within
  backbone column. Reject duplicates.
Input: {persona_brief, journey_notes, business_constraints}
```

```
System: You are a story-map reviewer. For each backbone item verify:
  - present in walking_skeleton, - has >=1 error/recovery task somewhere,
  - tasks are user-observable (not implementation steps).
Output: list of violations or {"ok": true}.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `mermaid-cli` | Render ASCII story-map → image; agent emits Mermaid flow/journey | `npm i -g @mermaid-js/mermaid-cli` |
| `gh project` | Persist tasks as items with backbone-as-field | https://cli.github.com/manual |
| `linear-cli` | Create cycle-per-slice and tasks-per-card | https://developers.linear.app |
| `miro-api-client` | Push generated map to a Miro board for human review | https://developers.miro.com |
| `figjam-api` | Same for FigJam | https://www.figma.com/developers/api |
| `pandoc` | Render story map JSON → presentable Markdown/HTML | https://pandoc.org |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| StoriesOnBoard | SaaS | Yes (REST) | Purpose-built story-mapping tool; releases as horizontal slices. |
| Avion | SaaS | Yes (REST) | Story mapping + Jira/Linear sync. |
| Easy Agile User Story Maps for Jira | SaaS plugin | Yes (Jira REST) | Native story map in Jira. |
| Miro | SaaS | Yes (REST) | Templates exist; agents can create boards programmatically. |
| FigJam | SaaS | Limited | Agent-friendly via plugins; lower fidelity for structured data. |
| Lucidspark | SaaS | Limited | Whiteboard-grade; weaker structured API. |
| Plane / OpenProject | OSS | Partial | No native map; emulate via swimlane views. |

## Templates & scripts
See `README.md` and `templates.md` for the Story Map and Story Card formats. Helper to validate a story-map JSON before pushing to tracker:

```python
import sys, yaml, collections as c
m = yaml.safe_load(open(sys.argv[1]))
errs = []
bb = m["backbone"]
if not (5 <= len(bb) <= 10): errs.append(f"backbone size {len(bb)} not in 5..10")
ids = {b["id"] for b in bb}
by_bb = c.defaultdict(list)
for t in m["tasks"]:
    if t["backbone_id"] not in ids:
        errs.append(f"task {t['id']} → unknown backbone {t['backbone_id']}")
    by_bb[t["backbone_id"]].append(t)
skeleton = next((s for s in m["slices"] if s["name"] == "walking_skeleton"), None)
if not skeleton: errs.append("missing walking_skeleton slice")
else:
    covered = {t["backbone_id"] for tid in skeleton["task_ids"]
               for t in m["tasks"] if t["id"] == tid}
    miss = ids - covered
    if miss: errs.append(f"walking_skeleton missing backbone columns: {miss}")
for e in errs: print("FAIL:", e)
sys.exit(1 if errs else 0)
```

## Best practices
- Build the backbone first, in a workshop with at least one user voice (interview notes count). Skipping this step is the #1 failure mode.
- Use verb phrases for backbone activities, never noun-only ("Create Project" not "Project").
- Always identify the walking skeleton — one task per activity, end-to-end. No skeleton ⇒ no defensible MVP.
- Limit slices to 3–5; more slices destroys release thinking.
- Include error / recovery / abandonment paths somewhere in the map; happy-path-only maps under-deliver.
- Pair with `mvp-scoping`: walking skeleton ≈ Must-Have list, slice 1 ≈ MVP, slice 2 ≈ MLP.
- Re-run the map after each release using actual usage data — vertical priorities should change.
- Store the map as structured data (JSON/YAML) not only as a whiteboard image; agents and humans both need it queryable.

## AI-agent gotchas
- Without persona context, agents produce generic backbones ("View", "Browse", "Manage") that fit nothing. Always inject a persona brief.
- Backbones drift toward implementation steps ("Authenticate user" instead of "Sign up"). Add a constraint that activities must be user-observable.
- Walking skeleton is silently dropped because it is "minimal" — explicitly require the slice "walking_skeleton" to exist and cover every column.
- Error/recovery tasks are routinely missing; tell the agent to allocate at least one error path per backbone column.
- Vertical priority is collapsed to monotonic 1..N which loses meaning; ask for tier (must/should/could) instead.
- Token cost: a 7-column × 5-task map fits in <2k tokens; do not over-engineer with chunking.
- Generated story cards often duplicate "As a user, I want to use the feature so that I can use it." Reject self-referential stories and force a measurable "so that".
- Agents will happily emit 50 task cards; cap with a hard maximum and require justification for exceeding 5 per column.

## References
- Jeff Patton — *User Story Mapping* (O'Reilly, the canonical reference).
- Jeff Patton blog: https://jpattonassociates.com/user-story-mapping/
- StoriesOnBoard — practical templates: https://storiesonboard.com/blog/
- Easy Agile — story mapping guide: https://www.easyagile.com/blog/user-story-mapping
- Roman Pichler — story map vs roadmap: https://www.romanpichler.com/blog/
- Atlassian — story mapping in Jira: https://www.atlassian.com/agile/project-management/user-stories
