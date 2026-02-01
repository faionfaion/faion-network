---
id: ui-lib-basics
name: "UI Component Library - Basics"
domain: DEV
skill: faion-software-developer
category: "development"
---

# UI Component Library - Basics

## Overview

A UI component library provides reusable, consistent interface elements that accelerate development and ensure design consistency across applications. This includes atomic components, compound components, and design system integration.

## When to Use

- Building consistent user interfaces across products
- Team collaboration on frontend development
- Scaling design systems
- Reducing code duplication
- Ensuring accessibility compliance

## Key Principles

- **Composition over configuration**: Compose simple components
- **Single responsibility**: Each component does one thing well
- **Accessibility first**: Built-in ARIA support
- **Consistent API**: Predictable props across components
- **Customizable**: Allow theming and style overrides

## Component Structure

```
src/
├── components/
│   ├── primitives/          # Basic building blocks
│   │   ├── Button/
│   │   │   ├── Button.tsx
│   │   │   ├── Button.test.tsx
│   │   │   ├── Button.stories.tsx
│   │   │   └── index.ts
│   │   ├── Input/
│   │   ├── Text/
│   │   └── Box/
│   │
│   ├── composite/           # Composed from primitives
│   │   ├── Card/
│   │   ├── Modal/
│   │   ├── Dropdown/
│   │   └── Form/
│   │
│   ├── patterns/            # Common UI patterns
│   │   ├── DataTable/
│   │   ├── Pagination/
│   │   └── SearchInput/
│   │
│   └── layout/              # Layout components
│       ├── Container/
│       ├── Stack/
│       ├── Grid/
│       └── Flex/
│
├── hooks/                   # Shared hooks
├── utils/                   # Utilities
├── tokens/                  # Design tokens
└── index.ts                 # Public exports
```

## Button Component Example

```tsx
// components/primitives/Button/Button.tsx
import { forwardRef, ButtonHTMLAttributes, ReactNode } from 'react';
import { clsx } from 'clsx';
import { Slot } from '@radix-ui/react-slot';
import styles from './Button.module.css';

export type ButtonVariant = 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger';
export type ButtonSize = 'sm' | 'md' | 'lg';

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  /** Visual variant of the button */
  variant?: ButtonVariant;
  /** Size of the button */
  size?: ButtonSize;
  /** Whether the button takes full width */
  fullWidth?: boolean;
  /** Loading state */
  isLoading?: boolean;
  /** Left icon */
  leftIcon?: ReactNode;
  /** Right icon */
  rightIcon?: ReactNode;
  /** Render as child element (for links styled as buttons) */
  asChild?: boolean;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      variant = 'primary',
      size = 'md',
      fullWidth = false,
      isLoading = false,
      leftIcon,
      rightIcon,
      asChild = false,
      className,
      disabled,
      children,
      ...props
    },
    ref
  ) => {
    const Comp = asChild ? Slot : 'button';

    return (
      <Comp
        ref={ref}
        className={clsx(
          styles.button,
          styles[variant],
          styles[size],
          fullWidth && styles.fullWidth,
          isLoading && styles.loading,
          className
        )}
        disabled={disabled || isLoading}
        {...props}
      >
        {isLoading && (
          <span className={styles.spinner} aria-hidden="true">
            <LoadingSpinner size={size} />
          </span>
        )}
        {leftIcon && !isLoading && (
          <span className={styles.icon} aria-hidden="true">
            {leftIcon}
          </span>
        )}
        <span className={styles.content}>{children}</span>
        {rightIcon && (
          <span className={styles.icon} aria-hidden="true">
            {rightIcon}
          </span>
        )}
      </Comp>
    );
  }
);

Button.displayName = 'Button';
```

