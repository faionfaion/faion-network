---
slug: supabase-rls-audit-checklist
tier: solo
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "89a6670f5cb381fd"
summary: "Supabase Rls Audit Checklist: produces a versioned, owner-signed artefact that closes the gap 'p1-solo-saas-builder/Pre-launch hardening: vibe-coded MVP → safe-to-bill production'."
tags: [supabase-rls-audit-checklist, infra, solo]
---
# Supabase Rls Audit Checklist

## Summary

**One-sentence:** Supabase Rls Audit Checklist: produces a versioned, owner-signed artefact that closes the gap 'p1-solo-saas-builder/Pre-launch hardening: vibe-coded MVP → safe-to-bill production'.

**One-paragraph:** Addresses the gap surfaced by 'p1-solo-saas-builder/Pre-launch hardening: vibe-coded MVP → safe-to-bill production': Supabase is the default stack for this ICP. There is no Supabase methodology anywhere in solo. RLS misconfiguration is the #1 leak vector for vibe-coded SaaS. Must exist at solo tier. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a supabase rls audit checklist artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'p1-solo-saas-builder/Pre-launch hardening: vibe-coded MVP → safe-to-bill production' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == solo or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working supabase rls audit checklist artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'p1-solo-saas-builder/Pre-launch hardening: vibe-coded MVP → safe-to-bill production' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/infra/infra` | parent domain group — provides operating context for Supabase Rls Audit Checklist |

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
| `templates/supabase-rls-audit-checklist.json` | JSON schema for the Supabase Rls Audit Checklist output contract |
| `templates/supabase-rls-audit-checklist.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-supabase-rls-audit-checklist.py` | Enforce Supabase Rls Audit Checklist output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `solo/infra/`
- upstream playbook: `p1-solo-saas-builder/Pre-launch hardening: vibe-coded MVP → safe-to-bill production`
- solo/infra/p1-solo-saas-builder
