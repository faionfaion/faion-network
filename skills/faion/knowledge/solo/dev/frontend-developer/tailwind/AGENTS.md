# Tailwind CSS

## Summary

Tailwind CSS is a utility-first framework configured via `tailwind.config.ts` (v3) or a CSS-first
`@theme` block (v4). Configure `content` globs explicitly to include all templates; theme tokens
(colors, spacing, radii) live in the config or `@theme`, never as hardcoded hex in components.
Use `prettier-plugin-tailwindcss` to canonicalize class order. `@apply` is allowed only in
`globals.css` for thin reset helpers (≤3 utilities) — abstractions belong in components.

## Why

Utility classes keep styling co-located with markup, eliminate dead CSS, and give agents a stable,
greppable styling surface. The JIT compiler ships only used classes. Canonical class order via
Prettier makes agent-generated diffs readable and conflict-free. Token-driven config enforces
design consistency without a separate CSS variable layer.

## When To Use

- Greenfield app or rewrite where you control HTML and want utility-first styling.
- Multi-developer or multi-agent project needing a stable, greppable styling surface.
- Fast iteration on visual design with token control via config.
- Pairing with React, Vue, Svelte, or HTMX where templating lives near markup.

## When NOT To Use

- Brownfield app with mature CSS-in-JS or BEM conventions — mixing causes specificity wars.
- Email templates, PDFs, or print-first surfaces (Tailwind's reset and JIT do not target these).
- Library/SDK shipping CSS — utility classes leak global resets onto consumer apps.
- Strict design system that bans "magic numbers" — utilities make ad-hoc spacing too easy.

## Content

| File | What's inside |
|------|---------------|
| `content/01-rules.xml` | Rules: explicit content glob, mobile-first breakpoints, no hex in components, @apply restrictions, v3 vs v4 config. |
| `content/02-patterns.xml` | Config examples, common layout patterns (container, card, stack, center), dark mode, plugin registration. |

## Templates

| File | Purpose |
|------|---------|
| `templates/tailwind.config.ts` | v3 config with extended colors, fontFamily, spacing, plugins. |
| `templates/globals-v4.css` | v4 CSS-first config with @theme block for brand tokens. |
| `templates/check-class-order.sh` | CI guard: Prettier + ESLint class-order check. |
