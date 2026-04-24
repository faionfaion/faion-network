# Workflow Design Phase Checklist

## Phase 1: Writing Design Documents

### Phase 1.1: Verify Prerequisites

- [ ] Confirm spec.md exists and is approved
- [ ] Confirm constitution.md exists at `.aidocs/`
- [ ] Confirm contracts.md exists (for API features)
- [ ] No missing dependencies

### Phase 1.2: Extract from Specification

- [ ] Read spec.md Problem Statement section
- [ ] Extract all FR-X functional requirements
- [ ] Extract all NFR-X non-functional requirements
- [ ] Note User Stories and personas
- [ ] Check Out of Scope section for boundaries
- [ ] Note any API contracts referenced

### Phase 1.3: Extract from Constitution

- [ ] Read Architecture Patterns section
- [ ] Read Code Standards section
- [ ] Understand Testing requirements
- [ ] Note any constraints or standards
- [ ] Identify similar patterns used before

### Phase 1.4: Research Codebase

- [ ] Use Grep/Glob to find similar models
- [ ] Identify similar service implementations
- [ ] Find similar view/controller patterns
- [ ] Document existing patterns and conventions
- [ ] Determine code organization and placement

### Phase 1.5: Make Architecture Decisions (AD-X)

- [ ] For each key decision: AD-001, AD-002, etc.
- [ ] Context: problem being solved
- [ ] Options: minimum 2 alternatives with pros/cons
- [ ] Decision: chosen solution
- [ ] Rationale: why chosen, influencing factors

### Phase 1.6: Define Technical Approach

- [ ] Identify Components: new and modified
- [ ] Document purpose, location, dependencies
- [ ] Create Component Diagram if complex
- [ ] Define Data Flow: inputs, transformations, outputs
- [ ] Define Data Models with types and constraints
- [ ] Reference API endpoints from contracts.md

### Phase 1.7: Plan File Changes

- [ ] List all files: CREATE, MODIFY, DELETE
- [ ] For each file: describe scope (what changes)
- [ ] Organize by layer: models, services, views, tests
- [ ] Show file structure for new packages

### Phase 1.8: Define Testing Strategy

- [ ] Unit Tests: isolated component testing
- [ ] Integration Tests: flow verification
- [ ] Test Data: fixtures and sample data
- [ ] Quality Gates: verification points
- [ ] Coverage targets

### Phase 1.9: Identify Risks

- [ ] Technical risks (API integrations, performance)
- [ ] Dependency risks (external services)
- [ ] Complexity risks (unclear requirements)
- [ ] For each: impact, likelihood, mitigation

### Phase 1.10: Review Architecture

- [ ] Present decisions to stakeholders
- [ ] Verify all FR requirements addressed
- [ ] Confirm design aligns with constitution
- [ ] Get approval from architect/tech lead

### Phase 1.11: Save Design Document

- [ ] Create `.aidocs/features/{status}/{feature}/design.md`
- [ ] Follow template structure
- [ ] Ensure all sections complete
- [ ] Set status to "Draft" or "Approved"

## Phase 2: Writing Implementation Plans

### Phase 2.1: Load Full Context

- [ ] Read `.aidocs/constitution.md` - principles and standards
- [ ] Read `{FEATURE}/spec.md` - extract all FR-X
- [ ] Read `{FEATURE}/design.md` - extract all AD-X
- [ ] Review `features/done/` for pattern examples
- [ ] Extract tech stack and constraints

### Phase 2.2: Analyze File Complexity

- [ ] List every file from design.md (CREATE/MODIFY)
- [ ] Estimate tokens for each file
- [ ] Consider dependencies, business logic, tests
- [ ] Apply WBS principle: break large items

### Phase 2.3: Define Work Units (WBS)

- [ ] Group related files into logical work units
- [ ] Each work unit has high cohesion
- [ ] Work units have low coupling
- [ ] Apply 8-80 rule: not too big, not too small

### Phase 2.4: Build Dependency Graph

- [ ] Map tasks to their Finish-to-Start dependencies
- [ ] Document why each dependency exists
- [ ] Verify no circular dependencies
- [ ] Identify critical path (longest sequence)

### Phase 2.5: Wave Analysis

- [ ] Group independent tasks (Wave 1)
- [ ] Group tasks depending on Wave 1 (Wave 2)
- [ ] Continue until all tasks assigned
- [ ] Define checkpoints between waves
- [ ] Estimate parallelization speedup

### Phase 2.6: Define Task-Level Details

- [ ] For each task: clear, single objective
- [ ] Map files to CREATE/MODIFY
- [ ] Link to FR-X requirements
- [ ] Link to AD-X decisions
- [ ] Estimate tokens (<100k each)

### Phase 2.7: Establish Critical Path

- [ ] Identify longest dependency chain
- [ ] Mark tasks that cannot be delayed
- [ ] Identify slack time for non-critical
- [ ] Plan checkpoints at critical points

### Phase 2.8: Assess Risks

- [ ] Technical risks and mitigations
- [ ] Dependency risks and contingencies
- [ ] Complexity risks and fallbacks
- [ ] Document prevention strategies

### Phase 2.9: Plan Rollout Strategy

- [ ] Deployment approach (all at once vs phased)
- [ ] Data migrations needed
- [ ] Rollback strategy
- [ ] Communication plan

### Phase 2.10: Quality Gate Verification

- [ ] All AD mapped to tasks
- [ ] All FR mapped to tasks
- [ ] All tasks <100k tokens
- [ ] Dependencies acyclic
- [ ] All tasks have success criteria
- [ ] Testing strategy covers scenarios
- [ ] Risks identified and mitigated

### Phase 2.11: Review Plan

- [ ] Present to stakeholders
- [ ] Verify 100k token rule
- [ ] Confirm dependencies and waves
- [ ] Get approval

### Phase 2.12: Save Implementation Plan

- [ ] Create `.aidocs/features/{feature}/implementation-plan.md`
- [ ] Status: Draft or Approved

## Phase 3: Task Creation

- [ ] Load all TASK information from implementation plan
- [ ] For each task: call task creator agent
- [ ] Generate comprehensive TASK_*.md file
- [ ] Include all context, dependencies, AC

## Phase 4: Parallelization Analysis

- [ ] Read all TASK_*.md files
- [ ] Extract dependencies from each
- [ ] Build full dependency graph
- [ ] Group tasks into waves
- [ ] Add checkpoints between waves
- [ ] Calculate parallelization speedup
- [ ] Generate execution plan with waves