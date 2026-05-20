---
slug: fixed-price-vs-tnm-decision-framework
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "47f6e7cb8e2f80f6"
summary: Fixed Price Vs Tnm Decision Framework delivers a concrete, testable methodology that turns the recurring task of 'Fixed-Price vs T&M Estimation with AI Risk Buffer' into an auditable artefact, addressing the gap: Decision rule (when does fixed-price burn margin, when does T&M los
tags: [pm, pro, decision, methodology]
---
# Fixed Price Vs Tnm Decision Framework

## Summary

**One-sentence:** Fixed Price Vs Tnm Decision Framework delivers a concrete, testable methodology that turns the recurring task of 'Fixed-Price vs T&M Estimation with AI Risk Buffer' into an auditable artefact, addressing the gap: Decision rule (when does fixed-price burn margin, when does T&M lose the deal) is craft knowledge today. A methodology with trigger checklist + margin-model template would directly raise win-rate for outsource specialists.

**One-paragraph:** Decision rule (when does fixed-price burn margin, when does T&M lose the deal) is craft knowledge today. A methodology with trigger checklist + margin-model template would directly raise win-rate for outsource specialists. Fixed Price Vs Tnm Decision Framework closes this gap with a small set of hard rules, a strict output contract, and a failure-mode catalogue tuned for LLM-assisted execution. The methodology is anchored to the triggering work 'Fixed-Price vs T&M Estimation with AI Risk Buffer' (p4-outsource-specialist, pro tier). It produces a structured artefact that a downstream agent or human reviewer can sign off without re-deriving the reasoning.

## Applies If (ALL must hold)

- The triggering activity 'Fixed-Price vs T&M Estimation with AI Risk Buffer' (role: p4-outsource-specialist) is in your current workload at least once per cycle.
- You have authority to act on the artefact this methodology produces (write access, sign-off rights).
- A named consumer exists for the artefact — human reviewer OR downstream agent.
- An auditable source-of-truth is available for the inputs the methodology needs.

## Skip If (ANY kills it)

- One-off, never-to-repeat work — methodology overhead does not pay back.
- No named consumer — artefact will be orphaned regardless of quality.
- Cannot access the input source-of-truth (system down, access denied) — paraphrased substitutes are worse than skipping.

## Prerequisites

- Read access to the systems / dashboards / docs that feed the methodology's inputs.
- A storage location for the produced artefact (git repo, doc, ticket) where the consumer can read it.
- Prior cycle's artefact (if any) accessible for carry-forward and trend comparison.

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies) |
| `pro/sdd/AGENTS.md` if present | SDD discipline for the artefact lifecycle (status flow, owners, review) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 3 testable rules every application enforces | ~900 |
| `content/02-output-contract.xml` | essential | Required output schema, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 5 detector + repair clauses for known agent failures | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `fixed_price_vs_tnm_decision_framework_template_fill` | haiku | Template fill, no judgment |
| `fixed_price_vs_tnm_decision_framework_evidence_check` | sonnet | Bounded comparison + judgment |
| `fixed_price_vs_tnm_decision_framework_synthesis` | opus | Cross-input synthesis + final write-up |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema for the methodology's required output |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-output.py` | Enforce the output-contract before main agent accepts | After subagent returns, before commit/publish |

## Related

- parent skill: `pro/pm/` (see neighbouring methodologies)
- triggering activity: `p4-outsource-specialist/Fixed-Price vs T&M Estimation with AI Risk Buffer`
- external: industry references cited inline in `content/01-core-rules.xml`
