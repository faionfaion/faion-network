---
slug: steerco-meeting-playbook
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
content_id: "7c41939c3a24db21"
summary: End-to-end Steering Committee (Steerco) playbook — pre-meeting prep, in-meeting facilitation, post-meeting follow-up — calibrated for outsource-PM monthly and product-PM quarterly cadences.
tags: [steerco, governance, meeting-facilitation, project-manager, pro, pm]
---
# Steerco Meeting Playbook

## Summary

**One-sentence:** A structured playbook for running Steering Committee (Steerco) meetings — pre-meeting prep pack, in-meeting facilitation arc, post-meeting follow-up — distinct from weekly status reports and quarterly retros.

**One-paragraph:** Steerco is the governance forum where the project's executive sponsor, client lead, vendor exec, and PM align on scope, escalations, and the next phase budget. Run badly, it becomes a status read-out that ends with "ok, see you next month" and no decisions. Run well, it is the only forum where the PM can re-baseline scope, raise the level of an escalation, and ask for re-investment with the right audience in one room. This methodology covers the three lifecycle phases — T-7 prep pack (pre-read materials, decisions log, ask list), T-0 facilitation arc (90-min standard agenda: status snapshot → escalations → decisions → next-phase asks), T+2 follow-up (decision memo + sign-off chase). Calibrated for two common cadences: outsource-PM monthly (P4 service delivery) and product-PM quarterly (P6 enterprise product).

## Applies If (ALL must hold)

- Project has a named Steering Committee with ≥3 senior stakeholders (sponsor, client lead, vendor lead).
- Cadence is regular (monthly OR quarterly) and the PM is the convener.
- Project duration ≥1 quarter (Steerco overhead is not worth it on 4-week engagements).
- Decisions worth Steerco-level air time exist (scope, budget, risk above PM's authority).

## Skip If (ANY kills it)

- The forum exists but is decorative — sponsor delegates, no quorum, decisions made elsewhere. Fix the forum first (escalate to sponsor about quorum) or stop running it.
- Project is in active rescue → Steerco is too slow; daily war room + ad-hoc exec calls instead.
- No decisions outstanding for this cycle — cancel the meeting (rule r3 below) instead of holding a status read-out.
- A weekly status report already covers the audience — Steerco would duplicate. Re-segment via `solo/pm/status-report-templates-by-audience`.

## Prerequisites

- A standing Steerco invite + agenda template held in the project workspace.
- A decisions log (running list of past Steerco decisions with date + owner + outcome).
- An asks list (open decisions needing Steerco approval).
- Pre-read materials sent T-3 days minimum.

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/project-manager/escalation-decision-template` | Steerco is often the target of an escalation; the decision template feeds the asks list. |
| `pro/pm/project-manager/client-status-report-multistyle` | Steerco pre-read often reuses the leadership-style status report. |
| `solo/pm/project-manager/status-report-templates-by-audience` | Calibrates which content goes in pre-read vs which is live discussion. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: pre-read 3 days early, ask list per meeting, cancel-if-no-decisions, decision memo 48h, asks not status focus | ~1200 |

## Related

- parent skill: `pro/pm/project-manager/`
- peer methodologies: `escalation-decision-template`, `client-status-report-multistyle`, `architecture-review-cadence-protocol`
- external: [PMI — Steering Committee Charter](https://www.pmi.org/) · [Harvard Business Review — Running Effective Steering Committees](https://hbr.org/)
