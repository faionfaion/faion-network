---
id: css-in-js-advanced
name: "CSS-in-JS Advanced"
domain: DEV
skill: faion-software-developer
category: "development"
---

# CSS-in-JS Advanced

## vanilla-extract (Zero-Runtime)

Zero-runtime CSS-in-JS solution with build-time extraction for optimal performance.

```typescript
// Button.css.ts
import { style, styleVariants, createVar } from '@vanilla-extract/css';
import { recipe, RecipeVariants } from '@vanilla-extract/recipes';

// Create CSS variables
const accentColor = createVar();

// Base styles
const base = style({
  display: 'inline-flex',
  alignItems: 'center',
  justifyContent: 'center',
  fontWeight: 500,
  borderRadius: '0.375rem',
  cursor: 'pointer',
  transition: 'all 0.2s ease',
  vars: {
    [accentColor]: '#3b82f6',
  },
  ':focus-visible': {
    outline: `2px solid ${accentColor}`,
    outlineOffset: '2px',
  },
  ':disabled': {
    opacity: 0.5,
    cursor: 'not-allowed',
  },
});

// Style variants
const colorVariants = styleVariants({
  primary: {
    background: '#3b82f6',
    color: '#ffffff',
    border: 'none',
    ':hover': {
      background: '#2563eb',
    },
  },
  secondary: {
    background: '#f3f4f6',
    color: '#1f2937',
    border: 'none',
    ':hover': {
      background: '#e5e7eb',
    },
  },
  outline: {
    background: 'transparent',
    color: '#111827',
    border: '1px solid #e5e7eb',
    ':hover': {
      background: '#f9fafb',
    },
  },
});

const sizeVariants = styleVariants({
  sm: {
    padding: '0.375rem 0.75rem',
    fontSize: '0.875rem',
  },
  md: {
    padding: '0.5rem 1rem',
    fontSize: '1rem',
  },
  lg: {
    padding: '0.75rem 1.5rem',
    fontSize: '1.125rem',
  },
});

// Recipe (combines variants)
export const button = recipe({
  base: {
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontWeight: 500,
    borderRadius: '0.375rem',
    cursor: 'pointer',
    transition: 'all 0.2s ease',
  },
  variants: {
    color: {
      primary: {
        background: '#3b82f6',
        color: '#ffffff',
        ':hover': { background: '#2563eb' },
      },
      secondary: {
        background: '#f3f4f6',
        color: '#1f2937',
        ':hover': { background: '#e5e7eb' },
      },
    },
    size: {
      sm: { padding: '0.375rem 0.75rem', fontSize: '0.875rem' },
      md: { padding: '0.5rem 1rem', fontSize: '1rem' },
      lg: { padding: '0.75rem 1.5rem', fontSize: '1.125rem' },
    },
  },
  defaultVariants: {
    color: 'primary',
    size: 'md',
  },
});

export type ButtonVariants = RecipeVariants<typeof button>;

// Button.tsx
import { button, ButtonVariants } from './Button.css';

interface ButtonProps extends ButtonVariants {
  children: React.ReactNode;
}

export function Button({ color, size, children }: ButtonProps) {
  return (
    <button className={button({ color, size })}>
      {children}
    </button>
  );
}
```

## vanilla-extract with Sprinkles

Utility-based CSS system using vanilla-extract for atomic CSS patterns.

```typescript
// sprinkles.css.ts
import { defineProperties, createSprinkles } from '@vanilla-extract/sprinkles';

const space = {
  none: 0,
  sm: '0.5rem',
  md: '1rem',
  lg: '1.5rem',
  xl: '2rem',
};

const colors = {
  primary: '#3b82f6',
  secondary: '#6b7280',
  white: '#ffffff',
  black: '#000000',
  transparent: 'transparent',
};

const responsiveProperties = defineProperties({
  conditions: {
    mobile: {},
    tablet: { '@media': 'screen and (min-width: 768px)' },
    desktop: { '@media': 'screen and (min-width: 1024px)' },
  },
  defaultCondition: 'mobile',
  properties: {
    display: ['none', 'flex', 'block', 'inline-flex', 'grid'],
    flexDirection: ['row', 'column'],
    alignItems: ['stretch', 'flex-start', 'center', 'flex-end'],
    justifyContent: ['flex-start', 'center', 'flex-end', 'space-between'],
    gap: space,
    padding: space,
    paddingTop: space,
    paddingBottom: space,
    paddingLeft: space,
    paddingRight: space,
    margin: space,
    marginTop: space,
    marginBottom: space,
  },
  shorthands: {
    p: ['padding'],
    px: ['paddingLeft', 'paddingRight'],
    py: ['paddingTop', 'paddingBottom'],
    m: ['margin'],
    mx: ['marginLeft', 'marginRight'],
    my: ['marginTop', 'marginBottom'],
  },
});

const colorProperties = defineProperties({
  conditions: {
    lightMode: {},
    darkMode: { '@media': '(prefers-color-scheme: dark)' },
  },
  defaultCondition: 'lightMode',
  properties: {
    color: colors,
    background: colors,
    borderColor: colors,
  },
});

export const sprinkles = createSprinkles(
  responsiveProperties,
  colorProperties
);

export type Sprinkles = Parameters<typeof sprinkles>[0];

// Usage
import { sprinkles } from './sprinkles.css';

function Card() {
  return (
    <div
      className={sprinkles({
        display: 'flex',
        flexDirection: { mobile: 'column', tablet: 'row' },
        gap: 'md',
        p: 'lg',
        background: { lightMode: 'white', darkMode: 'black' },
      })}
    >
      Content
    </div>
  );
}
```

