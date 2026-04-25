# Agent Integration — shadcn/ui

## When to use
- New React/Next.js apps that need design-system primitives without locking into a third-party library version. Code is copied into the codebase, owned by the team.
- Internal tools / dashboards where Tailwind + Radix Primitives + CVA is already the stack.
- LLM-driven UI work — components are local TypeScript files agents can edit, not opaque npm packages they cannot reshape.
- Branding-heavy products where design tokens (`globals.css` CSS vars) need full control.
- Migration off Material UI / Chakra UI / Mantine where vendor lock-in or bundle size hurts.

## When NOT to use
- Apps that need a fully maintained, versioned component package — shadcn intentionally is not a package. You own bug fixes.
- Non-React stacks (Vue, Svelte, Angular). Use respective ports (`shadcn-vue`, `shadcn-svelte`) — same philosophy, different repo.
- Mobile-first React Native — shadcn assumes web DOM + Tailwind.
- Fast prototyping where you want zero design — fully designed kits (Mantine, Material) ship faster.
- Teams without Tailwind discipline — shadcn requires Tailwind config + `cn()` utility + understanding of CVA. Onboarding cost.

## Where it fails / limitations
- **Component drift across copies.** Agents add a Button to project A, project B; project B never gets bugfixes from upstream. Pin a "shadcn version" in `components.json`; run `npx shadcn diff` weekly.
- **CVA variant explosion.** New variants accumulate; `buttonVariants` becomes 200 lines with conflicting compound variants. Refactor to nested CVAs or split into `<IconButton>` etc.
- **`cn()` precedence surprises.** `cn("p-4", className)` with `className="p-2"` — `tailwind-merge` resolves to `p-2`, but only for known utility groups. Custom utilities or arbitrary values bypass merge.
- **Radix Primitives API churn.** Major Radix bumps require manual port across all your `ui/*` files. Agents miss subtle prop renames.
- **Dark mode flash.** Without `next-themes` + `suppressHydrationWarning` + script-in-head, SSR renders light, client switches dark → FOUC. Agents skip the `<ThemeProvider>` wrap.
- **Form integration.** shadcn `Form` ties to `react-hook-form` + `zod`. Agents drop one and the typing breaks.
- **Server Components.** Many shadcn primitives use `useState` / `useRef` → `'use client'` everywhere. Agents add `'use client'` to entire pages instead of leaf components, defeating RSC.
- **Accessibility regressions.** Forking a Radix-based primitive and adding custom logic often drops focus management. ARIA tests catch this; agents need an a11y gate.

## Agentic workflow
Drive shadcn work in 4 stages: (1) a **token-curator** subagent reviews `globals.css` CSS variables and `tailwind.config.ts` to ensure brand tokens (HSL ranges, radii, spacing) are defined before any component is added; (2) an **add-component** subagent runs `npx shadcn@latest add <name>` and audits the generated file against project lint rules; (3) a **composer** subagent builds feature components in `components/<feature>/` using shadcn primitives + CVA, never inline arbitrary Tailwind; (4) an **a11y-checker** subagent runs `axe-core` against Storybook stories or Playwright E2E to catch focus/ARIA regressions. Always commit `components.json` + `lib/utils.ts` (with `cn()`) early; agents adding components without those error out cryptically.

### Recommended subagents
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — quality gate runs `tsc --noEmit && eslint . && next build` after UI changes.
- A purpose-built **shadcn-add-agent** (worth creating): given a Figma frame or component description, picks the closest shadcn primitive(s), runs `npx shadcn add`, and emits the composed feature component.
- A **cva-refactor-agent** (worth creating): when a `*Variants` block exceeds 100 lines, proposes split into compound variants or sub-components.
- A **shadcn-diff-agent** (worth creating): runs `npx shadcn diff` and surfaces upstream patches the team hasn't applied.
- An **a11y-axe-agent** (worth creating): runs `axe-playwright` or `@storybook/addon-a11y` and reports violations + fix proposals (often `aria-label`, `role`, `tabIndex`).
- `password-scrubber-agent` (`agents/password-scrubber-agent.md`) — scrub any `.env`, MSW handlers, or Storybook fixtures before commit.

