---
name: design-tokens-minimal
description: Create a single tokens.css with CSS custom properties for colors, typography, spacing, and radius — then apply them across your product via var().
tier: solo
group: ui-design
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a single `tokens.css` file defining 8 colors (3 brand, 2 grays, success/warning/error), 4 font sizes, 4 spacing steps, and 1 border-radius as CSS custom properties. Every component in your project will reference them via `var(--color-primary)` and similar, so one edit in `tokens.css` propagates your entire UI.

## Prerequisites

- A web project (any stack: plain HTML, React, Vue, Gatsby, Next.js — anything that loads CSS).
- A text editor and a browser with DevTools.
- No design tool required. No build step required.
- A rough brand color in mind (a hex value or a direction like "deep navy").

## Steps

1. Create `src/styles/tokens.css` (or `static/tokens.css` for a plain HTML project) with the following content — replace the three brand hex values with your own:

```css
/* ============================================================
   Design tokens — single source of truth
   Edit here; everything else uses var(--token-name).
   ============================================================ */

:root {
  /* --- Brand colors (3) --- */
  --color-primary:        #1a56db;   /* main CTA, links, focus rings */
  --color-primary-dark:   #1341a8;   /* hover state of primary */
  --color-accent:         #f97316;   /* highlights, badges, secondary CTA */

  /* --- Grays (2) --- */
  --color-surface:        #f8fafc;   /* page background, card background */
  --color-text:           #1e293b;   /* body copy, headings */

  /* --- Semantic status (3) --- */
  --color-success:        #16a34a;
  --color-warning:        #d97706;
  --color-error:          #dc2626;

  /* --- Font sizes (4-step type scale) --- */
  --font-size-sm:         0.875rem;  /* 14px @ 16px root */
  --font-size-base:       1rem;      /* 16px — body copy */
  --font-size-lg:         1.25rem;   /* 20px — subheadings */
  --font-size-xl:         1.75rem;   /* 28px — page headings */

  /* --- Spacing (4-step scale, base-4 grid) --- */
  --space-1:              0.25rem;   /* 4px  — icon gap, tight padding */
  --space-2:              0.5rem;    /* 8px  — inline elements */
  --space-4:              1rem;      /* 16px — standard component padding */
  --space-8:              2rem;      /* 32px — section gaps */

  /* --- Border radius (1) --- */
  --radius:               0.375rem;  /* 6px — buttons, inputs, cards */
}
```

2. Import `tokens.css` before any other stylesheet. In plain HTML:

```html
<link rel="stylesheet" href="/static/tokens.css">
<link rel="stylesheet" href="/static/main.css">
```

In a React/Next.js project, add to `src/app/layout.tsx` or `pages/_app.tsx`:

```ts
import '../styles/tokens.css';
```

In Gatsby, add to `gatsby-browser.js`:

```js
import './src/styles/tokens.css';
```

3. Replace every hardcoded color, size, and spacing value in your existing CSS with the matching token. Example migration:

```css
/* Before */
.btn-primary {
  background: #1a56db;
  padding: 8px 16px;
  font-size: 16px;
  border-radius: 6px;
}

/* After */
.btn-primary {
  background: var(--color-primary);
  padding: var(--space-2) var(--space-4);
  font-size: var(--font-size-base);
  border-radius: var(--radius);
}
```

4. Apply status colors to feedback elements:

```css
.alert-success { color: var(--color-success); border-color: var(--color-success); }
.alert-warning { color: var(--color-warning); border-color: var(--color-warning); }
.alert-error   { color: var(--color-error);   border-color: var(--color-error);   }
```

5. Set base typography on `body` using tokens:

```css
body {
  background-color: var(--color-surface);
  color: var(--color-text);
  font-size: var(--font-size-base);
}

h1, h2 { font-size: var(--font-size-xl); }
h3, h4 { font-size: var(--font-size-lg); }
small   { font-size: var(--font-size-sm); }
```

6. Test a brand color change: open `tokens.css`, change `--color-primary` to `#7c3aed` (purple), save, and hard-refresh. Every button, link, and focus ring should update instantly without touching any other file.

7. Revert the test change and commit `tokens.css` to version control.

## Verify

Open DevTools → Elements → select `<html>` → Computed → filter by `--color`. You should see all 8 `--color-*` variables listed. Then run:

```
grep -r "var(--color-primary)" src/ | wc -l
```

A count > 0 confirms the token is actually used. If the count is 0, you haven't migrated any usages yet — go back to Step 3.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Tokens defined in `:root` but not applying | `tokens.css` imported after a stylesheet that overrides the property | Move the `tokens.css` `<link>` or `import` to the top of your stylesheet chain |
| `var(--color-primary)` renders as an empty value (transparent/black) | Typo in the variable name — CSS silently falls back to initial value | Open DevTools → Elements → filter Computed styles by `--color`; confirm the exact spelling; CSS variable names are case-sensitive |
| Dark mode breaks after adding tokens | Tokens use single light-mode values with no dark override | Add a `@media (prefers-color-scheme: dark) { :root { ... } }` block at the bottom of `tokens.css` overriding color tokens for dark backgrounds |
| Token file loads but changes don't propagate in Next.js dev | Next.js fast-refresh doesn't always invalidate global CSS | Full browser refresh (Cmd/Ctrl + Shift + R) forces recompile |

## Next

- Add a `@media (prefers-color-scheme: dark)` block to `tokens.css` to implement dark mode by overriding only the 8 color tokens — no duplicate component CSS needed.
- Promote to a three-tier hierarchy (global → semantic → component) when your project has >3 components sharing token overrides; see the `design-tokens-fundamentals` methodology.
- Extract tokens to a design tool (Figma Tokens or Style Dictionary) once you have a team that edits in Figma.

## References

- [knowledge/solo/ux/ui-designer/design-tokens-fundamentals](../../../knowledge/solo/ux/ui-designer/design-tokens-fundamentals) — single-source-of-truth token hierarchy that backs Step 6: one edit in `:root` propagates everywhere because semantic tokens alias global values, not raw hex.
