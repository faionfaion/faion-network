# Use Case: [UC-XXX] [Verb + Noun]

**Version:** [X.X]
**Status:** [Draft | Review | Approved]
**Source:** [interview line, SoW section, screenshot ID]
**Regulation anchors:** [21CFR11.10(e), IEC62304-5.2.2, or none]

## Overview

- **ID:** UC-[XXX]
- **Name:** [Verb + Noun]
- **Description:** [One sentence: what the actor achieves and why]
- **Primary Actor:** [Name] (type: human | system | time)
- **Secondary Actors:** [Other actors, or none]

## Preconditions

- [Verifiable condition before use case starts]
- [Another precondition]

## Postconditions

**Success:**
- [Observable state after successful completion — DB row, message, file, audit log]

**Failure:**
- [Observable state if use case fails]

## Triggers

- [What initiates this use case]

## Main Flow (5-9 steps)

| Step | Actor Action | System Response |
|------|--------------|-----------------|
| 1 | [Actor does X] | [System validates/persists/emits/notifies Y] |
| 2 | [Actor does X] | [System validates/persists/emits/notifies Y] |
| 3 | [Actor does X] | [System validates/persists/emits/notifies Y] |

## Alternative Flows

### AF-1: [Name]
**Trigger:** At step [X], [condition].

| Step | Actor Action | System Response |
|------|--------------|-----------------|
| [Xa] | [Action] | [Response] |

**Return:** Step [N] of main flow.

## Exception Flows

### EX-1: [Name]
**Trigger:** At step [X], [error condition].

| Step | System Response |
|------|-----------------|
| [Xa] | [Error handling with observable end state] |

**End State:** [How use case ends — rollback, error logged, user notified]

## Business Rules

- BR-[X]: [Business rule that applies]

## Related Use Cases

- [UC-XXX]: [includes | extends | generalization]

## Non-Functional Requirements

- [Performance, security, or other NFRs]
