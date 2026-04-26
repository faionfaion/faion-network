// tailwind.config.ts — Design-token-driven Tailwind v3 config
// Consumes Style Dictionary outputs from tokens/dist/js/tokens.js
// All color, spacing, font, radius, and shadow values come from token JSON.

import type { Config } from 'tailwindcss';

// If not using Style Dictionary, replace token imports with inline values.
// import tokens from './tokens/dist/js/tokens.js';

export default {
  content: ['./src/**/*.{ts,tsx,mdx}'],
  darkMode: 'class',

  theme: {
    extend: {
      // Semantic colors via CSS custom properties (enables dark mode via class)
      colors: {
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',
        primary: {
          DEFAULT: 'hsl(var(--primary))',
          foreground: 'hsl(var(--primary-foreground))',
        },
        secondary: {
          DEFAULT: 'hsl(var(--secondary))',
          foreground: 'hsl(var(--secondary-foreground))',
        },
        destructive: {
          DEFAULT: 'hsl(var(--destructive))',
          foreground: 'hsl(var(--destructive-foreground))',
        },
        muted: {
          DEFAULT: 'hsl(var(--muted))',
          foreground: 'hsl(var(--muted-foreground))',
        },
        border: 'hsl(var(--border))',
        input: 'hsl(var(--input))',
        ring: 'hsl(var(--ring))',
      },

      // Semantic spacing tokens
      spacing: {
        section: '6rem',
        container: '80rem',
      },

      // Semantic radius tokens
      borderRadius: {
        card: '0.75rem',
        button: '0.5rem',
        input: '0.375rem',
      },

      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
    },
  },

  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
} satisfies Config;
