---
slug: fitness-function-wiring
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
content_id: "de67e8d6e9da4b97"
summary: "Map each high-priority QAA scenario to a concrete, scheduled CI job (k6, Gatling, Chaos Monkey, OWASP ZAP) with explicit breach actions, bridging architecture decisions and continuous verification instead of leaving fitness functions as a checkbox."
tags: [dev, pro, architecture, fitness-functions, qaa, ci, k6, chaos]
---
# Fitness Function Wiring

## Summary

Quality-Attribute-driven Architecture (QAA) literature mentions fitness functions but treats them as an unsourced checkbox, leaving architects with prose obligations and no enforcement. This methodology bridges architecture-as-code and CI: every (High-impact, High-likelihood) scenario in the QAA register is wired to a concrete tool — k6 / Gatling for performance, Chaos Monkey / Litmus for resilience, OWASP ZAP / Trivy for security — with a tool-specific config artefact, a breach threshold, a scheduled cadence, and a named breach-action. Architecture decisions become executable contracts that fail loudly when reality drifts from the design freeze.

## Applies If

- A QAA register exists with scenarios scored by impact and likelihood (at minimum a High/Medium/Low matrix).
- The team owns a CI/CD platform where new jobs can be added and scheduled (GitHub Actions, GitLab CI, Jenkins, etc.).
- A cost + latency budget has been agreed before design freeze and is documented as numeric thresholds.
- Architecture artefacts (ADRs, c4 models, repo layout) are version-controlled.

## Skip If

- No QAA scenarios are scored — wire scoring first.
- The team has no CI capacity to run additional jobs even at a weekly cadence.
- The system is throwaway prototype work where breach actions would have no consumer.

## Content

| File | Depth | What's inside |
|------|-------|---------------|
| `content/01-core-rules.xml` | essential | Five testable rules linking (H,H) scenarios to CI jobs, breach thresholds, and on-breach actions |

## Related

- parent skill: `pro/dev/`
- triggering activity: `Architecture-as-code repository — continuous maintenance with monthly review`, `Cost + latency budget BEFORE design freeze`
- neighbouring: `pro/dev/perf-budget-as-code`, `pro/dev/load-profile-cookbook`, `pro/dev/threat-model-as-code`
