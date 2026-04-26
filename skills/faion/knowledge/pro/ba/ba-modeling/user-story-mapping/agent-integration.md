# Agent Integration — User Story Mapping (BA Modeling)

> BA-modeling angle on Jeff Patton's User Story Mapping. Sibling pages cover use-case-modeling, business-process-analysis, acceptance-criteria. This file is about how a BA + Claude subagents drive the map from a flat backlog or feature pitch through release-ready slices.

## When to use

- Stakeholders hand you a flat backlog (50–500 items in Jira/ClickUp/Linear) with no journey context — agents reverse-engineer activities from titles and group stories under them.
- New product / new module kick-off where the BA has personas + goals but no scope yet — story map becomes the contract between PO, design, and engineering before sprint zero.
- Release planning for a 3–6 month roadmap that needs a "walking skeleton" cut — vertical slicing into MVP / MLP / R2 / R3 with explicit thin-slice defense.
- Migration / replatforming — current journey is mapped first, then target journey is overlaid; gaps and parity holes pop visually.
- Stakeholder workshop prep — agents pre-populate a draft map from interview transcripts and a brain-dump so the workshop debates cuts and priorities, not vocabulary.
- Audit existing Jira backlog for journey coverage gaps — agent ingests epics/stories and produces a coverage matrix vs. backbone activities.
- B2B SaaS where multiple personas hit the same product — separate maps per persona, then a merged "shared backbone" view.

## When NOT to use

- Small, single-feature work (one screen, one form) — story mapping overhead exceeds the value; write 3 stories with AC and ship.
- Pure platform / API-only services with no end-user journey — switch to `interface-analysis` and use-case-modeling. Story maps don't fit B2B middleware contracts.
- Hard-deadline regulated work (audit response, legal compliance fix) — scope is already defined by the regulation; mapping wastes the wrong calories.
- Pre-PMF zero-to-one where the journey changes weekly — you'll throw the map out faster than agents can synthesize one. Use `customer-development` + working prototypes.
- Large enterprise programs that demand BABOK Use Case Specs and BPMN traceability — story mapping is too lossy for compliance trails. Pair it with use-cases, don't replace.
- Research/exploratory spikes — there's no journey to map; use opportunity-solution-trees.
- Pure infrastructure / DevOps backlogs — non-user activities don't belong on a story map; track separately as enablers.

## Where it fails / limitations

- "Activities" become epic titles and the map degenerates into a 2D Jira view — backbone must read as narrative verbs ("Browse → Choose → Pay"), not feature names ("Catalog → PDP → Checkout").
- Vertical priority dimension collapses to "1, 2, 3" — without a forcing function (release line + capacity), everything ends up in R1.
- Multi-persona maps merge prematurely — one map for shoppers + admins + ops produces an unreadable mess. Always start per-persona; merge only after each is stable.
- Maps go stale within 2 sprints if not owned — without a single owner re-running the synthesizer weekly, the map and Jira drift.
- Walking skeleton fallacy — teams declare R1 as "skeleton" but include nice-to-haves because they're "already built". Forces ID-tagged minimum-task list before R1 freeze.
- Vertical slicing collapses under technical dependencies — auth/payment/infra often must precede thin-slice user stories. Mark them explicitly as enabler tasks, not journey tasks.
- Tool fragmentation — Miro/FigJam are visual but not queryable; Jira is queryable but not visual. Agents need a structured source of truth (YAML/JSON) with renderers on both sides.
- Story-mapping workshops produce 200 sticky notes that nobody transcribes — without a digitization step, the artifact dies on the wall.

## Agentic workflow

BA owns the map; agents mechanize ingestion, synthesis, slicing, and Jira sync. Six hand-offs across a typical 1–2 week mapping cycle, each gated by BA review.

