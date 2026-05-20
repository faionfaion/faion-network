---
slug: stakeholder-disagree-and-commit-protocol
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: Explicit disagree-and-commit protocol for product roadmap decisions — named-dissent capture, escalation thresholds, and a time-boxed revisit trigger that prevents stakeholder drift from quietly unwinding the roadmap mid-quarter.
content_id: "ee01fb481e0f69e2"
tags: [product-manager, stakeholder-management, disagree-and-commit, roadmap, prioritisation, escalation]
---
# Stakeholder Disagree-and-Commit Protocol

## Summary

**One-sentence:** A documented disagree-and-commit protocol where dissenting stakeholders sign a "commit now, revisit at trigger" line on a prioritisation decision, plus explicit escalation thresholds, so the roadmap stops getting silently unwound by post-decision lobbying.

**One-paragraph:** Generic stakeholder-management methodologies talk about alignment in the abstract but offer no concrete protocol for the moment a prioritisation decision is taken with active disagreement. The result on P6 product teams: a roadmap is approved, then dissenting stakeholders quietly lobby individual engineers, ask for "small additions", or re-litigate at the next review. This methodology codifies the disagree-and-commit moment: name the dissenting stakeholder, capture the grounds, get them to sign one of `commit-with-revisit` or `escalate-now`, set an explicit revisit trigger (metric crosses threshold OR date passes), and route any escalation to a pre-named threshold owner within the same week. The artefact lives in the decision register and becomes the canonical reference if the conflict re-surfaces. Replaces "we discussed it and decided" entries with auditable commitments.

## Applies If (ALL must hold)

- Prioritisation or roadmap decision was taken with at least one stakeholder objecting on the record.
- The PM owns the decision register and roadmap document.
- Project has a pre-named threshold owner (program head, VP product, sponsor) for escalation.
- Decision affects work that will be committed for at least the current quarter.

## Skip If (ANY kills it)

- Unanimous decision — no dissent to capture.
- Pure operational ticket (bug fix, small enhancement) — over-engineered.
- Project does not maintain a roadmap (e.g., pure backlog scheduling) — protocol has no home document.
- No threshold owner is reachable (vacancy, gap) — fix that first; without escalation the protocol is incomplete.

## Prerequisites

- Decision register / roadmap location agreed and writable by the PM.
- Named threshold owner for escalation documented in project charter.
- Metric or date the team agrees to use as a revisit trigger (e.g., "if churn >5% by end Q3").

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/project-manager/stakeholder-management` | Underlying stakeholder mapping and engagement plan. |
| `pro/ba/decision-rationale-capture` | Format for the written decision artefact. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Five rules: named dissent only, signed commit/escalate choice, explicit trigger, threshold owner routing, no-relitigate window. | ~900 |

## Related

- parent skill: `pro/pm/project-manager/`
- peer: `stakeholder-conflict-facilitation-script`, `escalation-decision-template`, `cross-team-handoff-tracker`
- external: "Disagree and commit" — Amazon Leadership Principles (Bezos 1997 shareholder letter)