### Prompt pattern
Add + compose:
```
You are a Next.js 14 + shadcn/ui engineer.
1. Run: npx shadcn@latest add dialog form input button label
2. Generate components/users/CreateUserDialog.tsx using:
   - Dialog (shadcn/ui)
   - Form + zodResolver(createUserSchema)
   - Inputs: email (type=email, required), name (required)
   - Submit Button with loading state (disabled + Spinner)
3. Use cn() from @/lib/utils for classNames.
4. Add 'use client' only to this file (parent stays RSC).
5. Run: pnpm typecheck && pnpm lint
```

CVA refactor:
```
Audit components/ui/button.tsx::buttonVariants. If >100 lines or
>3 compound variants, split into:
- buttonVariants (base)
- iconButtonVariants (icon-only sizes)
Update consumer call sites in /app and /components.
Verify Storybook stories still render.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `npx shadcn@latest` | Add/diff components, init project | https://ui.shadcn.com |
| `class-variance-authority` (cva) | Variant API | https://cva.style |
| `tailwind-merge` | Resolve Tailwind class conflicts | https://github.com/dcastil/tailwind-merge |
| `clsx` | Conditional class joiner | https://github.com/lukeed/clsx |
| `tailwindcss` | Atomic CSS engine | https://tailwindcss.com |
| `prettier-plugin-tailwindcss` | Auto-sort classes | https://github.com/tailwindlabs/prettier-plugin-tailwindcss |
| `eslint-plugin-tailwindcss` | Lint class order, unused | https://github.com/francoismassart/eslint-plugin-tailwindcss |
| `@axe-core/playwright` | A11y in E2E | https://github.com/dequelabs/axe-core-npm |
| `@storybook/react` | Component sandbox | https://storybook.js.org |
| `storybook-addon-a11y` | A11y in Storybook | https://storybook.js.org/addons |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| shadcn registry | OSS | yes (CLI) | `npx shadcn add` reads JSON registry; supports private registries via `components.json`. |
| v0.dev | SaaS | yes (web + API) | Vercel's Generative UI; emits shadcn-compatible components. |
| Storybook | OSS | yes | Catalog UI; agent-readable stories. |
| Chromatic | SaaS | yes | Visual regression on Storybook stories. |
| Percy | SaaS | yes | Visual diffs for shadcn components in app context. |
| Figma → shadcn (community plugins) | SaaS | partial | Some plugins emit JSX; mileage varies. |
| Vercel | SaaS | yes | Hosts Next.js + shadcn natively. |
| Tailwind Play | SaaS | yes (URL share) | Quick prototyping; agent can paste class strings to validate. |

## Templates & scripts
See `templates.md` and `examples.md` for `components.json`, theming, `cn()` patterns. Add a "drift detector" (≤50 lines):

```bash
#!/usr/bin/env bash
# shadcn-drift-check.sh — warn on local diffs vs upstream registry.
# Usage: shadcn-drift-check.sh [components/ui/*.tsx ...]
set -euo pipefail
ROOT="${ROOT:-components/ui}"
DRIFT=0
mkdir -p .shadcn-drift && cd .shadcn-drift
for f in "$@"; do
  name="$(basename "$f" .tsx)"
  pristine=".pristine-$name.tsx"
  npx --yes shadcn@latest add "$name" --yes --overwrite \
       --cwd ../.shadcn-drift-tmp >/dev/null 2>&1 || continue
  cp "../.shadcn-drift-tmp/$ROOT/$name.tsx" "$pristine"
  if ! diff -q "../$f" "$pristine" >/dev/null; then
    echo "drift: $f"
    diff -u "$pristine" "../$f" | head -40
    DRIFT=$((DRIFT + 1))
  fi
