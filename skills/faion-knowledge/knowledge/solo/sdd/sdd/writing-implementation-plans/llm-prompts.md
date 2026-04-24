# LLM Prompts for Implementation Plans

Prompts for generating and validating implementation plans.

---

## Prompt 1: Generate Implementation Plan from Design

```markdown
You are an implementation plan writer. Create an implementation plan from the provided design document.

**Input Documents:**
- Constitution: [paste relevant sections]
- Spec: [paste spec.md]
- Design: [paste design.md]

**Requirements:**
1. Break down all AD-X decisions into executable tasks
2. Each task must be < 100k tokens
3. Map dependencies as DAG with FS/SS/FF types
4. Group tasks into waves for parallel execution
5. Calculate critical path
6. Estimate tokens per task using:
   - Simple (15-30k): 1-2 files, clear pattern
   - Normal (30-60k): 3-5 files, some research
   - Complex (60-100k): 6+ files, deep research

**Output Format:**
Follow the implementation plan template with:
- Dependency graph (ASCII visualization)
- Wave analysis table
- Task definitions with INVEST validation
- Critical path calculation
- Risk assessment

**Constraints:**
- NO time estimates (use token estimates only)
- Every task traces to AD-X and FR-X
- Every task has testable acceptance criteria
- Maximum 100k tokens per task
```

---

## Prompt 2: Decompose Large Task

```markdown
You are a task decomposition specialist. Break down this large task into smaller tasks.

**Large Task:**
[paste task with > 100k token estimate]

**Current Token Estimate:** [X]k tokens

**Requirements:**
1. Split into tasks each < 100k tokens
2. Maintain clear dependencies between subtasks
3. Preserve traceability to original AD-X/FR-X
4. Each subtask must be independently completable
5. Consider natural boundaries:
   - File boundaries (one file per task when possible)
   - Layer boundaries (DB / service / API / test)
   - Feature boundaries (CRUD operations)

**Output:**
- List of subtasks with token estimates
- Dependency graph showing subtask relationships
- Updated wave assignment

**Example Split Pattern:**
Large API Feature (~150k) splits into:
- TASK-A: Database schema (~25k)
- TASK-B: Service layer (~35k)
- TASK-C: API endpoint (~40k)
- TASK-D: Validation (~25k)
- TASK-E: Tests (~25k)
```

---

## Prompt 3: Build Dependency Graph

```markdown
You are a dependency analyst. Create a dependency graph for these tasks.

**Tasks:**
[paste list of tasks with descriptions]

**Analyze each task for:**
1. What files/data does it need that other tasks create?
2. What does it produce that other tasks need?
3. Can it start before its dependencies finish (SS)?
4. Must it finish when another finishes (FF)?

**Dependency Types:**
- FS (Finish-to-Start): B starts when A finishes
- SS (Start-to-Start): B can start when A starts
- FF (Finish-to-Finish): B finishes when A finishes
- SF (Start-to-Finish): B finishes when A starts (rare)

**Output Format:**
```
TASK-001 (Description)
    |
    +--[FS]---> TASK-003 (Description)
    |               |
    |               +--[FS]---> TASK-005
    |
    +--[SS]---> TASK-004

TASK-002 --[SS]---> TASK-003
         --[SS]---> TASK-004
```

**Also provide:**
- Dependency table with all relationships
- Identification of any circular dependencies (invalid)
- Suggested wave assignments
```

---

## Prompt 4: Calculate Critical Path

```markdown
You are a critical path analyst. Calculate the critical path for this implementation plan.

**Dependency Graph:**
[paste dependency graph]

**Token Estimates:**
| Task | Tokens |
|------|--------|
[paste estimates]

**Calculate:**
1. All possible paths from start to end
2. Token sum for each path
3. Identify longest path (critical path)
4. Identify tasks with zero slack (on critical path)
5. Identify bottleneck task (largest on critical path)

**Output:**
```
Critical Path: TASK-001 --> TASK-003 --> TASK-005 --> TASK-007
Token Sum: [X]k

Path Analysis:
| Path | Tasks | Tokens | Slack |
|------|-------|--------|-------|
| A (Critical) | 001→003→005→007 | 150k | 0 |
| B | 002→004→006 | 85k | 65k |
| C | 001→004→006 | 75k | 75k |

