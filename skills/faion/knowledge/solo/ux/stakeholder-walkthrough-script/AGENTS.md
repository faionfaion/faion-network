---
slug: stakeholder-walkthrough-script
tier: solo
group: ux
domain: ux
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: One-hour stakeholder design walkthrough script that opens with problem + decision-ask, presents options not artefacts, and closes with a signed decision line — short-circuits the demo-mode "pretty pictures" trap.
content_id: "2c439e5f1c4b949c"
tags: [ux-ui-designer, design-walkthrough, stakeholder, decision-ask, anti-demo, solo-design]
---
# Stakeholder Walkthrough Script

## Summary

**One-sentence:** A one-hour design walkthrough script that opens with `problem + decision-ask` (not portfolio narration), presents two-or-three labelled design options, and closes with a written decision line — converting the meeting from a "show pretty pictures" event into a recorded decision artefact.

**One-paragraph:** Designers default to demo-mode: walk the stakeholders through the artefact in chronological build order ("here's the wireframe, here's the mid-fi, here's the hi-fi..."), which positions the stakeholders as audience rather than deciders. The meeting ends with vague reactions ("looks great, maybe consider X") and no decision. This methodology defines a script that flips the framing: open the meeting by stating the design problem and the explicit decision the stakeholders need to make today, present 2-3 labelled options addressing that decision (not the entire portfolio), use the body of the hour to walk trade-offs option-by-option, and close by recording the decision and any deferred sub-decisions in writing. Output is one paragraph in the design log signed by the stakeholders, not a feeling.

## Applies If (ALL must hold)

- The designer is presenting work to non-design stakeholders (PM, founder, exec, client) who hold a decision the designer needs.
- The work is at a stage where 2-3 substantive options exist — not so early there are 12 options, not so late only one option survives.
- The meeting has at most 1 hour booked.
- The designer has authority to refuse a "just show us everything" framing and push for a decision-ask.

## Skip If (ANY kills it)

- Pure design review with other designers — different ceremony, different goals.
- Stakeholder cannot make the decision in the meeting (delegate without authority) — reschedule.
- Work is exploratory / pre-options — use a discovery script instead.
- Meeting is a marketing/sales setting (showing portfolio to a prospect) — different intent entirely.

## Prerequisites

- A one-sentence written design problem.
- A one-sentence written decision-ask ("by end of this meeting, we need a decision on X").
- 2-3 labelled design options ready to walk through.
- Design log file with a stub entry pre-created.

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/ui-designer/` | Baseline design-deliverable conventions. |
| `pro/ba/decision-rationale-capture` | Format for the closing written decision. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Five rules: open with problem + ask, ban demo-mode chronology, 2-3 labelled options, written closing decision, no-decision-equals-reschedule. | ~900 |

## Related

- parent skill: `solo/ux/ui-designer/`
- peer: `handoff-spec-template`, `critical-issue-triage-protocol`, `figma-comment-triage-protocol`
- external: Articulating Design Decisions (Tom Greever, O'Reilly) — Ch. 8 "Reactions and Responses"
