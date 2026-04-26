// tailwind.config.js — design token integration example
// All values reference CSS custom properties defined in tokens.css
// No hardcoded hex, px, or raw values in this file

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{js,ts,jsx,tsx,html}'],

  // Safelist dynamic token classes assembled via string concatenation
  safelist: [],

  theme: {
    colors: {
      // Semantic tokens — action
      primary: {
        DEFAULT: 'rgb(var(--color-primary-rgb) / <alpha-value>)',
        hover:   'rgb(var(--color-primary-hover-rgb) / <alpha-value>)',
      },
      // Semantic tokens — feedback
      error:   'rgb(var(--color-error-rgb) / <alpha-value>)',
      success: 'rgb(var(--color-success-rgb) / <alpha-value>)',
      warning: 'rgb(var(--color-warning-rgb) / <alpha-value>)',
      // Semantic tokens — surface
      surface: {
        DEFAULT: 'var(--color-surface)',
        raised:  'var(--color-surface-raised)',
      },
      // Semantic tokens — text
      text: {
        DEFAULT:   'var(--color-text)',
        secondary: 'var(--color-text-secondary)',
        disabled:  'var(--color-text-disabled)',
      },
    },

    spacing: {
      xs: 'var(--spacing-xs)',   // 4px
      sm: 'var(--spacing-sm)',   // 8px
      md: 'var(--spacing-md)',   // 16px
      lg: 'var(--spacing-lg)',   // 24px
      xl: 'var(--spacing-xl)',   // 32px
      '2xl': 'var(--spacing-2xl)', // 48px
    },

    fontFamily: {
      sans: ['var(--font-family-sans)', 'system-ui', 'sans-serif'],
      mono: ['var(--font-family-mono)', 'monospace'],
    },

    fontSize: {
      sm:   ['var(--font-size-sm)',   { lineHeight: 'var(--line-height-sm)' }],
      base: ['var(--font-size-base)', { lineHeight: 'var(--line-height-base)' }],
      lg:   ['var(--font-size-lg)',   { lineHeight: 'var(--line-height-lg)' }],
      xl:   ['var(--font-size-xl)',   { lineHeight: 'var(--line-height-xl)' }],
    },

    borderRadius: {
      sm: 'var(--radius-sm)',
      md: 'var(--radius-md)',
      lg: 'var(--radius-lg)',
      full: '9999px',
    },
  },

  plugins: [],
};
