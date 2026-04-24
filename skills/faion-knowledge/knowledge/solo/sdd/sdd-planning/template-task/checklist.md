# Template Task Checklist

## Phase 1: Create Task File Structure

- [ ] Create file at `.aidocs/features/{status}/{feature}/todo/TASK_{NNN}_{slug}.md`
- [ ] Add task identifier: TASK_{NNN}
- [ ] Set status: todo (when created)
- [ ] Add feature name and created date
- [ ] Link to feature folder

## Phase 2: Add SDD References

- [ ] Create reference table with Document, Path links
- [ ] Link to spec.md at feature level
- [ ] Link to design.md at feature level
- [ ] Link to implementation-plan.md at feature level
- [ ] These enable agent to understand context without re-reading

## Phase 3: Document Task Dependency Tree

- [ ] Create table showing dependencies (other TASK files)
- [ ] For each dependency: Task ID, Status, Key Output
- [ ] List what each dependency provided
- [ ] If complex: show dependency relationships
- [ ] Help agent understand task order

## Phase 4: Define Requirements Coverage

- [ ] For each FR from spec: state "FR-X: {Full requirement text}"
- [ ] Write which part(s) this task covers
- [ ] For each NFR from spec: include if applicable
- [ ] Show traceability back to spec
- [ ] Verify this task implements specific FR(s)

## Phase 5: Write Clear Objective

- [ ] Single, measurable goal
- [ ] Specific and actionable
- [ ] Understandable by AI agent
- [ ] NOT a vague or open-ended statement
- [ ] Example: "Create User model with email validation and bcrypt hashing"

## Phase 6: List Dependencies

- [ ] State which tasks must complete first
- [ ] Format: "TASK_{XXX} must complete first (provides {what})"
- [ ] Finish-to-Start (FS) dependency type
- [ ] No circular dependencies
- [ ] Mark blocking relationships

## Phase 7: Write Acceptance Criteria

- [ ] Create AC-{NNN}.1, AC-{NNN}.2, etc.
- [ ] Use Given-When-Then format or specific criteria
- [ ] Cover happy path scenarios
- [ ] Cover error scenarios
- [ ] Each criterion is testable (pass/fail)
- [ ] Use specific values

## Phase 8: Define Technical Approach

- [ ] Step-by-step numbered approach
- [ ] Research phase (read existing code)
- [ ] Implementation phase (write code)
- [ ] Testing phase (write tests)
- [ ] Verification phase (ensure AC met)

## Phase 9: List Files to Change

- [ ] Create table: File, Action (CREATE/MODIFY), Scope
- [ ] For CREATE: what to create and purpose
- [ ] For MODIFY: what changes and extent
- [ ] Organize by layer: models, services, views, tests
- [ ] Show approximate LOC for each

## Phase 10: Estimate Token Budget

- [ ] State approximate token count (~30k, ~50k, etc.)
- [ ] Ensure <100k total including research and tests
- [ ] Budget breakdown: research, implementation, testing
- [ ] Include buffer for unexpected complexity

## Phase 11: Create Implementation Section

- [ ] Section for Changes Made (fill during execution)
- [ ] List files created/modified with change descriptions
- [ ] Section for Tests Added (fill during execution)
- [ ] List test files and test descriptions

## Phase 12: Create Summary Section

- [ ] Section for Completed items (fill after completion)
- [ ] Checklist of what was accomplished
- [ ] Section for Issues Encountered (if any)
- [ ] Issue description and resolution
- [ ] Section for Lessons Learned
- [ ] Document patterns discovered
- [ ] Document mistakes and fixes
- [ ] Help future tasks and team learning

## Phase 13: Quality Gate Before Assignment

- [ ] Objective is single, clear, achievable
- [ ] Acceptance criteria cover happy path and errors
- [ ] Dependencies documented
- [ ] Files list is complete
- [ ] Token estimate <100k
- [ ] Task is atomic (not multiple concerns)
- [ ] Task status is "todo"
- [ ] Ready for agent execution

## Phase 14: State Transitions

- [ ] Created: status = todo
- [ ] Execution starts: status = in-progress
- [ ] Completion: status = done
- [ ] Block by another task: document blocker
- [ ] Move between subfolders: todo/ → in-progress/ → done/