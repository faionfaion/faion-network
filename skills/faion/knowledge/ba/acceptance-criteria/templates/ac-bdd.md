<!--
purpose: Given/When/Then acceptance-criteria skeleton for one story
consumes: story id + requirement summary from the backlog
produces: Markdown artefact conforming to content/02-output-contract.xml
depends-on: content/01-core-rules.xml
token-budget-impact: ~250 tokens when loaded as context
variables:
  - name: story_id
    type: string
    required: true
    description: The tracker id these criteria belong to (PROJ-412). Criteria that float free of a story get re-litigated in QA, by people who were not in the refinement session.
  - name: requirement_summary
    type: text
    required: true
    description: What the story delivers, one sentence, from the user's side. If you cannot say it without naming a table or an endpoint, you are describing a task and the criteria will test the wrong thing.
  - name: author
    type: string
    required: true
    description: Who wrote these criteria. Ambiguity gets resolved by asking a person, and "the team" is not a person you can ask on the day the build is red.
  - name: happy_path_name
    type: string
    required: true
    description: Four or five words naming the main scenario - the path when nothing goes wrong. It becomes the test name people quote in standup, so make it readable out loud.
  - name: error_scenario_name
    type: string
    required: true
    description: Name of the failure scenario. Every set needs at least one - a story with no failure path does not lack failures, it lacks tested ones.
  - name: perf_threshold
    type: text
    required: true
    description: The performance criterion as a number and a percentile - "p95 under 2s with 50 concurrent users". "Fast" is not testable and will be argued about the week after release.
  - name: security_rule
    type: text
    required: true
    description: The role-based rule this story must enforce, by role and action - "only Admin may delete records". Say who may NOT do it as well; that half is what gets missed.
-->
# Acceptance Criteria: {{story_id}}

**Requirement:** {{requirement_summary}}
**Author:** {{author}}

## Scenarios

### Scenario 1: {{happy_path_name}}
**Given** [precondition / system state]
**And** [additional precondition]
**When** [action taken by actor]
**Then** [expected observable outcome]
**And** [additional observable outcome]

### Scenario 2: [Alternative Path Name]
**Given** [precondition]
**When** [different action or condition]
**Then** [expected outcome for this variation]

### Scenario 3: {{error_scenario_name}}
**Given** [precondition]
**When** [action that triggers the error condition]
**Then** [error message or system recovery behavior — observable]
**And** [system state after error — no partial changes, rollback, etc.]

## Non-Functional Criteria

- Performance: {{perf_threshold}}
- Security: {{security_rule}}

## Out of Scope

- [What is explicitly NOT covered by these acceptance criteria]
