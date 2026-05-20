---
slug: scope-creep-park-list-template
tier: solo
group: ux
domain: ux
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: Scope-Creep Park-List Template: a one-page format used live in stakeholder design walkthroughs to capture "wouldn't it be cool if" ideas without committing to them.
content_id: "315932eacb4ece49"
tags: [scope-creep-park-list-template, ux, solo]
---
# Scope-Creep Park-List Template

## Summary

**One-sentence:** A live park-list format the designer fills during a stakeholder walkthrough so every "wouldn't it be cool if" idea is acknowledged, written down, and visibly disposed of (kept / parked / dropped) — preventing promise-by-omission while honoring the stakeholder input.

**One-paragraph:** Stakeholder design walkthroughs reliably spawn "wouldn't it be cool if" ideas. When the designer nods politely and moves on, the stakeholder remembers it as agreement; weeks later, the missing feature becomes a credibility hit. When the designer pushes back live, the meeting derails. This methodology defines the on-screen park-list (a single live document the stakeholder sees being updated), the four-bucket disposition (in-scope-now, change-order, backlog-v2, dropped-with-reason), the 90-second-per-item rule, and the end-of-meeting sign-off where the stakeholder confirms each disposition. Output is a per-walkthrough park-list record that the engagement file references and that downstream design and roadmap work can cite.

## Applies If (ALL must hold)

- a stakeholder design walkthrough is scheduled (≥30 min, ≥2 attendees including the buyer/sponsor)
- there is an existing scope or design brief the walkthrough sits inside
- the walkthrough surface (screen share, doc, prototype) can render a live park-list
- tier == solo or higher

## Skip If (ANY kills it)

- the walkthrough is explicitly an open-ended ideation session — use a generative-ideation pattern instead
- the engagement uses a strict written change-control process where verbal park-list entries are non-binding regardless — defer to that process
- the walkthrough has only 1 stakeholder and zero scope already exists (greenfield kickoff; use kickoff template instead)

## Prerequisites

- the existing scope / design brief reference
- a visible surface (Figma sticky board, shared doc, Notion page) the stakeholder sees update in real time
- 5 minutes at the end of the meeting reserved for sign-off
- access to the engagement backlog for parked items

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/ui-designer` | parent role skill |
| `solo/ux/anti-pattern-rationale-template` | upstream rationale pattern referenced when items get `dropped-with-reason` |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: visible-live-capture, four-bucket-disposition, 90s-per-item-cap, end-of-meeting-signoff, parked-item-shelf-life | ~1100 |

## Related

- parent skill: `solo/ux/ui-designer`
- upstream playbook: `role-ux-ui-designer/Stakeholder design walkthrough (1hr)`
- companion methodology: `pro/ba/scope-creep-firewall`
