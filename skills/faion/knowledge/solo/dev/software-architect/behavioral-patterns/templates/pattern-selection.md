# purpose: Behavioural pattern selection record.
# consumes: inputs declared in AGENTS.md Prerequisites; schema in content/02-output-contract.xml
# produces: a behavioral-patterns artefact validating against scripts/validate-behavioral-patterns.py
# depends-on: content/01-core-rules.xml, content/02-output-contract.xml
# token-budget-impact: ~400-1500 tokens once filled
---
artefact_id: behavioral-pattern-selection-<system>-2026-05-23
owner: <Full Name> <email>
version: 1.0.0
last_reviewed: 2026-05-23
---

## Variance hotspot

`<module.path.function>` — uses if/elif on type / mode / strategy.

## Diagnosed pattern

- Pattern: `<Strategy|State|Chain of Responsibility|Observer|Command|Template Method|Mediator|Iterator|Visitor>`
- Reason: <one sentence>

## Refactor sketch

- new abstract: `<Type>`
- concrete implementations: `<Type1>`, `<Type2>`, `<Type3>`
- selection: <factory / DI container / config>

## Anti-misuse note

<one sentence on which other pattern this is NOT and why>
