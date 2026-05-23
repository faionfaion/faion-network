---
slug: test-self-healing-locators-audited
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a healer policy (role+accessible-name match + reviewable `healed-selectors.diff`) so AI-fixed E2E selectors don't silently click the wrong button.
content_id: "324c066ffe22f341"
complexity: medium
produces: config
est_tokens: 4200
tags: [self-healing, playwright, e2e-testing, locators, accessibility-tree]
---
# Self-Healing Locators with Mandatory Audit Diff

## Summary

**One-sentence:** Restrict E2E selector self-healing to candidates matching the original locator's accessibility role AND accessible name; require every heal to land as a reviewable diff before CI consumes it.

**One-paragraph:** In Playwright, Cypress, or Selenium suites where an AI healer auto-repairs broken selectors, restrict healing to candidates that match the original locator's accessibility role and accessible name, and require every heal to land as a reviewable diff (`healed-selectors.diff` or equivalent) before the next CI run consumes it. Auto-healing without an audit trail is silent test rot; allowing arbitrary CSS-substitution heals is how an E2E suite ends up clicking the wrong button on a payment screen.

**Ефективно для:**

- Playwright/Cypress/Selenium suites з частими selector breaks.
- WCAG-aware UIs, де role+accessible-name надійні.
- Payment / checkout flows: silent click-wrong-button — недопустиме.
- Audit-driven QA orgs: heal-diff як changelog для tests.

## Applies If (ALL must hold)

- E2E suite (Playwright / Cypress / Selenium) where locators break often.
- AI healer is enabled or proposed.
- Reviewer capacity exists to triage `healed-selectors.diff` weekly.

## Skip If (ANY kills it)

- Suite small enough that broken locators are fixed by hand in minutes.
- Application has no accessible-name affordances (legacy / canvas-only UI).
- Team unwilling to gate healing on review — healer will be effectively disabled.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Existing E2E suite | code | tests/e2e/ |
| Accessibility-tree snapshot of app | JSON | tests/fixtures/ |
| Healer plugin / CLI | binary | deps |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | This methodology has no upstream dependencies. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip-this-methodology | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom/root-cause/fix) | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure with decision gates | 800 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion ref=rule-id | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-output` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/healer-ci.yml` | CI workflow that emits heals to a diff file and gates next run on human merge. |
| `templates/healer-policy.json` | Healer policy with match dimensions, blocklist, scope, rollback window. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-test-self-healing-locators-audited.py` | Validate produced artefact against schema | CI on each artefact change; pre-commit |

## Related

- [[test-mutation-feedback-loop]]
- [[test-tdd-red-green-split-agents]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (input shape, infra availability, decision class) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
