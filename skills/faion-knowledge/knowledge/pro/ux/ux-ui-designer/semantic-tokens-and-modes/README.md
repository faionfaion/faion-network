# Semantic Tokens and Modes

## Problem

Tokens need to adapt to different contexts (themes, platforms, breakpoints).

## Mode Types

| Collection | Modes Example |
|------------|---------------|
| Color | Light, Dark, High contrast |
| Typography | Desktop, Mobile, Compact |
| Density | Default, Compact, Comfortable |
| Brand | Brand A, Brand B, White-label |

## Figma Variables Implementation

```
Collection: Colors
  Mode: Light
    surface.primary → #FFFFFF
    text.primary → #1A1A1A
  Mode: Dark
    surface.primary → #1A1A1A
    text.primary → #FFFFFF
```

## Multi-platform Tokens

```json
{
  "spacing": {
    "button": {
      "padding": {
        "value": "16px",
        "ios": "14px",
        "android": "12px"
      }
    }
  }
}
```

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Wireframing and sketching | haiku | Mechanical task: translating requirements into wireframes |

## Sources

- [Figma Variables Documentation](https://help.figma.com/hc/en-us/articles/15339657135383-Guide-to-variables-in-Figma)
- [Semantic Tokens Guide](https://www.designsystems.com/semantic-tokens/)
- [Design Token Modes](https://css-tricks.com/design-token-modes/)
- [Theme Switching with Tokens](https://www.smashingmagazine.com/2025/theme-tokens/)
- [Multi-platform Token Strategy](https://amzn.github.io/style-dictionary/architecture/)
