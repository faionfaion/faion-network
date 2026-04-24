# Pattern Memory

## Overview

Pattern memory is a system for capturing, storing, and retrieving successful patterns learned during development sessions. It creates an evolving knowledge base that improves agent performance over time by enabling consistent application of proven solutions.

Unlike traditional documentation, pattern memory is **actively used by LLM agents** during task execution, not just passively stored for human reference.

## Core Concepts

### What is a Pattern?

A pattern is a **reusable solution** to a recurring problem, consisting of:

| Component | Description |
|-----------|-------------|
| Problem | What situation triggers this pattern |
| Context | When/where to apply it |
| Solution | The proven approach |
| Evidence | Tasks where it succeeded |
| Confidence | Validation score (0.5-1.0) |

### Pattern vs Code Snippet

| Aspect | Pattern | Code Snippet |
|--------|---------|--------------|
| Abstraction | High (problem + context) | Low (just code) |
| Reusability | Cross-project | Project-specific |
| Metadata | Validation, provenance | None |
| Evolution | Improves over time | Static |

## Pattern Categories

### 1. Code Patterns

Low-level implementation patterns:

- **Error Handling**: Try-catch, fallback strategies, retry mechanisms
- **Data Management**: State patterns, caching, transformations
- **API Design**: Endpoint structure, response formats, versioning
- **Testing**: Unit test patterns, mocking strategies, test data

### 2. Architecture Patterns

System-level design patterns:

- **Structural**: Component organization, module boundaries, layer separation
- **Behavioral**: Event handling, pub-sub, command patterns
- **Integration**: API integration, service communication, data sync

### 3. Workflow Patterns

Process and methodology patterns:

- **Planning**: Estimation, decomposition, risk assessment
- **Execution**: Implementation order, debugging approaches
- **Review**: Code review practices, quality gates

## Memory Architecture

```
.aidocs/memory/
├── patterns.md           # Active patterns (high confidence)
├── patterns-archive.md   # Deprecated/retired patterns
├── mistakes.md           # Anti-patterns, lessons learned
├── decisions.md          # Key architectural decisions
└── session.md            # Current session state
```

### Hierarchical Memory (2026 Best Practice)

Modern LLM agents use hierarchical memory to balance context limits with information retrieval:

| Memory Type | Scope | Retention | Access |
|-------------|-------|-----------|--------|
| **Working** | Current task | Session | Always loaded |
| **Session** | Current feature | Conversation | On-demand |
| **Project** | Single project | Persistent | By query |
| **Global** | Cross-project | Permanent | By relevance |

## Pattern Lifecycle

```
Discovery → Capture → Validation → Establishment → Maintenance
    |           |           |             |              |
   0.5        0.6-0.7     0.8-0.9       0.9+       Review/Archive
```

### Confidence Levels

| Level | Confidence | Criteria |
|-------|------------|----------|
| **Initial** | 0.5 | First successful use |
| **Validated** | 0.6-0.7 | 2-3 successful uses in similar contexts |
| **Established** | 0.8-0.9 | 5+ uses, verified across different contexts |
| **Proven** | 0.9+ | 10+ uses, adopted as standard practice |

## CLAUDE.md Integration

Patterns are synced to project CLAUDE.md for immediate availability:

```markdown
## Learned Patterns

### PAT-001: Async Error Boundary
**Confidence:** 0.92 | **Uses:** 15 | **Success:** 93%
- Wrap async operations with try-catch-finally
- Manage loading/error/data states explicitly
- Display appropriate UI for each state
```

### What to Include in CLAUDE.md

- High-confidence patterns (0.8+)
- Frequently used patterns (5+ uses)
- Project-specific conventions
- Critical anti-patterns from mistakes.md

### What NOT to Include

- Low-confidence patterns (still validating)
- Obvious patterns (well-known best practices)
- Verbose code examples (link to examples.md instead)

## Pattern Scoring

### Score Calculation

```
confidence = base_score * usage_factor * success_factor * recency_factor

Where:
- base_score: 0.5 (initial)
- usage_factor: min(usage_count / 10, 1.5)
- success_factor: success_rate ^ 0.5
- recency_factor: 1.0 - (days_since_last_use / 365) * 0.3
```

### Score Triggers

| Event | Score Change |
|-------|--------------|
| First successful use | Set to 0.5 |
| Successful reuse | +0.05 to +0.10 |
| Failed application | -0.10 to -0.20 |
| No use for 90 days | -0.05 |
| Peer validation | +0.10 |

## Best Practices

### Pattern Quality

1. **Specific but generalizable** - Clear context, broad applicability
2. **Complete documentation** - Problem, solution, trade-offs
3. **Working examples** - Real code, not just theory
4. **Known limitations** - When NOT to use

### Memory Management

1. **Selective storage** - Not all solutions are patterns
2. **Regular cleanup** - Archive unused patterns (90+ days)
3. **Merge duplicates** - Avoid fragmentation
4. **Version control** - Track pattern evolution

### Capture Triggers

Capture a new pattern when:
- Solution works in 2+ different contexts
- Solution solves a problem you've seen before
- Solution includes non-obvious insight
- Solution prevents a common mistake

Do NOT capture:
- One-off fixes
- Well-known best practices (already in docs)
- Project-specific configurations
- Trivial implementations


## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Writing specification templates | haiku | Form completion, mechanical setup |
| Reviewing specifications for clarity | sonnet | Language analysis, logical consistency |
| Architecting complex system specs | opus | Holistic design, novel combinations |
## Related Files

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Pattern capture checklist |
| [examples.md](examples.md) | Pattern examples by category |
| [templates.md](templates.md) | Pattern file templates |
| [llm-prompts.md](llm-prompts.md) | Prompts for pattern extraction |

## References

### Research Papers

- [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366)
- [Memory in the Age of AI Agents: A Survey](https://github.com/Shichun-Liu/Agent-Memory-Paper-List)
- MAGMA: Multi-Graph based Agentic Memory Architecture (2026)
- EverMemOS: Memory Operating System for Structured Reasoning (2026)

### Frameworks

- [LangChain Long-term Memory](https://langchain-ai.github.io/langmem/concepts/conceptual_guide/)
- [Mem0 Memory Layer](https://mem0.ai/blog/memory-in-agents-what-why-and-how)
- [MemGPT Operating System Paradigm](https://memgpt.ai/)

### Design Patterns

- [Design Patterns (GoF)](https://www.oreilly.com/library/view/design-patterns-elements/0201633612/)
- [Patterns of Enterprise Application Architecture](https://martinfowler.com/eaaCatalog/)
- [Software Design Patterns](https://refactoring.guru/design-patterns)
