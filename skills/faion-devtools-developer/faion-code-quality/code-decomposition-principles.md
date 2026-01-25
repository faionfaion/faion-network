# Code Decomposition Principles

Core principles and guidelines for breaking code into manageable, LLM-friendly pieces.

## Why Decomposition Matters

### For LLMs
- Context window limits (100K-200K tokens, effective ~20-50K)
- Better understanding of isolated, focused code
- Easier to generate, review, and modify smaller units
- Reduced hallucination risk with clear boundaries

### For Humans
- Easier navigation and comprehension
- Better code reviews (smaller diffs)
- Parallel development (fewer merge conflicts)
- Clearer ownership and responsibility

---

## Core Principles

### 1. Single File Responsibility

Each file should have ONE clear purpose.

```
BAD: user.py (500+ lines)
├── User model
├── User serializer
├── User views
├── User permissions
├── User utils
└── User tests

GOOD: users/
├── models.py        # Data structure only
├── serializers.py   # API representation
├── views.py         # HTTP handlers
├── permissions.py   # Access control
├── services.py      # Business logic
└── tests/
    ├── test_models.py
    ├── test_views.py
    └── test_services.py
```

### 2. Optimal File Size

| File Type | Ideal Lines | Max Lines | Action if Exceeded |
|-----------|-------------|-----------|-------------------|
| Model/Entity | 50-100 | 200 | Split by domain |
| Service | 100-200 | 300 | Extract sub-services |
| View/Controller | 50-150 | 250 | Extract handlers |
| Component (React) | 50-150 | 250 | Extract sub-components |
| Test file | 100-300 | 500 | Split by scenario |
| Config | 50-100 | 150 | Split by environment |

### 3. Token Budget Planning

For LLM-assisted development, plan token usage:

```
100K Token Budget:
├── Task context:     ~5K (spec, design, task file)
├── Existing code:   ~20K (files to read)
├── Generation:      ~30K (new code to write)
├── Testing:         ~20K (tests to write)
└── Buffer:          ~25K (errors, iterations)
```

**Rule:** If a single file exceeds 500 lines (~15K tokens), split it.

---

## When to Split (Checklist)

Split a file when:

- [ ] **Lines > 300** - Too long for comfortable reading
- [ ] **Multiple classes/components** - Should be separate files
- [ ] **Multiple responsibilities** - Violates SRP
- [ ] **Frequent conflicts** - Multiple people editing
- [ ] **Hard to test** - Need to mock too much
- [ ] **Hard to name** - "utils", "helpers", "misc"
- [ ] **Circular imports** - Entangled dependencies
- [ ] **LLM struggles** - AI gives incomplete/wrong answers

## When NOT to Split

Keep together when:

- [ ] **Tightly coupled** - Always change together
- [ ] **Small total size** - Under 100 lines combined
- [ ] **Single concept** - Logical unit
- [ ] **Would create indirection** - Extra files without benefit
- [ ] **Would break encapsulation** - Exposes internals

---

## Anti-Patterns

### 1. God File
```
# BAD: utils.py with 2000 lines of unrelated functions
# Split by domain: string_utils.py, date_utils.py, etc.
```

### 2. Micro-Files
```
# BAD: One function per file
add.py: def add(a, b): return a + b
subtract.py: def subtract(a, b): return a - b

# GOOD: Group related operations
math_operations.py: Contains add, subtract, multiply, divide
```

### 3. Leaky Abstractions
```
# BAD: Service knows about HTTP
class UserService:
    def get_user(self, request):  # Coupled to HTTP
        user_id = request.query_params['id']

# GOOD: Pure business logic
class UserService:
    def get_user(self, user_id: int):  # Framework agnostic
        return self.repository.find(user_id)
```

### 4. Barrel Files Gone Wrong
```typescript
// BAD: index.ts re-exports everything (breaks tree-shaking)
export * from './UserService';
export * from './OrderService';
export * from './PaymentService';
// ... 50 more exports

// GOOD: Explicit exports
export { UserService } from './UserService';
export type { User } from './types';
```

---

## Decomposition Workflow

### Step 1: Analyze
```
1. Identify file size (lines, tokens)
2. List responsibilities (what does it do?)
3. Map dependencies (what does it use?)
4. Find natural boundaries (where to cut?)
```

### Step 2: Plan
```
1. Draw target structure
2. Define interfaces between new modules
3. Plan migration order (tests first)
4. Estimate effort per split
```

### Step 3: Execute
```
1. Create new files with empty structure
2. Move code piece by piece
3. Update imports
4. Run tests after each move
5. Commit each logical step
```

### Step 4: Verify
```
1. All tests pass
2. No circular imports
3. Each file has single responsibility
4. File sizes within limits
5. Clear naming
```

---

## Industry Best Practices (2024-2026)

### DORA Report Findings

Organizations implementing modular architectures:
- **Deploy 973x more frequently** than low performers
- **Change failure rates 5x lower** than monolithic approaches
- **25-35% productivity improvement** with clear module ownership

### Modular Monolith Patterns

From [Microservices.io](https://microservices.io/post/architecture/2024/09/09/modular-monolith-patterns-for-fast-flow.html):

```
Modular Monolith Structure:
├── Core Module (minimal, stable)
│   └── Extension points for plugins
├── Domain Modules (loosely coupled)
│   ├── users/        # DDD bounded context
│   ├── orders/       # DDD bounded context
│   └── payments/     # DDD bounded context
└── Plugin Modules (optional, extensible)
    └── Third-party integrations
```

**Benefits:**
- 40-60% reduction in core codebase complexity
- Easier to extract into microservices later
- Clear team ownership per module

### LLM Coding Workflow (Addy Osmani)

From [AddyOsmani.com](https://addyosmani.com/blog/ai-coding-workflow/):

1. **Spec First:** Create `spec.md` with requirements, architecture, data models
2. **Plan Generation:** Feed spec to reasoning model for project plan
3. **Task Breakdown:** Break into logical, bite-sized milestones
4. **Iterative Execution:** Execute tasks with AI as pair programmer

> "Treat the LLM as a powerful pair programmer that requires clear direction, context and oversight rather than autonomous judgment."

### Context File Strategy

Create `llms.txt` or `CLAUDE.md` describing:
- High-level system goals
- Key areas of codebase
- Important knowledge per area
- Full file structure

> "This is a bit of work, but it's a one-time cost that pays off in the long run." — Simon Willison

### Multi-Model Strategy

> "Sometimes it can be valuable to try two or more LLMs in parallel to cross-check how they might approach the same problem differently. Each model has its own 'personality'."

---

## Related

- [code-decomposition-patterns.md](code-decomposition-patterns.md) - Decomposition patterns and examples
- [llm-friendly-architecture.md](llm-friendly-architecture.md) - LLM-optimized code patterns
- [refactoring-patterns.md](refactoring-patterns.md) - Refactoring techniques
- [react-component-architecture.md](react-component-architecture.md) - React patterns
- [../faion-sdd/ai-context-aware-decomposition.md](../faion-sdd/ai-context-aware-decomposition.md) - AI task decomposition

## Sources

- [My LLM Coding Workflow (Addy Osmani)](https://addyosmani.com/blog/ai-coding-workflow/)
- [Modular Monolith Patterns (Microservices.io)](https://microservices.io/post/architecture/2024/09/09/modular-monolith-patterns-for-fast-flow.html)
- [Patterns of Modular Architecture (DZone)](https://dzone.com/refcardz/patterns-modular-architecture)
- [2024 DORA Report](https://www.devops-research.com/)
