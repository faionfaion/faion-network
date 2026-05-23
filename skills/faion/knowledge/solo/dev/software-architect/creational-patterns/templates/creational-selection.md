# purpose: Creational pattern selection record.
# consumes: inputs declared in AGENTS.md Prerequisites; schema in content/02-output-contract.xml
# produces: a creational-patterns artefact validating against scripts/validate-creational-patterns.py
# depends-on: content/01-core-rules.xml, content/02-output-contract.xml
# token-budget-impact: ~400-1500 tokens once filled
---
artefact_id: creational-pattern-selection-<system>-2026-05-23
owner: <Full Name> <email>
version: 1.0.0
last_reviewed: 2026-05-23
---

## Construction hotspot

`<module.path.Type>` — has N params or invariants on construction.

## Diagnosed pattern

- Pattern: `<FactoryMethod|AbstractFactory|Builder|Prototype|Singleton|ObjectPool|DI>`
- Reason: <one sentence>

## DI container

- Container: `<dependency-injector|wired|punq|manual>`
- Scope: `<request|app|singleton>`

## Anti-misuse note

<one sentence on which other pattern this is NOT and why>
