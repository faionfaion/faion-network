---
slug: ai-accessibility-automation-2026
tier: geek
group: ux
domain: ux
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a 2026 accessibility automation config wiring AI-powered scanning (axe-core + Lighthouse + AI triage) into CI, with automated WCAG 2.2 AA reporting and a human-required-for-AT testing gate.
content_id: "8dc65b2e896ba292"
complexity: deep
produces: config
est_tokens: 4200
tags: [accessibility, wcag, ai-automation, compliance, triage]
---
# AI Accessibility Automation 2026

## Summary

**One-sentence:** Produces a 2026 accessibility automation config wiring AI-powered scanning (axe-core + Lighthouse + AI triage) into CI, with automated WCAG 2.2 AA reporting and a human-required-for-AT testing gate.

**One-paragraph:** 2026 a11y tooling combines deterministic scanners (axe-core, Lighthouse) with AI triage (severity classification, false-positive filter, fix suggestion). Together they catch 60–70 % of WCAG 2.2 AA issues; the remaining 30–40 % require human + assistive-technology testing. This methodology produces a CI config wiring all three stages (scan + AI triage + report) with explicit AT-testing requirements logged for the remainder.

**Ефективно для:** a11y engineer, що автоматизує WCAG 2.2 AA сканування в CI на топі deterministic scanners + AI triage.

## Applies If (ALL must hold)

- Product targets WCAG 2.2 AA conformance.
- CI environment available with browser automation.
- AT testing budget exists for the 30–40 % the scanners cannot catch.

## Skip If (ANY kills it)

- AT testing budget does not exist — automation alone is incomplete.
- Product is in early prototype (no stable URLs to scan).
- Compliance target is below AA (legacy systems) — automation overshoots.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Site URL inventory | JSON array | ops |
| Scanner provider config (axe / Lighthouse versions) | JSON | engineering |
| AI triage model + prompt | config | engineering |
| AT testing roster + cadence | calendar | a11y team |

## Assumes Loaded

| Methodology | Why |
|---|---|
| [[ai-assisted-accessibility]] | Pipeline + AT-testing context. |
| [[ai-spatial-computing]] | Companion for spatial / XR a11y. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules + rationale + source. | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid / forbidden examples. | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom / root-cause / fix). | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end. | ~800 |
| `content/06-decision-tree.xml` | essential | Routing tree → conclusion(ref=rule-id). | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `decide-applies` | sonnet | Decision tree application. |
| `produce-config` | sonnet | Structured output composition. |
| `validate-output` | haiku | Schema check. |

## Templates

| File | Purpose |
|---|---|
| `templates/a11y-ci.yml` | GitHub Actions workflow scaffolding scanner + AI triage + CI fail policy. |
| `templates/triage-prompt.txt` | AI triage prompt template with severity rubric. |
| `templates/_smoke-test.yml` | Filled WCAG 2.2 AA workflow. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-ai-accessibility-automation-2026.py` | Validate the artefact against the output contract. | Pre-commit + CI. |

## Related

- [[ai-assisted-accessibility]]
- [[ai-spatial-computing]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals to a rule in `01-core-rules.xml`. Walk it before producing the config; mis-routing leads to producing the wrong artefact shape.
