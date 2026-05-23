<!-- purpose: per-use-case skeleton (actor + goal + pre/post + flows) -->
<!-- consumes: actor inventory + backlog title + glossary -->
<!-- produces: one entry in use_cases[] -->
<!-- depends-on: content/01-core-rules.xml, content/02-output-contract.xml -->
<!-- token-budget-impact: ~350 tokens loaded as template context -->

# Use Case: [UC-XXX] [Verb+Noun Name]

**Version:** 1.0
**Status:** Draft | Review | Approved

## Overview

**ID:** UC-[XXX]
**Primary Actor:** [Actor name]
**Secondary Actors:** [Other actors, or "none"]
**Description:** [One sentence: what goal the primary actor achieves]

## Preconditions

- [Verifiable system state before use case starts]
- [Additional precondition]

## Triggers

- [Event or action that initiates this use case]

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
- [Observable system state — record created, message sent, file written]

**Failure:**
- [Observable system state — no change, rollback, notification sent]

## Business Rules

- BR-[X]: [Rule that applies to this use case]

## Related Use Cases

- [UC-XXX]: [Relationship — includes / extends / related]

## Non-Functional Requirements

- [Performance, security, or other requirements specific to this use case]
