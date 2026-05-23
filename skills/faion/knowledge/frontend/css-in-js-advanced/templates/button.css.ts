// button.css.ts — vanilla-extract recipe example
// Install: pnpm add @vanilla-extract/css @vanilla-extract/recipes
import { createVar } from '@vanilla-extract/css';
import { recipe, type RecipeVariants } from '@vanilla-extract/recipes';

const focusColor = createVar();

export const button = recipe({
  base: {
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontWeight: 500,
    borderRadius: '0.375rem',
    cursor: 'pointer',
    transition: 'all 0.2s ease',
    vars: { [focusColor]: '#3b82f6' },
    ':focus-visible': {
      outline: `2px solid ${focusColor}`,
      outlineOffset: '2px',
    },
    ':disabled': { opacity: 0.5, cursor: 'not-allowed' },
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
      outline: {
        background: 'transparent',
        color: '#111827',
        border: '1px solid #e5e7eb',
        ':hover': { background: '#f9fafb' },
      },
    },
    size: {
      sm: { padding: '0.375rem 0.75rem', fontSize: '0.875rem' },
      md: { padding: '0.5rem 1rem', fontSize: '1rem' },
      lg: { padding: '0.75rem 1.5rem', fontSize: '1.125rem' },
    },
  },
  defaultVariants: { color: 'primary', size: 'md' },
});

export type ButtonVariants = RecipeVariants<typeof button>;
