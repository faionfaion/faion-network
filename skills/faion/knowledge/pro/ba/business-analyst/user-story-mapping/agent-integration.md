# Agent Integration — User Story Mapping (BA angle)

This file complements the methodology with the **business-analyst** lens: BA's
role as workshop facilitator and the translation of a story map into formal
BA artifacts (BRD/SRS, BPMN, traceability matrix, requirements packages).
For the product-discovery / sprint-zero angle see
`pro/ba/ba-modeling/user-story-mapping/agent-integration.md`.

## When to use

- Sprint-zero or pre-discovery workshop where the BA owns scope definition and must turn a fuzzy idea into a release plan stakeholders can sign off on.
- Brownfield project where the BA inherits a flat 200+ ticket backlog and must re-establish journey context before re-prioritizing.
- Stakeholder alignment session with mixed business + IT audience — the map is the only artifact that lets a CFO and a backend engineer talk about the same release slice.
- Compliance / regulated project where each story must trace to a process step, a regulation clause, and an acceptance criterion — the map is the source for the traceability matrix.
- Replacing a vendor system or migrating off a legacy product: the existing journey is the backbone, gap analysis fills the cells.

## When NOT to use

- Maintenance backlog with isolated bug fixes and tech debt — there is no journey, just a list. Use WSJF or RICE.
- Pure platform / API-only product with no end-user persona — model with C4 + use cases instead.
- Team already on a stable release cadence with a healthy product backlog and clear roadmap; rebuilding the map is sunk cost.
- One-off internal automation script (single user, single happy path) — a 5-step checklist beats a wall map.
- When stakeholders cannot commit 2–4 contiguous hours; a half-attended map is worse than no map (false consensus).

## Where it fails / limitations

- The map is a snapshot. Without a discipline of re-mapping every release, it diverges from reality within ~6 weeks.
- Vertical "priority" axis collapses MoSCoW + value + risk + sequencing into one column — BAs frequently lose the *why* behind the order. Keep a separate prioritization matrix.
- LLMs hallucinate plausible-but-fake user activities when the persona is thin. The walking-skeleton check (can a real user complete the flow end-to-end?) breaks if the map was written from imagination.
- Cross-functional (B2B2C, marketplace, multi-actor) journeys do not fit a single backbone. You need swimlane variants per persona, which most tools do not render cleanly.
- Non-functional requirements (performance, security, accessibility, audit) have no natural cell on the map and routinely get dropped — they must be captured in a parallel NFR register.

## Agentic workflow

A BA-led story-mapping engagement maps cleanly to a 4-stage subagent pipeline:
**(1) elicitation prep** — research stakeholders, prior artifacts, regulations;
**(2) workshop facilitation** — structured prompts to extract activities/tasks/stories live, BA validates;
**(3) artifact translation** — convert the map into BRD sections, BPMN, traceability matrix, JIRA epics;
**(4) validation loop** — run an LLM critic over each story for INVEST + AC completeness, then a human BA sign-off.
Use the existing repo agents as building blocks (see below); spin a `faion-ba-agent` only for stage 2 facilitation prompts where domain context matters.

### Recommended subagents

- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — once stories slice into Release 1, hand the map cells off as SDD `spec.md` + `test-plan.md` seeds; the executor enforces quality gates per story.
- `nero-sdd-executor-agent` — same pattern for NERO-internal mapping sessions; pulls memory from `.aidocs/memory/` so prior personas/processes carry over.
- `password-scrubber-agent` — run before publishing the rendered map (Miro export, Confluence push) when stakeholders pasted real credentials into sticky notes (it happens).
- Ad-hoc `ba-facilitator` Task subagent — short-lived, prompted with the persona pack + BABOK glossary; emits the live transcript-to-map JSON.
- Ad-hoc `ba-translator` Task subagent — consumes the final map JSON, emits BRD/SRS sections, BPMN XML, RTM CSV in one pass.

### Prompt pattern