```
Day 1  backlog-ingester    (haiku)  → flat list of stories+epics extracted from Jira / CSV / docs
Day 1  persona-resolver    (sonnet) → personas.yaml; each story tagged with persona_id
Day 2  activity-extractor  (sonnet) → backbone candidates: verbs in user voice, ordered
Day 3  task-grouper        (sonnet) → tasks under activities; orphan stories surfaced
Day 4  story-rewriter      (sonnet) → INVEST-compliant stories; AC stub via acceptance-criteria
Day 5  release-slicer      (opus)   → R1/R2/R3 cuts with walking-skeleton defense
Day 6  jira-syncer         (haiku)  → patch epics/labels; emit diff for BA approval
Weekly map-validator       (sonnet) → drift check vs Jira, freshness warnings
```

The map lives at `.product/story-maps/<product>/<persona>.yaml` (tree-as-code). Renderers produce Markdown matrix, Mermaid graph, Miro/FigJam JSON via API. Jira sync is one-way write (BA approves diff before push), one-way read (Jira is source of truth for status).

### Recommended subagents

| Subagent | Model | Cadence | Inputs | Outputs |
|----------|-------|---------|--------|---------|
| `backlog-ingester` | haiku | On demand | Jira export / Linear API / CSV / docs | Normalized story list (JSON) with title, desc, status, labels |
| `persona-resolver` | sonnet | Per cycle | Existing personas, raw stories, BA notes | personas.yaml + story→persona_id mapping |
| `activity-extractor` | sonnet | Per cycle | Persona goals, story titles, journey docs | Ordered backbone (verb-phrases) with rationale |
| `task-grouper` | sonnet | Per cycle | Backbone, normalized stories | Tasks-under-activities tree; orphan-story list |
| `story-rewriter` | sonnet | Per story batch | Raw stories, persona, task | INVEST-compliant "As a / I want / So that" + AC stubs |
| `release-slicer` | opus | Per release planning | Full map, capacity, dependencies, outcome | R1/R2/R3 cuts; walking-skeleton report (gaps, risks, enablers) |
| `dependency-tagger` | sonnet | Pre-slice | Story map + tech architecture notes | Enabler/dependency edges between stories |
| `coverage-auditor` | sonnet | Weekly | Story map + Jira current state | Coverage matrix: tasks without stories, stories without tasks |
| `jira-syncer` | haiku | On approval | Approved map diff | Jira API patches (epic, label, parent links); rollback plan |
| `map-renderer` | haiku | On commit | map.yaml | Markdown table, Mermaid, Miro JSON |
| `workshop-prep` | sonnet | Pre-workshop | Map + open questions | Workshop deck, debate points, sticky-note seed list |
| `walking-skeleton-defender` | opus | Pre-release | R1 slice + outcome metric | Justification per task; "why this is in/out of MVP" memo |

Cheap models for ingestion, rendering, and Jira mechanics. Sonnet for structured authoring (personas, activities, tasks, stories). Opus only for release slicing and walking-skeleton defense — these are cross-cutting reasoning tasks where capacity, journey completeness, and outcome trade off.

In this repo: `agents/faion-sdd-executor-agent.md` consumes the map output as input to `implementation-plan.md`. Pair user-story-mapping with `pro/ba/ba-modeling/acceptance-criteria` (for AC stubs) and `solo/sdd/sdd-planning` (for the spec→tasks bridge).

### Prompt pattern

```xml
<role>You are the {agent} for a Business Analyst running User Story Mapping (Jeff Patton).</role>

<inputs>
  <map>{path to map.yaml}</map>
  <personas>{path to personas.yaml}</personas>
  <backlog>{normalized backlog JSON}</backlog>
  <outcome>{measurable product outcome + target}</outcome>
  <capacity>{team velocity per sprint, sprint count to release}</capacity>
  <constraints>{regulatory, deadline, dependencies}</constraints>
</inputs>

<rules>
  - Backbone activities MUST be verb-phrases in the user's voice ("Find a place to stay"), never feature names ("Search").
  - Every story MUST link to exactly one task and one persona; orphans go to an `unassigned` bucket for BA review.
  - Walking skeleton = thin vertical slice covering >=1 task per backbone activity that delivers a complete (degraded) user journey end-to-end.
  - Reject stories phrased as "implement X" or "as a developer I want" — those are tasks, not user stories.
  - Emit map changes as YAML diffs (add/move/rewrite/archive), never full-tree rewrites.
  - Every release slice MUST include capacity-feasibility evidence (story-points sum vs velocity × sprints).
  - Surface dependency conflicts: if story A's release < story B's release but A depends on B, flag and stop.
  - Output JSON to schema {schema_path}; markdown digest <= 80 lines.
</rules>

<task>{cadence-specific instruction}</task>
```

