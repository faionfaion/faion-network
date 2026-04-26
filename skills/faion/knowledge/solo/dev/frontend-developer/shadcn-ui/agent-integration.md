# Agent Integration — shadcn/ui

## When to use
- React app on Tailwind that needs a stylable, accessible component baseline you can fork freely.
- You want Radix primitives' a11y wiring without committing to a closed component library.
- Design system in flux: copy-in components let agents diverge per project without npm dependency drift.
- Greenfield SaaS / dashboards where you control the design tokens via CSS variables.

## When NOT to use
- Non-React stacks (Vue, Svelte, vanilla) — community ports exist but lack agent-friendly tooling.
- You need vendor-supported components with SLAs (use MUI, Mantine, or Ant Design instead).
- Strict design system with no tolerance for upstream drift; copying creates many forks to maintain.
- Bundle-size paranoia at the byte level; CVA + class-variance-authority + tailwind-merge add overhead.

## Where it fails / limitations
- "Copy don't install" means upstream fixes (Radix bumps, a11y patches) do not flow to you automatically.
- The CLI generator overwrites local edits if `--overwrite` is used; agents that re-run setup wipe customizations.
- Tailwind + CSS variable theme means agents must keep `globals.css`, `tailwind.config.ts`, and `components.json` in sync — three sources of truth.
- Form integration assumes `react-hook-form` + `zod`; swapping validators breaks the generated `<Form>` types.
- Server Components: many shadcn components mark `"use client"`; agents adding them to RSC trees cause hydration mismatches.

## Agentic workflow
Use a two-phase loop: (1) discover-and-add — agent reads `components.json`, runs `npx shadcn@latest add <name>` with explicit list, then commits without editing; (2) compose — agent builds feature components in `components/<feature>/` that import only from `components/ui/`. Forbid agents from editing `components/ui/*` after the initial add; treat that directory as vendored. Whenever a Radix peer dep version drifts, kick a human review.

### Recommended subagents
- `faion-frontend-component-agent` — compose feature components on top of shadcn primitives with stories.
- `faion-storybook-agent` — generate stories for added primitives so visual regression catches Tailwind drift.
- `faion-sdd-executor-agent` — run `shadcn add`, lint, typecheck, write tests, gate PR.

### Prompt pattern
```
Task: add a Combobox to components/ui via shadcn CLI, then build SearchUserCombobox in components/users/.
Constraints: do not edit files under components/ui after generation. Use cn() from lib/utils. Keep all variants in cva().
Deliver: shell command(s), file diffs, one Storybook story, one Playwright a11y test.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `shadcn` (formerly `shadcn-ui`) | Add/update components | `npx shadcn@latest init`, `npx shadcn@latest add button` |
| `class-variance-authority` (cva) | Variant API | `npm i class-variance-authority` |
| `tailwind-merge` | Resolve Tailwind class conflicts in `cn()` | `npm i tailwind-merge` |
| `tailwindcss-animate` | Animation utilities used by primitives | `npm i tailwindcss-animate` |
| `@radix-ui/*` | Underlying headless primitives | autoinstalled per add |
| `lucide-react` | Default icon set | `npm i lucide-react` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| ui.shadcn.com | OSS docs site | Yes (stable URLs, deterministic snippets) | Source of truth for component code |
| v0.dev | SaaS (Vercel) | Yes (API + chat) | Generates shadcn-styled UIs from prompts; output drops straight into project |
| TweakCN | SaaS | Yes (config export) | Visual editor for shadcn theme tokens; exports `globals.css` |
| Chromatic | SaaS | Yes (CI integration) | Visual regression for Storybook; pairs well with shadcn forks |
| Radix UI | OSS | Yes | Upstream primitives; agents read changelog before bumping |

## Templates & scripts
See `templates.md` and `examples.md`. Useful guard script that fails CI if `components/ui/*` was hand-edited:

```bash
#!/usr/bin/env bash
# scripts/check-shadcn-pristine.sh
set -euo pipefail
DIRTY=$(git diff --name-only HEAD~1 HEAD -- 'components/ui/*' || true)
ALLOW_FILE='.shadcn-allow'
if [[ -n "$DIRTY" ]]; then
  if [[ ! -f "$ALLOW_FILE" ]]; then
    echo "Edits inside components/ui/ require explicit allowlist:"
    echo "$DIRTY"
    exit 1
  fi
  while IFS= read -r f; do
    grep -qxF "$f" "$ALLOW_FILE" || { echo "Unapproved edit: $f"; exit 1; }
  done <<< "$DIRTY"
fi
echo "shadcn primitives untouched (or all edits approved)."
```

## Best practices
- Treat `components/ui/` as vendored; commit changes only via `shadcn add`. Wrap, do not edit.
- Centralize tokens in CSS variables (`--background`, `--primary`, etc.) so theming is one file, not class rewrites.
- Use cva() for variants; do not pass long Tailwind strings as props (loses tree-shaking and consistency).
- Prefix custom components by feature (`components/billing/PlanCard.tsx`), never dump into `ui/`.
- Pin shadcn CLI and Radix versions in lockfile; bump in a dedicated PR with visual regression diff.
- Run `npx shadcn@latest diff` before bumping to read what will change.

## AI-agent gotchas
- LLMs frequently rewrite `components/ui/button.tsx` to "improve" it; lock the directory in CODEOWNERS or a CI guard.
- Agents miss `"use client"` directive when porting components to Next.js App Router; results in cryptic "ReactCurrentDispatcher" errors.
- Tailwind class conflicts (e.g. `p-2 p-4`) silently pick the wrong one without `cn()` + `tailwind-merge`. Force agents to import `cn` from `lib/utils`.
- The CLI changed package name from `shadcn-ui` to `shadcn`; older training data uses the deprecated name. Pin in docs the agent reads.
- `components.json` aliases (`@/components`, `@/lib/utils`) must match `tsconfig.json` paths — agents that scaffold a new project often skip the tsconfig update.
- Theming via CSS variables uses HSL channel triplets (`--primary: 221 83% 53%`). Agents writing hex values into `globals.css` break the alpha helpers.

## References
- https://ui.shadcn.com/
- https://www.radix-ui.com/primitives
- https://cva.style/docs
- https://github.com/dcastil/tailwind-merge
- https://v0.dev/
