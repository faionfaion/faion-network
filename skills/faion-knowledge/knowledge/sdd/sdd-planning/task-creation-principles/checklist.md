# Task Creation Principles Checklist

## Phase 1: Apply Right Size Principle (8-80 Rule)

- [ ] Define task complexity: simple (<30k tokens) vs normal (30-60k) vs complex (60-100k)
- [ ] Ensure task effort is 1-4 hours of work (single work session)
- [ ] If too large: break into smaller tasks
- [ ] If too small: combine with related work
- [ ] Set hard maximum: 100k tokens per task

## Phase 2: Validate INVEST Criteria

- [ ] **Independent:** Task can be done separately without blocking others?
- [ ] **Negotiable:** Details can be refined and discussed?
- [ ] **Valuable:** Clear user or business value?
- [ ] **Estimable:** Can estimate effort in tokens?
- [ ] **Small:** Fits in 1-4 hours?
- [ ] **Testable:** Clear acceptance criteria defined?

## Phase 3: Define Clear Boundaries

- [ ] **Input:** What must exist before task starts (files, data, dependencies)
- [ ] **Output:** What will exist after (new files, features, data)
- [ ] **Success Criteria:** How to verify completion (tests, AC, metrics)
- [ ] Document what is and is NOT included in this task

## Phase 4: Apply SMART Criteria to Task Goals

- [ ] **Specific:** Only one interpretation of what to do
- [ ] **Measurable:** Can verify completion objectively
- [ ] **Achievable:** Technically feasible with given context
- [ ] **Relevant:** Traces to business need (FR-X)
- [ ] **Time-bound:** Effort estimate provided

## Phase 5: Establish Traceability Links

- [ ] Link task to FR-X (spec) - WHY this task exists
- [ ] Link task to AD-X (design) - HOW to implement
- [ ] Link task to NFR-X (if applicable) - constraints
- [ ] Create Requirements Coverage section in task file
- [ ] Create Architecture Decisions section in task file

## Phase 6: Write Acceptance Criteria (Given-When-Then)

- [ ] Define AC-1: Happy path (successful scenario)
- [ ] Define AC-2: Alternative path (valid variation)
- [ ] Define AC-3: Boundary conditions (limits, edge cases)
- [ ] Define AC-4: Error handling (invalid inputs, failures)
- [ ] Define AC-5: Security scenarios (unauthorized access)
- [ ] Define AC-6: Performance (if NFR applies)
- [ ] Use specific values, not vague language

## Phase 7: Identify Task Dependencies

- [ ] List all tasks that must complete before this one
- [ ] Document WHY each dependency exists
- [ ] Use Finish-to-Start (FS) format
- [ ] Verify no circular dependencies
- [ ] Mark on dependency graph

## Phase 8: Estimate Token Context Budget

- [ ] SDD Documents: ~15% (constitution, spec, design)
- [ ] Task Dependency Tree: ~10% (completed tasks summary)
- [ ] Research: ~25% (existing code patterns)
- [ ] Implementation: ~40% (actual coding)
- [ ] Testing: ~10% (verification)
- [ ] Total must be <100k tokens

## Phase 9: Document Task Dependency Tree

- [ ] Include summary of each completed dependency task
- [ ] For each dependency show: Summary, Files, Patterns, Key code
- [ ] Link to actual dependency task files
- [ ] Extract patterns to follow from prior work
- [ ] Show how this task builds on prior tasks

## Phase 10: Specify Related Files

- [ ] List files that will be created (new code)
- [ ] List files that will be modified (existing code)
- [ ] For each file: describe scope of changes
- [ ] Identify similar files in codebase to reference
- [ ] Document code patterns to follow

## Phase 11: Add Risk Pre-identification

- [ ] Identify technical risks (API rate limits, schema issues, etc.)
- [ ] Identify dependency risks (external services unavailable)
- [ ] For each risk: estimate likelihood (Low/Med/High)
- [ ] For each risk: estimate impact (Low/Med/High)
- [ ] Document mitigation strategy
- [ ] List potential blockers that would halt progress

## Phase 12: Quality Checklist Verification

- [ ] Task definition complete (metadata, objective, files)
- [ ] INVEST criteria all met
- [ ] SMART criteria all met
- [ ] Acceptance criteria in Given-When-Then format
- [ ] Context and traceability included
- [ ] Dependency tree documented
- [ ] Token estimate <100k
- [ ] Risks and mitigations identified
- [ ] Task file follows template structure
- [ ] Ready for agent execution