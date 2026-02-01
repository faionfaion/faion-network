---
id: design-tokens-basics
name: "Design Tokens: Basics & Definition"
domain: DEV
skill: faion-software-developer
category: "development"
---

# Design Tokens: Basics & Definition

## Overview

Design tokens are the atomic values of a design system, storing visual design decisions as data. They ensure consistency across platforms (web, iOS, Android) and enable theming while maintaining a single source of truth.

## When to Use

- Building design systems
- Multi-platform applications
- Theming support (dark mode, white-label)
- Design-to-development handoff
- Maintaining brand consistency

## Key Principles

- **Single source of truth**: One definition, multiple outputs
- **Platform agnostic**: Tokens work across web, mobile, desktop
- **Semantic naming**: Names describe purpose, not value
- **Hierarchical structure**: Primitive to semantic to component
- **Version controlled**: Tokens in code, not just design tools

## Token Hierarchy

```
┌─────────────────────────────────────────────────────────────┐
│                    TOKEN HIERARCHY                          │
├─────────────────────────────────────────────────────────────┤
│ PRIMITIVE TOKENS (Core)                                     │
│   Raw values: colors, sizes, fonts                          │
│   Example: blue-500: #3B82F6                                │
├─────────────────────────────────────────────────────────────┤
│ SEMANTIC TOKENS (Alias)                                     │
│   Purpose-based references to primitives                    │
│   Example: color-primary: {blue-500}                        │
├─────────────────────────────────────────────────────────────┤
│ COMPONENT TOKENS (Specific)                                 │
│   Component-specific tokens                                 │
│   Example: button-bg-primary: {color-primary}               │
└─────────────────────────────────────────────────────────────┘
```

## Token Definition Format

### Primitive Tokens

```json
// tokens/primitive.json
{
  "color": {
    "gray": {
      "50": { "value": "#f9fafb" },
      "100": { "value": "#f3f4f6" },
      "200": { "value": "#e5e7eb" },
      "300": { "value": "#d1d5db" },
      "400": { "value": "#9ca3af" },
      "500": { "value": "#6b7280" },
      "600": { "value": "#4b5563" },
      "700": { "value": "#374151" },
      "800": { "value": "#1f2937" },
      "900": { "value": "#111827" },
      "950": { "value": "#030712" }
    },
    "blue": {
      "50": { "value": "#eff6ff" },
      "100": { "value": "#dbeafe" },
      "200": { "value": "#bfdbfe" },
      "300": { "value": "#93c5fd" },
      "400": { "value": "#60a5fa" },
      "500": { "value": "#3b82f6" },
      "600": { "value": "#2563eb" },
      "700": { "value": "#1d4ed8" },
      "800": { "value": "#1e40af" },
      "900": { "value": "#1e3a8a" }
    },
    "red": {
      "500": { "value": "#ef4444" },
      "600": { "value": "#dc2626" },
      "700": { "value": "#b91c1c" }
    },
    "green": {
      "500": { "value": "#22c55e" },
      "600": { "value": "#16a34a" },
      "700": { "value": "#15803d" }
    }
  },
  "spacing": {
    "0": { "value": "0" },
    "1": { "value": "0.25rem" },
    "2": { "value": "0.5rem" },
    "3": { "value": "0.75rem" },
    "4": { "value": "1rem" },
    "5": { "value": "1.25rem" },
    "6": { "value": "1.5rem" },
    "8": { "value": "2rem" },
    "10": { "value": "2.5rem" },
    "12": { "value": "3rem" },
    "16": { "value": "4rem" },
    "20": { "value": "5rem" }
  },
  "fontSize": {
    "xs": { "value": "0.75rem" },
    "sm": { "value": "0.875rem" },
    "base": { "value": "1rem" },
    "lg": { "value": "1.125rem" },
    "xl": { "value": "1.25rem" },
    "2xl": { "value": "1.5rem" },
    "3xl": { "value": "1.875rem" },
    "4xl": { "value": "2.25rem" }
  },
  "fontWeight": {
    "normal": { "value": "400" },
    "medium": { "value": "500" },
    "semibold": { "value": "600" },
    "bold": { "value": "700" }
  },
  "borderRadius": {
    "none": { "value": "0" },
    "sm": { "value": "0.125rem" },
    "md": { "value": "0.375rem" },
    "lg": { "value": "0.5rem" },
    "xl": { "value": "0.75rem" },
    "2xl": { "value": "1rem" },
    "full": { "value": "9999px" }
  },
  "shadow": {
    "sm": { "value": "0 1px 2px 0 rgb(0 0 0 / 0.05)" },
    "md": { "value": "0 4px 6px -1px rgb(0 0 0 / 0.1)" },
    "lg": { "value": "0 10px 15px -3px rgb(0 0 0 / 0.1)" },
    "xl": { "value": "0 20px 25px -5px rgb(0 0 0 / 0.1)" }
  }
}
```

