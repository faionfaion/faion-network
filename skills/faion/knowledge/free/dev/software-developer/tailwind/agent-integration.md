# Agent Integration — Tailwind CSS

## When to use
- Greenfield React / Vue / Svelte / Astro / Next.js projects where utility-first + JIT bundle savings matter.
- Design systems that need a single source of tokens — `tailwind.config.ts` `theme.extend` is the canonical place.
- Component libraries built on shadcn/ui / Radix / Headless UI — Tailwind is the assumed styling layer.
- LLM-driven UI work — agents pattern-match Tailwind utilities reliably and bundle output is predictable.
- Email templates with `tailwindcss-mail` / `react-email` — utility-first translates well to inline-styled HTML emails.

## When NOT to use
- Apps with strong server-rendered CSS architecture (Rails Asset Pipeline + Sass mixins, Phoenix LiveView component lib) where introducing Tailwind doubles CSS strategy.
- Designer-led codebases where designers write CSS-in-Figma → developer ports to Sass. Tailwind requires designer fluency in tokens.
- Highly dynamic class strings — `bg-${color}-500` defeats JIT purge. CSS Modules are simpler for this.
- Print stylesheets — Tailwind's print variants exist (`print:`) but a dedicated `print.css` is cleaner.
- Constraint-driven CSS (`grid-template-areas`, container queries pre-Tailwind v3.4) — vanilla CSS is more readable.

## Where it fails / limitations
- **Class string explosion.** Components grow to 80+ utilities; readability craters. Use CVA / `tailwind-variants` to encapsulate.
- **Specificity wars when mixing with library CSS.** Bootstrap remnants override Tailwind utilities. `important: true` is a sledgehammer; prefer scoping `prefix: 'tw-'` instead.
- **JIT purge false negatives.** Dynamically constructed classes (`\`bg-${variant}-500\``) get purged. Add to `safelist` or precompute full strings.
- **Tailwind v4 migration churn.** v4 (released 2024-12) removes `tailwind.config.js` in favor of CSS-first config; existing tutorials lag. Pin v3.x or fully migrate; don't half-step.
- **Arbitrary values everywhere.** `w-[37.5px]` for one-off measurements bypasses the design system. Cap usage to a budget; refactor common arbitrary values into theme tokens.
- **Dark mode + class strategy + SSR.** Without script-in-head theme detection, light-to-dark FOUC. Use `next-themes` + `class` strategy; agents skip the script.
- **`@apply` overuse.** "Extracting" patterns to `@apply` defeats JIT and recreates Sass partials. Always prefer component composition.
- **Plugin churn.** `@tailwindcss/forms`, `typography`, `aspect-ratio` add scoped resets that surprise debuggers. Audit conflicts when adopting.
- **Container queries before v3.2** require plugin; agents reach for media queries reflexively.
- **Tooling coupling.** PostCSS + autoprefixer + Tailwind requires careful build order. Vite, Next.js, Astro abstract; bare `npx tailwindcss` does not.

## Agentic workflow
Drive Tailwind work in 4 stages: (1) a **token-curator** subagent reviews `tailwind.config.ts` `theme.extend` for brand colors, spacing, typography — adds before any utility class is written; (2) a **utility-author** subagent writes JSX with utilities in concentric order (layout → box → border → bg → typography → effects), keeping arbitrary values <5% of total; (3) a **cn-discipline** subagent flags raw template-literal class joins and auto-converts to `cn()` (`clsx` + `tailwind-merge`); (4) a **bundle-audit** subagent runs production build and reports CSS size + top utility hot spots; flags safelist gaps. Always run `prettier --check` (with `prettier-plugin-tailwindcss`) and `eslint` (`eslint-plugin-tailwindcss`) before commit; LLMs commonly emit unsorted class lists.

### Recommended subagents
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — quality gate runs `pnpm lint && pnpm build && pnpm test`.
- A purpose-built **tailwind-token-agent** (worth creating): proposes `theme.extend` additions when a magic color/spacing recurs ≥3 times in JSX.
- A **class-sort-agent** (worth creating): wraps `prettier-plugin-tailwindcss` and reports/auto-fixes ordering.
- A **safelist-agent** (worth creating): scans for dynamic class construction patterns; emits a `safelist` config.
- A **css-budget-agent** (worth creating): builds prod CSS, asserts <50KB gzipped; alerts on regressions.
- An **a11y-contrast-agent** (worth creating): checks `text-foreground` vs `bg-card` resolved colors meet WCAG AA.
- `password-scrubber-agent` (`agents/password-scrubber-agent.md`) — catch any committed `.env` for build tooling.

