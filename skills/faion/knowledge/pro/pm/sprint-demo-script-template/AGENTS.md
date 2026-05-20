---
slug: sprint-demo-script-template
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: Sprint demo script for the senior-dev-runs-the-demo-for-exec-client variant — explicit per-AC accept/reject prompt, owner-named scope-cut decisions, and a decision log entry the engagement manager signs.
content_id: "17febee337121987"
tags: [project-manager, sprint-demo, client-review, p4-outsource, acceptance-criteria, decision-log]
---
# Sprint Demo Script Template (Senior-Dev-Runs-The-Demo Variant)

## Summary

**One-sentence:** A 45-minute sprint demo script for an outsource senior dev presenting to an executive client, where every acceptance criterion is presented with an explicit accept/reject prompt and the decision is captured before the next AC starts.

**One-paragraph:** Generic sprint review ceremonies assume a Scrum-Master-led, full-team format. P4 outsource engagements often have the senior developer alone with the client exec — no PM in the room, no team to absorb tough questions. This script replaces the "let me show you what we built" narration with a per-AC structured loop: state the AC verbatim → demonstrate it on the staging build → ask "accept / accept-with-defect / reject" → log the answer + named owner → only then move on. Output is a signed acceptance log the engagement manager can use for invoicing and for change-request triggering. Replaces the soft "any feedback?" close that historically gives outsource shops no defensible record.

## Applies If (ALL must hold)

- Engagement is fixed-price or milestone-billed AND demos gate invoice approval.
- The senior developer (not a PM) is leading the demo for the client side.
- Sprint has at least one acceptance criterion with a verifiable demo path.
- Client has an exec-level signer attending (not a delegate without authority).

## Skip If (ANY kills it)

- Internal product where the team is also the customer — use a peer sprint review instead.
- Engagement is pure T&M with no milestone gate — over-engineered for the value at stake.
- Demo is a continuous "show me as you build" cadence, not a sprint-boundary review.
- Client refuses to sign anything during the meeting — the script's output is a signed log; without it, the artefact does not exist.

## Prerequisites

- List of acceptance criteria for the sprint, each with a numbered ID and a verifiable demo path.
- Staging build URL/credentials shared with the client at least 24h before the demo.
- Decision log file (`demos/sprint-NN-decisions.md`) created before the meeting starts.

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ba/business-analyst/` | Acceptance criteria authoring conventions. |
| `pro/pm/client-status-report-multistyle` | Status reporting that consumes the demo log output. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Five rules: per-AC loop, three-option accept prompt, decision-log fields, signer authority check, change-request trigger. | ~900 |

## Related

- parent skill: `pro/pm/project-manager/`
- peer: `client-status-email-template-agency`, `cr-impact-memo-template`, `handover-pack-template-outsource`
- external: Scrum Guide 2020 §Sprint Review (baseline ceremony being specialised here)
