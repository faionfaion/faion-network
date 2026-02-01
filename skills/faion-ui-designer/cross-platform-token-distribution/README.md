# Cross-Platform Token Distribution

## Problem

Design tokens must work across iOS, Android, Web.

## Tools

| Tool | Function |
|------|----------|
| Style Dictionary | Token transformation |
| Tokens Studio | Figma plugin + sync |
| Supernova | Design system platform |
| Specify | Token distribution |

## Pipeline

```
Figma Tokens
    ↓
Token Studio export (JSON)
    ↓
Style Dictionary transform
    ↓
Platform outputs:
  → CSS variables
  → SCSS maps
  → iOS Swift
  → Android XML
  → React Native
```

## Output Examples

**CSS:**
```css
:root {
  --color-primary: #3B82F6;
  --spacing-md: 16px;
}
```

**iOS Swift:**
```swift
struct Colors {
  static let primary = UIColor(hex: "#3B82F6")
}
```

**Android XML:**
```xml
<color name="primary">#3B82F6</color>
<dimen name="spacing_md">16dp</dimen>
```

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Design token organization | haiku | Systematic task: creating and organizing design tokens |

## Sources

- [Style Dictionary Documentation](https://amzn.github.io/style-dictionary/)
- [Tokens Studio for Figma](https://tokens.studio/)
- [Cross-Platform Design Tokens](https://www.designsystems.com/cross-platform-tokens/)
- [Supernova Platform](https://www.supernova.io/)
- [Design Token Distribution Guide](https://css-tricks.com/design-token-distribution/)