Bottleneck: TASK-003 (45k tokens, largest on critical path)

Optimization Suggestions:
- [Any ways to reduce critical path]
```
```

---

## Prompt 5: Wave Analysis

```markdown
You are a parallelization specialist. Create a wave analysis for these tasks.

**Tasks with Dependencies:**
[paste tasks and their dependencies]

**Algorithm:**
1. Wave 1: All tasks with no dependencies
2. Wave 2: All tasks whose dependencies are in Wave 1
3. Wave 3: All tasks whose dependencies are in Wave 1 or 2
4. Continue until all tasks assigned

**Output Format:**
| Wave | Tasks | Parallel? | Dependencies | Total Tokens |
|------|-------|-----------|--------------|--------------|
| 1 | TASK-001, TASK-002 | Yes | None | 45k |
| 2 | TASK-003, TASK-004 | Yes | Wave 1 | 80k |
| 3 | TASK-005 | No | Wave 2 | 50k |

**Wave Visualization:**
```
Wave 1          Wave 2          Wave 3
+---------+     +---------+     +---------+
| TASK-01 |---->| TASK-03 |---->| TASK-05 |
+---------+  |  +---------+     +---------+
             |
+---------+  |  +---------+
| TASK-02 |--+->| TASK-04 |
+---------+     +---------+
```

**Parallelization Metrics:**
- Total tasks: [N]
- Total waves: [M]
- Maximum parallel tasks: [K]
- Speedup potential: [N/M]x
```

---

## Prompt 6: Token Estimation

```markdown
You are a token estimation specialist. Estimate tokens for this task.

**Task Description:**
[paste task description]

**Files to Change:**
[paste file list with actions]

**Estimation Components:**

| Component | Tokens | Reasoning |
|-----------|--------|-----------|
| Task context loading | ~[X]k | [task file, deps, AC] |
| Design doc reading | ~[X]k | [relevant AD-X sections] |
| Existing code reading | ~[X]k | [files to understand] |
| Pattern research | ~[X]k | [similar implementations] |
| Code generation | ~[X]k | [new files/modifications] |
| Test generation | ~[X]k | [test files] |
| Verification | ~[X]k | [running tests, checking AC] |
| **TOTAL** | **~[X]k** | |

**Complexity Assessment:**
- Files changed: [N] (weight: 25%)
- Dependencies: [N] (weight: 25%)
- Research level: Low/Med/High (weight: 20%)
- Testing scope: Unit/Integration/E2E (weight: 15%)
- Risk level: Low/Med/High (weight: 15%)

**Final Estimate:**
- Complexity: simple / normal / complex
- Token estimate: ~[X]k
- Confidence: Low / Medium / High

**If > 100k:** Suggest split into [N] subtasks
```

---

## Prompt 7: INVEST Validation

```markdown
You are a task quality validator. Validate this task against INVEST criteria.

**Task:**
[paste full task definition]

**INVEST Validation:**

| Criterion | Status | Analysis |
|-----------|--------|----------|
| **Independent** | PASS/FAIL | [Can execute after deps without pending work?] |
| **Negotiable** | PASS/FAIL | [Implementation flexible or over-specified?] |
| **Valuable** | PASS/FAIL | [Clear business value or pure technical?] |
| **Estimable** | PASS/FAIL | [Token estimate provided and reasonable?] |
| **Small** | PASS/FAIL | [Under 100k tokens?] |
| **Testable** | PASS/FAIL | [AC specific and verifiable?] |

**Issues Found:**
1. [Issue 1 with suggested fix]
2. [Issue 2 with suggested fix]

**Recommended Changes:**
[Specific changes to make task INVEST-compliant]
```

---

## Prompt 8: Risk Assessment

