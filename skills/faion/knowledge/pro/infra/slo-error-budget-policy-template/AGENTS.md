---
slug: slo-error-budget-policy-template
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: SLO Error Budget Policy Template — a one-page policy artefact mapping error-budget state (healthy / yellow / red / exhausted) to concrete actions (ship / freeze / focus / escalate).
content_id: "393bdce7c187e8e0"
tags: [slo-error-budget-policy-template, infra, pro]
---
# SLO Error Budget Policy Template

## Summary

**One-sentence:** A one-page, signed policy artefact mapping error-budget state to action — ship freely while healthy, slow when yellow, freeze when red, escalate when exhausted — so the burn-rate alert turns into a pre-agreed decision instead of a re-litigation.

**One-paragraph:** Faion has burn-rate alerting and SLO design content, but the policy artefact that maps budget state → action (ship / freeze / focus) is missing. Teams keep re-litigating "should we freeze releases?" each time the budget burns; the policy template ends that by pre-committing the answer in writing, signed jointly by engineering and product before the budget ever hits red.

## Applies If (ALL must hold)

- at least one SLO with a defined error budget exists for the service
- burn-rate alerting is wired to a usable channel
- product and engineering have a shared decision-maker (founder, head of product, GM) who can sign the policy
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- no SLO exists yet — design one first (see `slo-design-from-user-journeys`)
- the team already has a signed error-budget policy — extend, don't rewrite
- the org has no concept of release-velocity decisions to gate (single-person hobby project)

## Content

| File | What's inside |
|------|---------------|
| `content/01-core-rules.xml` | 5 testable rules: four states, signed by product+eng, action per state, exit criterion, named decision-maker |

## Related

- upstream playbook: `role-devops-engineer/SLO error-budget burn review`
- parent skill: `pro/infra/`
- related methodologies: `pro/infra/burn-rate-multi-window-alerting`, `pro/infra/error-budget-policy-and-freeze-rules`, `pro/infra/slo-design-from-user-journeys`
