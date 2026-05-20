---
slug: build-or-waitlist-decision-tree
tier: solo
group: product
domain: product
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Build or Waitlist Decision Tree: codified product-management practice that turns the recurring 'p1-solo-saas-builder/New feature scoping session (per-feature, on demand)' decision into a repeatable, auditable artefact.
content_id: "d4f0bdce059d5aa8"
tags: [build-or-waitlist-decision-tree, product, solo]
---
# Build or Waitlist Decision Tree

## Summary

**One-sentence:** Build or Waitlist Decision Tree: codified product-management practice that turns the recurring 'p1-solo-saas-builder/New feature scoping session (per-feature, on demand)' decision into a repeatable, auditable artefact.

**One-paragraph:** Build or Waitlist Decision Tree addresses the gap identified by the p1-solo-saas-builder/New feature scoping session (per-feature, on demand) playbook: Solo builders chronically over-build; need a hard gate that demands waitlist signal before code; nothing chains mom-test → micro-MVP today. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of p1-solo-saas-builder/New feature scoping session (per-feature, on demand) OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == solo or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the p1-solo-saas-builder/New feature scoping session (per-feature, on demand) task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/product-manager` | parent role skill — provides the operating context for this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 4 testable rules: r1-bound-scope, r2-typed-input, r3-named-owner, r4-versioned | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | Template fill, bounded transformation |
| `synthesize_decision` | sonnet | Per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | Cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/build-or-waitlist-decision-tree.json` | JSON schema for the Build or Waitlist Decision Tree output contract |
| `templates/build-or-waitlist-decision-tree.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-build-or-waitlist-decision-tree.py` | Enforce Build or Waitlist Decision Tree output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `solo/product/`
- upstream playbook: `p1-solo-saas-builder/New feature scoping session (per-feature, on demand)`
