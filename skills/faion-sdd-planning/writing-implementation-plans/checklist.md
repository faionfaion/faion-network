# Writing Implementation Plans Checklist

## Phase 1: Load SDD Context

- [ ] Read `.aidocs/constitution.md` for project principles and standards
- [ ] Read `{FEATURE}/spec.md` and extract all FR-X requirements
- [ ] Read `{FEATURE}/design.md` and extract all AD-X architecture decisions
- [ ] Review `features/done/` for completed implementation plan patterns
- [ ] Extract file changes list (CREATE/MODIFY/DELETE)

## Phase 2: Define Prerequisites

- [ ] List all dependencies that must be satisfied first
- [ ] Identify external services or libraries needed
- [ ] Check database schema prerequisites
- [ ] Verify all AD (architecture decisions) are documented
- [ ] Confirm no circular dependencies

## Phase 3: Create Work Breakdown Structure (WBS)

- [ ] List all files that need CREATE/MODIFY/DELETE actions
- [ ] Group related files into logical work units
- [ ] Estimate token complexity for each work unit
- [ ] Identify natural task boundaries (high cohesion, low coupling)
- [ ] Apply 8-80 rule: not too big, not too small

## Phase 4: Build Dependency Graph

- [ ] Create table mapping tasks to their dependencies
- [ ] Identify Finish-to-Start (FS) dependencies (most common)
- [ ] Document why each dependency exists
- [ ] Verify no circular dependencies
- [ ] Identify critical path (longest sequence)

## Phase 5: Perform Wave Analysis

- [ ] Group independent tasks that can run in parallel (Wave 1)
- [ ] Group tasks depending on Wave 1 (Wave 2)
- [ ] Continue until all tasks assigned to waves
- [ ] Define checkpoint criteria between waves
- [ ] Estimate speedup from parallelization

## Phase 6: Define Task-Level Details

- [ ] For each task: write clear, single-agent executable objective
- [ ] Map files to change (CREATE/MODIFY actions)
- [ ] Link to FR-X requirements being implemented
- [ ] Link to AD-X architecture decisions being applied
- [ ] Estimate token complexity (<100k for each task)

## Phase 7: Establish Critical Path

- [ ] Identify longest dependency chain through graph
- [ ] Mark critical tasks that cannot be delayed
- [ ] For non-critical tasks, identify slack time
- [ ] Establish baseline schedule based on critical path
- [ ] Plan checkpoints at critical decision points

## Phase 8: Assess Risks

- [ ] Identify technical risks (API integrations, performance, scaling)
- [ ] Identify dependency risks (external services, blockers)
- [ ] Identify complexity risks (unclear requirements, architecture)
- [ ] For each risk: document mitigation strategy
- [ ] Plan contingency if risk occurs

## Phase 9: Define Testing Strategy

- [ ] List unit tests needed (isolated component testing)
- [ ] List integration tests needed (flow verification)
- [ ] Define test data and fixtures required
- [ ] Plan quality gates per wave
- [ ] Define final acceptance criteria verification

## Phase 10: Plan Rollout Strategy

- [ ] Determine how to deploy changes (all at once vs phased)
- [ ] Identify dependencies on other features
- [ ] Plan any data migrations needed
- [ ] Define rollback strategy if issues found
- [ ] Plan communication/notification for stakeholders

## Phase 11: Quality Gate Verification

- [ ] All AD decisions mapped to tasks
- [ ] All FR requirements mapped to tasks
- [ ] All tasks fit <100k token budget
- [ ] All dependencies documented and acyclic
- [ ] All tasks have clear success criteria
- [ ] Testing strategy covers happy path and errors
- [ ] Risks identified and mitigated
- [ ] Critical path clearly marked

## Phase 12: Review & Approval

- [ ] Present implementation plan to stakeholders
- [ ] Verify 100k token rule compliance
- [ ] Confirm dependencies and wave execution plan
- [ ] Get approval before creating task files
- [ ] Update plan based on feedback