done
rm -rf ../.shadcn-drift-tmp
[ "$DRIFT" -eq 0 ] && echo "OK — no drift" || { echo "drift in $DRIFT files"; exit 1; }
```

Run weekly in CI to surface upstream fixes.

## Best practices
- **Treat `components/ui/*` as vendored code.** Review via PR; don't edit on autopilot. Each edit is a deliberate fork point.
- **One CSS-variable theme in `globals.css`.** Light + dark + brand. Never hardcode colors in component files.
- **Composition over `@apply`.** Build feature components from primitives; never `@apply` to extract patterns (defeats Tailwind's JIT advantages).
- **`cn()` as the only class merger.** Forbid `className={\`${a} ${b}\`}` via lint rule.
- **CVA with `compoundVariants` for cross-cutting states.** Hover + disabled + variant=destructive → one compound rule, not 12 base classes.
- **Server Components by default.** Add `'use client'` only on leaf components that need state. Most data fetching stays server-side.
- **Forms via `react-hook-form` + `zod`.** shadcn `Form` wraps both; don't bypass.
- **Storybook every primitive + every variant.** Drives Chromatic + a11y addon coverage.
- **Pin shadcn CLI version** in `package.json` `devDependencies` to avoid surprise output formatting changes mid-team.
- **`tailwind-merge` config matches Tailwind config.** Custom utility groups (e.g., a `text-display-2xl`) need explicit config in `extendTailwindMerge`; otherwise `cn()` lets duplicates through.

## AI-agent gotchas
- **Hallucinated imports.** LLMs import `@shadcn/ui/button` (npm-style) instead of `@/components/ui/button`. There is no npm package. Force prompt to use the local alias.
- **Inline styles instead of variants.** Agent writes `<Button className="bg-red-500">` instead of `variant="destructive"`. Reduces theme cohesion.
- **`'use client'` over-application.** Agent slaps `'use client'` on a server-only page just to use `<Button>`. Move client logic to a leaf component.
- **Forgetting `forwardRef`.** Removing `React.forwardRef` from a primitive breaks Radix's `asChild` composition. Subtle bug; only surfaces with portals.
- **`asChild` misuse.** Agent uses `<Button asChild><a /></Button>` and adds `onClick` to the Button — handler dropped because asChild merges children. Put handler on the child.
- **Theme tokens as strings.** Hardcoding `#1e3a8a` in JSX bypasses dark-mode tokens. Surface as `text-foreground` / `bg-card` etc.
- **Variant prop type drift.** Adding a new variant in CVA but not in component props type. TypeScript happy, runtime crash on consumer pass-through.
- **Mixed `clsx` + `cn`.** Agent imports both; redundant. Pick `cn` everywhere.
- **`ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement>`** lost when refactoring; spread `{...props}` no longer accepts `disabled`. TS error obscure.
- **Dialog accessibility.** Forgetting `<DialogTitle>` (visually hidden if needed via `<VisuallyHidden>` from Radix). Agent skip. Screen reader silent.
- **Tailwind safelist gaps.** Dynamic class strings (`bg-${color}-500`) get purged. Either add to `safelist` in tailwind.config or precompute the full class string in code.
- **Radix `Popover`/`Tooltip` portal mounted outside theme provider** — dark mode tokens unset. Wrap portal target with theme class.
- **Storybook doesn't load globals.** Agent forgets `import '@/styles/globals.css'` in `.storybook/preview.ts`; primitives render unstyled.
- **`shadcn add` overwriting local edits.** Agent re-runs `add button` and clobbers the team's customizations. Use `--yes` only with version control + diff review; `npx shadcn diff` first.

## References
- shadcn/ui docs: https://ui.shadcn.com/docs
- shadcn registry: https://ui.shadcn.com/docs/components
- CVA docs: https://cva.style/docs
- Radix Primitives: https://www.radix-ui.com/primitives
- Tailwind CSS: https://tailwindcss.com/docs
- tailwind-merge: https://github.com/dcastil/tailwind-merge
- v0.dev: https://v0.dev
- Sibling methodologies: `free/dev/software-developer/tailwind/`, `free/dev/software-developer/storybook-setup/`, `free/dev/software-developer/css-in-js/`.