Pin the map schema and require diffs. BA reviews diffs in PR form; raw rewrites are rejected. For workshop synthesis, feed raw transcript spans with participant IDs — never paraphrased summaries.

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `jira-cli` (ankitpokhrel) | Read/write Jira issues, epics, labels | github.com/ankitpokhrel/jira-cli |
| `acli` (Atlassian official) | Atlassian Cloud CLI: Jira + Confluence | developer.atlassian.com/cloud/acli |
| `linear-cli` / Linear GraphQL | Linear backlog ingestion + sync | developers.linear.app |
| `gh` | Map-as-PR; review tree diffs in GitHub | cli.github.com |
| `miro-api` / FigJam REST | Push map to workshop canvas | developers.miro.com |
| `mermaid-cli` (`mmdc`) | Render map.yaml → Mermaid SVG/PNG | github.com/mermaid-js/mermaid-cli |
| `pandoc` | Map markdown → PDF / DOCX for stakeholders | pandoc.org |
| `yq` | YAML query/transform for map manipulation | github.com/mikefarah/yq |
| `whisper.cpp` | STT for workshop recordings | github.com/ggerganov/whisper.cpp |
| `~/bin/tg-send` | Notify BA of stale maps, drift, blockers | NERO local |

## Services & apps

| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Jira (Atlassian Cloud) | SaaS | Yes (REST + acli) | Most common backlog source; epic = activity, story = leaf. Watch rate limits. |
| Linear | SaaS | Yes (GraphQL) | Cleaner API than Jira; project = release, issue = story. |
| ClickUp / Azure DevOps / Shortcut | SaaS | Yes/Partial (REST) | Hierarchy maps onto activity/task/story; reconcile work-item types. |
| StoriesOnBoard / Avion / FeatureMap | SaaS | Yes/Partial (REST) | Purpose-built USM tools with Jira/Trello sync. |
| Easy Agile User Story Maps | Jira plugin | Partial (Jira API) | Lives inside Jira; map is a Jira view. |
| Miro / FigJam / Mural | SaaS | Partial (REST) | Workshop canvases; export to JSON, not source of truth. |
| Notion / Confluence | SaaS | Yes (REST) | Map narrative + tables; weak hierarchy. |
| Productboard / Aha! | SaaS | Yes (REST) | Feeds opportunities/strategy into map; pair with discovery. |
| n8n / Zapier / Tray | iPaaS | Yes | Wire Jira ↔ map.yaml ↔ Miro round-trip. |

## Templates & scripts

Map schema (`map.yaml`) — central artifact. Tree-as-code; agents emit YAML diffs, BA applies via PR.

```yaml
product: faion-checkout
persona: returning_shopper
outcome:
  metric: completed_checkout_rate
  baseline: 0.62
  target: 0.78
backbone:
  - id: act_browse
    verb: "Browse what's available"
    tasks:
      - id: tsk_search
        title: "Search by keyword"
        stories:
          - id: STR-101
            user: returning_shopper
            want: "search by keyword"
            so_that: "I find a product fast"
            release: R1
            size: M
            ac_ref: AC-101
            status: ready
            depends_on: []
            enabler: false
      - id: tsk_filter
        title: "Filter results"
        stories:
          - id: STR-104
            release: R2
            size: M
  - id: act_pay
    verb: "Pay for the order"
    tasks:
      - id: tsk_card
        stories:
          - id: STR-201
            release: R1
            size: L
            depends_on: [STR-090]   # auth enabler
releases:
  R1:
    name: walking_skeleton
    sprints: 3
    capacity_points: 90
    walking_skeleton: true
  R2:
    name: enhanced_checkout
    sprints: 4
    capacity_points: 120
```

