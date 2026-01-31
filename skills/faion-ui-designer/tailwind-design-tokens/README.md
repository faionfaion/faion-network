# Tailwind + Design Tokens

## Problem

CSS frameworks need systematic token integration.

## Configuration

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    colors: {
      primary: {
        50: 'var(--color-primary-50)',
        100: 'var(--color-primary-100)',
        // ... generated from tokens
      }
    },
    spacing: {
      xs: 'var(--spacing-xs)',
      sm: 'var(--spacing-sm)',
      md: 'var(--spacing-md)',
      lg: 'var(--spacing-lg)',
      xl: 'var(--spacing-xl)',
    },
    fontFamily: {
      sans: 'var(--font-family-sans)',
      mono: 'var(--font-family-mono)',
    }
  }
}
```

## Best Practices

1. Define tokens in tailwind.config.js
2. Create reusable component patterns
3. Document in Storybook
4. Enforce consistent usage
5. Generate CSS variables from tokens

## Sources

- [Tailwind CSS Documentation](https://tailwindcss.com/docs/theme)
- [Tailwind Design Tokens Integration](https://www.smashingmagazine.com/2025/tailwind-design-tokens/)
- [CSS Variables with Tailwind](https://tailwindcss.com/docs/customizing-colors#using-css-variables)
- [Design System + Tailwind](https://www.designsystems.com/tailwind-integration/)
- [Tailwind Theme Configuration](https://tailwindcss.com/docs/configuration)
