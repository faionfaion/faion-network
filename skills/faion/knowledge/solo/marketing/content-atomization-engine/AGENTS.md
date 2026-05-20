---
slug: content-atomization-engine
tier: solo
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Content Atomization Engine: codified marketing practice that turns the recurring 'role-growth-marketing/Synthesis: Ship one piece of content into 10 channels with AI-assisted atomization' decision into a repeatable, auditable artefact.
content_id: "6188247bed1e00ed"
tags: [content-atomization-engine, marketing, solo]
---
# Content Atomization Engine

## Summary

**One-sentence:** Content Atomization Engine: codified marketing practice that turns the recurring 'role-growth-marketing/Synthesis: Ship one piece of content into 10 channels with AI-assisted atomization' decision into a repeatable, auditable artefact.

**One-paragraph:** Content Atomization Engine addresses the gap surfaced by 'role-growth-marketing/Synthesis: Ship one piece of content into 10 channels with AI-assisted atomization'. One canonical asset → N channel-native units is the dominant content economics of 2026 (Justin Welsh, Lenny, Marie Forleo all run this). Faion has channel-specific tactics but no methodology for the atomization process itself: extraction → transformation per channel → quality check → distribution. Mechanism: typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of 'role-growth-marketing/Synthesis: Ship one piece of content into 10 channels with AI-assisted atomization' OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == solo or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is a greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)
- single-use throwaway task — overhead of the contract is not justified

## Prerequisites

- recent context for the 'role-growth-marketing/Synthesis: Ship one piece of content into 10 channels with AI-assisted atomization' task (last 30 days of activity)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream
- baseline conventions documented (CLAUDE.md / AGENTS.md / CONVENTIONS.md)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/marketing/content-marketer` | parent role skill — provides the operating context for this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: r1-bound-scope, r2-typed-input, r3-named-owner, r4-versioned, r5-traceable-decision | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | Template fill, bounded transformation |
| `synthesize_decision` | sonnet | Per-instance judgment with bounded inputs |
| `review_for_compliance` | opus | Cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/content-atomization-engine.json` | JSON schema for the Content Atomization Engine output contract |
| `templates/content-atomization-engine.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-content-atomization-engine.py` | Enforce Content Atomization Engine output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `solo/marketing/content-marketer/`
- upstream playbook: `role-growth-marketing/Synthesis: Ship one piece of content into 10 channels with AI-assisted atomization`
- methodology family: `solo/marketing/` (gap-p2 batch, F-059-063)
