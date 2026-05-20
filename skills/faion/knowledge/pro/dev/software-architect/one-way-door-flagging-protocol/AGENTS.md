---
slug: one-way-door-flagging-protocol
tier: pro
group: dev
domain: software-architect
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "6962551855d94354"
summary: An explicit decision-time protocol that flags each architecture choice as one-way-door (irreversible within 6 months without significant cost) vs two-way-door, gating one-way doors behind a heavier review path while letting two-way doors ship at velocity.
tags: [architecture, decision-making, adr, reversibility, two-way-door, amazon]
---

# One-Way-Door Flagging Protocol

## Summary

**One-sentence:** Tag every architecture decision as one-way-door or two-way-door at the moment of decision, route the two classes through different review paths, and capture the classification in the ADR header so future readers see the intended reversibility.

**One-paragraph:** Reversibility is the second most-cited driver of architecture regret (after "we did not consider scale"). Most teams implicitly know some choices are irreversible (vendor lock-in, data-model migration, public API surface) and others are easily reversible (logging format, internal naming, route handler structure), but the distinction lives in tribal knowledge instead of the ADR itself. The flagging protocol formalises the call: every ADR opens with `decision_class: one-way-door | two-way-door`, the writer justifies the call in one paragraph, and the two classes route through different review paths. One-way doors get a 48h cooldown, a named devil's-advocate reviewer, and a documented rollback estimate. Two-way doors ship with the standard PR-review path. Primary output: a `decision_class` field in every ADR, plus a quarterly review of misclassified decisions for calibration.

## Applies If (ALL must hold)

- team uses ADRs (Architecture Decision Records) or an equivalent structured decision log
- team makes ≥ 2 architecturally-meaningful decisions per quarter
- engineering leader has authority to enforce a heavier review path for irreversible decisions
- team has experienced at least one architecture regret in the past 12 months (any team past Year 2 has)

## Skip If (ANY kills it)

- team has no ADR habit — establish ADRs first (`pro/dev/software-architect/adr-staleness-audit` is the right starting point)
- single-engineer codebase — the protocol's value is in the review-path differentiation; with one engineer there is no second reviewer
- prototype phase pre-customer — reversibility is cheap by definition, premature gating slows learning
- regulated environment where every architecture change is already gated by external compliance — apply compliance first, this protocol second

## Prerequisites

- ADR template in use (markdown or otherwise) with consistent header structure
- one engineer designated as the protocol owner (typically tech lead or principal engineer)
- a definition of "significant cost" for the team — typically engineer-weeks-to-reverse, customer-facing-impact, or vendor-contractual-exit-clauses

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/software-architect/adr-staleness-audit` | ADRs are the carrier for the decision_class flag |
| `pro/dev/software-architect/quality-attributes-analysis` | Quality-attribute analysis often surfaces the reversibility dimension |
| `solo/dev/software-architect/strangler-fig-playbook-vendor` | Strangler-fig is the standard reversal pattern for one-way doors that turn out to be wrong |

## Content

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: explicit class, cooldown for one-way, devil's-advocate reviewer, rollback estimate, quarterly miscall review | ~900 |
| `content/02-output-contract.xml` | essential | ADR header schema with decision_class field, reversal-estimate schema | ~600 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: every-decision-flagged-two-way, no rollback estimate, after-the-fact reclassification, etc. | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify_decision_one_way_or_two_way` | sonnet | Cross-input judgment from problem statement and proposed solution |
| `estimate_reversal_cost` | sonnet | Per-decision bounded estimation in engineer-weeks |
| `identify_devils_advocate_reviewer` | haiku | Lookup based on domain expertise tags |
| `quarterly_miscall_review` | opus | Cross-decision synthesis: which class did we get wrong, what is the calibration error |

## Templates

| File | Purpose |
|------|---------|
| `templates/adr-template-with-class.md` | ADR template with the decision_class field and reversal-estimate paragraph wired in |
| `templates/one-way-door-checklist.md` | Pre-cooldown checklist (rollback plan, vendor exit clause, customer migration cost, public API surface impact) |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/adr-classify-lint.py` | Pre-commit hook that rejects ADRs without the decision_class field set | On every ADR PR |
| `scripts/miscall-review.py` | Reads ADRs from the past quarter, surfaces any decision whose actual reversal effort diverged from the original estimate by &gt;= 2x | Quarterly |

## Related

- parent skill: `pro/dev/software-architect/SKILL.md`
- peer methodologies: `pro/dev/software-architect/adr-staleness-audit`, `pro/dev/software-architect/quality-attributes-analysis`
- external: [Bezos 1997 letter, two-way door framing] · [Michael Nygard, Documenting Architecture Decisions (2011)] · [Pais and Skelton, Team Topologies Chapter 5 (IT Revolution, 2019)]
