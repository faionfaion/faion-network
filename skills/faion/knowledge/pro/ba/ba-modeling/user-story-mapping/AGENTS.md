---
slug: user-story-mapping
tier: pro
group: ba
domain: ba
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Arrange stories along horizontal user-journey activities + vertical priority bands (R1 walking skeleton through R4 nice-to-have) as YAML-in-git for release planning.
content_id: "c615a84e28b6c652"
complexity: medium
produces: spec
est_tokens: 4000
tags: [user-story-mapping, release-planning, agile, user-journey, backlog]
---
# User Story Mapping

## Summary

**One-sentence:** Arrange stories along horizontal user-journey activities + vertical priority bands (R1 walking skeleton through R4 nice-to-have) as YAML-in-git for release planning.

**One-paragraph:** Story-map output is a 2-D YAML structure: x-axis is the user journey (activities → tasks), y-axis is release bands (R1 = walking skeleton; R2-R4 = enhancements). Map lives in git as canonical source; renderers produce Markdown, Mermaid, and Miro outputs. Output is a `spec` for release planning: thin R1 slice plus traceable backlog items.

**Ефективно для:**

- Pre-roadmap scope conversation: спостерігати walking skeleton + R2-R4 slices.
- Auditing flat Jira backlog для журнейних gaps.
- Migration / replatform — current journey overlay → target journey.
- Stakeholder workshop prep — draft map як стартова точка.

## Applies If (ALL must hold)

- Flat backlog of 50-500 items lacks journey context.
- 3-6 month roadmap needs walking-skeleton release cut.
- Personas + goals exist but scope is undefined.
- Cross-functional team will reference the map for release planning.

## Skip If (ANY kills it)

- Single-feature work (one screen, one form).
- API-only service with no end-user journey.
- Hard-deadline regulated work with scope fixed by regulation.
- Pre-PMF zero-to-one where the journey changes weekly.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Persona list | Markdown / YAML | UX |
| Goal statements | Markdown | product |
| Existing backlog (if any) | CSV / Jira export | product |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[use-case-modeling]] | Downstream — story-map nodes become use-case backlog titles |
| [[acceptance-criteria]] | Downstream — R1 stories receive AC first |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: walking-skeleton R1 has end-to-end story per activity, persona-tagged, YAML-in-git canonical, ≤8 activities, vertical bands fixed | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema + examples | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: feature-list masquerading as map, R1 not walking, persona collapse, prose journey | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure | 700 |
| `content/06-decision-tree.xml` | essential | Routing on map shape | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `journey_extraction` | sonnet | Synthesize activities from interviews + backlog. |
| `r1_slicing` | opus | Walking-skeleton cut requires careful goal coverage. |
| `yaml_emit` | haiku | Mechanical emission of YAML structure. |

## Templates

| File | Purpose |
|------|---------|
| `templates/story-map.yaml` | Canonical YAML skeleton (activities → tasks → stories with release band) |
| `templates/_smoke-test.yaml` | Minimum viable filled map |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-user-story-mapping.py` | Validate map against output-contract | Pre-commit; before roadmap review |

## Related

- [[use-case-modeling]]
- [[acceptance-criteria]]
- [[business-process-analysis]]
- [[ba-planning]]

## Decision tree

See `content/06-decision-tree.xml`. Routes on map shape (R1 walking? persona-tagged? ≤8 activities?) to the rule firing.
