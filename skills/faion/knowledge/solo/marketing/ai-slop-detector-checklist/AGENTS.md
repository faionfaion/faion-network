---
slug: ai-slop-detector-checklist
tier: solo
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Ai Slop Detector Checklist: codified growth-marketing practice that turns the recurring 'role-growth-marketing/Blog post brief → AI draft → human polish (per-post)' decision into a repeatable, auditable artefact.
content_id: "247afaad15f2fcc1"
tags: [ai-slop-detector-checklist, marketing, solo]
---
# Ai Slop Detector Checklist

## Summary

**One-sentence:** Ai Slop Detector Checklist: codified growth-marketing practice that turns the recurring 'role-growth-marketing/Blog post brief → AI draft → human polish (per-post)' decision into a repeatable, auditable artefact.

**One-paragraph:** Ai Slop Detector Checklist addresses the gap identified by the role-growth-marketing/Blog post brief → AI draft → human polish (per-post) playbook: Direct pain point in the unit context. AI drafts ship to prod with hedging, generic intros, zero original signal — Google and humans both notice. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of role-growth-marketing/Blog post brief → AI draft → human polish (per-post) OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == solo or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the role-growth-marketing/Blog post brief → AI draft → human polish (per-post) task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/marketing/marketing-manager` | parent role skill — provides the operating context for this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: r1-bound-scope, r2-typed-input, r3-named-owner, r4-versioned, r5-llm-grounding | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | Template fill, bounded transformation |
| `synthesize_decision` | sonnet | Per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | Cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/ai-slop-detector-checklist.json` | JSON schema for the Ai Slop Detector Checklist output contract |
| `templates/ai-slop-detector-checklist.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-slop-detector-checklist.py` | Enforce Ai Slop Detector Checklist output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `solo/marketing/`
- upstream playbook: `role-growth-marketing/Blog post brief → AI draft → human polish (per-post)`
- external: [RAGAS](https://docs.ragas.io/) · [Anthropic agent design](https://docs.anthropic.com/en/docs/build-with-claude/agents)