Markdown matrix (renderer output) — what stakeholders read:

```markdown
# Story Map: faion-checkout / returning_shopper

| Browse | Choose | Pay | Receive | Resolve |
|--------|--------|-----|---------|---------|
| **R1** STR-101 search | **R1** STR-150 PDP | **R1** STR-201 card | **R1** STR-301 status | **R1** STR-401 contact |
| **R2** STR-104 filter | **R2** STR-152 compare | **R2** STR-205 saved card | **R2** STR-303 push | **R2** STR-405 returns |
| **R3** STR-108 voice  | **R3** STR-156 reviews | **R3** STR-209 wallet | **R3** STR-306 ETA | **R3** STR-409 chat |

Walking-skeleton coverage: 5/5 activities. Capacity: 87/90 points used. Zero unresolved enablers.
```

Map → Jira sync (`scripts/map_to_jira.py`, ~45 lines):

```python
import sys, yaml, os, requests
from pathlib import Path

JIRA = os.environ["JIRA_URL"]
AUTH = (os.environ["JIRA_USER"], os.environ["JIRA_TOKEN"])
PROJECT = os.environ["JIRA_PROJECT"]

def upsert(issue_type, summary, parent_key=None, labels=None, story_id=None):
    payload = {
        "fields": {
            "project": {"key": PROJECT},
            "summary": summary,
            "issuetype": {"name": issue_type},
            "labels": labels or [],
        }
    }
    if parent_key:
        payload["fields"]["parent"] = {"key": parent_key}
    if story_id:
        payload["fields"]["labels"].append(f"map:{story_id}")
    r = requests.post(f"{JIRA}/rest/api/3/issue", json=payload, auth=AUTH, timeout=30)
    r.raise_for_status()
    return r.json()["key"]

def main(map_path: str):
    m = yaml.safe_load(Path(map_path).read_text())
    diff = []
    for act in m["backbone"]:
        epic_key = upsert("Epic", act["verb"], labels=[f"activity:{act['id']}"])
        diff.append(("epic", act["id"], epic_key))
        for tsk in act.get("tasks", []):
            for s in tsk.get("stories", []):
                key = upsert(
                    "Story",
                    f"As a {s.get('user','user')}, I want {s.get('want','...')} so that {s.get('so_that','...')}",
                    parent_key=epic_key,
                    labels=[f"task:{tsk['id']}", f"release:{s.get('release','TBD')}"],
                    story_id=s["id"],
                )
                diff.append(("story", s["id"], key))
    Path("jira-sync.diff.json").write_text(__import__("json").dumps(diff, indent=2))

if __name__ == "__main__":
    main(sys.argv[1])
```

Cron / scheduled triggers for the BA week:

```
0 9  * * 1   claude run /usm-coverage-audit       # Mon 9am: drift check
0 14 * * 3   claude run /usm-jira-resync          # Wed 2pm: pull Jira state, refresh statuses
0 10 1 * *   claude run /usm-stale-map-prune      # Monthly: archive cold branches
```

## Best practices

