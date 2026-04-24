# LLM Prompts for Task Decomposition

Effective prompts for using LLMs to assist with task decomposition and planning.

---

## Planning Prompts

### 1. Feature Analysis Prompt

Use before decomposition to understand scope.

```
I need to break down this feature into executable tasks.

**Feature:** {feature name}

**Context:**
- Spec: {paste relevant FR-X requirements}
- Design: {paste relevant AD-X decisions}
- Codebase: {describe existing patterns}

**Analysis needed:**
1. What are the main components/modules needed?
2. What are the dependencies between them?
3. What can be parallelized?
4. What needs research before implementation?

Think step by step. Don't write code yet - just analyze and create a decomposition plan.
```

### 2. Task Breakdown Prompt

Use to generate initial task list.

```
Break down this implementation plan into LLM-executable tasks.

**Constraints:**
- Each task must fit in ~100k tokens (single context window)
- Each task must be independently testable
- Each task must have clear input/output boundaries
- Tasks must follow INVEST criteria

**Implementation Plan:**
{paste implementation plan sections}

**Output format for each task:**
1. Task title (action verb + object)
2. Complexity: simple (<30k) / normal (30-60k) / complex (60-100k)
3. Dependencies: [list of task IDs]
4. Goals: 3-5 specific deliverables
5. Files to change: CREATE/MODIFY + path

Group tasks into parallel waves where dependencies allow.
```

### 3. Dependency Graph Prompt

Use to validate and visualize dependencies.

```
Given these tasks, create a dependency graph and identify parallel waves.

**Tasks:**
{list tasks with their dependencies}

**Output:**
1. ASCII dependency graph showing task relationships
2. Dependency type labels (FS/SS/FF)
3. Parallel waves (tasks that can run simultaneously)
4. Critical path (longest dependency chain)
5. Any circular dependencies or issues

Format the graph clearly using arrows (→) and vertical connectors (│).
```

### 4. Wave Planning Prompt

Use to optimize parallelization.

```
Optimize this task list for maximum parallelization.

**Current tasks:**
{list tasks with dependencies}

**Constraints:**
- Maintain correctness (dependencies must be respected)
- Minimize total execution time
- Balance wave sizes for parallel executors

**Output:**
1. Reorganized waves with parallel tasks
2. Critical path tokens
3. Estimated speedup vs sequential
4. Any tasks that could be split further
```

---

## Task Definition Prompts

### 5. Acceptance Criteria Generation

Use to generate Given-When-Then criteria.

```
Generate comprehensive acceptance criteria for this task.

**Task:** {task title}
**Description:** {task description}
**FR-X Coverage:** {requirement text}

**Generate ACs for:**
1. Happy path (successful execution)
2. Alternative paths (valid variations)
3. Error handling (invalid inputs, failures)
4. Boundary conditions (limits, edge cases)
5. Security considerations (if applicable)

**Format:**
AC-N: {Scenario name}
- Given: {precondition}
- When: {action}
- Then: {expected result, specific and testable}
```

### 6. Context Research Prompt

Use to identify patterns and related files.

```
I'm about to implement this task. Help me research the codebase.

**Task:** {task title}
**Goals:** {list goals}
**Files to create/modify:** {list files}

**Research questions:**
1. What similar implementations exist in the codebase?
2. What patterns should I follow?
3. What utilities/helpers already exist that I should reuse?
4. What tests exist that I should mirror?

Search for: {relevant keywords, function names, patterns}

**Output:**
- Related files with their purposes
- Patterns to follow (with code snippets)
- Code dependencies to import
- Anti-patterns to avoid
```

### 7. Task Dependency Tree Generation

Use when creating task with dependencies.

```
Generate a Task Dependency Tree section for this task.

**This task:** TASK-{XXX} - {title}
**Depends on:** {list dependency task IDs}

**For each dependency, extract:**
1. Status (should be DONE)
2. Summary (what was accomplished)
3. Files created/modified
4. Patterns established
5. Key code snippets (critical for understanding)
6. Decisions made

**Format as ASCII tree with arrows showing flow into current task.**
```

### 8. Risk Assessment Prompt

Use to identify potential blockers.

```
Analyze risks for this task.

**Task:** {task title}
**Technical approach:** {brief description}
**Dependencies:** {list}

**Assess:**
1. Technical risks (what could go wrong technically)
2. Integration risks (how might it conflict with other code)
3. External dependencies (APIs, libraries, services)
4. Knowledge gaps (unfamiliar areas)
5. Testing challenges (what's hard to verify)

**Output format:**
| Risk | Likelihood | Impact | Mitigation |
```

---

## Execution Prompts

### 9. Task Execution Kickoff

Use to start task execution with proper context.

```
Execute TASK-{XXX}: {title}

**Context loaded:**
- Constitution: {summarize relevant sections}
- Spec FR-X: {full text}
- Design AD-X: {full text}

**Dependency Tree:**
{paste dependency tree section}

**Acceptance Criteria:**
{paste all ACs}

**Files to Change:**
{paste files table}

**Instructions:**
1. First, read the dependency task summaries
2. Research existing patterns in the codebase
3. Implement following established patterns
4. Write tests for each AC
5. Run tests and verify all pass
6. Document implementation in Summary section

Think carefully before coding. Ask yourself: "What patterns should I follow?"
```

