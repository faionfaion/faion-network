# Agent Integration — Tailwind Architecture

## When to use
- Greenfield React / Next.js / Vue / Svelte / Astro projects committing to utility-first CSS as the single styling layer for the lifetime of the codebase.
- Design-system codification: consolidating brand tokens (colors, spacing, type, radii) into `tailwind.config.ts` `theme.extend` plus CSS variables for runtime theming.
- shadcn/ui-based component libraries — Tailwind is the assumed substrate for Radix/Headless UI primitives.
- LLM-driven UI authoring — agents pattern-match Tailwind utilities reliably and produce predictable bundle output.
- Multi-package monorepos that need a shared `tailwind-config` package consumed by app, marketing site, email templates, and Storybook.

## When NOT to use
- Apps with established server-rendered CSS pipelines (Rails Asset Pipeline + Sass partials, Phoenix LiveView component libs) where bolting on Tailwind doubles the styling strategy.
- Print-heavy outputs (PDFs, invoices) — Tailwind's `print:` variants exist but a dedicated `print.css` is cleaner and easier to audit.
- Codebases where most styling is highly dynamic (`bg-${brandColor}-${shade}`) — JIT purge will silently delete classes; CSS Modules + CSS variables are simpler.
- Teams shipping a CSS-Modules / vanilla-extract migration in flight; mixing layers regresses bundle predictability.
- Tiny static sites where hand-written CSS (<2KB) beats the Tailwind toolchain overhead.

## Where it fails / limitations
- **Class-string explosion.** Components grow to 80+ utilities; readability craters. Mitigation: CVA / `tailwind-variants` for variant APIs and component extraction (NOT `@apply`).
- **JIT purge false negatives** on dynamically constructed class strings. Symptom: classes work in dev, vanish in prod. Mitigation: `safelist` regex or precompute full strings server-side.
- **Tailwind v4 (CSS-first config) vs v3 churn.** v4 removes `tailwind.config.js`; existing tutorials/agents lag. Pin a single major version per repo; do not half-step.
- **Arbitrary values everywhere.** `w-[37.5px]`, `bg-[#3b82f6]` bypass the design system. Cap usage to a documented budget and refactor recurrent values into theme tokens.
- **Specificity wars** when Tailwind ships alongside Bootstrap remnants or vendor CSS. `important: true` is a sledgehammer; prefer `prefix: 'tw-'` scoping.
- **Dark mode FOUC** with `class` strategy + SSR unless an inline head script reads `localStorage` / `prefers-color-scheme` before hydration. Use `next-themes` (Next.js) or framework equivalent.
- **`@apply` overuse** recreates Sass partials, undoes the utility-first contract, and inflates CSS. Reserve for true library-level base resets only.
- **`tailwind-merge` blind spots** with custom utilities — without `extendTailwindMerge` the merger cannot dedupe `text-display-2xl` vs `text-base`; both ship.
- **Plugin scoped resets** (`@tailwindcss/forms`, `@tailwindcss/typography`) silently override input/`prose` styling and surprise debuggers. Audit before adoption.

## Agentic workflow
Drive Tailwind architecture in five stages: (1) a **token-curator** subagent reviews `tailwind.config.ts` `theme.extend` and CSS variables before any utility lands; (2) a **utility-author** subagent emits JSX with concentric class order (layout → box → border → background → typography → effects), keeping arbitrary values <5% of total; (3) a **cn-discipline** subagent flags raw template-literal class joins and rewrites them with `cn()` (`clsx` + `tailwind-merge`); (4) a **bundle-audit** subagent runs the production build and reports CSS gzip size + top utility hot spots, flagging safelist gaps; (5) `faion-sdd-executor-agent` runs the standard `pnpm lint && pnpm build && pnpm test` quality gate. Always run `prettier --check` (with `prettier-plugin-tailwindcss`) and `eslint-plugin-tailwindcss` before commit; LLMs commonly emit unsorted class lists or hallucinated utilities like `text-3.5xl`.

### Recommended subagents
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — runs lint/build/test gates; rejects unknown Tailwind classes via build failure.
- A purpose-built **tailwind-token-agent** — proposes `theme.extend` additions when a literal color/spacing/font-size recurs ≥3 times across `src/**/*.{tsx,vue,svelte}`.
- A **class-sort-agent** — wraps `prettier-plugin-tailwindcss` and reports/auto-fixes ordering as a pre-commit hook.
- A **safelist-agent** — scans for dynamic class construction patterns (`` `bg-${x}-500` ``, `clsx(..., dynamic)`) and emits a `safelist` config block.
- A **css-budget-agent** — runs prod build, asserts `<50KB` gzipped CSS, alerts on regressions.
- An **a11y-contrast-agent** — resolves theme tokens (e.g. `text-foreground` over `bg-card`) and checks WCAG AA contrast.
- `password-scrubber-agent` (`agents/password-scrubber-agent.md`) — catches stray secrets in build configs / `.env.example`.

