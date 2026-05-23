<!-- purpose: Markdown template for a Scrum user story (As a / I want / So that, AC). -->
<!-- consumes: see content/02-output-contract.xml inputs for azure-devops-boards -->
<!-- produces: config -->
<!-- depends-on: content/01-core-rules.xml + content/02-output-contract.xml -->
<!-- token-budget-impact: ~200-1000 tokens when loaded as context -->

# User Story: [Title]

**As a** [persona/role],  
**I want** [capability or action],  
**So that** [benefit or outcome].

## Acceptance Criteria

```gherkin
Given [precondition]
When [action]
Then [expected result]

Given [precondition]
When [action]
Then [expected result]
```

## Description

[Additional context, background, and details not captured in the user story statement.]

## Design

[Link to Figma mockups or design document]

## Technical Notes

[Implementation considerations, API changes, database migrations, performance impact]

## Dependencies

- Depends on: #[work item ID or external dependency]
- Blocks: #[work item ID]

## Out of Scope

- [Explicitly excluded capability 1]
- [Explicitly excluded capability 2]

## Definition of Done

- [ ] Code complete and pushed to feature branch
- [ ] Unit tests written (coverage >80%)
- [ ] Code review approved by at least 1 reviewer
- [ ] Integration tests passing in CI
- [ ] Documentation updated
- [ ] Deployed to staging environment
- [ ] Product Owner accepted in staging