```markdown
You are a risk analyst. Assess risks for this implementation plan.

**Implementation Plan Summary:**
- Feature: [name]
- Tasks: [count]
- Critical path: [tokens]
- Technologies: [list]

**Risk Categories to Analyze:**

1. **Technical Risks:**
   - New technology/unfamiliar patterns
   - Complex integrations
   - Performance concerns
   - Security considerations

2. **Dependency Risks:**
   - External services/APIs
   - Third-party libraries
   - Team dependencies
   - Environment dependencies

3. **Scope Risks:**
   - Requirement ambiguity
   - Hidden complexity
   - Scope creep potential

**Output Format:**
| Risk | Category | Likelihood | Impact | Mitigation |
|------|----------|------------|--------|------------|
| [Risk 1] | Technical | Low/Med/High | Low/Med/High | [Strategy] |

**Contingency Buffer Recommendation:**
- Base buffer: 15%
- Technical risk adjustment: +[X]%
- Dependency risk adjustment: +[X]%
- **Total buffer: [X]%**
```

---

## Prompt 9: Review Implementation Plan

```markdown
You are an implementation plan reviewer. Review this plan for quality.

**Implementation Plan:**
[paste full implementation plan]

**Review Checklist:**

### Completeness
- [ ] All AD-X from design have tasks
- [ ] All FR-X from spec have coverage
- [ ] Prerequisites documented
- [ ] Testing plan included

### Structure
- [ ] Tasks follow INVEST criteria
- [ ] Dependencies explicitly documented
- [ ] Token estimates provided
- [ ] No task exceeds 100k tokens

### Parallelization
- [ ] Dependency graph correct (no cycles)
- [ ] Waves identified
- [ ] Critical path calculated
- [ ] Parallel opportunities maximized

### Risk
- [ ] Risks identified
- [ ] Mitigations documented
- [ ] Rollback plan exists

**Issues Found:**
| Severity | Issue | Location | Recommendation |
|----------|-------|----------|----------------|
| High | [issue] | [section] | [fix] |
| Medium | [issue] | [section] | [fix] |

**Overall Assessment:**
- Quality Score: [1-10]
- Ready for Execution: Yes / No
- Required Changes: [list]
```

---

## Prompt 10: Create Task Files from Plan

```markdown
You are a task file generator. Create TASK_XXX.md files from this implementation plan.

**Implementation Plan:**
[paste relevant section]

**For each task, generate:**
1. Full task file following template
2. All sections populated from plan
3. Subtasks broken down (3-5 steps)
4. Technical notes with patterns to follow

**Template:**
```markdown
# TASK_XXX: [Title]

## SDD References
| Document | Path |
|----------|------|
| Spec | [path] |
| Design | [path] |
| Implementation Plan | [path] |

## Task Metadata
| Field | Value |
|-------|-------|
| Phase | [N] |
| Wave | [N] |
| Complexity | [level] |
| Tokens | ~[X]k |
| Status | todo |

## Task Dependency Tree
### Dependencies
| Task | Status | Description |
|------|--------|-------------|

### Blocks
| Task | Description |
|------|-------------|

## Requirements Coverage
### AD-XXX: [Title]
[Full text]

### FR-XXX: [Title]
[Full text]

## Description
[From plan]

## Acceptance Criteria
[From plan, in Given-When-Then or declarative format]

## Files to Change
[From plan]

## Subtasks
- [ ] 01. [First step]
- [ ] 02. [Second step]
- [ ] 03. [Third step]
- [ ] 04. Write tests
- [ ] 05. Verify AC

## Technical Notes
[Patterns, gotchas, config]

## Tests
[Required tests]
```

**Output:** One complete TASK_XXX.md file per task in the plan.
```

---

## Usage Notes

### Prompt Chaining

For complete implementation plan creation:

```
1. Generate Plan (Prompt 1)
   |
2. Build Dependency Graph (Prompt 3)
   |
3. Calculate Critical Path (Prompt 4)
   |
4. Wave Analysis (Prompt 5)
   |
5. Token Estimation per task (Prompt 6)
   |
6. INVEST Validation per task (Prompt 7)
   |
7. Risk Assessment (Prompt 8)
   |
8. Review Plan (Prompt 9)
   |
9. Generate Task Files (Prompt 10)
```

### Prompt Customization

Replace bracketed placeholders with:
- `[paste ...]` - Actual content from documents
- `[X]` - Specific numbers
- `[name]` - Actual names

### Token Efficiency

These prompts are designed for efficiency:
- Clear structure reduces back-and-forth
- Tables format output consistently
- Examples guide correct output format
- Constraints prevent common errors

---

*Prompts | SDD Foundation | Version 3.0.0*
