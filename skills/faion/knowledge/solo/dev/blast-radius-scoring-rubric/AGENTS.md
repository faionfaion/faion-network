---
slug: blast-radius-scoring-rubric
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: Rubric that scores a PR's blast radius (services × users × reversibility) and routes it to deep-read vs light-skim review, making daily multi-PR review tractable for solo devs and outsource leads.
content_id: 3db94916b876c484
---

# Blast Radius Scoring Rubric

## Summary
A scoring rubric that estimates a PR or incident's blast radius along three axes — services touched, users affected, reversibility — and routes the review/response accordingly. Outcome: every PR gets a 1-minute triage score; auth/data/infra get a deep read, copy/CSS get a light skim, and the reviewer never spends 30 minutes on a Tailwind tweak again.

## Applies If
- You review ≥3 PRs per day (solo dev, outsource lead, micro-agency tech lead)
- You have at least once approved a PR that broke production
- You touch a codebase with multiple services or modules
- You can name the auth / data / infra surfaces in your stack

## Skip If
- You merge your own PRs without review (no rubric needed — write tests)
- All your PRs are single-service and single-table (radius is always the same)
- You have a dedicated SRE team running staged rollouts (rely on their gates)
- You are reviewing a 1-line copy fix (just skim and merge)

## Content
See `content/01-core-rules.xml`.

## Related
- [[outsource-pr-etiquette]]
- [[ci-quality-gate-design]]
- [[deploy-notes-template-with-rollback]]
- [[qa-prioritization-rubric]]
