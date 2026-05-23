<!-- purpose: Template fixture for user-story-mapping: story-map.md -->
<!-- consumes: content/01-core-rules.xml -->
<!-- produces: Markdown artefact -->
<!-- depends-on: content/02-output-contract.xml -->
<!-- token-budget-impact: small -->
# User Story Map: [Product Name]

**Version:** [X.X]
**Date:** [Date]
**Product Owner:** [Name]
**Business Analyst:** [Name]

## Personas

- [Persona 1]: [Brief description and primary goal]
- [Persona 2]: [Brief description and primary goal]

## Backbone (Activities)

| Step | Activity | Persona Goal |
|------|----------|-------------|
| 1 | [Activity 1] | [What user wants to achieve] |
| 2 | [Activity 2] | [What user wants to achieve] |
| 3 | [Activity 3] | [What user wants to achieve] |

## Walking Skeleton (Tasks per Activity)

| Activity 1 | Activity 2 | Activity 3 |
|------------|------------|------------|
| Task 1.1 | Task 2.1 | Task 3.1 |
| Task 1.2 | Task 2.2 | Task 3.2 |

## Story Map

### Activity 1: [Name]

**Task 1.1: [Name]**

| Release | Story | Persona | Priority | Size |
|---------|-------|---------|----------|------|
| R1 | [Story title] | [Persona] | Must | S/M/L |
| R2 | [Story title] | [Persona] | Should | S/M/L |
| R3 | [Story title] | [Persona] | Could | S/M/L |

**Exception path (red row):**
- [Exception scenario 1]
- [Exception scenario 2]

## Release Plan

### Release 1: Walking Skeleton
**Goal:** [What coherent end-to-end journey this release delivers]
**Walking skeleton check:** Read each cell aloud as a contiguous narrative — does it form a coherent user story?

### Release 2: [Theme]
**Goal:** [Enhancement delivered]

## NFR Register (linked, not mapped)

| NFR | Category | Applies To | Owner |
|-----|----------|------------|-------|
| [NFR] | perf/sec/a11y/audit | [Release/Activity] | [Owner] |
