---
slug: qa-exploratory-charter-template
tier: solo
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Run a 60-90 minute Session-Based exploratory test session with a single written mission, time-box, observation log, and within-24h debrief — the human-only complement to automated and AI-generated tests.
content_id: "9a2d4e6f80b1c2d3"
complexity: medium
produces: report
est_tokens: 4800
tags: [exploratory-testing, sbtm, qa, charter, sessions]
---
# Exploratory Testing Charter Template

## Summary

**One-sentence:** Run a structured 60-90 minute exploratory testing session with a single mission, 3-5 focus areas, time-boxed test ideas, observation log, and a debrief — converting "poke around the feature" into the highest-yield human test technique against AI-generated code.

**One-paragraph:** Exploratory testing is the single most effective human-only technique against AI-generated code: AI tests cover what the spec says, exploration covers what the spec did not say. Session-Based Test Management (Bach / Bolton) formalises the technique into 60-90 minute sessions with a written charter (mission, focus areas, target), an observation log (test ideas tried, bugs found, questions raised), and a debrief (key findings, follow-ups, debt). This methodology pins the charter format and the session rhythm so exploratory testing can be scheduled like any other engineering activity rather than improvised opportunistically. Primary output: one filled-in charter per session, posted to the team channel, plus a session log for the QA wiki.

**Ефективно для:**

- Newly shipped features where automated coverage is high but real-user behaviour is unknown.
- Probing AI-generated code for unspecified edge cases the spec did not mention.
- Cross-cutting concerns (i18n, timezone, network failure, permission transitions) that escape unit tests.
- Documenting patterns of failure (debrief themes) rather than one-off bugs.
- Building a recurring QA cadence the team can actually schedule.

## Applies If (ALL must hold)

- Product is interactive (UI, API, CLI) with user-meaningful workflows.
- Feature has just shipped OR is mid-flight, with at least one AC documented.
- Team has 1-3 hours per week to invest in exploratory testing.
- Automated tests run for the feature (so exploratory time is not spent on what tests already cover).

## Skip If (ANY kills it)

- Feature is pure infrastructure with no user-meaningful surface — automated + integration tests are the right investment.
- Pre-release with the build broken — fix the build first; exploration on broken builds finds noise.
- Team has no QA capacity at all — exploratory time needs to be claimed explicitly, not hoped for.
- The only available explorer wrote the code AND no second perspective is available — bias makes solo exploration low-yield; either pair or skip.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Working environment for the feature | staging / preview deploy / local with seeded data | engineering |
| Recent automated-test runs | CI artefact | engineering |
| 60-90 minute uninterrupted block | calendar | operator |
| Written mission for the session | one sentence | explorer |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[qa-risk-matrix-method]] | Risk matrix drives the focus-area selection. |
| [[qa-ac-to-assertion-mapping]] | The AC mapping bounds the exploration (do not re-cover what is already mapped). |
| [[qa-changed-lines-coverage-dashboard]] | The dashboard shows which files are thinly covered; explorer prioritises those. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules + skip rule: single mission pre-committed, time-box strict, observation log continuous, debrief within 24h, no-test-script only ideas | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for charter + observation log + debrief + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns (symptom/root-cause/fix) | ~900 |
| `content/04-procedure.xml` | essential | 5-step procedure: charter draft → prep → session → debrief → publish | ~800 |
| `content/05-examples.xml` | essential | Worked example: onboarding-email i18n exploration session | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `mission_drafting_from_feature_spec` | sonnet | Bounded synthesis from AC + risk matrix. |
| `focus_area_proposal` | sonnet | 3-5 areas selected from spec and risk inputs. |
| `bug_clustering_from_observation_log` | sonnet | Per-bug judgement on severity and area. |
| `debrief_synthesis` | opus | Cross-observation synthesis: themes, follow-ups, debt. |

## Templates

| File | Purpose |
|------|---------|
| `templates/charter.md` | One-page charter: mission, focus, target, time-box. |
| `templates/observation-log.md` | Time-stamped log of test ideas, observations, questions, bugs. |
| `templates/debrief.md` | Post-session debrief: findings, follow-ups, debt, time spent. |
| `templates/_smoke-test.json` | Minimum viable charter+log+debrief artefact for the validator self-test. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-qa-exploratory-charter-template.py` | Validate the charter + observation log + debrief against `content/02-output-contract.xml`. | After every session, before publishing the debrief. |

## Related

- [[qa-risk-matrix-method]]
- [[qa-ac-to-assertion-mapping]]
- [[qa-changed-lines-coverage-dashboard]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs — feature surface, build status, exploration capacity, explorer bias — onto a rule id from `content/01-core-rules.xml`. Walk it before scheduling: it catches broken-build sessions and solo-biased exploration upstream.
