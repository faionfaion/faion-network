---
slug: process-mining-tool-shortlist
tier: pro
group: ba
domain: ba
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "e3d17412d98920b8"
summary: Process Mining Tool Shortlist — pinned shortlist for the business analyst: fixed shape + named owner + evidence anchors + outcome review, so process improvement initiative (8 weeks) stops being folklore and starts being a reviewable operating tool.
tags: [ba, pro, shortlist, process, mining, tool]
---
# Process Mining Tool Shortlist

## Summary

**One-sentence:** Process Mining Tool Shortlist — pinned shortlist for the business analyst: fixed shape + named owner + evidence anchors + outcome review, so process improvement initiative (8 weeks) stops being folklore and starts being a reviewable operating tool.

**One-paragraph:** In business analysis, the business analyst runs process improvement initiative (8 weeks) on a recurring cadence — but the corpus only covers the upstream concepts, not the artefact that closes the loop. 'process-mining-automation' exists but is conceptual. BAs picking between Celonis / UiPath Process Mining / Disco / open-source need a practical comparison and decision criteria. `process-mining-tool-shortlist` pins the artefact: a fixed shape, named owner, evidence anchors, and a published review cadence. It is loaded when the business analyst starts the block named in the trigger and produces a committed artefact reviewed against outcomes at the next iteration. Mechanism: rule-bound output contract + per-application evidence + outcome review. Primary output: a versioned, owned, evidence-anchored shortlist committed to the team's knowledge space.

## Applies If (ALL must hold)

- the block this methodology unblocks is on the operating cadence: - `role-business-analyst/Process improvement initiative (8 weeks)`
- the business analyst owns the artefact (or escalates ownership to a named role).
- the team uses a version-controlled or wiki-style space where the artefact lives.
- the methodology's trigger event fires at a published cadence (event, threshold, or schedule).

## Skip If (ANY kills it)

- one-shot work with no recurrence — write a single doc, not a versioned artefact.
- team has < 3 instances per year — the review cadence costs more than it returns.
- regulated context that mandates a different shape (use the regulator's template instead).
- no named owner is available — defer until ownership is resolved; an anonymous artefact rots.

## Prerequisites

- access to the repository / knowledge space that will host the artefact.
- a named owner accountable for refresh and outcome review.
- the upstream methodologies in `Assumes Loaded` are already routine for the business analyst.
- the trigger event is observable (alert, ticket, calendar slot, threshold crossing).

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ba/<upstream-canon>` | Upstream concept; this methodology consumes its output without re-teaching it. |
| `solo/sdd/sdd/sdd-document-templates` | Document-as-code conventions; artefact lives in the team's SDD space. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules — fixed shape, evidence anchors, named owner, version + last_reviewed, outcome review | ~1000 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, self-check checklist | ~700 |
| `content/03-failure-modes.xml` | essential | 6 known failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-artefact` | haiku | Template fill from header + section list, low cost. |
| `populate-evidence-fields` | sonnet | Per-section judgment: select correct evidence, summarise without losing specifics. |
| `outcome-review-synthesis` | opus | Cross-cycle synthesis: does the artefact change behaviour? |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | Canonical section list with `not_applicable: <reason>` markers per section. |
| `templates/header.yaml` | Frontmatter schema: owner, version, last_reviewed, evidence_root. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-fill.py` | Validate that filled artefact matches canonical schema + carries evidence links | Pre-merge |
| `scripts/staleness-check.py` | Flag artefacts whose `last_reviewed` exceeds the published window | Weekly cron |

## Related

- parent skill: `pro/ba/`
- peer methodology: `<related-canonical-from-the-corpus>`
- external: see Christensen, Gawande, Kahneman, Allspaw and the empirical sources cited in `content/01-core-rules.xml`.