Facilitation:
```
You are a BABOK-aligned BA facilitator. Persona pack: {personas}.
Current backbone: {activities}. We are decomposing activity "{a}" into tasks.
Ask 3 elicitation questions targeting the persona's goal, constraints, and
exception path. Output JSON: {questions: [], suggested_tasks: []}.
No prose. No invented tasks not grounded in a question.
```

Translation:
```
Input: story-map.json (activities, tasks, stories, releases).
For each Release-1 story emit: BRD section (problem, scope, AC), BPMN
participant + task, RTM row (story_id, requirement_id, process_step,
test_case_id). Flag any story missing AC or persona reference. Output
strict JSON matching schema {brd, bpmn, rtm, gaps}.
```

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `featmap-cli` | Headless story-map render to SVG/JSON; usable in CI | https://github.com/amborle/featmap |
| `storiesonboard-api` | Read/write StoriesOnBoard maps via REST | https://docs.storiesonboard.com/api |
| `jira-cli` (`ankitpokhrel/jira-cli`) | Push map cells as Epics/Stories with parent links | https://github.com/ankitpokhrel/jira-cli |
| `bpmn-js-cli` | Convert task list → BPMN 2.0 XML headless | https://github.com/bpmn-io/bpmn-js |
| `python-docx` + Jinja2 | BRD/SRS rendering from map JSON | https://python-docx.readthedocs.io |
| `mermaid-cli` (`mmdc`) | Render journey diagrams from map backbone | https://github.com/mermaid-js/mermaid-cli |
| `pandoc` | Map markdown → DOCX/PDF stakeholder package | https://pandoc.org |
| `gh` + GitHub Projects v2 GraphQL | Sync stories as Project items with custom fields | https://cli.github.com |

## Services & apps

| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| StoriesOnBoard | SaaS | Yes — REST API + webhook | Purpose-built for story mapping; Jira sync |
| FeatMap | OSS (self-host) | Yes — JSON export | Lightweight; good for a BA running their own server |
| Avion | SaaS | Partial — Jira sync, no public API | Strong UX for live workshops |
| Miro | SaaS | Partial — REST API, sticky-note granularity | Most common in workshops; agent must template the board layout |
| Mural | SaaS | Yes — REST API + OAuth | Better outline → map conversion |
| Jira + Easy Agile User Story Maps | SaaS plugin | Yes — Jira REST | Map lives inside Jira; BA's RTM source of truth |
| Azure DevOps + Delivery Plans | SaaS | Yes — REST | Common in regulated enterprises |
| Lucidchart / Lucidspark | SaaS | Yes — REST API | Useful when map → BPMN conversion is required |
| Confluence (publish layer) | SaaS | Yes — REST | Where the BRD + RTM end up; agent renders Markdown → Confluence storage format |

## Templates & scripts

See `templates.md` for the BRD/RTM templates the BA fills from the map.
A small renderer that turns a story-map JSON into a BABOK-style Requirements
Package skeleton + RTM CSV:

```python
# render_ba_package.py — story-map.json -> BRD.md + RTM.csv
import json, csv, sys, pathlib
m = json.loads(pathlib.Path(sys.argv[1]).read_text())
out = pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)

brd = ["# Business Requirements Document", f"\nProduct: {m['product']}\n"]
rtm_rows = [("req_id","story_id","activity","task","persona","ac_count","release")]
for act in m["activities"]:
    brd.append(f"\n## Activity: {act['name']}\nGoal: {act['goal']}\n")
    for task in act["tasks"]:
        brd.append(f"\n### Task: {task['name']}\n")
        for s in task["stories"]:
            rid = f"REQ-{s['id']}"
            brd.append(f"- **{rid}** ({s['release']}, {s['priority']}): "
                       f"As a {s['persona']}, I want {s['want']} so that {s['why']}.")
            for i, ac in enumerate(s.get("ac", []), 1):
                brd.append(f"  - AC{i}: Given {ac['given']}; When {ac['when']}; Then {ac['then']}.")
            rtm_rows.append((rid, s["id"], act["name"], task["name"],
                             s["persona"], len(s.get("ac", [])), s["release"]))
            if not s.get("ac"):
                brd.append(f"  - GAP: missing AC for {rid}")

(out / "BRD.md").write_text("\n".join(brd))
with (out / "RTM.csv").open("w") as f:
    csv.writer(f).writerows(rtm_rows)
print(f"BRD + RTM written to {out}")
```

