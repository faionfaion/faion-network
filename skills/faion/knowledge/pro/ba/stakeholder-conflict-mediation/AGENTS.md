---
slug: stakeholder-conflict-mediation
tier: pro
group: ba
domain: ba
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: Live mediation playbook for stakeholder conflicts surfacing during requirements review meetings — pause-reframe-isolate-decide-confirm loop with a fallback escalation criterion when the room cannot converge.
content_id: "71ad8e5f7b3956e7"
tags: [business-analyst, stakeholder-conflict, mediation, requirements-review, live-meeting, p4-outsource]
---
# Stakeholder Conflict Mediation

## Summary

**One-sentence:** A live-meeting mediation loop for the BA running a requirements review when two stakeholders openly conflict — pause → reframe to the requirement → isolate the disputed clause → propose a decision path → confirm next step in writing — with a defined escalation criterion if the loop fails twice.

**One-paragraph:** Whereas `stakeholder-conflict-facilitation-script` runs a *scheduled* conflict-resolution meeting, conflicts often erupt mid-requirements-review without warning. The static `stakeholder-analysis` methodology classifies stakeholders but offers no in-the-moment playbook. This methodology gives the BA a five-step loop they can run inside the same meeting: pause the broader review, reframe the argument back to the disputed requirement clause, isolate the specific point of disagreement (often only one of several), propose a decision path (decide-now / async-with-rubric / escalate), and confirm the next step is captured in writing before resuming review. If the loop iterates twice without convergence, the BA invokes a pre-agreed escalation criterion to a named sponsor rather than letting the meeting hostage the rest of the agenda.

## Applies If (ALL must hold)

- Conflict erupts during an active requirements review meeting (not pre-scheduled mediation).
- The BA is the meeting facilitator or co-facilitator.
- At least two named stakeholders are taking opposing positions on a specific requirement.
- An escalation contact (sponsor, product head) has been agreed in the project charter.

## Skip If (ANY kills it)

- Pre-scheduled conflict meeting — use `stakeholder-conflict-facilitation-script` instead.
- Conflict is interpersonal/political, not requirements-based — defer to HR/manager, not BA.
- Meeting has under 10 minutes remaining — schedule a dedicated follow-up; do not attempt mediation in fragments.
- No agreed escalation path exists — fix that first; running this loop without it produces no exit.

## Prerequisites

- Project charter or kickoff doc names an escalation contact for unresolved requirements conflicts.
- BA has access to the requirements doc to surface the specific clause in dispute.
- Meeting is recorded or has a designated note-taker (so reframings can be quoted back).

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ba/business-analyst/stakeholder-analysis` | Stakeholder authority map informs escalation thresholds. |
| `pro/ba/decision-rationale-capture` | Format for capturing the written confirm step. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Five rules: pause + reframe, isolate to one clause, propose three paths, written confirm, two-iter escalation cap. | ~900 |

## Related

- parent skill: `pro/ba/business-analyst/`
- peer: `stakeholder-conflict-facilitation-script`, `decision-rationale-capture`, `cr-impact-memo-template`
- external: Interest-Based Relational approach (Fisher & Ury, Getting to Yes) §Separate the people from the problem