## Performance Considerations

Optimize CSS-in-JS for production with these patterns.

```tsx
// Avoid creating styles in render
// BAD
function BadComponent({ color }) {
  // Creates new styled component every render!
  const Box = styled.div`
    background: ${color};
  `;
  return <Box />;
}

// GOOD - Use props
const Box = styled.div<{ $color: string }>`
  background: ${({ $color }) => $color};
`;

function GoodComponent({ color }) {
  return <Box $color={color} />;
}

// GOOD - Use CSS variables for frequently changing values
const AnimatedBox = styled.div`
  transform: translateX(var(--x, 0));
  transition: transform 0.1s ease;
`;

function AnimatedComponent({ x }) {
  return <AnimatedBox style={{ '--x': `${x}px` }} />;
}

// GOOD - Memoize computed styles
const DynamicButton = styled.button`
  ${({ $styles }) => $styles}
`;

function OptimizedComponent({ variant }) {
  const styles = useMemo(
    () =>
      css`
        background: ${variant === 'primary' ? 'blue' : 'gray'};
      `,
    [variant]
  );

  return <DynamicButton $styles={styles}>Click</DynamicButton>;
}
```

## CSS Extraction (SSR/SSG)

Server-side rendering setup for styled-components with Next.js.

```tsx
// _document.tsx (Next.js with styled-components)
import Document, { Html, Head, Main, NextScript } from 'next/document';
import { ServerStyleSheet } from 'styled-components';

export default class MyDocument extends Document {
  static async getInitialProps(ctx) {
    const sheet = new ServerStyleSheet();
    const originalRenderPage = ctx.renderPage;

    try {
      ctx.renderPage = () =>
        originalRenderPage({
          enhanceApp: (App) => (props) =>
            sheet.collectStyles(<App {...props} />),
        });

      const initialProps = await Document.getInitialProps(ctx);
      return {
        ...initialProps,
        styles: [initialProps.styles, sheet.getStyleElement()],
      };
    } finally {
      sheet.seal();
    }
  }

  render() {
    return (
      <Html>
        <Head />
        <body>
          <Main />
          <NextScript />
        </body>
      </Html>
    );
  }
}
```

## Best Practices

### Do

- Use zero-runtime solutions for static styles
- Extract styles to separate files for reusability
- Implement server-side style extraction for SSR
- Use CSS variables for frequently changing values
- Memoize computed styles

### Don't

- Create styled components inside render functions
- Over-nest selectors (max 3 levels)
- Mix multiple CSS-in-JS libraries
- Ignore bundle size impact
- Skip SSR style extraction

## References

- [vanilla-extract](https://vanilla-extract.style/)
- [vanilla-extract Recipes](https://vanilla-extract.style/documentation/packages/recipes/)
- [vanilla-extract Sprinkles](https://vanilla-extract.style/documentation/packages/sprinkles/)
- [styled-components SSR](https://styled-components.com/docs/advanced#server-side-rendering)
- [Emotion SSR](https://emotion.sh/docs/ssr)

## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Fix CSS typo, update Tailwind class, run prettier | haiku | Direct text replacement and formatting |
| Code review component accessibility compliance | sonnet | WCAG standards evaluation |
| Debug responsive layout issues across breakpoints | sonnet | Testing and debugging |
| Design system architecture and token structure | opus | Complex organization and scaling |
| Refactor React component for performance | sonnet | Optimization and code quality |
| Plan design token migration across 50+ components | opus | Large-scale coordination |
| Build storybook automation and interactions | sonnet | Testing and documentation setup |
