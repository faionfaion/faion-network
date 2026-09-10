# Use Case Modeling

## Summary

**One-sentence:** Express functional requirements as named-actor → system interaction sequences (main scenario + alternative + exception flows) with preconditions, postconditions, and trigger per use case.

**One-paragraph:** Pre-development functional spec: identify primary + secondary + offstage actors, write use-case briefs with goal-in-context, main success scenario, alternative flows, exception flows, preconditions and postconditions. Output is a `spec` artefact: machine-checkable use-case set ready for AC generation and test-case derivation.

**Ефективно для:**

- Functional-spec stage перед development для actor-driven domains.
- Pre-AC generation — use cases dive into flows перед Gherkin.
- Test-case derivation — main + alt + exception → test cases 1:1.
- Compliance domains де actor authority matters (banking, healthcare).

## Applies If (ALL must hold)

- System exposes ≥3 actor-driven interactions (login, checkout, approve, refund...).
- Functional requirements need flow detail beyond user-story summary.
- Test team will derive scenarios from spec.
- Each actor is identifiable (role title acceptable; "Team" is not).

## Skip If (ANY kills it)

- Event-driven / pipeline system with no human actor — use process modeling instead.
- Single-actor CRUD app where stories suffice.
- Pure UI / styling work with no domain flow.
- Spike / prototype throwaway.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Actor inventory | YAML / Markdown table | BA + stakeholders |
| Domain glossary | Markdown | BA |
| Use-case backlog (titles) | list | product |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[user-story-mapping]] | Upstream — story map produces the use-case backlog titles |
| [[acceptance-criteria]] | Downstream — each use case main+alt+exception → AC set |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: named actors, main + alt + exception, pre/postconditions, single goal, trace-id to backlog | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema + examples | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: anonymous actor, missing exception flow, prose preconditions, kitchen-sink scope | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure | 700 |
| `content/05-examples.xml` | essential | Worked example: "User books an appointment" | 700 |
| `content/06-decision-tree.xml` | essential | Routing on flow completeness + actor naming | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `actor_enumeration` | haiku | Mechanical pull from glossary + interviews. |
| `main_scenario_drafting` | sonnet | Step-by-step interaction needs light judgment. |
| `exception_flow_brainstorm` | opus | Edge-case enumeration benefits from deeper reasoning. |

## Templates

| File | Purpose |
|------|---------|
| `templates/use-case.md.j2` | Markdown skeleton (actor + goal + pre/post + main + alt + exception) |
| `templates/use-case.md` | Markdown skeleton (actor + goal + pre/post + main + alt + exception) Generated from `templates/use-case.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.json` | Minimum viable use-case JSON |

| `templates/use-case-diagram.md.j2` | solution-wide UML use-case diagram (mermaid) |
| `templates/use-case-diagram.md` | solution-wide UML use-case diagram (mermaid) Generated from `templates/use-case-diagram.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/use-case-spec.md.j2` | per-use-case skeleton (actor + goal + pre/post + flows) |
| `templates/use-case-spec.md` | per-use-case skeleton (actor + goal + pre/post + flows) Generated from `templates/use-case-spec.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[user-story-mapping]]
- [[acceptance-criteria]]
- [[business-process-analysis]]
- [[interface-analysis]]

## Decision tree

See `content/06-decision-tree.xml`. Routes on actor naming + flow completeness to the rule firing. Use when in doubt whether a use case is ready for AC derivation.