## Best practices

- Run a *pre-mortem* in the first 15 min: ask "what would make this map useless in 3 months?". Capture answers as risks; assign owners. Maps die from neglect, not from bad structure.
- Keep two priority axes, not one: vertical = release slice, color/badge = MoSCoW. Single-axis maps lose the regulatory "must" stories under "nice-to-haves" the loudest stakeholder pushed up.
- The BA, not the PO, owns the persona pack going into the workshop. If personas are not validated against real research (≥5 interviews per persona), the map is fiction — flag this in the BRD assumptions section.
- Tag every story cell with `persona_id` + `process_step_id` at write time. Retrofitting this for the RTM after the workshop is the single biggest time sink in BA delivery.
- Capture the *exception/unhappy paths* on a separate row band below the main tasks — same activities, red stickies. Workshops chronically optimize the happy path and ship products that fail under real conditions.
- Walk the Release-1 line vertically with a real user (or surrogate) before sign-off: read each cell aloud as a contiguous narrative. If it does not form a coherent story, the slice is wrong, not the stories.
- Park NFRs (perf, sec, a11y, audit) in a sidebar register linked to the map header; review them per release slice, not per cell.
- Version the map JSON in git alongside the BRD. The diff between v1 and v2 is the change request.

## AI-agent gotchas

- LLMs invent activities to fill obvious-looking gaps in a journey. Constrain the facilitator agent: "only emit activities grounded in a stakeholder quote or prior artifact"; require source citation per node.
- Story generation drifts from INVEST: agents produce stories that are too large (epics in disguise) or technical ("As a system, I want…"). Run an INVEST critic pass with a strict checklist before accepting any agent output.
- Acceptance criteria from LLMs default to happy-path Given/When/Then. Force a structured prompt: "emit ≥1 happy, ≥1 alternate, ≥1 error AC; cite the persona's exception scenario from elicitation".
- Do not let the agent decide release boundaries unsupervised. Slicing is a business + risk decision; the agent proposes, the BA + stakeholders dispose. Lock the agent to "suggest releases" mode, never "commit releases".
- Map JSON schemas drift between tools (Miro, Jira, FeatMap). Pin one canonical schema in your repo; convert on the boundary. Otherwise downstream BRD/RTM renderers break silently.
- Persona leakage: agents conflate personas across stories ("As a user…"). Enforce a `persona_id` enum in the schema and reject stories without it.
- Token blow-up on large maps (200+ stories). Render BRD per activity, not per map; chunk the agent input to one activity at a time and concatenate.
- Human-in-the-loop checkpoints (mandatory): (a) backbone approval before tasks; (b) Release-1 slice approval before stories; (c) BRD + RTM diff review before publication; (d) NFR register review before sign-off.

## References

- Jeff Patton, *User Story Mapping: Discover the Whole Story, Build the Right Product* (O'Reilly, 2014).
- BABOK v3, §10.46 Story Mapping; §10.50 Use Cases and Scenarios; §10.41 Requirements Modeling.
- IIBA Agile Extension v2, §4 Strategy Horizon → Initiative Horizon mapping.
- Mike Cohn, *User Stories Applied*, ch. 2 (INVEST) and ch. 7 (acceptance criteria).
- StoriesOnBoard API — https://docs.storiesonboard.com/api
- Easy Agile User Story Maps for Jira — https://www.easyagile.com/products/user-story-maps
- BPMN 2.0 spec — https://www.omg.org/spec/BPMN/2.0/
- BABOK Requirements Traceability — https://www.iiba.org/standards-and-resources/babok/
