---
slug: critical-issue-triage-protocol
tier: solo
group: ux
domain: ux
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Turns post-session UX triage from a gut-feel argument into a 30-minute deterministic protocol: severity × frequency × context modifier yields a same-day-fix / sprint / backlog / discard decision per finding.
content_id: "5ec341067661d690"
complexity: medium
produces: report
est_tokens: 4200
tags: ["ux-research", "usability-testing", "severity", "triage", "same-day-fix"]
---
# Critical-Issue Triage Protocol

## Summary

**One-sentence:** Turns post-session UX triage from a gut-feel argument into a 30-minute deterministic protocol: severity × frequency × context modifier yields a same-day-fix / sprint / backlog / discard decision per finding.

**One-paragraph:** After every research or usability session, findings pile up and the team improvises priority. This protocol pins a 30-minute triage: every finding is scored 0-4 severity using a calibrated rubric, frequency expressed in bands against observed N, modified by revenue-criticality / regulated user / internal-tool context, then routed via a deterministic action matrix. Overrides require a written one-line justification; verbal overrides are rejected.

**Ефективно для:**

- Solo researcher with weekly usability sessions who needs a 30-min triage ritual.
- Founder receiving session notes from a remote tester and needing same-day vs backlog clarity.
- Cross-functional review where eng, design, and PM disagree on what is critical.
- Compliance contexts (accessibility, regulated user) where severity bumps are non-negotiable.

## Applies If (ALL must hold)

- At least one usability session or research interview ran in the last 7 days with findings to triage.
- Findings include observable user behaviour (not opinion).
- A backlog tool exists where 'same-day-fix' / 'next-sprint' / 'backlog' / 'discard' map to real lanes.
- Designer or PM has 30 minutes blocked for triage.

## Skip If (ANY kills it)

- Findings are PM-anecdote, not session-based — score with a different rubric first.
- Greenfield prototype with no real users — triage is premature.
- All findings are catastrophic and team is already in fire-drill mode — drop the protocol, go fix.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Session notes or replay link | URL / md | Research tool (Maze, UserTesting, Lookback) or notebook |
| Finding list | array of strings | Triage spreadsheet column A |
| Sample size N | integer | Session recruiter manifest |
| Context tag per route | enum | Product taxonomy: revenue-critical / regulated / internal / other |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/heuristic-eval-severity-rubric` | Severity 0..4 calibration source. |
| `solo/ux/anti-pattern-rationale-template` | Captures repeated findings for the bank. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | >=5 testable rules + skip + run rules | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | >=3 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | End-to-end worked example | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `score-per-finding` | sonnet | Per-finding judgement on severity + frequency. |
| `apply-context-modifier` | haiku | Deterministic enum lookup, no judgement needed. |
| `full-session-triage-pass` | opus | 30+ findings, cross-cutting context, override review. |

## Templates

| File | Purpose |
|------|---------|
| `templates/critical-issue-triage-protocol.json` | JSON skeleton conforming to the output-contract schema. |
| `templates/critical-issue-triage-protocol.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-critical-issue-triage-protocol.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[heuristic-eval-severity-rubric]]
- [[anti-pattern-rationale-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs (precondition pass, named owner, input reachability) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
