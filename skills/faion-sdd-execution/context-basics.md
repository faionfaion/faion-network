# AI Context-Aware Decomposition: Basics

Understanding context limits and token budgets for LLM-based development.

---

## The Context Problem

LLMs have limited context windows:
- GPT-4: 128K tokens (~300 pages)
- Claude: 200K tokens (~500 pages)
- **Effective context:** 20-50K tokens (quality degrades with length)

**Impact:** Large files and complex tasks lead to:
- Incomplete code generation
- Missed edge cases
- Hallucinated imports/methods
- Lost context mid-task

---

## Token Budget Framework

### Task-Level Budget (100K Rule)

```
Total Budget:     100K tokens
─────────────────────────────
Context Loading:   20K (spec, design, existing code)
Task Definition:    5K (task file, requirements)
Code Generation:   30K (new code to write)
Test Generation:   20K (tests for new code)
Iteration Buffer:  25K (fixes, refinements)
```

### File-Level Budget

| File Type | Target Tokens | Target Lines | Max Tokens |
|-----------|---------------|--------------|------------|
| Model/Entity | 1-3K | 50-100 | 5K |
| Service | 3-6K | 100-200 | 10K |
| View/Handler | 2-5K | 50-150 | 8K |
| Component | 2-5K | 50-150 | 8K |
| Test file | 5-10K | 150-300 | 15K |
| Config | 1-3K | 50-100 | 5K |

**Token estimation:** ~3 tokens per line of code (average)

---

## Task Sizing Guidelines

### Atomic Task Checklist

A task is properly sized when:

- [ ] **Single responsibility** - One clear outcome
- [ ] **Under 100K tokens** - Fits in context
- [ ] **Testable in isolation** - Has clear acceptance criteria
- [ ] **1-3 files modified** - Focused scope
- [ ] **Clear inputs/outputs** - Defined interfaces
- [ ] **No blocking dependencies** - Can start independently

### Splitting Large Tasks

```
BEFORE: "Implement user authentication"
  - Too vague, too large (~50K+ tokens needed)

AFTER: Split into atomic tasks
  1. Create User model with password hashing (5K tokens)
  2. Create auth service with login/logout (8K tokens)
  3. Create JWT token utilities (5K tokens)
  4. Create login/register views (10K tokens)
  5. Create auth middleware (5K tokens)
  6. Write auth integration tests (10K tokens)

  Total: 43K tokens, but spread across 6 focused tasks
```

### Task Template

```markdown
## Task: [Verb] [Object] [Context]

### Context (what AI needs to know)
- Relevant spec sections: [links]
- Existing code to read: [file paths]
- Patterns to follow: [examples]

### Scope (what to do)
- CREATE: [new files]
- MODIFY: [existing files]
- DO NOT: [out of scope]

### Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

### Token Estimate
- Read: ~5K (list files)
- Write: ~10K (list outputs)
- Total: ~15K
```

---

## Context Loading Optimization

### Minimize Context

```python
# BAD: Load entire file
"Read the entire user module" (2000 lines)

# GOOD: Load specific sections
"Read UserService.create_user method" (50 lines)
"Read User model definition" (30 lines)
```

### Use Summaries

```markdown
## Context Summary (instead of full code)

### User Model
- Fields: id, name, email, password_hash, created_at
- Methods: is_valid(), set_password(), check_password()
- Relations: has_many :orders, has_one :profile

### User Service
- create_user(data) -> User
- update_user(id, data) -> User
- delete_user(id) -> bool
```

### Reference by Interface

```python
# Instead of loading full implementation
"UserRepository implements: find(id), save(user), delete(id)"

# AI can generate compatible code without seeing implementation
```

---

## File Structure for AI

### Flat Over Nested

```
# BAD: Deep nesting (hard to reference)
src/features/users/domain/entities/user/user.model.ts

# GOOD: Shallow structure (easy to reference)
src/users/user.model.ts
```

### Explicit Over Implicit

```
# BAD: Magic imports (AI might hallucinate)
from utils import *

# GOOD: Explicit imports (AI knows exactly what's available)
from utils.validation import validate_email, validate_phone
from utils.formatting import format_date, format_currency
```

### Self-Documenting Names

```
# BAD: Generic names
handlers.py, utils.py, helpers.py

# GOOD: Purpose-clear names
user_http_handlers.py
email_validation_utils.py
date_formatting_helpers.py
```

---

## Metrics & Monitoring

### Task Health Indicators

| Metric | Healthy | Warning | Critical |
|--------|---------|---------|----------|
| Task token estimate | <30K | 30-60K | >60K |
| Files per task | 1-3 | 4-6 | >6 |
| Dependencies | 0-2 | 3-4 | >4 |
| Acceptance criteria | 2-5 | 6-8 | >8 |

### Red Flags

- Task description > 500 words
- "Implement entire feature"
- "Fix all bugs in module"
- Dependencies on incomplete tasks
- No clear acceptance criteria

---

## Examples

### Good Decomposition

```markdown
## Feature: User Registration

### Tasks (properly decomposed)

TASK-001: Create User model
- Create: users/models.py
- Token estimate: 5K
- Dependencies: none

TASK-002: Create registration serializer
- Create: users/serializers.py
- Modify: users/models.py (add validation method)
- Token estimate: 8K
- Dependencies: TASK-001

TASK-003: Create registration view
- Create: users/views.py
- Token estimate: 10K
- Dependencies: TASK-001, TASK-002

TASK-004: Write registration tests
- Create: users/tests/test_registration.py
- Token estimate: 12K
- Dependencies: TASK-001, TASK-002, TASK-003
```

### Bad Decomposition

```markdown
## Feature: User Registration

### Tasks (poorly decomposed)

TASK-001: Implement user registration
- Description: Create user model, add validation, create views,
  handle email verification, implement password reset, write tests,
  add admin interface, create API docs...
- Token estimate: 150K+ (way over budget!)
- Dependencies: unclear
```

---

## Practical Checklist

### Before Starting Task

- [ ] Clear previous session context
- [ ] Identify minimum required files
- [ ] Load only direct dependencies
- [ ] Check token budget (~30K ideal)

### During Task

- [ ] Add files only when needed
- [ ] Remove irrelevant context
- [ ] Use summaries for large files
- [ ] Reference interfaces, not implementations

### After Task

- [ ] Document learnings in memory
- [ ] Update CLAUDE.md if patterns emerged
- [ ] Clear session for next task

---

## Related

- [context-strategies.md](context-strategies.md) - Advanced strategies
- [writing-implementation-plans.md](writing-implementation-plans.md) - Implementation planning
- [task-creation-principles.md](task-creation-principles.md) - Task decomposition principles
- [task-creation-template-guide.md](task-creation-template-guide.md) - Task template & context
- [task-parallelization.md](task-parallelization.md) - Parallelization
- [task-dependencies.md](task-dependencies.md) - Dependency analysis
- [../faion-software-developer/code-decomposition-guidelines.md](../faion-software-developer/code-decomposition-guidelines.md) - Code-level decomposition
- [../faion-software-developer/llm-friendly-architecture.md](../faion-software-developer/llm-friendly-architecture.md) - LLM-optimized patterns
