---
slug: critical-issue-triage-protocol
tier: solo
group: ux
domain: ux
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "5ec341067661d690"
summary: A decision rule for when a UX research finding is a same-day-fix vs a backlog item — severity scoring, frequency thresholds, and a 30-minute triage protocol that prevents both overreaction and silent neglect.
tags: [ux-research, usability-testing, severity, triage, same-day-fix]
---
# Critical UX Issue Triage Protocol

## Summary

**One-sentence:** A 30-minute triage protocol the UX designer (or solo product owner) runs after each usability test session to classify findings as same-day-fix / next-sprint / backlog / discard — replacing improvised "this seems bad, let's just patch it" with a defensible severity rule.

**One-paragraph:** When a usability test surfaces a catastrophic break (user cannot complete a critical task, accessibility-blocking bug, dead-end error state), the designer faces a snap decision: patch today, defer, or document. Currently improvised. The result: either the team panic-patches and breaks adjacent flows, or the issue sits in the backlog and surfaces again in the next test. This methodology gives a deterministic decision rule using severity (1-4) and frequency (% of users hitting it in observed sample) crossed with a context modifier (revenue-critical path, regulated user, etc.). Output: a triage table per session with classified actions, owner per action, and the rationale.

## Applies If (ALL must hold)

- A usability test session (moderated or unmoderated) has completed.
- Designer/owner has a list of observed findings with frequency data (how many of N users hit it).
- A backlog or issue tracker exists for routing.
- The designer has authority to escalate or has a defined escalation path.

## Skip If (ANY kills it)

- Pre-test phase (test plan, recruit, etc.) — different methodology.
- Single-finding emergency (production outage from a usability bug) — go to incident response, not triage.
- Large multi-session program — use the pro-tier ux-research-program-management methodology.
- Findings without frequency data — usability test was not properly logged; fix that first.

## Prerequisites

- Findings log per session: one row per observed issue with brief description.
- Frequency count per finding (users-out-of-N who hit it).
- A severity rubric (provided in templates).
- A timer (literal 30-minute box).

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/ui-designer/usability-testing-basics` | Test setup, observation, finding capture assumed. |
| `solo/ux/ui-designer/heuristic-evaluation` | Severity scale aligns with Nielsen 0-4. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 4 rules: severity scale, frequency band, context modifier, action matrix, 30-min box | ~800 |
| `content/02-output-contract.xml` | essential | Triage table shape, decision rationale, escalation log | ~600 |
| `content/03-failure-modes.xml` | essential | 5 failure modes: panic-patch, "loud user" bias, low-sev pile, etc. | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify-severity` | sonnet | Bounded judgment using rubric |
| `compute-action` | haiku | Lookup against the action matrix |
| `escalation-draft` | sonnet | Draft escalation message with rationale |

## Templates

| File | Purpose |
|------|---------|
| `templates/severity-rubric.md` | Nielsen-style 0-4 with examples per level |
| `templates/triage-table.md` | One-row-per-finding skeleton |
| `templates/action-matrix.md` | Severity × frequency → action lookup |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/triage-summary.py` | Aggregate session-triage outputs over a research cycle | End of cycle |

## Related

- parent skill: `solo/ux/ui-designer/`
- peer methodology: `usability-testing-basics`, `heuristic-evaluation`, `accessibility-quick-pass`
- external: [Nielsen severity rating](https://www.nngroup.com/articles/how-to-rate-the-severity-of-usability-problems/) · [Jakob Nielsen — usability principles](https://www.nngroup.com/)
