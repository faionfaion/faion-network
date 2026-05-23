# Design Review Facilitation Script

## Summary

**One-sentence:** Pinned 45-minute design-review script that opens with the review-ask, runs structured rounds of feedback (clarify → critique → suggest), and closes with a triaged action list per reviewer.

**One-paragraph:** Design reviews degenerate into preference debates without a script. This template pins a 45-min review: 5 min framing (review-ask + ground rules), 25 min structured feedback in three rounds (clarify-questions → critique → suggest-alternatives), 10 min triage (each reviewer picks one must-fix), 5 min recap. The artefact captures who said what and which items the designer commits to fix.

**Ефективно для:**

- Solo designer running fortnightly peer-review with 2-3 reviewers.
- Cross-team design review where reviewer roles differ (eng / PM / a11y).
- AI agent generating review summary notes that must surface action items.
- Pre-launch design freeze where reviews must produce binding action lists.

## Applies If (ALL must hold)

- A design artefact (component, screen, flow) is ready for review.
- ≥2 reviewers are available with 45 min blocked.
- Designer is willing to commit to action items at meeting close.
- Action items can be routed to a tracker (JIRA, Linear, Github).

## Skip If (ANY kills it)

- Quick sanity check with 1 reviewer — async writeup is faster.
- Late-stage polish review where commitments will not change scope.
- Conflict between designer and reviewer; resolve 1-1 first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Review artefact URL | Figma / Loom / repo path | Designer canvas |
| Review-ask statement | string | Designer's framing |
| Reviewer roster + roles | list | Team directory |
| Tracker URL | URL | Issue tracker |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/heuristic-eval-severity-rubric` | Severity rubric used in triage round. |
| `solo/ux/design-decision-log-template` | Captured decisions graduate to the log. |

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
| `draft-review-script` | sonnet | Per-review judgement on framing + ground rules. |
| `track-feedback-rounds` | haiku | Deterministic capture of feedback per round. |
| `multi-reviewer-synthesis` | opus | Cross-reviewer pattern detection. |

## Templates

| File | Purpose |
|------|---------|
| `templates/design-review-facilitation-script.json` | JSON skeleton conforming to the output-contract schema. |
| `templates/design-review-facilitation-script.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-design-review-facilitation-script.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[design-decision-log-template]]
- [[heuristic-eval-severity-rubric]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs (precondition pass, named owner, input reachability) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
