# Ideation Methods: SCAMPER, Mind Mapping, Starbursting

## Summary

**One-sentence:** Generates a structured idea artefact via SCAMPER (7 lenses on an existing product), Mind Map (visual branching), or Starbursting (5W+H question matrix).

**One-paragraph:** Structured frameworks for generating and developing ideas systematically: SCAMPER (Substitute, Combine, Adapt, Modify, Put to other use, Eliminate, Reverse — apply 7 lenses to an existing product to generate variants), Mind Mapping (visual branching from a central node for exploring connections), Starbursting (5W+H question generation before answering). Unlike group brainstorming, these work solo or in small groups and produce structured idea artefacts, not lists.

**Ефективно для:**

- Solo founder iterating on an existing product without a workshop.
- Generating variants of a feature ('what if we removed X?').
- Exhaustive scoping of a vague initiative via Starbursting.
- Mind-mapping a learning topic for content planning.

## Applies If (ALL must hold)

- Subject exists (SCAMPER needs a thing to modify; pure-greenfield uses brainstorming).
- Operator works solo or in pair, no group required.
- Output is meant as structured artefact (worksheet), not free list.
- 30-60 min uninterrupted available.

## Skip If (ANY kills it)

- Group facilitation needed for buy-in — use brainstorming-techniques.
- Decision is between 2 known options — evaluation methodology applies.
- Subject does not exist yet — use generation-only brainstorming first.
- Author is in evaluation mode — these methods are for divergence only.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Subject | existing product / feature / concept | operator |
| Worksheet tool | doc / Miro / paper | logistics |
| Downstream consumer | who will read the artefact | session owner |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[brainstorming-techniques]] | for group facilitation alternative |
| [[brainstorming-ideation]] | for agentic pipeline alternative |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + sourced rationale | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 700 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 500 |
| `content/06-decision-tree.xml` | essential | Routes by observable signal to a rule from 01-core-rules.xml | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `method-selection` | sonnet | Light judgment on goal fit. |
| `scamper-lens-fill` | sonnet | Variant generation per lens. |
| `mindmap-expand` | sonnet | Connection exploration. |
| `starbursting-questions` | sonnet | Question generation. |

## Templates

| File | Purpose |
|------|---------|
| `templates/scamper-worksheet.md` | 7-lens SCAMPER worksheet skeleton |
| `templates/starbursting-worksheet.md` | 5W+H matrix worksheet skeleton |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ideation-methods.py` | Validate ideation-methods artefact against the schema | CI on each artefact change; pre-commit |

## Related

- [[brainstorming-techniques]]
- [[brainstorming-ideation]]
- [[stakeholder-communication]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes by goal type (variants / connections / scoping) to the matching method and the coverage rule.
