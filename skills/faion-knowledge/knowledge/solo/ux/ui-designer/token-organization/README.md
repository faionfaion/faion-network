# Token Organization

## Problem

Token bloat reduces discoverability and defeats the purpose of systematization.

## Hierarchy

```
Primitives (raw values)
    ↓
Semantic tokens (purpose-based)
    ↓
Component tokens (component-specific, use sparingly)
```

## Best Practices

| Practice | Description |
|----------|-------------|
| Start lean | MVP mindset, not waterfall |
| Avoid bloat | Don't create token for every variation |
| Clear naming | `color.surface.primary` not `blue-1` |
| Document purpose | Why this token exists |
| Version control | Track changes over time |

## Token Naming Convention

```
{category}.{property}.{variant}.{state}

Examples:
color.background.primary
color.background.primary.hover
spacing.component.button
typography.heading.xl
```

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Design token organization | haiku | Systematic task: creating and organizing design tokens |

## Sources

- [Design Token Naming Best Practices](https://www.designsystems.com/token-naming/)
- [Token Organization Patterns](https://css-tricks.com/organizing-design-tokens/)
- [Avoiding Token Bloat](https://www.smashingmagazine.com/2025/design-token-organization/)
- [Semantic Token Architecture](https://www.nngroup.com/articles/design-token-architecture/)
- [Design Token Hierarchy](https://bradfrost.com/blog/post/design-token-hierarchy/)
