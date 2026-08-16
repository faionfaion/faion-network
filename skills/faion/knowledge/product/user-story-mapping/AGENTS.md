# User Story Mapping

## Summary

**One-sentence:** Build a user story map (backbone of activities → user tasks → stories), slice the map into MVP / Release-1 / Release-2 horizontally so scope decisions are visible and shippable.

**One-paragraph:** Replaces flat backlogs with a 2-D map: the horizontal axis is the user journey (left → right), the vertical axis is alternative stories per task (top → bottom). A horizontal slice across the map is a coherent release. Visible scope-cutting beats invisible deprioritisation in a flat list.

**Ефективно для:**

- Solo PM with a feature touching ≥2 user steps and ≥1 dev-week of scope — needs a visual artefact to decide what ships in v1 without losing the bigger journey.
- Solo founders who need a defensible artefact to hold a line under stakeholder pressure.
- Teams syncing outcome work across PM, design and engineering before sprint planning.
- Rescuing a flat backlog that has lost its journey context.

## Applies If (ALL must hold)

- Feature spans ≥3 user activities and benefits from a 2-D view.
- Scope cuts will happen and need to be visible to stakeholders.
- Team includes ≥1 designer / engineer who needs the journey context.
- An MVP or walking skeleton has to be identified out of a larger scope.

## Skip If (ANY kills it)

- Single-step feature (a setting, a flag, a fix) or a single-screen UI — a story map is overkill.
- Pure technical work (refactor, infra) — there is no user-facing backbone.
- Pre-discovery — user journey not validated; run journey-mapping or JTBD first.
- Solo dev shipping a 1-day change.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| User persona | markdown | Research |
| Journey hypotheses | list | Discovery output |
| Capacity available for v1 | estimate | Team plan |
| Backlog or feature list | ticket export | Backlog tool |
| Workshop participants | PM + design + eng | Team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/product-planning/mvp-scoping` | Capacity constraints that drive the v1 slice. |
| `solo/product/product-manager/spec-writing` | Downstream artefact for each prioritised story. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules + skip + run rules | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + 6 forbidden patterns | 1000 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns with symptom + root-cause + fix | 1100 |
| `content/04-procedure.xml` | essential | 6-step procedure: frame → backbone → tasks → stories → skeleton → slices | 1000 |
| `content/05-examples.xml` | essential | Two worked examples, one with a concrete backbone | 900 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-user-story-mapping` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-user-story-mapping` | haiku | Schema check + threshold checks; deterministic. |
| `review-user-story-mapping` | opus | Cross-cycle synthesis; high-stakes change to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/user-story-mapping.json` | JSON skeleton conforming to the output contract schema. |
| `templates/user-story-mapping.md.j2` | Markdown skeleton for human-readable artefact rendering. |
| `templates/user-story-mapping.md` | Markdown skeleton for human-readable artefact rendering. Generated from `templates/user-story-mapping.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/story-map.md.j2` | Story-map worksheet: context, backbone, walking skeleton, release slices, parking lot. |
| `templates/story-map.md` | Story-map worksheet: context, backbone, walking skeleton, release slices, parking lot. Generated from `templates/story-map.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/story-card.md.j2` | Single story card: placement, story frame, acceptance criteria, error path, size. |
| `templates/story-card.md` | Single story card: placement, story frame, acceptance criteria, error path, size. Generated from `templates/story-card.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/storymap-check.py` | Checks one-task-per-activity skeleton coverage and full-backbone release spans (stdin JSON). |
| `templates/validate-story-map.py` | Checks backbone size, task→backbone referential integrity and skeleton coverage (YAML input). |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-user-story-mapping.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[mvp-scoping]]
- [[spec-writing]]
- [[release-planning]] — release slices feed the release plan.

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/user-story-mapping.json`

```json
{
  "artefact_id": "user-story-mapping-example",
  "version": "1.0.0",
  "last_reviewed": "2026-05-23",
  "persona": "persona value",
  "backbone": [
    "Sign up",
    "Create Project",
    "Invite Teammate",
    "Track Task",
    "Close Project"
  ],
  "tasks": [
    "magic-link signup",
    "blank project",
    "email invite",
    "plain task list",
    "one-click close"
  ],
  "walking_skeleton": [
    "magic-link signup",
    "blank project",
    "email invite",
    "plain task list",
    "one-click close"
  ],
  "release_slices": [
    "walking-skeleton",
    "release-1",
    "later"
  ],
  "owner": "@solo-founder"
}
```
