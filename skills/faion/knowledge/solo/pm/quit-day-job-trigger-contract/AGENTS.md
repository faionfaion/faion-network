---
slug: quit-day-job-trigger-contract
tier: solo
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
content_id: "294a1c0e4e91f7ae"
summary: Pre-commitment contract that names the exact quit-day-job trigger (numeric, dated, named owner) and the reversal clause — so the $0→$4k MRR bootstrap stops being folklore.
complexity: light
produces: decision-record
est_tokens: 3400
tags: [pm, solo, quit, day, job, trigger, contract]
---
# Quit Day Job Trigger Contract

## Summary

**One-sentence:** A pre-commitment artefact that defines the exact numeric trigger to quit the day job, the named owner accountable for executing it, the evidence anchors used to verify the trigger fires, and the reversal clause.

**One-paragraph:** The bootstrap journey ($0→$4k MRR while keeping the day job) collapses into folklore without an artefact that names the trigger and the reversal. This methodology pins a contract with five fields — trigger (numeric, dated, named — not "when needed"), output shape (bounded), evidence anchors, named owner, outcome review cadence — so the solo SaaS builder has a reviewable instrument instead of a feeling. Output is a versioned contract committed to the team's knowledge space.

**Ефективно для:**

- Solo SaaS builder approaching the $4K MRR full-time leap.
- Pre-commitment device that pairs with the financial-runway model.
- Documenting the reversal clause (when to return to a day job) before the decision is emotional.
- Quarterly review of the contract against actual MRR + savings trajectory.

## Applies If (ALL must hold)

- Solo SaaS builder running a $0→$4k MRR bootstrap journey.
- Solo SaaS builder owns the artefact (or escalates ownership to a named role).
- Team uses a version-controlled or wiki-style space where the artefact lives.
- The trigger event is observable (alert, ticket, dashboard threshold, calendar slot).

## Skip If (ANY kills it)

- One-shot work with no recurrence — write a single decision doc, not a versioned artefact.
- Builder has &lt; 3 trigger checks per year — review cadence costs more than it returns.
- Regulated context that mandates a different shape — use the regulator's template.
- No named owner — defer until ownership is resolved; an anonymous artefact rots.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Access to the repository / wiki hosting the contract | repo path | platform |
| Named owner accountable for refresh + outcome review | identity | builder |
| Runway model + MRR dashboard | artefacts | builder |
| Defined trigger event (numeric threshold + date window) | spec | builder |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[side-project-financial-runway]] | Runway model feeds the trigger and reversal clause. |
| [[solo-mrr-dashboard-template]] | Canonical MRR is the numeric trigger input. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules — explicit trigger, bounded output, evidence-anchored, named owner, iteration loop | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for the contract artefact + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 6 known failure modes with detector + repair | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold_contract` | haiku | Template fill from header + section list. |
| `populate_evidence` | sonnet | Per-section judgement: select correct evidence, summarise. |
| `outcome_review_synthesis` | opus | Cross-cycle synthesis: does the contract change behaviour? |

## Templates

| File | Purpose |
|------|---------|
| `templates/contract-skeleton.md` | Canonical contract sections (trigger / reversal / evidence / owner / review) |
| `templates/header.yaml` | Frontmatter schema: owner, version, last_reviewed, evidence_root |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-quit-day-job-trigger-contract.py` | Validate the filled contract against 02-output-contract schema | Pre-merge + quarterly review |

## Related

- [[side-project-financial-runway]]
- [[solo-mrr-dashboard-template]]
- [[solo-burnout-tripwires]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes by trigger specificity, output shape, evidence presence, owner naming, and review staleness onto a rule from `content/01-core-rules.xml`. Walk it on every quarterly review.