### 10. Task Verification Prompt

Use after implementation to verify completion.

```
Verify TASK-{XXX} completion against acceptance criteria.

**Acceptance Criteria:**
{paste all ACs}

**Implementation:**
{describe what was implemented}

**Files Changed:**
{list files with changes}

**Verification checklist:**
For each AC:
1. Is the scenario fully implemented?
2. Does the test cover this case?
3. What command verifies this works?

**Run these verification commands:**
{list test commands}

If any AC is not met, explain what's missing and how to fix.
```

### 11. Task Summary Generation

Use after completion to write summary.

```
Generate a Summary section for this completed task.

**Task:** TASK-{XXX} - {title}
**What was implemented:** {describe}
**Files changed:** {list}

**Generate summary with:**
1. Completion date
2. What was done (bullet points)
3. Key decisions made (with rationale)
4. Files changed (with CREATE/MODIFY and line counts)
5. Patterns established (for future tasks to follow)
6. Test results

This summary will be used by future tasks as context.
Keep it concise but include all critical patterns.
```

---

## Quality Prompts

### 12. Task Review Prompt

Use to review task definition quality.

```
Review this task definition for quality issues.

**Task file:**
{paste full task markdown}

**Check for:**
1. INVEST criteria compliance
2. Clear, measurable goals
3. Testable acceptance criteria (Given-When-Then)
4. Complete traceability (FR-X, AD-X links)
5. Realistic token budget
6. Complete dependency information
7. Sufficient context for standalone execution

**Rate each aspect 1-5 and provide specific improvements.**
```

### 13. Decomposition Review Prompt

Use to review entire decomposition.

```
Review this feature decomposition for completeness.

**Spec requirements:**
{list all FR-X}

**Tasks created:**
{list all tasks with their FR-X coverage}

**Check:**
1. All FR-X requirements are covered by tasks
2. No gaps between tasks (nothing falls through)
3. No overlapping scope (duplication)
4. Dependencies are logical and complete
5. Waves are balanced
6. Critical path is reasonable

**Identify issues and suggest fixes.**
```

### 14. Pattern Extraction Prompt

Use after completing multiple tasks to extract patterns.

```
Extract reusable patterns from these completed tasks.

**Completed tasks:**
{paste Summary sections from multiple tasks}

**Extract:**
1. Code patterns (naming, structure, organization)
2. Testing patterns (how to test similar features)
3. Error handling patterns
4. Common utilities created
5. Documentation patterns

**Output for memory file:**
Format as bullet points suitable for .aidocs/memory/patterns.md
```

---

## Specialized Prompts

### 15. API Task Decomposition

```
Break down this API feature into tasks.

**API Requirements:**
{paste API spec}

**Standard API task pattern:**
1. Database migration task
2. Model creation task
3. Endpoint implementation task (per endpoint)
4. Authentication/authorization task
5. Input validation task
6. Error handling task
7. API documentation task
8. Integration tests task

**Apply this pattern to the requirements.**
```

### 16. Frontend Task Decomposition

```
Break down this frontend feature into tasks.

**UI Requirements:**
{paste UI spec with mockups reference}

**Standard frontend task pattern:**
1. Component creation tasks (atomic → composed)
2. State management task
3. API integration task
4. Styling/theming task
5. Accessibility task
6. Responsive design task
7. Animation/transitions task
8. E2E tests task

**Apply this pattern considering component hierarchy.**
```

### 17. Refactoring Task Decomposition

```
Break down this refactoring into safe incremental tasks.

**Current state:** {describe}
**Target state:** {describe}
**Constraint:** Must not break existing functionality

**Strangler pattern approach:**
1. Add new implementation alongside old
2. Migrate consumers one by one
3. Add deprecation warnings
4. Remove old implementation

**Create tasks that each leave the system working.**
```

---

## Prompt Modifiers

Add these modifiers to any prompt for specific behaviors.

### Think Step by Step
```
Think step by step before answering. Show your reasoning.
```

### Extended Thinking
```
Think hard about this. Take extra time to consider edge cases.
```

### Ultrathink (Complex Problems)
```
Ultrathink this problem. This is complex and requires deep analysis.
Consider multiple approaches before choosing.
```

### No Code Yet
```
Do not write code. Only analyze and plan.
```

### Format as Markdown
```
Output as clean markdown with proper headings and tables.
```

### Be Specific
```
Be specific. Avoid vague language. Give concrete examples.
```

---

## Prompt Templates Quick Reference

| Situation | Prompt Number |
|-----------|---------------|
| Starting decomposition | #1, #2 |
| Validating dependencies | #3 |
| Optimizing parallelization | #4 |
| Writing acceptance criteria | #5 |
| Researching codebase | #6 |
| Creating task with deps | #7 |
| Assessing risks | #8 |
| Starting task execution | #9 |
| Verifying completion | #10 |
| Writing summary | #11 |
| Reviewing task quality | #12 |
| Reviewing decomposition | #13 |
| Extracting patterns | #14 |
| API features | #15 |
| Frontend features | #16 |
| Refactoring | #17 |

---

*Prompts v3.0.0 | Tested with Claude, GPT-4, Gemini*
