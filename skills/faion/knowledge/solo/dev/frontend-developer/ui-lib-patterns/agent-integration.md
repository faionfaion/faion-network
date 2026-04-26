# Agent Integration — UI Library Advanced Patterns

## When to use
- Designing compound components (Card, Tabs, Accordion) with shared context for an in-house UI library.
- Building accessible Modal/Dialog/Popover with portals, focus trap, ESC + overlay-click semantics.
- Producing a `Component.stories.tsx` for every primitive in a Storybook-backed library.
- Migrating a one-off React component into a reusable, themeable, typed library entry.

## When NOT to use
- One-off page UI that will never be reused — compound pattern adds context overhead with no payoff.
- Apps that already adopt Radix UI / React Aria primitives — wrap those instead of re-implementing dialog/menu/listbox semantics.
- Server Components-only trees: compound components rely on React context, which forces a `'use client'` boundary.

## Where it fails / limitations
- Compound components break tree-shaking when all sub-components are exported via `Object.assign`; bundlers can't drop unused parts.
- Modal `useEffect` body-scroll lock conflicts with iOS Safari (still scrolls under overlay) — needs `position: fixed` + scroll restoration shim.
- `createPortal` to `document.body` breaks SSR if the call is not gated by a mount check.
- Storybook autodocs miss prop tables when `react-docgen-typescript` can't resolve generic component types.

## Agentic workflow
Use Claude subagents to scaffold the entire 5-file methodology output (component, stories, tests, types, MDX docs) per primitive. Drive generation from a typed component spec (props table + variants + a11y requirements) so the agent has unambiguous input. Keep human review on every accessibility behavior (focus trap, aria-* wiring) — those are the load-bearing parts and the most common LLM regression points.

### Recommended subagents
- `faion-sdd-executor-agent` — wrap the "scaffold component → write stories → run a11y/visual tests → commit" loop with quality gates.
- `password-scrubber-agent` — only relevant before publishing examples that quote real `.env.local` API keys; safe to skip otherwise.

### Prompt pattern
- "Generate compound component for `<Tabs>` matching the Card pattern in `ui-lib-patterns/README.md`. Required sub-components: Root, List, Trigger, Panel. Use Radix UI primitives under the hood. Output `.tsx`, `.module.css`, `.stories.tsx`, `.test.tsx`."
- "Audit `Modal.tsx` against the WAI-ARIA Authoring Practices dialog pattern. Return a diff that fixes any gaps in focus trap, initial focus, return focus, and ESC handling."

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `npx storybook@latest init` | Bootstrap Storybook 8.x with framework auto-detect | https://storybook.js.org/docs |
| `npx shadcn-ui@latest add <comp>` | Drop battle-tested compound components into the repo, then customize | https://ui.shadcn.com |
| `pnpm dlx tsx scripts/gen-component.ts` | Custom scaffolder for the 5-file pattern | repo-local |
| `npx playwright test --grep @a11y` | Run @axe-core/playwright a11y suite against Storybook | https://playwright.dev |
| `npx chromatic --project-token=$CHROMATIC_TOKEN` | Visual regression on every story | https://www.chromatic.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Chromatic | SaaS | Yes (CLI + GH Action) | Visual regression + Storybook hosting; agent commits and reads PR-status checks. |
| Storybook | OSS | Yes | `storybook dev`, `storybook build` are scriptable; CSF stories are typed and easy for LLMs to write. |
| Radix UI | OSS | Yes | Accept Radix as compound-component primitives — agents only style + compose. |
| React Aria (Adobe) | OSS | Partial | Hooks-based; LLMs misuse `mergeProps`. Pin examples in prompts. |
| Figma → Tokens Studio | SaaS | Yes (REST + plugin export) | Sync design tokens into the lib; pair with `style-dictionary`. |

## Templates & scripts
See `templates.md` for the Card / Modal / Stories scaffolds. Minimal compound-component generator below.

```bash
#!/usr/bin/env bash
# scripts/gen-compound.sh <ComponentName> <SubComponents,Comma,Sep>
set -euo pipefail
NAME=$1; SUBS=${2:-Header,Content,Footer}
DIR="src/components/composite/$NAME"
mkdir -p "$DIR"
cat > "$DIR/$NAME.tsx" <<EOF
import { createContext, useContext, ReactNode } from 'react';
const Ctx = createContext<{} | null>(null);
function Root({ children }: { children: ReactNode }) {
  return <Ctx.Provider value={{}}><div data-component="$NAME">{children}</div></Ctx.Provider>;
}
EOF
IFS=',' read -ra PARTS <<< "$SUBS"
for P in "${PARTS[@]}"; do
  echo "function $P({ children }: { children: ReactNode }) { return <div>{children}</div>; }" >> "$DIR/$NAME.tsx"
done
echo "export const $NAME = Object.assign(Root, { $(IFS=,; echo "${PARTS[*]}") });" >> "$DIR/$NAME.tsx"
echo "Generated $DIR/$NAME.tsx"
```

## Best practices
- Export sub-components as named exports too, not only via `Object.assign`, so consumers can tree-shake.
- Throw a descriptive error from `useXContext()` when the hook is used outside the Provider — agents otherwise produce confusing nulls.
- Use `data-state="open|closed"` instead of conditional class strings — Radix-style state attributes simplify CSS and tests.
- For every primitive ship: component + stories + a11y test + visual test. No "component-only" PRs.
- Keep the compound API additive — never remove a sub-component without a deprecation cycle; downstream apps will pin the import shape.

## AI-agent gotchas
- LLMs frequently forget `'use client'` on compound components in Next.js App Router → silent SSR mismatch.
- Generated Modal code often skips `aria-modal="true"` or wires `aria-labelledby` to a non-existent id; require an a11y test that asserts both.
- Agents tend to inline raw color hex values; force them to read from `design-tokens-basics` semantic tokens.
- When asked to "make it dynamic", agents add `styled.div` inside the render body — block this in review (see `css-in-js-advanced` perf section).
- Storybook 8 deprecated `argTypesRegex` for actions in some setups; pin the Storybook version in the prompt or the generator emits stale config.

## References
- Radix UI Primitives — https://www.radix-ui.com/primitives
- shadcn/ui — https://ui.shadcn.com
- WAI-ARIA Authoring Practices, Dialog Pattern — https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/
- Kent C. Dodds, "Compound Components" — https://kentcdodds.com/blog/compound-components-with-react-hooks
- Storybook CSF 3 — https://storybook.js.org/docs/api/csf
