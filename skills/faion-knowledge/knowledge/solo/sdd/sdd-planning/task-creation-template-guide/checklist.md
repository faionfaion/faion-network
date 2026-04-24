# Task Creation Template Guide Checklist

## Phase 1: Manage Context Budget (100k Rule)

- [ ] Allocate 15% to SDD documents (constitution, spec, design)
- [ ] Allocate 10% to task dependency tree (completed task summaries)
- [ ] Allocate 25% to research (reading existing code patterns)
- [ ] Allocate 40% to implementation (actual coding)
- [ ] Allocate 10% to testing (verification and tests)
- [ ] Total budget must be <100k tokens

## Phase 2: Include SDD References

- [ ] Create reference table: Document, Path, Sections
- [ ] Include `.aidocs/constitution.md` link and relevant sections
- [ ] Include feature spec.md link and FR-X references
- [ ] Include feature design.md link and AD-X references
- [ ] Include contracts.md if API feature
- [ ] These links save agent ~15% of token budget

## Phase 3: Document Task Dependency Tree

- [ ] Create dependency tree showing all dependency tasks
- [ ] For each dependency: name, status (DONE), summary of work
- [ ] List files created/modified in each dependency
- [ ] Document patterns to follow from prior work
- [ ] Show key code snippets from completed dependencies
- [ ] Add implementation decisions made
- [ ] Link to actual completed TASK files to read
- [ ] This tree is CRITICAL for consistency

## Phase 4: Write Requirements Coverage

- [ ] Create FR-X section with full requirement text from spec
- [ ] For each FR: explain how this task implements it
- [ ] Create AD-X section with full decision text from design
- [ ] For each AD: explain how this task applies it
- [ ] Include NFR-X if non-functional requirements apply
- [ ] Ensure full FR/AD traceability

## Phase 5: Include Recommended Skills & Methodologies

- [ ] List skills with purpose (when to use)
- [ ] List methodologies with purpose (how it helps)
- [ ] Examples: faion-software-developer, code-review, shadcn-ui-components
- [ ] Help agent select right patterns and approaches

## Phase 6: Add Risk & Blocker Pre-identification

- [ ] Create Risks & Mitigations table: Risk, Likelihood, Impact, Mitigation
- [ ] Identify technical risks (API limits, schema issues)
- [ ] Identify dependency risks (external services)
- [ ] Identify complexity risks (unclear requirements)
- [ ] For each risk: mitigation strategy
- [ ] Create Potential Blockers checklist
- [ ] Document blockers that would halt progress

## Phase 7: Structure Enhanced Template

- [ ] Metadata: Complexity, Effort, Priority, Created, Project, Feature
- [ ] SDD References: Constitution, Spec, Design, Contracts
- [ ] Task Dependency Tree: all completed dependencies with summaries
- [ ] Recommended Skills & Methodologies
- [ ] Requirements Coverage: FR-X and AD-X text
- [ ] Description: 2-4 sentences of what to do
- [ ] Context: related files and code dependencies
- [ ] Goals: 3 specific, measurable goals
- [ ] Acceptance Criteria: AC-1, AC-2 in Given-When-Then
- [ ] Dependencies: task dependencies (FS format)
- [ ] Files to Change: CREATE/MODIFY table
- [ ] Risks & Mitigations
- [ ] Out of Scope: explicit exclusions
- [ ] Testing: unit and integration test specs
- [ ] Estimated Context: token budget breakdown
- [ ] Subtasks: research, implement, test, verify
- [ ] Implementation: (filled by executor)
- [ ] Summary: (filled after completion)
- [ ] Lessons Learned: (optional, patterns/mistakes)

## Phase 8: Apply Context Optimization

- [ ] SDD References reduce context needed (reuse docs)
- [ ] Task Dependency Tree reuses patterns from prior work
- [ ] Recommended Skills guide agent to right methodologies
- [ ] Risk pre-identification saves debugging time
- [ ] All this saves 30-40% of context budget

## Phase 9: Define Clear Task Scope

- [ ] Input: what must exist before task starts
- [ ] Output: what will exist after task completes
- [ ] Success Criteria: how to verify completion
- [ ] Document what is and is NOT in scope

## Phase 10: Verify Token Estimate

- [ ] SDD Docs: ~15k tokens
- [ ] Research: ~20-25k tokens
- [ ] Implementation: ~40-50k tokens
- [ ] Testing: ~10-15k tokens
- [ ] Buffer: ~10k tokens
- [ ] Total estimate <100k
- [ ] If estimate >100k: split into smaller tasks

## Phase 11: Quality Checklist

- [ ] SDD references complete and linked
- [ ] Dependency tree documents prior work
- [ ] Requirements coverage shows FR/AD traceability
- [ ] Acceptance criteria in Given-When-Then format
- [ ] Token estimate <100k
- [ ] Risks and blockers identified
- [ ] Task is single, focused objective
- [ ] All sections follow template
- [ ] Ready for agent execution

## Phase 12: Review & Approval

- [ ] Verify context budget breakdown
- [ ] Confirm dependency tree completeness
- [ ] Check requirement traceability
- [ ] Validate token estimate
- [ ] Get approval before assignment