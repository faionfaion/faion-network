# AI Context-Aware Decomposition: Strategies

Advanced strategies for context management and decomposition.

---

## Decomposition Strategies

### Strategy 1: Vertical Slicing

Split by feature, not layer.

```
# BAD: Horizontal (by layer)
Task 1: Create all models (User, Order, Payment)
Task 2: Create all views (User, Order, Payment)
Task 3: Create all tests

# GOOD: Vertical (by feature)
Task 1: User feature (model + view + test)
Task 2: Order feature (model + view + test)
Task 3: Payment feature (model + view + test)
```

**Why:** Each task is self-contained, testable, deployable.

### Strategy 2: Dependency-Ordered

Execute in dependency order to avoid stubs.

```
Task Graph:
    User Model ─────┬──► Order Model ──► Payment Model
                    │
    User Service ───┴──► Order Service ──► Payment Service

Execution Order:
Wave 1: [User Model]           # No dependencies
Wave 2: [User Service, Order Model]  # Depends on Wave 1
Wave 3: [Order Service, Payment Model]
Wave 4: [Payment Service]
```

### Strategy 3: Interface-First

Define interfaces before implementation.

```
# Task 1: Define interfaces (small, quick)
class UserRepositoryInterface(Protocol):
    def find(self, id: int) -> User | None: ...
    def save(self, user: User) -> User: ...

# Task 2: Implement repository (focused)
class PostgresUserRepository(UserRepositoryInterface):
    # Implementation only, interface is clear

# Task 3: Implement service (uses interface)
class UserService:
    def __init__(self, repo: UserRepositoryInterface):
        self.repo = repo
```

### Strategy 4: Test-Driven Decomposition

Write tests first, they define the boundary.

```
# Task 1: Write tests for User model
def test_user_creation():
    user = User(name="John", email="john@example.com")
    assert user.is_valid()

# Task 2: Implement User model (guided by tests)
class User:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

    def is_valid(self) -> bool:
        return bool(self.name and self.email)
```

---

## Decomposition Workflow for SDD

### Phase 1: Spec → Design

```
Specification (WHAT)
      │
      ├── Identify entities (nouns)
      ├── Identify actions (verbs)
      └── Identify boundaries (domains)
      │
      ▼
Design Document (HOW)
      │
      ├── Map entities to files
      ├── Define interfaces
      └── Establish dependencies
```

### Phase 2: Design → Implementation Plan

```
Design Document
      │
      ├── List all files to create/modify
      ├── Calculate token estimates
      ├── Identify dependencies
      └── Group into waves
      │
      ▼
Implementation Plan
      │
      ├── Wave 1: [Independent tasks]
      ├── Wave 2: [Depends on Wave 1]
      └── Wave 3: [Depends on Wave 2]
```

### Phase 3: Plan → Tasks

```
Implementation Plan
      │
      For each item:
      ├── Check token budget (<100K)
      │   ├── YES → Create task file
      │   └── NO → Split further
      │
      └── Add to appropriate wave
      │
      ▼
Task Files in todo/
```

---

## Industry Best Practices (2024-2026)

### Context Window Management

From [Andrej Karpathy (ex-OpenAI)](https://eval.16x.engineer/blog/llm-context-management-guide):

> "Context management is the delicate art and science of filling the context window with just the right information."

**Key Insight:** Simply filling the context window is a bad practice. This creates "context bloat" leading to worse performance and higher costs.

### Asymmetric Context Strategy

Research shows optimal context loading:

```
BEFORE change:  More context (understand existing code)
AFTER change:   Less context (focus on new code)

Example for a function edit:
├── Enclosing class:       Include (provides context)
├── Target function:       Include (main focus)
├── Related functions:     Include (dependencies)
├── Unrelated functions:   Exclude (noise)
└── Following code:        Minimal (less relevant)
```

### Dynamic Context by Structure

Instead of fixed line counts, adjust context based on logical structure:
- Include entire enclosing function/class
- Include direct dependencies only
- Exclude sibling functions unless referenced

### RAG for Large Codebases

From [Qodo Blog](https://www.qodo.ai/blog/context-windows/):

```
Query: "How does user authentication work?"
       │
       ▼
RAG System:
├── Search knowledge base
├── Find top 3-5 relevant chunks
└── Inject only those chunks into prompt

Result: 100-page codebase → 3 key files in context
```

**When to use RAG:**
- Codebase > 50K lines
- Query-specific context needed
- Multiple independent modules

### Session Management

> "Start a new session for each new task, clearing the current context window. This ensures the context contains only relevant information."

**Anti-pattern:** Continuing long sessions with accumulated context

**Best practice:** Fresh session per task with curated context

### Directory-Level Configuration

Structure CLAUDE.md files per directory:

```
project/
├── CLAUDE.md           # Project-wide rules
├── frontend/
│   └── CLAUDE.md       # Frontend-specific rules
├── backend/
│   └── CLAUDE.md       # Backend-specific rules
└── tests/
    └── CLAUDE.md       # Testing conventions
```

**Benefit:** Only relevant rules loaded based on working directory.

### Cost Optimization

Context window costs scale linearly with tokens:

| Context Size | Relative Cost | Performance |
|--------------|---------------|-------------|
| 10K tokens | 1x | Optimal |
| 50K tokens | 5x | Good |
| 100K tokens | 10x | Degraded |
| 200K tokens | 20x | Significantly degraded |

**Strategy:** Use input token caching for frequently referenced code.

### Performance Degradation Research

From [NoLiMa research](https://agenta.ai/blog/top-6-techniques-to-manage-context-length-in-llms):

> "Performance degrades significantly as context length increases."

**Practical implications:**
- Effective context ~20-50K (not full 200K)
- Quality > Quantity
- Focused > Comprehensive

---

## Sources

- [LLM Context Management Guide](https://eval.16x.engineer/blog/llm-context-management-guide)
- [Context Windows Best Practices (Qodo)](https://www.qodo.ai/blog/context-windows/)
- [Managing Context Length (Agenta)](https://agenta.ai/blog/top-6-techniques-to-manage-context-length-in-llms)
- [LLM Prompt Best Practices (Winder.ai)](https://winder.ai/llm-prompt-best-practices-large-context-windows/)
- [Optimizing LLM Accuracy (OpenAI)](https://platform.openai.com/docs/guides/optimizing-llm-accuracy)
