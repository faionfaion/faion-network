---
slug: workflow-design-phase
tier: solo
group: sdd
domain: sdd
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates the design.md artefact for an approved spec.md — file table, AD-X decisions, data models, API contracts, testing strategy, dependency graph.
content_id: "18a3ac3705b45aa8"
complexity: deep
produces: spec
est_tokens: 4500
tags: [sdd, workflow, design, planning, architecture-decisions]
---
# Workflow: Design Phase

## Summary

**One-sentence:** Generates the design.md artefact for an approved spec.md — file table, AD-X decisions, data models, API contracts, testing strategy, dependency graph.

**One-paragraph:** Step-by-step procedure for the SDD design phase. Reads the approved spec, surveys the existing codebase, makes architectural decisions (AD-X) with rationale and rejected alternatives, drafts a file table (CREATE / MODIFY / DELETE), data models, API contracts, and testing strategy. Output is an Accepted design.md ready to feed `writing-implementation-plans`. All decisions are traceable to FR-X from the spec.

**Ефективно для:**

- паст-готова основа для повторюваної задачі 'design-phase authoring' — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Approved spec.md exists (status: Accepted) for the feature.
- The feature needs a technical blueprint before coding starts (≥3 components or non-trivial data flow).
- The codebase has patterns that new work must follow — surveying is required.
- 2+ architectural options exist with real trade-offs that need an AD-X record.

## Skip If (ANY kills it)

- Spec is still Draft or unapproved — design decisions will be based on shifting requirements.
- Single-file bugfix or trivial change where a full design doc adds zero value.
- Pure infrastructure tweak (server config, CI knob) with no application-architecture impact.
- Exploratory spike where the goal is learning, not committing to an approach.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Approved spec.md (Accepted status) | markdown | `.aidocs/features/<status>/<feature>/spec.md` |
| Constitution / tech-decisions doc | markdown | `.aidocs/constitution.md` |
| Existing codebase tree | filesystem | repo root |
| Test convention doc | markdown | repo testing guide |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/sdd/sdd-planning/workflow-spec-phase` | Provides the spec.md that this phase consumes. |
| `solo/dev/software-architect/architecture-decision-records` | Defines the AD-X format embedded in design.md. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology fallback | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the design.md frontmatter + valid/invalid/forbidden examples | ~900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom + root-cause + fix | ~800 |
| `content/04-procedure.xml` | deep | 7-step procedure: load spec → survey codebase → draft AD-X → file table → data/API → testing → review | ~900 |
| `content/05-examples.xml` | medium | Worked example: design.md for a JWT refresh feature | ~600 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `survey-codebase` | sonnet | Grep/Glob/Read enumeration of existing patterns. |
| `draft-ad-x-decisions` | opus | Multi-option trade-off analysis with rejected alternatives. |
| `compose-file-table` | sonnet | Mechanical mapping of decisions to CREATE/MODIFY/DELETE rows. |
| `reviewer-pass` | opus | Cross-AD consistency + spec coverage audit. |

## Templates

| File | Purpose |
|------|---------|
| `templates/design.md` | Canonical design.md skeleton with AD-X, file table, data models, API contracts, testing sections. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/find-shared-files.py` | Detect implicit task dependencies via shared-file modifications across the file table. | After file-table draft, before promoting design to Accepted. |
| `scripts/validate-workflow-design-phase.py` | Validate the design.md frontmatter against the schema in `content/02-output-contract.xml`. | After subagent returns the design.md, before downstream consumer reads. |

## Related

- [[workflow-spec-phase]]
- [[writing-implementation-plans]]
- [[template-task]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (spec accepted, component count ≥3, trade-off options ≥2) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether to run the full design phase or skip to direct task authoring.
