# Framework Decomposition Patterns

LLM-friendly code organization for popular frameworks.

This file provides a quick overview and universal principles. For detailed framework-specific patterns, see:

- [decomposition-django.md](decomposition-django.md) - Django patterns (service layer, selectors)
- [decomposition-rails.md](decomposition-rails.md) - Ruby on Rails patterns (service objects, query objects)
- [decomposition-laravel.md](decomposition-laravel.md) - Laravel patterns (actions, DTOs)
- [decomposition-react.md](decomposition-react.md) - React/Next.js patterns (composition, hooks)

---

## Quick Reference

### Django

**Key Pattern:** Service layer + Selectors

**Details:** See [decomposition-django.md](decomposition-django.md)

### Ruby on Rails

**Key Pattern:** Service objects + Query objects

**Details:** See [decomposition-rails.md](decomposition-rails.md)

### Laravel

**Key Pattern:** Actions + DTOs

**Details:** See [decomposition-laravel.md](decomposition-laravel.md)

### React

**Key Pattern:** Component composition + Custom hooks

**Details:** See [decomposition-react.md](decomposition-react.md)

---

## Summary: Universal Principles

### File Size Limits by Type

| Type | Target | Max |
|------|--------|-----|
| Model/Entity | 50-80 | 150 |
| Service | 80-120 | 200 |
| Controller/View | 60-80 | 150 |
| Component | 50-80 | 150 |
| Hook/Composable | 40-60 | 100 |
| Test | 100-150 | 300 |

### Universal Patterns

1. **Service Layer** - Business logic extracted from controllers
2. **Repository/Selector** - Data access abstracted
3. **DTO/Input Objects** - Explicit data transfer
4. **Composition** - Small components composed into larger ones
5. **Hooks/Composables** - Reusable stateful logic extracted

### LLM Context Benefits

| Structure | Context Needed | LLM Success Rate |
|-----------|----------------|------------------|
| Fat controller/model | 50K+ tokens | ~60% |
| Service layer | 20-30K tokens | ~85% |
| Full decomposition | 10-20K tokens | ~95% |

---

## Framework-Specific Documentation

For complete patterns and examples, see framework-specific files:

- **[decomposition-django.md](decomposition-django.md)** - Django service layer, selectors, views (1576 tokens)
- **[decomposition-rails.md](decomposition-rails.md)** - Rails service objects, query objects (1450 tokens)
- **[decomposition-laravel.md](decomposition-laravel.md)** - Laravel actions, DTOs, resources (1390 tokens)
- **[decomposition-react.md](decomposition-react.md)** - React composition, hooks, Next.js (1725 tokens)

## Related

- [code-decomposition-principles.md](code-decomposition-principles.md) - Core principles and best practices
- [code-decomposition-patterns.md](code-decomposition-patterns.md) - Decomposition patterns and examples
- [llm-friendly-architecture.md](llm-friendly-architecture.md) - LLM optimization
- [../faion-sdd/ai-context-aware-decomposition.md](../faion-sdd/ai-context-aware-decomposition.md) - Task decomposition