```css
/* Button.module.css */
.button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  font-family: inherit;
  font-weight: 500;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
}

.button:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: 2px;
}

.button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Variants */
.primary {
  background: var(--color-primary);
  color: var(--color-primary-foreground);
  border: none;
}

.primary:hover:not(:disabled) {
  background: var(--color-primary-hover);
}

.secondary {
  background: var(--color-secondary);
  color: var(--color-secondary-foreground);
  border: none;
}

.outline {
  background: transparent;
  color: var(--color-foreground);
  border: 1px solid var(--color-border);
}

.outline:hover:not(:disabled) {
  background: var(--color-muted);
}

.ghost {
  background: transparent;
  color: var(--color-foreground);
  border: none;
}

.ghost:hover:not(:disabled) {
  background: var(--color-muted);
}

.danger {
  background: var(--color-danger);
  color: var(--color-danger-foreground);
  border: none;
}

/* Sizes */
.sm {
  height: 2rem;
  padding: 0 0.75rem;
  font-size: 0.875rem;
}

.md {
  height: 2.5rem;
  padding: 0 1rem;
  font-size: 1rem;
}

.lg {
  height: 3rem;
  padding: 0 1.5rem;
  font-size: 1.125rem;
}

.fullWidth {
  width: 100%;
}

/* Loading state */
.loading .content {
  opacity: 0;
}

.spinner {
  position: absolute;
}
```

## Input Component with Validation

```tsx
// components/primitives/Input/Input.tsx
import { forwardRef, InputHTMLAttributes, ReactNode, useId } from 'react';
import { clsx } from 'clsx';
import styles from './Input.module.css';

export interface InputProps extends Omit<InputHTMLAttributes<HTMLInputElement>, 'size'> {
  /** Label for the input */
  label?: string;
  /** Helper text below the input */
  helperText?: string;
  /** Error message */
  error?: string;
  /** Size variant */
  size?: 'sm' | 'md' | 'lg';
  /** Left addon */
  leftAddon?: ReactNode;
  /** Right addon */
  rightAddon?: ReactNode;
  /** Whether the field is required */
  required?: boolean;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  (
    {
      label,
      helperText,
      error,
      size = 'md',
      leftAddon,
      rightAddon,
      required,
      className,
      id: providedId,
      ...props
    },
    ref
  ) => {
    const generatedId = useId();
    const id = providedId || generatedId;
    const helperId = `${id}-helper`;
    const errorId = `${id}-error`;

    return (
      <div className={clsx(styles.wrapper, className)}>
        {label && (
          <label htmlFor={id} className={styles.label}>
            {label}
            {required && <span className={styles.required} aria-hidden="true">*</span>}
          </label>
        )}

        <div className={clsx(styles.inputWrapper, error && styles.hasError)}>
          {leftAddon && (
            <span className={styles.addon}>{leftAddon}</span>
          )}

          <input
            ref={ref}
            id={id}
            className={clsx(styles.input, styles[size])}
            aria-invalid={!!error}
            aria-describedby={
              error ? errorId : helperText ? helperId : undefined
            }
            aria-required={required}
            {...props}
          />

          {rightAddon && (
            <span className={styles.addon}>{rightAddon}</span>
          )}
        </div>

        {error && (
          <span id={errorId} className={styles.error} role="alert">
            {error}
          </span>
        )}

        {helperText && !error && (
          <span id={helperId} className={styles.helperText}>
            {helperText}
          </span>
        )}
      </div>
    );
  }
);

Input.displayName = 'Input';
```

## Anti-patterns

- **Prop explosion**: Too many props making components hard to use
- **Tight coupling**: Components depending on specific parent structure
- **Inconsistent API**: Different prop names for same concept
- **Missing accessibility**: No ARIA attributes or keyboard support
- **Over-abstraction**: Components that are too generic to be useful
- **CSS leakage**: Styles affecting elements outside component

## References

- [Radix UI](https://www.radix-ui.com/)
- [shadcn/ui](https://ui.shadcn.com/)
- [Storybook](https://storybook.js.org/)
- [React Aria](https://react-spectrum.adobe.com/react-aria/)

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
