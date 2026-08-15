<!--
purpose: Authoring template with inline guidance — the fill-in form of the Nygard record.
consumes: decision title, context forces, >=2 genuine alternatives, positive + negative consequences
produces: an ADR markdown file matching the shape adr-lint.sh greps for (r2, r3, r6, r7)
depends-on: content/01-core-rules.xml, content/02-output-contract.xml
token-budget-impact: ~400 tokens once filled
variables:
  - name: adr_number
    type: string
    required: true
    description: The sequence number, zero-padded to four digits here (0007) because adr-lint.sh greps for ADR-NNNN. Next free number in docs/adr; never reused.
  - name: adr_title
    type: string
    required: true
    description: Short noun phrase naming what is being decided, not the option that won. "Session storage for checkout", not "Adopt Redis" - the title has to still read true after a superseding ADR.
  - name: date
    type: string
    required: true
    description: The day the deciders actually agreed, ISO (2026-08-15) - not the day you wrote it up. The gap between those two dates is itself worth knowing.
  - name: deciders
    type: string
    required: true
    description: Who decided, as handles - "@olena, @taras". List only the people whose objection would have changed the outcome; everyone else was in the room, not in the decision.
  - name: context
    type: text
    required: true
    description: The situation and the forces - technical, business, team. Factual and value-neutral, constraints included. Tell me the numbers and the deadline; do not argue the case here.
  - name: decision_choice
    type: text
    required: true
    description: The specific thing you will do, phrased to complete "We will ___". A concrete choice, not a direction - "move session state to Redis with a 30-minute TTL", not "improve session handling".
  - name: decision_scope
    type: text
    required: true
    description: What the decision binds, phrased to complete "for ___". Name the systems, services or teams it applies to - and by omission, the ones it does not.
-->

# ADR-{{adr_number}}: {{adr_title}}

**Status:** Proposed
**Date:** {{date}}
**Deciders:** {{deciders}}

---

## Context

{{context}}

## Decision

We will _{{decision_choice}}_ for _{{decision_scope}}_.

## Alternatives Considered

**Option A: [Name]**
- Pro: ...
- Pro: ...
- Con: ...
- Rejected because: _one sentence_

**Option B: [Name]**
- Pro: ...
- Con: ...
- Rejected because: _one sentence_

**Do nothing**
- Rejected because: _one sentence_

## Consequences

**Positive:**
- ...

**Negative:**
- ...

**Risks and mitigations:**
- Risk: ... — Mitigation: ...

## Related ADRs

- Supersedes: (ADR-NNNN or none)
- Related: (ADR-NNNN or none)
