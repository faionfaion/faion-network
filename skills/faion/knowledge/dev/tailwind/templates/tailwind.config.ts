/*
 * purpose: Tokens (colors, spacing, typography) declared via theme.extend.
 * consumes: 01-core-rules.xml
 * produces: config
 * depends-on: content/01-core-rules.xml
 * token-budget-impact: small
 */

import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{ts,tsx}", "./.storybook/**/*.{ts,tsx}"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        primary: "var(--color-primary)",
        destructive: "var(--color-destructive)",
      },
      spacing: { "1": "4px", "2": "8px", "3": "12px", "4": "16px" },
    },
  },
};

export default config;
