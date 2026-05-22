---
slug: program-dependency-aging-chart-recipe
tier: geek
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: "Builds a program-dependency aging chart (count-of-blocked-tasks vs days-since-dependency-opened) so program managers spot dependency rot before milestones slip."
content_id: "4e9c06763e0e4c2d"
complexity: medium
produces: report
est_tokens: 3500
tags: [pm, program, dependency, aging-chart, multi-team]
---
# Program Dependency Aging Chart Recipe

## Summary

**One-sentence:** Builds a program-dependency aging chart (count-of-blocked-tasks vs days-since-dependency-opened) so program managers spot dependency rot before milestones slip.

**One-paragraph:** Builds a program-dependency aging chart (count-of-blocked-tasks vs days-since-dependency-opened) so program managers spot dependency rot before milestones slip. The methodology is anchored to a single named consumer (a PM, EM, portfolio owner, or downstream agent) and a fixed-shape artefact that downstream review can sign off without re-deriving reasoning. Inputs are explicit, evidence is anchored, and the artefact carries `version`, `owner`, and `last_reviewed` so it remains a living operating tool rather than folklore. Outputs that fail the contract are rejected at validation time, not at executive review.

**Ефективно для:** Програмному PM-у — щоб залежність, яка 'тихо лежить' три тижні, не зривала milestone у 6-му.

## Applies If (ALL must hold)

- Program involves ≥3 teams with documented cross-team dependencies.
- A typed dependency graph exists (or the dependency-graph-reasoning methodology runs).
- Weekly checkpoint cadence is in place.
- A named program PM owns the chart.

## Skip If (ANY kills it)

- Single-team project — aging chart adds no signal.
- No dependency graph — chart has nothing to age.
- Cadence is less than monthly — aging signal will be too late.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Dependency graph file | JSON/Mermaid | dependency-graph-reasoning output |
| Tracker dependency timestamps | API | Jira / Linear / GitHub Projects |
| Weekly checkpoint slot | calendar | program rituals |
| Named program PM | person | delivery-org |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/pm/dependency-graph-reasoning` | Source of the typed dependency graph. |
| `geek/pm/okr-cascade-team-to-company` | Cross-team OKR dependencies surface here too. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules every application enforces | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + self-check | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom / root-cause / fix | ~900 |
| `content/06-decision-tree.xml` | essential | Root question → branches → conclusions (rule refs) | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `age-band-compute` | haiku | Pure age math against graph timestamps. |
| `remediation-action-pick` | sonnet | Bounded judgement per edge. |
| `ritual-narrative` | opus | Cross-band synthesis for program review. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | Aging chart artefact skeleton: chart image link + table of edges by age band + remediation actions per band. |
| `templates/header.yaml` | Frontmatter contract: owner, version, last_reviewed for the produced artefact. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-program-dependency-aging-chart-recipe.py` | Validate produced artefact against the JSON Schema in `02-output-contract.xml`. | Pre-merge and on every artefact refresh. |

## Related

- [[dependency-graph-reasoning]]
- [[okr-cascade-team-to-company]]
- [[portfolio-evm-rollup-method]]

## Decision tree

The mandatory decision tree at `content/06-decision-tree.xml` Decides whether to plot the chart weekly (graph + ≥3 teams + weekly cadence + PM), block (no graph), or skip (single team / sparse cadence). Run before the chart is added to the program ritual.
