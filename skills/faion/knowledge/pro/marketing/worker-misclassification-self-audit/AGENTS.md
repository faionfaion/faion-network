---
slug: worker-misclassification-self-audit
tier: pro
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "b0b3beec9adcc533"
summary: "Worker Misclassification Self Audit: produces a versioned, owner-signed artefact that closes the gap 'p5-micro-agency-founder/Build a bench of vetted subcontractors without becoming an agency-of-agencies'."
tags: [worker-misclassification-self-audit, marketing, pro]
---
# Worker Misclassification Self Audit

## Summary

**One-sentence:** Worker Misclassification Self Audit: produces a versioned, owner-signed artefact that closes the gap 'p5-micro-agency-founder/Build a bench of vetted subcontractors without becoming an agency-of-agencies'.

**One-paragraph:** Addresses the gap surfaced by 'p5-micro-agency-founder/Build a bench of vetted subcontractors without becoming an agency-of-agencies': ops-contractor-management mentions misclassification once as a footnote. For a micro-agency that uses long-term contractors, this is existential — IRS/AB-5/UK IR35/EU equivalents can retroactively reclassify a contractor as an employee. A self-audit methodology (behavioral control, financial control, relationship factors per jurisdiction) is needed and missing. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a worker misclassification self audit artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'p5-micro-agency-founder/Build a bench of vetted subcontractors without becoming an agency-of-agencies' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working worker misclassification self audit artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'p5-micro-agency-founder/Build a bench of vetted subcontractors without becoming an agency-of-agencies' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/marketing` | parent domain group — provides operating context for Worker Misclassification Self Audit |

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
| `templates/worker-misclassification-self-audit.json` | JSON schema for the Worker Misclassification Self Audit output contract |
| `templates/worker-misclassification-self-audit.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-worker-misclassification-self-audit.py` | Enforce Worker Misclassification Self Audit output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/marketing/`
- upstream playbook: `p5-micro-agency-founder/Build a bench of vetted subcontractors without becoming an agency-of-agencies`
- pro/marketing/p5-micro-agency-founder