### Prompt pattern
Component authoring:
```
Generate components/PriceCard.tsx using Tailwind v3.4.
Layout: card with header / body / footer; hover: subtle lift.
Variants: default, popular (highlighted ring).
Rules:
- Use cn() from @/lib/utils for class joins (no template literals).
- Colors only via theme tokens (bg-card, text-foreground, ring-primary).
- No more than 1 arbitrary value across the whole component.
- prettier-plugin-tailwindcss-compatible class order.
- Compound prop type: { variant?: 'default' | 'popular' }.
- Provide Storybook story covering both variants in light + dark.
```

Token extraction:
```
Audit src/**/*.{tsx,vue} for repeated literal colors, spacings,
font sizes, radii. Output:
- token name (kebab-case): value
- occurrence count
- proposed tailwind.config.ts theme.extend diff
Only propose tokens with >= 3 occurrences.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `tailwindcss` | Core JIT engine | https://tailwindcss.com/docs |
| `@tailwindcss/forms` | Form reset plugin | https://github.com/tailwindlabs/tailwindcss-forms |
| `@tailwindcss/typography` | `prose` styling for markdown / CMS HTML | https://tailwindcss.com/docs/typography-plugin |
| `@tailwindcss/aspect-ratio` | Aspect-ratio plugin (pre-v3.2) | https://github.com/tailwindlabs/tailwindcss-aspect-ratio |
| `@tailwindcss/container-queries` | `@container` queries plugin | https://github.com/tailwindlabs/tailwindcss-container-queries |
| `prettier-plugin-tailwindcss` | Auto-sort class order | https://github.com/tailwindlabs/prettier-plugin-tailwindcss |
| `eslint-plugin-tailwindcss` | Lint duplicate / unknown / unsorted classes | https://github.com/francoismassart/eslint-plugin-tailwindcss |
| `tailwind-merge` | Resolve conflicting utilities at runtime | https://github.com/dcastil/tailwind-merge |
| `clsx` | Conditional class joiner | https://github.com/lukeed/clsx |
| `cva` (class-variance-authority) | Variant API for components | https://cva.style |
| `tailwind-variants` | Variants + slots alternative to CVA | https://www.tailwind-variants.org |
| `autoprefixer` | PostCSS prefixer (pair with Tailwind) | https://github.com/postcss/autoprefixer |
| `cssnano` | Minify final CSS | https://cssnano.co |
| `tailwindcss-language-server` | Editor IntelliSense, dead-class detection | https://github.com/tailwindlabs/tailwindcss-intellisense |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Tailwind Play | SaaS (free) | yes | Quick prototyping; agents can paste JSX + config and link a shareable URL. |
| Tailwind UI | SaaS (paid) | partial | Premium component snippets; license restricts redistribution by agents. |
| shadcn/ui registry | OSS | yes | `npx shadcn add` installs Tailwind + Radix primitives directly. |
| HyperUI / Flowbite / daisyUI | OSS / mixed | yes | Free/freemium Tailwind component libs; daisyUI ships pre-themed component classes. |
| Headless UI | OSS | yes | Tailwind Labs' unstyled accessible primitives. |
| Vercel / Netlify / Cloudflare Pages | SaaS | yes | Auto-build Tailwind through Next.js / Astro / Nuxt. |
| Storybook + Tailwind | OSS | yes | Pair for component sandboxing; requires `globals.css` import in `.storybook/preview.ts`. |

## Templates & scripts
See `templates.md` and `examples.md` for `tailwind.config.ts`, `cn()` setup, and CVA patterns. Wire this CSS-budget gate after `pnpm build` in CI:

```bash
#!/usr/bin/env bash
# tailwind-css-budget.sh — fail build if prod CSS exceeds budget.
# Usage: tailwind-css-budget.sh DIST_DIR MAX_KB
set -euo pipefail
DIST="${1:?dist dir required}"
MAX_KB="${2:-50}"
shopt -s globstar
TOTAL=0
declare -a ROWS
for f in "$DIST"/**/*.css; do
  [ -f "$f" ] || continue
  GZ=$(gzip -c "$f" | wc -c)
  KB=$(( (GZ + 1023) / 1024 ))
  TOTAL=$((TOTAL + KB))
  ROWS+=("$KB KB  $f")
