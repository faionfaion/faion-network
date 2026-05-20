---
slug: stripe-webhook-hardening
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "af330e78321b533b"
summary: "Stripe Webhook Hardening: produces a versioned, owner-signed artefact that closes the gap 'p1-solo-saas-builder/Pre-launch hardening: vibe-coded MVP → safe-to-bill production'."
tags: [stripe-webhook-hardening, dev, solo]
---
# Stripe Webhook Hardening

## Summary

**One-sentence:** Stripe Webhook Hardening: produces a versioned, owner-signed artefact that closes the gap 'p1-solo-saas-builder/Pre-launch hardening: vibe-coded MVP → safe-to-bill production'.

**One-paragraph:** Addresses the gap surfaced by 'p1-solo-saas-builder/Pre-launch hardening: vibe-coded MVP → safe-to-bill production': Existing solo/launch-operations/stripe-integration-basics is a happy-path setup playbook. Missing: signature verification, idempotency keys, replay-attack defence, webhook retry semantics. Skipping these breaks billing in production. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a stripe webhook hardening artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'p1-solo-saas-builder/Pre-launch hardening: vibe-coded MVP → safe-to-bill production' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == solo or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working stripe webhook hardening artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'p1-solo-saas-builder/Pre-launch hardening: vibe-coded MVP → safe-to-bill production' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/dev` | parent domain group — provides operating context for Stripe Webhook Hardening |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules grounded in the cited gap | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | template fill, bounded transformation |
| `synthesize_decision` | sonnet | per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/stripe-webhook-hardening.json` | JSON schema for the Stripe Webhook Hardening output contract |
| `templates/stripe-webhook-hardening.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-stripe-webhook-hardening.py` | Enforce Stripe Webhook Hardening output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `solo/dev/`
- upstream playbook: `p1-solo-saas-builder/Pre-launch hardening: vibe-coded MVP → safe-to-bill production`
- solo/dev/p1-solo-saas-builder
