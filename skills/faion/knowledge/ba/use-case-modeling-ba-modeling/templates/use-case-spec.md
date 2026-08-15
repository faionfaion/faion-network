<!--
purpose: per-use-case skeleton (actor + goal + pre/post + flows)
consumes: actor inventory + backlog title + glossary
produces: one entry in use_cases[]
depends-on: content/01-core-rules.xml, content/02-output-contract.xml
token-budget-impact: ~350 tokens loaded as template context
variables:
  - name: uc_id
    type: string
    required: true
    description: The use-case id (UC-014). The traceability matrix points at it, so allocate once and never renumber - a renumbered use case silently orphans every requirement that cited it.
  - name: uc_name
    type: string
    required: true
    description: Verb plus noun from the actor's side - "Submit Expense Claim". Not "Expense Module" and not a screen name; a use case is something a person does, not a place they do it.
  - name: primary_actor
    type: string
    required: true
    description: The single actor whose goal this satisfies, by role and not by name. If two roles want different outcomes from these steps, you are holding two use cases in one document.
  - name: goal_sentence
    type: text
    required: true
    description: One sentence - what the actor achieves and why they care. It must still read true with the system switched off; a goal that mentions a button is a screen description.
  - name: trigger
    type: text
    required: true
    description: The event that starts this - a user action, a schedule, an inbound message. Say what is observably true in the instant before step 1.
  - name: precondition
    type: text
    required: true
    description: A verifiable system state before the flow begins. Verifiable means somebody could query it - "user is authenticated and the claim period is open", not "user is ready".
  - name: success_postcondition
    type: text
    required: true
    description: What is observably true afterwards - the record written, the message emitted, the file produced. Name the thing an automated test could assert on.
-->

# Use Case: {{uc_id}} {{uc_name}}

**Version:** 1.0
**Status:** Draft | Review | Approved

## Overview

**ID:** {{uc_id}}
**Primary Actor:** {{primary_actor}}
**Secondary Actors:** [Other actors, or "none"]
**Description:** {{goal_sentence}}

## Preconditions

- {{precondition}}
- [Additional precondition]

## Triggers

- {{trigger}}

## Main Flow (Happy Path)

| Step | Actor Action | System Response |
|------|--------------|-----------------|
| 1    | [Actor does X] | [System validates/persists/emits Y] |
| 2    | [Actor does X] | [System validates/persists/emits Y] |
| 3    | [Actor does X] | [System validates/persists/emits Y] |

_(5-9 steps required)_

## Alternative Flows

### AF-1: [Name]
**Trigger:** At step [N], [condition].
| Step | Actor Action | System Response |
|------|--------------|-----------------|
| [N]a | [Action] | [Response] |

**Return:** [Which main flow step resumes]

## Exception Flows

### EX-1: [Name]
**Trigger:** At step [N], [error condition].
| Step | System Response |
|------|-----------------|
| 1    | [Error handling behavior] |

**End State:** [How use case ends — cart preserved, record rolled back, etc.]

## Postconditions

**Success:**
- {{success_postcondition}}

**Failure:**
- [Observable system state — no change, rollback, notification sent]

## Business Rules

- BR-[X]: [Rule that applies to this use case]

## Related Use Cases

- [UC-XXX]: [Relationship — includes / extends / related]

## Non-Functional Requirements

- [Performance, security, or other requirements specific to this use case]
