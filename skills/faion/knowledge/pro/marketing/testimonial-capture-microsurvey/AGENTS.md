---
slug: testimonial-capture-microsurvey
tier: pro
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Testimonial Capture Microsurvey: produces a versioned, owner-signed artefact that closes the gap 'p5-micro-agency-founder/Bi-weekly case-study / testimonial capture'."
content_id: "ccd5fac359978b1d"
complexity: light
produces: spec
est_tokens: 3800
tags: [testimonial-capture-microsurvey, marketing, pro]
---
# Testimonial Capture Microsurvey

## Summary

**One-sentence:** Testimonial Capture Microsurvey: produces a versioned, owner-signed artefact that closes the gap 'p5-micro-agency-founder/Bi-weekly case-study / testimonial capture'.

**One-paragraph:** Addresses the gap surfaced by 'p5-micro-agency-founder/Bi-weekly case-study / testimonial capture': growth-customer-testimonials is high-level; a 3-question microsurvey template + permission flow is the actual atomic task. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a testimonial capture microsurvey artefact (decision record, checklist, score sheet, or report).

**Ефективно для:**

- Bi-weekly testimonial capture для мікроагентства.
- Three-question microsurvey + explicit publish permission flow.
- Versioned + named-owner артефакт замість ad-hoc email.
- Замикання петлі від delivery → testimonial → sales asset.

## Applies If (ALL must hold)

- task is an instance of 'p5-micro-agency-founder/Bi-weekly case-study / testimonial capture' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working testimonial capture microsurvey artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'p5-micro-agency-founder/Bi-weekly case-study / testimonial capture' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/marketing` | parent domain group — provides operating context for Testimonial Capture Microsurvey |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules + self-routing anchors (run-the-checklist + skip-this-methodology) | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example | ~900 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns with description + reason + repair | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on preconditions → rule from `01-core-rules.xml` | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | template fill, bounded transformation |
| `synthesize_decision` | sonnet | per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/testimonial-capture-microsurvey.md` | Markdown skeleton (5-line header) for the artefact body. |
| `templates/testimonial-capture-microsurvey.json` | JSON Schema (draft-07) for the output contract — see `content/02-output-contract.xml`. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-testimonial-capture-microsurvey.py` | Validate a filled artefact against the schema declared in `content/02-output-contract.xml`. Supports `--help` and `--self-test`. | Pre-commit; before publishing the artefact. |

## Related

- parent skill: `pro/marketing/`
- upstream playbook: `p5-micro-agency-founder/Bi-weekly case-study / testimonial capture`
- pro/marketing/p5-micro-agency-founder

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable preconditions (Applies-If / Skip-If) to either `run-the-checklist` or `skip-this-methodology` from `01-core-rules.xml`. Use it whenever the operating trigger fires and you need to decide between applying this methodology now, deferring, or routing elsewhere.

