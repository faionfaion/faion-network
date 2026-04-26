# Use Case Modeling

## Summary

Use case modeling captures WHO interacts with a system, WHAT they do with it, and WHY — as a sequence of actor-system interactions that yields observable value. Each use case has a name (Verb + Noun), a primary actor, a main flow (5-9 steps), at least one alternative flow, and at least one exception flow. The deliverable is a UC spec plus a UC diagram showing actor-system boundaries. Use-case-driven BA is contractual: the UC catalog becomes the apples-to-apples grid for vendor evaluation and the traceability anchor for regulated-industry audits.

## Why

Requirements written as feature lists leave developers without user context, testers without scenario coverage, and projects without a basis for impact analysis when scope changes. UCs anchor requirements at actor-goal level — a stable abstraction above UI screens and API endpoints — giving all parties a shared language that survives redesigns. Traceability from actor goal to step to commit to test to audit evidence is the primary value in regulated sectors (21 CFR Part 11, ISO 13485, IEC 62304, SOX).

## When To Use

- Enterprise kickoffs requiring a UML UC diagram + UC specs as SoW deliverables (SAP, Salesforce, Dynamics rollouts, banking core upgrades).
- RFP/RFI authoring — UC catalog is the vendor evaluation grid.
- RUP-style use-case-driven projects in regulated or government contexts where iterations are scoped to UC sets.
- Regulated industries where UCs anchor actor goal → step → commit → test → audit evidence.
- Legacy migration (mainframe, Oracle Forms) where reverse-engineering screens into UCs is the safe path to a greenfield spec.
- Outsourced delivery where step-level UC specs replace ambient context the offshore team lacks.
- Stakeholder alignment workshops bridging executive outcomes and engineering features.

## When NOT To Use

- Lean/startup contexts — JTBD, Opportunity Solution Trees, or story mapping deliver faster discovery without SoW UC obligations.
- Data/analytics platforms — DFDs and dimensional models better expose the meaningful structure.
- Internal tools with a single actor and fewer than 10 transactions — a one-page acceptance-criteria sheet suffices.
- ML/LLM surfaces with probabilistic responses — UC main flows assume deterministic system responses and mislead.
- Event-sourced/reactive architectures — event storming better exposes the structure.
- Teams already running smoothly on user stories + acceptance criteria — layering UCs duplicates work.

## Content

| File | What's inside |
|------|---------------|
| `content/01-concepts.xml` | Use case components, actor types, relationship types (include/extend/generalization), quality checklist. |
| `content/02-process.xml` | Five-step modeling process: identify actors, identify UCs, create UC diagram, write UC specs, validate. |
| `content/03-examples.xml` | Place Order UC spec example with main/alternative/exception flows; common antipatterns. |

## Templates

| File | Purpose |
|------|---------|
| `templates/uc-spec.md` | Full use case specification template (ID, actors, preconditions, main/alt/exception flows, postconditions, business rules). |
| `templates/uc-diagram.md` | UC diagram template listing actors, UCs per actor, and relationships. |
| `templates/uc-to-plantuml.sh` | Script to emit a PlantUML UC diagram from a use-case-index.json file. |
