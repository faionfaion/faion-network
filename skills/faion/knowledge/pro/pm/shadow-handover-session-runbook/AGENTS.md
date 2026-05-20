---
slug: shadow-handover-session-runbook
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: Shadow Handover Session Runbook — codifies the offshore→onshore knowledge-transfer pattern (receiver-does, outgoing-watches) so handovers stop relying on tribal memory.
content_id: "f57a571847a0b2c9"
tags: [shadow-handover-session-runbook, pm, pro]
---
# Shadow Handover Session Runbook

## Summary

**One-sentence:** A runbook for live shadow-handover sessions where the receiver executes real work while the outgoing engineer watches silently, with structured checkpoints, written deliverables, and a sign-off gate.

**One-paragraph:** Existing onboarding methodologies cover hiring-from-scratch, not the offshore-to-onshore rotation pattern that dominates outsourced delivery. The "receiver does it, outgoing watches" approach prevents the most common failure (outgoing engineer demos confidently, receiver nods, receiver cannot reproduce). This methodology forces the inversion: the receiver drives the keyboard for predefined tasks, the outgoing engineer answers questions only on request, and both sign a written gap log at session end.

## Applies If (ALL must hold)

- engagement involves transferring operational ownership of a system from one engineer/team to another
- the outgoing engineer is still available and willing to be available for ≥1 session
- there are real, executable tasks the receiver can run during the session (not just docs reading)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the outgoing engineer is already gone — use forensic-handover artefacts instead
- the system is greenfield and the receiver built half of it already
- the transfer is purely documentation (no operational tasks) — use a doc-walkthrough pattern

## Content

| File | What's inside |
|------|---------------|
| `content/01-core-rules.xml` | 5 testable rules: receiver-drives, silent-watch default, written gap log, sign-off gate, no skipped tasks |

## Related

- upstream playbook: `p4-outsource-specialist/Pre-handover documentation pack`
- parent skill: `pro/pm/`