### Prompt pattern
Component authoring:
```
Generate components/PriceCard.tsx using Tailwind v3.4.
Layout: card with header / body / footer. Hover: subtle lift.
Variants: default, popular (highlighted border).
Rules:
- Use cn() from @/lib/utils for class joins (no template literals)
- Colors only via theme tokens (bg-card, text-foreground, etc.)
- No arbitrary values > 1
- prettier-plugin-tailwindcss-compatible class order
- Provide compound prop type: { variant?: 'default' | 'popular' }
- Storybook story with both variants
```

Token extraction:
```
Audit components/**/*.tsx for repeated literal colors, spacings,
or font sizes. Output:
- token name (snake_case): value
- occurrence count
- proposed tailwind.config.ts theme.extend diff
Only propose tokens with ≥3 occurrences.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `tailwindcss` | Core JIT engine | https://tailwindcss.com/docs |
| `@tailwindcss/forms` | Form reset plugin | https://github.com/tailwindlabs/tailwindcss-forms |
| `@tailwindcss/typography` | Prose styling for markdown | https://tailwindcss.com/docs/typography-plugin |
| `@tailwindcss/aspect-ratio` | Aspect ratio plugin (pre-v3.2) | https://github.com/tailwindlabs/tailwindcss-aspect-ratio |
| `@tailwindcss/container-queries` | `@container` queries plugin | https://github.com/tailwindlabs/tailwindcss-container-queries |
| `prettier-plugin-tailwindcss` | Auto-sort class order | https://github.com/tailwindlabs/prettier-plugin-tailwindcss |
| `eslint-plugin-tailwindcss` | Lint unused/duplicated classes | https://github.com/francoismassart/eslint-plugin-tailwindcss |
| `tailwind-merge` | Resolve conflicting utilities | https://github.com/dcastil/tailwind-merge |
| `clsx` | Conditional joiner | https://github.com/lukeed/clsx |
| `cva` (class-variance-authority) | Variant API | https://cva.style |
| `tailwind-variants` (tw-variants) | Alt to CVA with slot support | https://www.tailwind-variants.org |
| `autoprefixer` | PostCSS prefixer (pair with Tailwind) | https://github.com/postcss/autoprefixer |
| `cssnano` | CSS minifier in build | https://cssnano.co |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Tailwind Play | SaaS | yes (URL share) | Quick prototyping; agents can paste output for validation. |
| Tailwind UI | SaaS (paid) | partial | Premium component snippets; license-restricted. |
| shadcn/ui registry | OSS | yes | Tailwind + Radix primitives; `npx shadcn add`. |
| HyperUI | OSS | yes | Free Tailwind component library. |
| Headless UI | OSS | yes | Tailwind Labs' unstyled accessible components. |
| daisyUI | OSS | yes | Component-class library on top of Tailwind. |
| Flowbite | SaaS / OSS | yes | Tailwind component lib + Pro tier. |
| Vercel / Netlify / Cloudflare Pages | SaaS | yes | Auto-builds Next.js + Tailwind. |
| Storybook + Tailwind | OSS | yes | Pair for component sandboxing. |

## Templates & scripts
See `templates.md` and `examples.md` for `tailwind.config.ts`, `cn()` setup, CVA patterns. Add a CSS budget gate (≤50 lines):

```bash
#!/usr/bin/env bash
# tailwind-css-budget.sh — fail build if prod CSS exceeds budget.
# Usage: tailwind-css-budget.sh DIST_DIR MAX_KB
set -euo pipefail
DIST="${1:?dist dir required}"
MAX_KB="${2:-50}"
shopt -s globstar
TOTAL=0
declare -a FILES
for f in "$DIST"/**/*.css; do
  [ -f "$f" ] || continue
  GZ=$(gzip -c "$f" | wc -c)
  KB=$(( (GZ + 1023) / 1024 ))
  TOTAL=$((TOTAL + KB))
  FILES+=("$KB KB  $f")
done
printf '%s\n' "${FILES[@]}"
echo "TOTAL: $TOTAL KB gzipped (budget: $MAX_KB KB)"
if (( TOTAL > MAX_KB )); then
  echo "FAIL — over budget by $((TOTAL - MAX_KB)) KB"
  echo "Investigate: rg -tcss '@apply' src/ ; rg --no-heading 'safelist' tailwind.config.*"
  exit 1
