# AI-Assisted Accessibility (WCAG 2.2 AA)

## Summary

**One-sentence:** Produces a WCAG 2.2 AA conformance report combining AI-enhanced automated scanning (axe-core, Lighthouse) for 60–70 % coverage with structured AT + human testing plan for the remainder.

**One-paragraph:** WCAG 2.2 AA conformance cannot be proved by automation alone — automated tools catch ~60–70 % of issues, the remaining 30–40 % (cognitive, screen reader, voice navigation) require human + assistive-technology testing. This methodology produces a conformance report combining automated scan output (axe-core + Lighthouse + AI triage) with a human-AT test plan for the gap. Output is a single signed report that legal / procurement can rely on, not a screenshot of a dashboard.

**Ефективно для:** a11y engineer, що готує WCAG 2.2 AA conformance report для legal / procurement + знає що automation покриває 60–70%.

## Applies If (ALL must hold)

- Product is going to procurement or legal review requiring a conformance statement.
- Both automated scanning AND human + AT testing are available.
- Stakeholders need a signed report (PDF / signed JSON), not a dashboard link.

## Skip If (ANY kills it)

- Automation only available, no AT testing — report would be incomplete.
- Conformance target is below AA — methodology overshoots; use legacy methodology.
- Single-page prototype — automation overhead exceeds benefit.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Site URL inventory | JSON array | ops |
| Automated scan output | JSON | [[ai-accessibility-automation-2026]] |
| AT tester roster | list | a11y team |
| Conformance target | enum (AA / AAA) | legal |

## Assumes Loaded

| Methodology | Why |
|---|---|
| [[ai-accessibility-automation-2026]] | Automation pipeline that produces the input scans. |
| [[ai-design-assistant-patterns]] | AI surface patterns boundary. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules + rationale + source. | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid / forbidden examples. | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom / root-cause / fix). | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end. | ~800 |
| `content/05-examples.xml` | essential | One full worked example end-to-end. | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree → conclusion(ref=rule-id). | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `decide-applies` | sonnet | Decision tree application. |
| `produce-report` | sonnet | Structured output composition. |
| `validate-output` | haiku | Schema check. |

## Templates

| File | Purpose |
|---|---|
| `templates/conformance-report.json` | JSON skeleton: site + target + automated + AT + verdict + signature + next audit. |
| `templates/conformance-report.md` | Markdown narrative skeleton accompanying JSON. |
| `templates/_smoke-test.json` | Filled faion.net partial-conformance example. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-ai-assisted-accessibility.py` | Validate the artefact against the output contract. | Pre-commit + CI. |

## Related

- [[ai-accessibility-automation-2026]]
- [[ai-design-assistant-patterns]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals to a rule in `01-core-rules.xml`. Walk it before producing the report; mis-routing leads to producing the wrong artefact shape.
