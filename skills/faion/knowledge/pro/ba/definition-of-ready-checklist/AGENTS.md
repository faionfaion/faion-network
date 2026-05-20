---
slug: definition-of-ready-checklist
tier: pro
group: ba
domain: ba
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: Outsource-grade DoR checklist that gates a story before grooming — covering not just engineering readiness but also client-side dependencies (env access, data, regulator/legal/security sign-off).
content_id: 5b37524eaaf59bd0
---

# Definition Of Ready Checklist

## Summary
A definition-of-ready (DoR) checklist scoped for outsource and consultancy work, where most blockers are client-side (env access, data, regulator approvals, security sign-off) and not engineering effort. Outcome: stories enter grooming only after passing this gate, eliminating the "we estimated it three times and still cannot start" pattern that wastes 10-25% of an outsource team's velocity.

## Applies If
- You run grooming or estimation sessions for an outsource / consulting team
- You depend on a client for environments, test data, or regulator/legal approvals
- You have ≥1 story in the last quarter that was estimated but stayed blocked
- You can name the client-side stakeholders (PM, security, legal, data, infra)

## Skip If
- You are an in-house team with full control of all environments and data
- The team uses no-estimate flow with WIP limits (DoR is implicit in pull)
- Story is a research spike where "ready" is intentionally fuzzy
- You have <5 active stories at any time (overhead exceeds benefit)

## Content
See `content/01-core-rules.xml`.

## Related
- [[discovery-to-delivery-handover-protocol]]
- [[ambiguity-contradiction-detector]]
- [[traceability-matrix-template-csv]]
- [[change-request-impact-rubric]]
