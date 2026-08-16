<!--
purpose: Nygard-format single-decision ADR — context, decision, alternatives considered, consequences.
consumes: Feature spec.md context, design.md architecture context, alternatives shortlist (see Prerequisites)
produces: artefact conforming to content/02-output-contract.xml (ADR)
depends-on: content/01-core-rules.xml
token-budget-impact: ~350-600 tokens when loaded as context
-->

# ADR-{NNN}: <decision_title>

**Status:** Proposed | Accepted | Deprecated | Superseded by ADR-<status>
**Date:** YYYY-MM-DD
**Deciders:** <deciders>

## Context

{What is the issue? What forces are at play?
Include technical, business, and team constraints.
Describe the situation that requires a decision.}

## Decision

{What is the change being proposed or made?
Write in active voice: "We will use PostgreSQL because..."
Keep under 100 words. This is the choice, not the justification.}

## Alternatives Considered

### Alternative 1: <name>
- **Pros:** <benefits>
- **Cons:** <drawbacks>
- **Why rejected:** <specific_reason>

### Alternative 2: <name>
- **Pros:** <benefits>
- **Cons:** <drawbacks>
- **Why rejected:** <specific_reason>

## Consequences

### Positive
- {Benefit 1 — downstream effect, not restatement of the decision}
- <benefit_2>

### Negative
- {Tradeoff 1 — what this choice costs us}
- {Risk to mitigate}

### Neutral
- {Implication that is neither good nor bad}

## Related Decisions

- ADR-<adr>: <related_decision_title>