fi
echo "OK"
```

Wire after `pnpm build` in CI.

## Best practices
- **Concentric class order.** Layout → box → border → bg → typography → effects. Agents emit clean code with this rule.
- **`prettier-plugin-tailwindcss` enforces order.** Stop debating; format settles it.
- **`cn()` everywhere.** Forbid template-literal class joins via lint rule.
- **Theme tokens beat arbitrary values.** Cap arbitrary usage to a documented budget.
- **CVA / tw-variants for variant props.** Centralizes class strings; agents extend cleanly.
- **Dark mode via `class` strategy + `next-themes`** (or framework equivalent). Light-only baselines, `dark:` opt-in for tokens.
- **Container queries** for component-level breakpoints (Tailwind v3.2+) over global media queries.
- **Safelist sparingly.** Static class strings are best; safelist only when truly dynamic.
- **PurgeCSS via Tailwind's content** correctly globbed. Symptom: classes work in dev, vanish in prod → content path missing.
- **Avoid `@apply` for component patterns.** Compose components instead. `@apply` only inside library-level base styles or third-party reset overrides.
- **Pin Tailwind major version.** v3 → v4 is breaking; both can coexist briefly via aliases but lock a single version per app.

## AI-agent gotchas
- **Hallucinated utilities.** `text-3.5xl`, `bg-primary-500/0.6` (wrong opacity syntax). Real syntax: `bg-primary-500/60` or `bg-primary-500/[0.6]`. Force build to fail-fast on unknown classes.
- **Dynamic class strings.** `bg-${color}-500` purged in prod. Symptom: works in dev. Add `safelist` or build full strings server-side.
- **`@apply` reflex.** LLM extracts patterns to `@apply` "for cleanliness"; performance + maintenance regression. Reject in review.
- **Mixing arbitrary + token.** `text-[14px] text-base` — `tailwind-merge` resolves but agents can't predict. Pick one consistently.
- **Forgetting `.dark` variants.** Component looks correct in light, broken in dark mode. Pair every color utility with `dark:` if not using semantic tokens.
- **Conflicting plugins.** `@tailwindcss/forms` resets `<input>`; team's custom reset doubles up. Order matters in `plugins` array.
- **`important: true` to "fix" specificity.** Wins the war, loses the maintenance battle. Refactor source of conflict instead.
- **Class string lint vs runtime.** ESLint passes but JIT purges in prod. Use `tailwindcss-language-server` in editor to catch dead utilities live.
- **`group-hover:` / `peer-hover:` misuse.** Agent forgets to add `group` / `peer` class on parent; effect silently does nothing.
- **Container query plugin missing.** Agent writes `@container md:flex-row`; class purged or unrecognized. Install plugin or use CSS `@container` directly.
- **Tailwind v4 syntax in v3 codebase.** `@theme` blocks, CSS-first config — agent copies from new docs into v3 project; build breaks. Always check installed version.
- **`tailwind-merge` not configured for custom utilities.** Custom `text-display-2xl` has no group; merge can't dedupe; both classes ship. Configure `extendTailwindMerge`.
- **Inline styles for one-offs.** Agent uses `style={{ marginTop: 13 }}` for an off-token margin. Token it (`mt-[13px]` or extend theme) — keep all styling in one layer.
- **Storybook missing globals.** Component looks unstyled in Storybook; agent debugs JSX instead of `.storybook/preview.ts` import of `globals.css`.

## References
- Tailwind CSS docs: https://tailwindcss.com/docs
- Tailwind v4 announcement: https://tailwindcss.com/blog/tailwindcss-v4
- prettier-plugin-tailwindcss: https://github.com/tailwindlabs/prettier-plugin-tailwindcss
- tailwind-merge: https://github.com/dcastil/tailwind-merge
- CVA: https://cva.style/docs
- tailwind-variants: https://www.tailwind-variants.org
- shadcn/ui: https://ui.shadcn.com
- Tailwind Labs blog: https://tailwindcss.com/blog
- Adam Wathan — "Reusing Styles": https://tailwindcss.com/docs/reusing-styles
- Sibling methodologies: `free/dev/software-developer/shadcn-ui/`, `free/dev/software-developer/css-in-js/`, `free/dev/software-developer/storybook-setup/`.
