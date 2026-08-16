<!--
purpose: Checklist-form acceptance criteria — functional, validation, error-handling, performance and security criteria for one story.
consumes: recent task context for the story (see Prerequisites)
produces: acceptance-criteria checklist artefact
depends-on: content/02-output-contract.xml
token-budget-impact: ~230 tokens when filled
-->

# Acceptance Criteria: <story_requirement_id>

**Requirement:** <brief_description>

## Functional Criteria

- [ ] System must <behavior_1>
- [ ] System must <behavior_2>
- [ ] System must not <prohibited_behavior>
- [ ] When <condition>, system must <behavior>

## Validation Criteria

- [ ] <field> is required
- [ ] <field> must be [format/type — e.g. valid email, positive integer]
- [ ] <field> must be between <min> and <max>
- [ ] <field> must be unique [scope — e.g. per user, globally]

## Error Handling Criteria

- [ ] When <error_condition>, display "<exact_error_message>"
- [ ] When <error_condition>, system must [recovery behavior — preserve state, rollback, etc.]

## Performance Criteria

- [ ] [Action] must complete within <time> at <percentile> under <load>
- [ ] System must support [N] concurrent <users_transactions> without degradation

## Security Criteria

- [ ] Only <role> can [action]
- [ ] <sensitive_data> must be [encrypted at rest / masked in logs / not returned to <role>]
