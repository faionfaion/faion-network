# Implementation Plan: 100k Token Rule

## Problem

AI agents fail with tasks > 100k tokens because:
- Context window limitations
- Poor focus on relevant details
- Increased hallucination risk
- Longer execution time
- Higher cost

**Solution:** Break tasks down to < 100k tokens context budget.

---

## Context Budget

### Token Consumption Breakdown

| Source | Typical Size | Notes |
|--------|-------------|-------|
| **Agent prompt** | 5-10k | Role, instructions, examples |
| **Project context** | 10-20k | Constitution, contracts, standards |
| **Task file** | 2-5k | Task description, acceptance criteria |
| **Design docs** | 5-15k | Relevant AD-X decisions |
| **Codebase reading** | 30-70k | Files to modify + dependencies |
| **Buffer** | 10-20k | Safety margin |

**Total:** 62-140k tokens

**Target:** Keep total < 100k tokens

---

## Task Complexity Levels

| Complexity | Effort | Context | Description |
|------------|--------|---------|-------------|
| **Simple** | 1-2h | < 30k tokens | Single file, clear pattern |
| **Normal** | 2-3h | 30-60k tokens | Multiple files, some research |
| **Complex** | 3-4h | 60-100k tokens | Many files, deep research |

**If > 100k tokens:** Split into multiple tasks.

---

## Context Estimation Guide

### Single File Changes

```markdown
**Context Estimate:** ~15k tokens

Breakdown:
- Agent prompt: 5k
- Project context: 8k
- Task file: 2k
- File to modify: 500 tokens
```

### Multi-File Changes (3-5 files)

```markdown
**Context Estimate:** ~45k tokens

Breakdown:
- Agent prompt: 5k
- Project context: 10k
- Task file: 3k
- Files to modify: 15k (5 files × 3k avg)
- Dependencies: 12k (4 files × 3k avg)
```

### Complex Refactoring (10+ files)

```markdown
**Context Estimate:** ~85k tokens

Breakdown:
- Agent prompt: 8k
- Project context: 15k
- Task file: 5k
- Files to modify: 35k (10 files × 3.5k avg)
- Dependencies: 20k (6 files × 3.3k avg)
- Buffer: 2k
```

---

## Splitting Large Tasks

### When to Split

Split if:
- Context estimate > 100k tokens
- Task touches > 10 files
- Task requires deep research across many modules
- Task has multiple independent sub-goals

### How to Split

#### Option 1: By Component

```markdown
Before:
TASK-001: Implement user authentication (150k tokens)

After:
TASK-001: Create user database schema (25k tokens)
TASK-002: Implement password hashing utilities (20k tokens)
TASK-003: Create registration handler (30k tokens)
TASK-004: Create login handler (35k tokens)
TASK-005: Add authentication middleware (25k tokens)
```

#### Option 2: By Layer

```markdown
Before:
TASK-001: Build payment system (180k tokens)

After:
TASK-001: Payment database models (30k tokens)
TASK-002: Payment service layer (40k tokens)
TASK-003: Payment API endpoints (35k tokens)
TASK-004: Payment UI components (35k tokens)
TASK-005: Payment integration tests (40k tokens)
```

#### Option 3: By Dependency Wave

```markdown
Before:
TASK-001: Implement notification system (140k tokens)

After:
Wave 1:
  TASK-001: Notification data models (25k tokens)
  TASK-002: Email sender utility (20k tokens)

Wave 2 (depends on Wave 1):
  TASK-003: Notification service (35k tokens)
  TASK-004: Notification templates (25k tokens)

Wave 3 (depends on Wave 2):
  TASK-005: Notification API (35k tokens)
```

---

## Work Breakdown Structure (WBS)

### WBS Principles

| Level | Description | Example |
|-------|-------------|---------|
| **Phase** | Logical grouping | "Phase 1: Infrastructure" |
| **Task** | Atomic work unit | "TASK-001: Create users table" |
| **Subtask** | Steps within task | "01. Create migration file" |

### Decomposition Rules

- **100% Rule:** All work is accounted for
- **Mutually Exclusive:** No overlap between tasks
- **Completeness:** Each task has clear done criteria
- **AI Context:** Each task < 100k tokens

### Example WBS

```
Feature: User Management System (350k tokens total)
│
├── Phase 1: Infrastructure (80k tokens)
│   ├── TASK-001: Database schema (30k)
│   │   └── Subtasks: migration file, indexes, constraints
│   └── TASK-002: Base models (50k)
│       └── Subtasks: User model, UserProfile model, tests
│
├── Phase 2: Core Logic (150k tokens)
│   ├── TASK-003: Registration service (45k)
│   ├── TASK-004: Login service (40k)
│   ├── TASK-005: Password reset (35k)
│   └── TASK-006: Profile management (30k)
│
└── Phase 3: Testing (120k tokens)
    ├── TASK-007: Unit tests (40k)
    ├── TASK-008: Integration tests (45k)
    └── TASK-009: E2E tests (35k)
```

---

## Wave-Based Task Creation

### Principle

Create detailed TASK files in waves, not all at once.

### Approach

```
Wave 1: Create TASK_001, TASK_002 files (outline only)
    ↓ execute
Wave 2: Create TASK_003, TASK_004 files (incorporate learnings)
    ↓ execute
Wave 3: Create TASK_005, TASK_006 files (incorporate patterns)
    ...
```

### Benefits

- Later tasks incorporate learnings from earlier waves
- Patterns discovered in Wave 1 are documented
- Better context from completed dependency tasks
- Reduced rework from early discoveries

### Implementation Plan Content

**In implementation-plan.md:**
- All tasks listed with brief description (2-3 sentences)
- Context estimates for each task
- Dependency graph
- Wave assignments

**In TASK_XXX.md files:**
- Full task details created wave-by-wave
- Incorporate patterns from previous waves
- Reference completed tasks for context

---

## Quality Checklist

### Context Budget Validation

**Per Task:**
- [ ] Context estimate provided
- [ ] Estimate < 100k tokens
- [ ] Breakdown shows calculation
- [ ] Files to read listed

**Per Implementation Plan:**
- [ ] All tasks estimated
- [ ] No task > 100k tokens
- [ ] Total effort calculated
- [ ] Critical path identified

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Tasks too large | Break down to < 4 hours, < 100k tokens |
| No context estimate | Always estimate token budget |
| Guessing context size | Calculate from file list + dependencies |
| Ignoring agent prompt overhead | Include 5-10k for agent context |
| No buffer | Add 10-20k safety margin |
| All tasks created at once | Create in waves, incorporate learnings |

---

## Sources

- [Anthropic Claude Context Windows](https://docs.anthropic.com/claude/docs/models-overview) - Token limits documentation
- [OpenAI Token Counting](https://platform.openai.com/tokenizer) - Token estimation tool
- [Work Breakdown Structure Guide](https://www.pmi.org/learning/library/applying-work-breakdown-structure-project-lifecycle-6979) - PMI WBS practices
- [Agile Task Decomposition](https://www.atlassian.com/agile/project-management/epics-stories-themes) - Story splitting patterns
- [Context Window Best Practices](https://simonwillison.net/2023/Oct/23/embeddings/) - LLM context management
