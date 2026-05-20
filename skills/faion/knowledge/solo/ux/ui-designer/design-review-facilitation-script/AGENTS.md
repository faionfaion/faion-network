---
slug: design-review-facilitation-script
tier: solo
group: ux
domain: ui-designer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: A 60-minute design-review facilitation script: agenda curation, time-boxing per artifact, structured feedback prompts, and action capture so the weekly review produces decisions not vibes.
content_id: "6499eb3ff52a336c"
tags: [ux, design-review, facilitation, design-critique, meeting, action-capture]
---

# Design Review Facilitation Script

## Summary

**One-sentence:** A 60-minute weekly design-review facilitation script with a 4-block agenda (intake / structured critique / decisions / action capture), strict per-artifact time-boxing, and a feedback-protocol that converts vibes into decisions.

**One-paragraph:** Design-critique methodology covers principles (separating problem from solution, focusing on goals, etc.) but most teams fail at the meeting MECHANICS — agenda curation, time-boxing, action capture, decision recording. Result: 90-minute reviews that produce no decisions and no shared memory of what was discussed. Mechanism: a 4-block agenda with explicit time-boxes per artifact (5/10/15 min by stage), a structured feedback protocol (clarifying / suggesting / blocking, no "looks great"), real-time action capture by a named scribe, and a recap email with decisions + owners + dates within 24h. Primary output: per-meeting decision log + queued actions traceable back to the artifact reviewed.

## Applies If (ALL must hold)

- team has >= 1 designer + >= 2 stakeholders (PM, engineering lead, marketing, founder)
- weekly cadence of design work to review (1+ artifact per week ready for critique)
- meeting calendar has a fixed 60-min slot for the review
- prior reviews have produced "we'll figure out later" decisions or unattributable changes

## Skip If (ANY kills it)

- solo designer + solo founder — async critique in PR / Figma comments is faster
- artifact-readiness is unpredictable (some weeks nothing to review) — switch to on-demand reviews
- attendees won't pre-read the agenda — facilitate one async-pre-read pilot first, then revisit
- review consistently has < 3 participants — too small for the structured protocol to matter

## Prerequisites

- intake form / channel where designers register artifacts for review (with frame links, context, decision-needed)
- pre-read sent &gt;= 24h before meeting (with agenda + artifact list + key decision questions)
- facilitator named and not the artifact author (rotates between designers OR is a non-designer for neutrality)
- scribe role assigned per meeting (rotates) — captures actions during the meeting, not after

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/ui-designer/design-critique-principles` | This methodology operationalizes the principles into meeting mechanics |
| `pro/comms/hr-recruiter/feedback-protocol` | Structured feedback (clarifying / suggesting / blocking) framework consumed here |
| `solo/sdd/sdd/decision-records` | Decisions captured during the review are documented per this format |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: 60-min-hard-cap, structured-feedback-protocol, decision-or-explicit-defer, scribe-during-not-after, 24h-recap-published | ~1000 |
| `content/02-output-contract.xml` | essential | Meeting record schema + decision/action contract + forbidden patterns | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes (LGTM cascade, scope rabbit hole, scribe drift, etc.) with detector + repair | ~1000 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pre_read_drafting` | sonnet | Compose pre-read from artifact intake forms |
| `feedback_categorization` | sonnet | During / after meeting, classify each comment as clarifying / suggesting / blocking |
| `decision_extraction` | sonnet | From transcript, extract crisp decision statements with owners + dates |
| `recap_email_drafting` | haiku | Template fill from captured decisions + actions |

## Templates

| File | Purpose |
|------|---------|
| `templates/agenda.md` | 4-block agenda template with time-boxes |
| `templates/intake-form.md` | Per-artifact registration form (link, context, decision-needed) |
| `templates/meeting-record.json` | JSON Schema for the meeting output |
| `templates/recap-email.md` | Post-meeting recap email template |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/build-agenda.py` | Builds the agenda from intake-form submissions with capacity check (60 min total) | 24h before meeting |
| `scripts/scan-recap-for-decisions.py` | Audits recap email for decision count vs meeting duration | Post-meeting |

## Related

- parent skill: `solo/ux/ui-designer/`
- peer methodologies: `design-critique-principles`, `design-review-pr-checklist`, `design-to-dev-handoff`
- external: [Jared Spool — Design Critique](https://articles.uie.com/) · [Adam Connor — Discussing Design](https://www.discussingdesign.com/) · [Jake Knapp — Sprint design-review patterns](https://www.thesprintbook.com/)
