---
slug: linkedin-founder-post-template
tier: pro
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Linkedin Founder Post Template: codified marketing practice that turns the recurring 'p5-micro-agency-founder/Weekly LinkedIn positioning post' decision into a repeatable, auditable artefact.
content_id: "bd344ce6bcb2964e"
tags: [linkedin-founder-post-template, marketing, pro]
---
# Linkedin Founder Post Template

## Summary

**One-sentence:** Linkedin Founder Post Template: codified marketing practice that turns the recurring 'p5-micro-agency-founder/Weekly LinkedIn positioning post' decision into a repeatable, auditable artefact.

**One-paragraph:** Linkedin Founder Post Template addresses the gap identified by the p5-micro-agency-founder/Weekly LinkedIn positioning post playbook: Content-marketer covers content strategy but not the 200-word founder-voice LinkedIn post format with hook templates. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of p5-micro-agency-founder/Weekly LinkedIn positioning post OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the p5-micro-agency-founder/Weekly LinkedIn positioning post task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/growth-marketer` | parent role skill — provides the operating context for this methodology |

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
| `synthesize_decision` | sonnet | Per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | Cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/linkedin-founder-post-template.json` | JSON schema for the Linkedin Founder Post Template output contract |
| `templates/linkedin-founder-post-template.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-linkedin-founder-post-template.py` | Enforce Linkedin Founder Post Template output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/marketing/growth-marketer/`
- upstream playbook: `p5-micro-agency-founder/Weekly LinkedIn positioning post`
