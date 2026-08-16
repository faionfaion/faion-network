<!--
purpose: Single ADR-style design decision — context, decision, options considered, rationale, consequences.
consumes: Approved spec.md, constitution.md per Prerequisites
produces: artefact conforming to content/02-output-contract.xml (design, ADR variant)
depends-on: content/01-core-rules.xml
token-budget-impact: ~400-650 tokens when loaded as context
-->

# ADR-{NNN}: <decision_title>

**Status:** Proposed / Accepted / Deprecated / Superseded by ADR-<status>
**Date:** <date>
**Feature:** {feature-NNN-name or "cross-cutting"}

## Context

{What situation or problem prompted this decision. Relevant constraints, requirements, or forces at play. What makes this a non-trivial decision worth recording.}

## Decision

{What was decided. State it clearly and specifically — not "we'll use a good approach" but "we'll use PostgreSQL for session storage".}

## Options Considered

### Option A: <name>

<description>

Pros:
- <pro>
- <pro>

Cons:
- <con>
- <con>

### Option B: <name>

<description>

Pros:
- <pro>

Cons:
- <con>

### Option C: <name> (if applicable)

{Description, pros, cons}

## Rationale

{Why this option was chosen over the alternatives. Reference specific constraints, data, or principles from constitution.md that drove the decision.}

## Consequences

**Positive:**
- {What becomes easier or better}
- {What new capability this enables}

**Negative:**
- <what_becomes_harder>
- {Technical debt or risk accepted}

**Neutral:**
- {Side effects that are neither good nor bad}

## Related

- ADR-<adr>: <related_decision>
- Constitution section: <relevant_section>
