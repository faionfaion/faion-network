// tailwind.config.js — token-backed Tailwind configuration
// Uses RGB channel pattern for color tokens to support opacity modifiers (bg-primary/50).
// Uses theme.extend to preserve Tailwind defaults (font-sans, spacing scale, etc.).
// CSS variables are declared in a @layer base { :root { } } block in globals.css.

module.exports = {
  content: ['./src/**/*.{ts,tsx,js,jsx}'],
  theme: {
    extend: {
      colors: {
        // RGB channel pattern: rgb(var(--color-X-rgb) / <alpha-value>)
        // Enables: bg-primary, bg-primary/50, text-primary, border-primary
        primary: {
          default: 'rgb(var(--color-primary-default-rgb) / <alpha-value>)',
          hover: 'rgb(var(--color-primary-hover-rgb) / <alpha-value>)',
        },
        feedback: {
          error: 'rgb(var(--color-feedback-error-rgb) / <alpha-value>)',
        },
        text: {
          default: 'rgb(var(--color-text-default-rgb) / <alpha-value>)',
          muted: 'rgb(var(--color-text-muted-rgb) / <alpha-value>)',
        },
        surface: {
          subtle: 'rgb(var(--color-surface-subtle-rgb) / <alpha-value>)',
        },
      },
      spacing: {
        // Semantic token names coexist with Tailwind's numeric scale
        xs: 'var(--spacing-xs)',
        sm: 'var(--spacing-sm)',
        md: 'var(--spacing-md)',
        lg: 'var(--spacing-lg)',
        xl: 'var(--spacing-xl)',
        '2xl': 'var(--spacing-2xl)',
      },
    },
  },
  plugins: [],
};

// Companion globals.css — declare custom properties:
/*
@layer base {
  :root {
    --color-primary-default-rgb: 59 130 246;
    --color-primary-hover-rgb: 37 99 235;
    --color-feedback-error-rgb: 239 68 68;
    --color-text-default-rgb: 17 24 39;
    --color-text-muted-rgb: 75 85 99;
    --color-surface-subtle-rgb: 243 244 246;
    --spacing-xs: 4px;
    --spacing-sm: 8px;
    --spacing-md: 16px;
    --spacing-lg: 24px;
    --spacing-xl: 32px;
    --spacing-2xl: 48px;
  }
}
*/