done
printf '%s\n' "${ROWS[@]}"
echo "TOTAL: $TOTAL KB gzipped (budget: $MAX_KB KB)"
if (( TOTAL > MAX_KB )); then
  echo "FAIL — over budget by $((TOTAL - MAX_KB)) KB"
  echo "Investigate: rg -tcss '@apply' src/ ; rg --no-heading 'safelist' tailwind.config.*"
  exit 1
fi
echo "OK"
```

## Best practices
- **Concentric class order** (layout → box → border → bg → typography → effects). Agents emit consistent code with this rule and `prettier-plugin-tailwindcss` enforces it.
- **`cn()` everywhere** — forbid raw template-literal class joins via lint rule; prevents `tailwind-merge` skips.
- **Theme tokens beat arbitrary values.** Cap arbitrary usage to a documented budget; promote recurring literals into `theme.extend`.
- **CVA / tw-variants** centralize variant class strings — agents extend variants without sprawling JSX.
- **Dark mode via `class` strategy + framework theme manager** (e.g. `next-themes`) with semantic tokens (`bg-background`, `text-foreground`) over `dark:` opt-in everywhere.
- **Container queries** (Tailwind v3.2+) for component-level breakpoints over global media queries.
- **Safelist sparingly** — static class strings are best; safelist only when truly dynamic.
- **PurgeCSS via `content` glob correctness.** Symptom: classes work in dev, vanish in prod → `content` paths missing or globs wrong.
- **No `@apply` for component patterns.** Compose components instead. Reserve `@apply` for library base styles or third-party overrides.
- **Pin Tailwind major version.** v3 ↔ v4 is breaking; don't migrate piecemeal.
- **Shared `tailwind-config` package** in monorepos: app + Storybook + email templates consume the same tokens; one source of truth.

## AI-agent gotchas
- **Hallucinated utilities.** `text-3.5xl`, `bg-primary-500/0.6` (wrong opacity syntax). Real syntax: `bg-primary-500/60` or `bg-primary-500/[0.6]`. Force JIT to error on unknown classes.
- **Dynamic class strings.** `` `bg-${color}-500` `` purged in prod. Symptom: works in dev only. Add `safelist` or compute full strings.
- **`@apply` reflex.** LLMs extract patterns to `@apply` "for cleanliness"; reject in review.
- **Mixing arbitrary + token.** `text-[14px] text-base` — `tailwind-merge` resolves but agents can't predict the winner. Pick one consistently.
- **Forgetting `dark:` variants.** Component looks correct in light, broken in dark. Use semantic tokens (`bg-card`) instead of pairing every utility with `dark:`.
- **Conflicting plugins.** `@tailwindcss/forms` resets `<input>`; team's custom reset doubles up. Order matters in the `plugins` array.
- **`important: true` to "fix" specificity.** Wins the war, loses maintenance. Refactor the source of conflict or scope with `prefix:`.
- **`group-hover:` / `peer-hover:` misuse.** Agent forgets to add `group` / `peer` class on parent; effect silently does nothing.
- **Container query plugin missing.** Agent writes `@container md:flex-row`; class purged. Install `@tailwindcss/container-queries` or use raw CSS `@container`.
- **Tailwind v4 syntax in v3 codebase.** `@theme` blocks, CSS-first config — agent copies from new docs into v3 project; build breaks. Always check installed version.
- **`tailwind-merge` not configured for custom utilities.** Without `extendTailwindMerge`, custom token group merges fail; both classes ship.
- **Inline `style={{ marginTop: 13 }}` for off-token margins.** Token it (`mt-[13px]` or extend theme); keep all styling in one layer.
- **Storybook missing globals.** Component looks unstyled in Storybook — agent debugs JSX instead of `.storybook/preview.ts` `import './globals.css'`.

## References
- Tailwind CSS docs: https://tailwindcss.com/docs
- Tailwind v4 announcement: https://tailwindcss.com/blog/tailwindcss-v4
- prettier-plugin-tailwindcss: https://github.com/tailwindlabs/prettier-plugin-tailwindcss
- tailwind-merge: https://github.com/dcastil/tailwind-merge
- CVA: https://cva.style/docs
- tailwind-variants: https://www.tailwind-variants.org
- shadcn/ui: https://ui.shadcn.com
- Adam Wathan, "Reusing Styles": https://tailwindcss.com/docs/reusing-styles
- Sibling methodologies: `solo/dev/frontend-developer/tailwind-patterns/`, `free/dev/software-developer/shadcn-ui/`, `free/dev/software-developer/css-in-js/`.