- One persona per map. If two personas share a journey, build two maps and merge as a derived "shared backbone" view; never start merged.
- Backbone first, frozen for the cycle — debate and lock activities before adding tasks. Activity churn invalidates everything below.
- Tag enablers explicitly (auth, payment infra, telemetry) and pin them as dependencies of journey stories, not as journey tasks themselves.
- Walking skeleton is a contract — at least one story per backbone activity in R1, all linked to a single outcome metric. If you can't articulate the outcome impact of R1, R1 isn't ready.
- Quote-level provenance for story origin: every story carries `source: interview/STR-091/q42` or `source: ticket/JIRA-1234`. Without this, "why is this in here?" debates eat workshops.
- Vertical slicing > horizontal — slicing off "all of activity 5 for R1" is a feature-factory antipattern. Force thin-slice end-to-end first, fatten later.
- Capacity feasibility is part of the slice — release-slicer must emit "story-points sum / velocity × sprints" and reject overrun.
- Map-as-code: YAML in git, PRs for changes, renderers regenerate Miro/Markdown. The visual surfaces are render targets, never the source of truth.
- Re-run coverage-auditor weekly; workshop output digitized within 24h. A stale map is worse than no map.
- Pair USM with `acceptance-criteria` (Given/When/Then stubs auto-emitted), `use-case-modeling` for compliance trails, `personas` for the persona resolver.
- Token budget: cap activity-extractor and task-grouper at 80k tokens; release-slicer up to 200k for the full map + capacity + dependencies.
- Anonymize customer quotes before they enter the map repo — once it's in git, it's leaked.

## AI-agent gotchas

- Activity-extractor over-fits to feature labels — produces "Search & Browse" instead of "Find a place to stay". Require user-voice verb-phrases; reject noun-only activities.
- Story-rewriter inflates AC — emits 7 scenarios for a 1-point story. Cap at 3 AC scenarios; rest go to `nice_to_have_ac`.
- Persona-resolver collapses personas — "user" becomes the catch-all. Require >=2-feature differential between personas; reject otherwise.
- Release-slicer optimizes for capacity over journey integrity — produces R1 with 87/90 points but missing one backbone activity. Force backbone-coverage as a hard rule.
- Walking-skeleton inflation — opus pads R1 with "delight" stories. Constrain R1 to "minimum to validate outcome metric"; require removal justification per non-essential story.
- Dependency-tagger misses cross-stream enablers (auth, billing, analytics). Seed with a dependency taxonomy: auth, payment, infra, data, compliance, telemetry.
- Jira-syncer overwrites manual edits. Always two-way merge with conflict prompt; never blind overwrite.
- Story duplication — same story under two tasks. Dedup by source-ID + persona before commit.
- Capacity inflation — agent uses "best-week velocity" instead of rolling-3-sprint average. Force capacity input to be a 90-day median.
- Backbone reorder churn — agents reorder activities each run. Pin backbone order as immutable for the cycle; require explicit `unfreeze: true` to reorder.
- Persona drift — new persona spawned for every edge-case story. Persona changes go through `persona-resolver` + BA approval, not as a story-rewrite side-effect.
- Workshop seed bias — pre-populated stickies anchor the room. Keep agent-generated seed under 30% of total; tag them so the room knows what to challenge.
- Outcome amnesia — release-slicer ignores the outcome after first run. Re-pin outcome every prompt; reject slices missing outcome rationale per release.
- Slicing-strategy collapse — agent picks horizontal slicing because it's easier to articulate. Force "first slice must touch >=N-1 backbone activities".

## References

- Jeff Patton — *User Story Mapping: Discover the Whole Story, Build the Right Product* (O'Reilly, 2014). Canonical source. jpattonassociates.com/the-new-backlog.
- Mike Cohn — *User Stories Applied* (2004) for INVEST and AC fundamentals; pair with USM.
- BABOK v3 — Requirements Analysis and Design Definition; map outputs feed BABOK traceability.
- Siblings: `pro/ba/ba-modeling/use-case-modeling/` (compliance trails), `acceptance-criteria/` (AC stubs), `business-process-analysis/` (BPMN feeds backbone).
- Siblings: `solo/sdd/sdd-planning/` (map → spec → tasks bridge), `pro/product/product-manager/` (outcome + roadmap consumer).
- Atlassian Jira REST v3, Linear GraphQL, Miro REST v2 API docs.
- Anthropic Claude Agent SDK — structured outputs + scheduled triggers (`schedule` skill in this repo).
