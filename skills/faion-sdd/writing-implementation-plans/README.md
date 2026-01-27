# Writing Implementation Plans

## Metadata

| Field | Value |
|-------|-------|
| **ID** | writing-implementation-plans |
| **Version** | 3.0.0 |
| **Category** | SDD Foundation |
| **Difficulty** | Intermediate |
| **Tags** | #methodology, #sdd, #implementation, #planning, #llm-agents |
| **Domain Skill** | faion-sdd |
| **Agents** | faion-impl-plan-reviewer-agent |

---

## What is an Implementation Plan?

An implementation plan bridges the gap between design documents and executable tasks. It transforms architectural decisions (AD-X) into ordered, actionable work units optimized for LLM agent execution.

**Document Hierarchy:**

```
SPEC (what) → DESIGN (how) → IMPL PLAN (order) → TASKS (execution)
  FR-X         AD-X          TASK-XXX outline    TASK_XXX.md files
                                   |
                              Wave 1: TASK-001, TASK-002 (parallel)
                              Wave 2: TASK-003, TASK-004 (depends on W1)
                              Wave 3: TASK-005 (depends on W2)
```

**Key Components:**

| Component | Purpose |
|-----------|---------|
| Dependency Graph | DAG of task relationships |
| Wave Analysis | Parallel execution opportunities |
| Token Estimates | Context budget per task |
| Critical Path | Longest dependency chain |
| Risk Assessment | Potential blockers and mitigations |

---

## The 100k Token Rule

**Why 100k?** LLM agents perform optimally within a focused context window. Research shows that model performance degrades as input length increases, often in surprising and non-uniform ways. Most models become unreliable around 65-80% of their advertised context limit.

### Token Budget Guidelines

| Complexity | Token Budget | Characteristics |
|------------|--------------|-----------------|
| **Simple** | < 30k | Single file, clear pattern, minimal context |
| **Normal** | 30-60k | Multiple files, some research, moderate deps |
| **Complex** | 60-100k | Many files, deep research, complex deps |
| **Split Required** | > 100k | Must decompose into smaller tasks |

### Token Estimation Formula

```
Task Tokens = Context + Files + Research + Output

Where:
- Context: ~5-10k (task definition, AC, deps)
- Files: ~2-5k per file (read/write operations)
- Research: ~10-30k (codebase exploration, patterns)
- Output: ~5-20k (generated code, tests)
```

### Practical Token Estimates

| Task Type | Typical Range | Notes |
|-----------|---------------|-------|
| Create single file | 15-25k | Schema, utils, simple components |
| Modify existing file | 20-35k | Requires reading + understanding |
| Create API endpoint | 30-50k | Route + handler + validation + tests |
| Feature slice | 50-80k | Multiple files, integration |
| Complex refactor | 60-100k | Cross-file dependencies |

---

## Dependency Analysis for Parallelization

### Dependency Types

| Type | Meaning | Symbol | Example |
|------|---------|--------|---------|
| **FS** | Finish-to-Start | `→` | TASK-002 starts when TASK-001 finishes |
| **SS** | Start-to-Start | `⇉` | TASK-002 can start when TASK-001 starts |
| **FF** | Finish-to-Finish | `⇶` | TASK-002 finishes when TASK-001 finishes |
| **SF** | Start-to-Finish | `⇷` | Rare: TASK-002 finishes when TASK-001 starts |

### Building a Dependency Graph (DAG)

**Step 1: Identify all tasks from design document**

Extract from design.md:
- All AD-X architectural decisions
- All file changes (CREATE/MODIFY)
- All integration points

**Step 2: Map dependencies**

For each task, ask:
1. What files does this task need to exist?
2. What data/types does this task consume?
3. What must be configured/deployed first?

**Step 3: Visualize as DAG**

```
TASK-001 (DB Schema)
    |
    +--[FS]--→ TASK-003 (API Handler)
    |              |
    |              +--[FS]--→ TASK-005 (API Tests)
    |
    +--[FS]--→ TASK-004 (Service Layer)
                   |
                   +--[FS]--→ TASK-006 (Service Tests)

TASK-002 (Utils) --[SS]--→ TASK-003 (API Handler)
                 --[SS]--→ TASK-004 (Service Layer)
```

### Wave Identification Algorithm

**Algorithm:**

```
1. Find all tasks with no dependencies → Wave 1
2. Remove Wave 1 tasks from graph
3. Find all tasks whose dependencies are satisfied → Wave 2
4. Repeat until all tasks assigned to waves
```

**Example Wave Analysis:**

| Wave | Tasks | Parallel? | Dependencies | Token Load |
|------|-------|-----------|--------------|------------|
| Wave 1 | TASK-001, TASK-002 | Yes | None | 25k + 20k |
| Wave 2 | TASK-003, TASK-004 | Yes | Wave 1 | 45k + 35k |
| Wave 3 | TASK-005, TASK-006 | Yes | Wave 2 | 30k + 30k |
| Wave 4 | TASK-007 | No | Wave 3 | 50k |

**Parallelization Benefits:**

| Waves | Sequential | Parallel | Speedup |
|-------|-----------|----------|---------|
| 3 | 6 tasks | 3 batches | 2x |
| 4 | 8 tasks | 4 batches | 2x |
| 5 | 12 tasks | 5 batches | 2.4x |

---

## Complexity Estimation

### Complexity Factors

| Factor | Weight | Low | Medium | High |
|--------|--------|-----|--------|------|
| **Files Changed** | 25% | 1-2 | 3-5 | 6+ |
| **Dependencies** | 25% | 0-1 | 2-3 | 4+ |
| **Research Required** | 20% | Pattern exists | Some exploration | Novel solution |
| **Testing Scope** | 15% | Unit only | Unit + Integration | E2E required |
| **Risk Level** | 15% | Low | Medium | High |

