---
slug: testing-with-assistive-technology
tier: pro
group: ux
domain: ux
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces an AT-testing config: three tiers — automated scan in CI (every PR), manual screen-reader and keyboard sweep (every release), assistive-user session (quarterly) — with bug-report format (WCAG SC + repro + ARIA APG pattern + scope).
content_id: "ce2fa9cf82831858"
complexity: medium
produces: config
est_tokens: 4000
tags: [accessibility, wcag, testing, assistive-technology, screen-reader]
---
# Testing with Assistive Technology

## Summary

**One-sentence:** Produces an AT-testing config: three tiers — automated scan in CI (every PR), manual screen-reader and keyboard sweep (every release), assistive-user session (quarterly) — with bug-report format (WCAG SC + repro + ARIA APG pattern + scope).

**One-paragraph:** Automated a11y tools catch only 30-50% of real WCAG issues; the remainder requires manual screen-reader/keyboard sweep and lived-experience sessions with users who use assistive tech daily. This methodology declares the three-tier testing config: CI scan (axe/pa11y/lighthouse, every PR), manual sweep (NVDA/JAWS/VoiceOver/keyboard, every release), AT-user session (recruited via a11y-research partner, quarterly). Each tier's expected coverage + bug-report format (WCAG SC reference + repro snippet + suggested ARIA APG pattern + scope estimate) is enforced.

**Ефективно для:**

- Pre-launch a11y readiness audit ('did we test enough?').
- Setting CI a11y gate (axe/pa11y/lighthouse on every PR).
- Quarterly assistive-user research planning + budgeting.
- Standardising bug reports так, що engineering може діяти без translation cost.

## Applies If (ALL must hold)

- Product surface ships to public users (US/EU/Ontario/federal).
- Engineering can integrate axe / pa11y / lighthouse into CI.
- Budget exists for ≥1 AT-user session per quarter.

## Skip If (ANY kills it)

- Pre-MVP internal alpha — full three-tier overhead too high.
- Implementation-level fixes — use specific WCAG rule methodologies.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| CI pipeline | config files | engineering |
| Tier list (free/solo/pro/geek) | list | PM |
| AT-user recruiting partner | vendor or list | a11y research |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[wcag-22-compliance]] | test target standard is defined |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: three-tier-mandatory, automated-on-every-pr, manual-sweep-per-release, at-user-session-quarterly, bug-report-format | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the produced artefact + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 900 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals -> rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `configure-ci` | haiku | Mechanical install + config. |
| `plan-manual-sweep` | sonnet | Coverage planning. |
| `recruit-at-users` | opus | Partner outreach + ethics. |

## Templates

| File | Purpose |
|------|---------|
| `templates/at-testing-config.json` | Skeleton three-tier config |
| `templates/a11y-bug-template.md` | Bug-report template (Jira / Linear) |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-testing-with-assistive-technology.py` | Validate the artefact against the schema | Pre-commit; CI on each artefact change |

## Related

- [[wcag-22-compliance]]
- [[regulatory-compliance-2026]]
- [[accessibility-evaluation]]

## Decision tree

See `content/06-decision-tree.xml`. Branches by launch context (pre-launch / post-launch maintenance) and enforces tier completeness. Missing AT-user-quarterly downgrades compliance. Each leaf cites a rule from `01-core-rules.xml`.
