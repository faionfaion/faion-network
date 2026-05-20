---
slug: qa-exploratory-charter-template
tier: solo
group: dev
domain: testing-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "b23a171cd084a8cc"
summary: A session-based exploratory testing charter template (Bach/Bolton style) that turns vague "have a poke around" into a structured 60-90 minute session with mission, focus areas, time-boxed test ideas, observations, and a debrief — the single highest-yield human technique against AI-generated code.
tags: [exploratory-testing, sbtm, session-based, qa, charter, bug-bash]
---

# Exploratory Testing Charter Template

## Summary

**One-sentence:** Run a structured 60-90 minute exploratory testing session with a single mission, 3-5 focus areas, time-boxed test ideas, observations log, and a debrief — converting vague "poke around the feature" into the highest-yield human test technique on AI-generated code.

**One-paragraph:** Exploratory testing is absent from Faion's testing-developer skill. It is the single most effective human-only technique against AI-generated code: AI-tests cover what the spec says, exploratory testing covers what the spec did not say. Session-Based Test Management (Bach / Bolton) formalises the technique into 60-90 minute sessions with a written charter (mission, focus, target), an observation log (test ideas tried, bugs found, questions raised), and a debrief (key findings, follow-ups, debt). This methodology pins the charter format and the session rhythm so exploratory testing can be scheduled like any other engineering activity rather than improvised opportunistically. Primary output: one filled-in charter per session, posted to the team channel, plus a session log for the QA wiki.

## Applies If (ALL must hold)

- product is interactive (UI, API, CLI) with user-meaningful workflows
- feature has just shipped OR is mid-flight, and has at least one AC documented
- team has 1-3 hours per week to invest in exploratory testing
- automated tests run for the feature (so exploratory time is not spent on what tests already cover)

## Skip If (ANY kills it)

- feature is pure infrastructure with no user-meaningful surface — automated tests + integration tests are the right investment
- pre-release with the build broken — fix the build first; exploratory testing on broken builds finds noise
- team has no QA capacity at all — exploratory time needs to be claimed explicitly, not hoped for
- engineer doing exploration is the same one who wrote the code AND there is no second perspective available — bias makes solo exploration low-yield; either pair or skip

## Prerequisites

- working environment for the feature (staging, preview deploy, local with seeded data)
- access to recent automated-test runs (so the explorer knows what NOT to re-cover)
- a quiet block of 60-90 minutes that will not be interrupted
- a single mission written down BEFORE the session starts

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/testing-developer/qa-risk-matrix-method` | Risk matrix drives the focus area selection |
| `solo/dev/testing-developer/qa-ai-generated-test-audit-checklist` | What the automated tests are likely missing — input for the exploration |
| `solo/dev/testing-developer/qa-ac-to-assertion-mapping` | What the AC mapping says is covered — boundaries of the exploration |

## Content

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: single mission, time-boxed, observation log, debrief, no-test-script (only ideas) | ~900 |
| `content/02-output-contract.xml` | essential | Charter schema, observation-log schema, debrief schema | ~600 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: drift from mission, multi-tasking, no debrief, etc. | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `mission_drafting_from_feature_spec` | sonnet | Bounded synthesis from AC + risk matrix |
| `focus_area_proposal` | sonnet | 3-5 areas selected from spec and risk inputs |
| `bug_clustering_from_observation_log` | sonnet | Per-bug judgment on severity and area |
| `debrief_synthesis` | opus | Cross-observation synthesis: themes, follow-ups, debt |

## Templates

| File | Purpose |
|------|---------|
| `templates/charter.md` | One-page charter: mission, focus, target, scope |
| `templates/observation-log.md` | Time-stamped log of test ideas, observations, questions, bugs |
| `templates/debrief.md` | Post-session debrief: findings, follow-ups, debt, time spent |
| `templates/heuristic-cheatsheet.md` | Bach/Bolton heuristics summary (SFDPOT, etc.) |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/charter-from-spec.py` | Reads a feature spec, suggests a mission and 3-5 focus areas | Pre-session prep |
| `scripts/index-debrief.py` | Appends the debrief to a per-feature exploratory log indexed by feature id | Post-session |

## Related

- parent skill: `solo/dev/testing-developer/SKILL.md`
- peer methodologies: `solo/dev/testing-developer/qa-risk-matrix-method`, `solo/dev/testing-developer/qa-test-pyramid-vs-trophy-decision`
- external: [Bach and Bolton, Session-Based Test Management (2003) original paper] · [James Whittaker, Exploratory Software Testing (Addison-Wesley, 2009)] · [Bach Rapid Software Testing course materials] · [Michael Bolton testing blog]