### Semantic Tokens (Light Theme)

```json
// tokens/semantic.json
{
  "color": {
    "bg": {
      "primary": { "value": "{color.white}" },
      "secondary": { "value": "{color.gray.50}" },
      "tertiary": { "value": "{color.gray.100}" },
      "inverse": { "value": "{color.gray.900}" }
    },
    "text": {
      "primary": { "value": "{color.gray.900}" },
      "secondary": { "value": "{color.gray.600}" },
      "tertiary": { "value": "{color.gray.500}" },
      "inverse": { "value": "{color.white}" },
      "disabled": { "value": "{color.gray.400}" }
    },
    "border": {
      "default": { "value": "{color.gray.200}" },
      "hover": { "value": "{color.gray.300}" },
      "focus": { "value": "{color.blue.500}" }
    },
    "action": {
      "primary": { "value": "{color.blue.600}" },
      "primaryHover": { "value": "{color.blue.700}" },
      "secondary": { "value": "{color.gray.100}" },
      "secondaryHover": { "value": "{color.gray.200}" }
    },
    "status": {
      "success": { "value": "{color.green.600}" },
      "error": { "value": "{color.red.600}" },
      "warning": { "value": "{color.yellow.500}" },
      "info": { "value": "{color.blue.500}" }
    },
    "focus": {
      "ring": { "value": "{color.blue.500}" }
    }
  }
}
```

### Semantic Tokens (Dark Theme)

```json
// tokens/semantic-dark.json
{
  "color": {
    "bg": {
      "primary": { "value": "{color.gray.900}" },
      "secondary": { "value": "{color.gray.800}" },
      "tertiary": { "value": "{color.gray.700}" },
      "inverse": { "value": "{color.white}" }
    },
    "text": {
      "primary": { "value": "{color.gray.50}" },
      "secondary": { "value": "{color.gray.300}" },
      "tertiary": { "value": "{color.gray.400}" },
      "inverse": { "value": "{color.gray.900}" },
      "disabled": { "value": "{color.gray.600}" }
    },
    "border": {
      "default": { "value": "{color.gray.700}" },
      "hover": { "value": "{color.gray.600}" },
      "focus": { "value": "{color.blue.400}" }
    },
    "action": {
      "primary": { "value": "{color.blue.500}" },
      "primaryHover": { "value": "{color.blue.400}" }
    }
  }
}
```

## Best Practices

### Naming Conventions

- **Primitive tokens**: Describe what they are (color, size, font)
  - `color-blue-500`, `spacing-4`, `font-size-base`
- **Semantic tokens**: Describe purpose, not value
  - `color-text-primary`, `color-bg-secondary`, `spacing-content-gap`
- **Component tokens**: Specific to component usage
  - `button-padding-horizontal`, `card-border-radius`

### Token Organization

```
tokens/
├── primitive.json         # Core values
├── semantic.json          # Light theme aliases
├── semantic-dark.json     # Dark theme aliases
└── components/            # Component-specific tokens
    ├── button.json
    ├── card.json
    └── input.json
```

### Version Control Strategy

- Store tokens in Git with code
- Use semantic versioning for token packages
- Document breaking changes in token values
- Provide migration guides for major versions

## Anti-patterns

- **Hardcoded values**: Using raw colors/sizes instead of tokens
- **Too many tokens**: Creating tokens for every variation
- **Poor naming**: Using values in names (blue-500 as semantic)
- **No hierarchy**: Flat token structure without levels
- **Platform-specific**: Tokens that only work on one platform
- **Missing documentation**: Tokens without usage guidance

## References

- [Style Dictionary](https://amzn.github.io/style-dictionary/)
- [Design Tokens W3C](https://design-tokens.github.io/community-group/format/)
- [Tokens Studio](https://tokens.studio/)
- [Design Tokens Format Module](https://tr.designtokens.org/format/)


## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Implementation setup | haiku | Applying standard methodology patterns |
| Design decisions | sonnet | Trade-offs analysis |
| Complex scenarios | opus | Novel or complex solutions |
## Related

- [design-tokens-implementation.md](design-tokens-implementation.md) - Implementation, tooling, usage