### Complexity Matrix

```
Complexity = (Files * 0.25) + (Deps * 0.25) + (Research * 0.20) +
             (Testing * 0.15) + (Risk * 0.15)

Score 1.0-2.0 = Simple  (~25k tokens)
Score 2.1-3.5 = Normal  (~50k tokens)
Score 3.6-5.0 = Complex (~80k tokens)
```

### Task Size Indicators

**Task is TOO LARGE if:**
- Touches more than 5 files
- Has more than 3 direct dependencies
- Requires E2E testing
- Estimated tokens > 100k
- Cannot be completed in single context

**Task is TOO SMALL if:**
- Only changes one line
- Takes more overhead to describe than execute
- Should be combined with related changes

---

## Writing Process

### Phase 1: Context Loading

```
Read and understand:
1. .aidocs/constitution.md - project standards
2. {FEATURE_DIR}/spec.md - requirements (FR-X)
3. {FEATURE_DIR}/design.md - architecture (AD-X)
4. .aidocs/done/ - completed plans for patterns
```

### Phase 2: Prerequisites Check

Document everything needed before starting:
- Infrastructure (DB, cache, queues)
- Environment (env vars, secrets)
- Code dependencies (base classes, types)
- Documentation (approved spec, design)

### Phase 3: Work Breakdown (WBS)

Apply WBS decomposition:
- **100% Rule:** All work accounted for
- **Mutually Exclusive:** No overlap
- **Completeness:** Clear done criteria
- **AI-Optimized:** Each task < 100k tokens

### Phase 4: Dependency Graph

Build DAG with:
- All task nodes
- All dependency edges (FS/SS/FF/SF)
- Clear visualization

### Phase 5: Wave Analysis

Group tasks by execution order:
- Identify parallel opportunities
- Calculate wave dependencies
- Optimize for maximum parallelism

### Phase 6: Task Definition

For each task:
- INVEST validation
- Token estimation
- Acceptance criteria
- File manifest
- Test requirements

### Phase 7: Critical Path

Identify longest dependency chain:
- Sum token estimates
- Identify bottlenecks
- Add contingency buffer

### Phase 8: Risk Assessment

Document risks and mitigations:
- Technical risks
- Dependency risks
- External risks

---

## INVEST Validation

Every task must pass INVEST criteria:

| Criterion | Question | Pass | Fail |
|-----------|----------|------|------|
| **Independent** | No code deps on pending tasks? | Can run after deps complete | Needs unfinished task |
| **Negotiable** | Implementation flexible? | "User can register" | "Use bcrypt 5.1.0" |
| **Valuable** | Clear business value? | Enables feature | Technical debt only |
| **Estimable** | Token estimate possible? | "~45k tokens" | "Unknown" |
| **Small** | Under 100k tokens? | 60k tokens | 150k tokens |
| **Testable** | AC verifiable? | "Returns 201 status" | "Works correctly" |

---

## Critical Path Analysis

The critical path is the longest chain of dependent tasks that determines minimum completion scope.

**Example:**

```
Path A: TASK-001 → TASK-003 → TASK-005 → TASK-007
        25k         45k        30k        50k    = 150k tokens

Path B: TASK-002 → TASK-004 → TASK-006
        20k        35k         30k        = 85k tokens

Critical Path = Path A (150k tokens)
```

**Implications:**
- Feature cannot complete faster than critical path
- Critical path tasks have zero slack
- Delays on critical path delay entire feature
- Optimize critical path tasks first

---

## Related Documents

- [checklist.md](checklist.md) - Implementation plan quality checklist
- [templates.md](templates.md) - Plan and task templates
- [examples.md](examples.md) - Real-world plan examples
- [llm-prompts.md](llm-prompts.md) - Prompts for plan creation

---

## Related Methodologies

| Methodology | Domain | Application |
|-------------|--------|-------------|
| wbs-decomposition | PM | Work breakdown structure |
| dependency-management | PM | Dependency types (FS/SS/FF/SF) |
| risk-assessment | PM | Risk identification |
| schedule-management | PM | Timeline analysis |
| requirements-traceability | BA | AD-X to TASK mapping |
| backlog-management | PdM | INVEST principle |
| testing-strategy | Dev | Test planning |
| task-creation-parallelization | SDD | Wave analysis |

---

## External Resources

- [Task Decomposition for Coding Agents](https://mgx.dev/insights/task-decomposition-for-coding-agents-architectures-advancements-and-future-directions/a95f933f2c6541fc9e1fb352b429da15) - Architectures and future directions
- [GAP: Graph-based Agent Planning](https://arxiv.org/abs/2510.25320) - Parallel tool use with dependency awareness
- [Context Rot: How Input Tokens Impact LLM Performance](https://research.trychroma.com/context-rot) - Why 100k limit matters
- [Tokenomics in Agentic Software Engineering](https://arxiv.org/html/2601.14470) - Token consumption patterns
- [LLM Agent Best Practices](https://rajatnigam89.medium.com/llm-agent-sos-best-practices-and-considerations-for-implementation-90bda9583cba) - Implementation considerations
- [Multi-Agent Parallel Workflows](https://jiahaoxiang2000.github.io/blog/tools/multi-agent-parallel) - 2026 workflow patterns

---

## Agent

**faion-impl-plan-reviewer-agent** reviews implementation plans. Invoke with:
- "Review this implementation plan"
- "Break down this design into tasks"
- "Analyze dependency graph for parallelization"
- "Calculate critical path"
- "Estimate tokens for task"

---

*Methodology | SDD Foundation | Version 3.0.0*
*Optimized for LLM Agent Execution*
