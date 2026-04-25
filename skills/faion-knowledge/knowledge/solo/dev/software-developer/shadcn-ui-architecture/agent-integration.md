# Agent Integration — shadcn/ui Component Architecture

## When to use
- Bootstrapping a Tailwind + Radix-based design system where the team owns the component source instead of importing a versioned library.
- Solo/small teams that need to fork primitives (Button, Dialog, Form) and tweak variants without forking an upstream npm package.
- Projects that already use Next.js, Remix, Vite + React, or Astro with Tailwind v3/v4 and want a CVA-driven variant system.
- Building accessible primitives quickly when an agent can scaffold via the official CLI and then layer business compositions on top.

## When NOT to use
- Vue, Svelte, Solid, or framework-agnostic stacks — pick the framework-specific port (`shadcn-vue`, `shadcn-svelte`) instead of the React reference.
- Apps that require versioned, signed, audited UI dependencies (regulated environments) — copy-paste source obscures supply-chain provenance.
- Teams that want a closed black-box library with semver guarantees; shadcn is intentionally a starter, not a maintained dependency.
- Pure styling without Radix — if you don't need headless behavior (focus traps, roving tabindex), a CSS-only kit is lighter.

## Where it fails / limitations
- No automatic upgrades: when shadcn ships a fix you must re-run `add` and merge changes manually — agents must diff, not overwrite.
- Tailwind v3 ↔ v4 token migration is breaking; the registry switched from HSL CSS vars to OKLCH and `@theme` blocks, and old generators emit broken classes.
- CVA variants explode if the agent keeps adding `variant: "newcase"` instead of composing — leads to a junk-drawer Button with 12 variants.
- Dark mode and theme color drift: every copied component duplicates token references; renaming a token requires a global codemod.
- `asChild` + `forwardRef` interaction is easy to break when an agent adds wrapping divs; loses focus management and breaks Radix slots.

## Agentic workflow
Drive shadcn from a Claude subagent that owns three phases: (1) install primitives via `npx shadcn@latest add` based on a feature spec, (2) compose feature-level components in `components/<feature>/` referencing only `components/ui/*` primitives, (3) verify a11y + variant coverage against the checklist. Use the official `shadcn` MCP server so the agent can read the registry, list available components, and resolve dependencies before writing code. Keep `components/ui/*` in a protected glob — agents propose patches there as separate PRs, never silent edits.

### Recommended subagents
- `frontend-implementer` (Sonnet) — runs `shadcn add`, scaffolds compositions, wires CVA variants from a spec.
- `ui-reviewer` (Sonnet) — diffs new compositions against `templates.md` patterns, flags variant explosion and missing `forwardRef`/`displayName`.
- `a11y-auditor` (Haiku) — runs the accessibility checklist (semantic HTML, ARIA, keyboard, focus traps) on every new primitive composition.
- `tailwind-token-curator` (Haiku) — keeps `globals.css` CSS variables and `tailwind.config.*` tokens in sync; rejects hardcoded colors.

### Prompt pattern
```
Task: Add a confirmation dialog to <feature>.
Constraints:
- Use existing components/ui/dialog.tsx (do NOT modify).
- New file: components/<feature>/confirm-action-dialog.tsx.
- Compose Dialog + Button (variant="destructive") + Form.
- forwardRef + displayName required.
- All colors via design tokens (--destructive, --background); zero hex values.
Output: file content + 3-line variant-coverage note.
```

```
Task: Migrate Button.tsx from Tailwind v3 HSL tokens to v4 OKLCH @theme.
Use: shadcn registry diff at https://ui.shadcn.com/docs/tailwind-v4.
Verify: existing variants (default/destructive/outline/ghost) render identically in dark mode.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `shadcn` CLI | Init project, add components from registry | `npx shadcn@latest init` · https://ui.shadcn.com/docs/cli |
| `shadcn` MCP server | Lets agents query registry, list components, resolve deps | https://ui.shadcn.com/docs/mcp |
| `class-variance-authority` (cva) | Variant authoring | `npm i class-variance-authority` · https://cva.style |
| `tailwind-merge` + `clsx` | The `cn()` helper | `npm i tailwind-merge clsx` |
| `tailwindcss` (v3 or v4) | Required peer | https://tailwindcss.com |
| `@radix-ui/react-*` | Headless primitives (auto-pulled by shadcn add) | https://www.radix-ui.com |
| Storybook 8 | Visualize variants and states | `npx storybook@latest init` |
| `@axe-core/cli` | A11y audit on built site | `npm i -D @axe-core/cli` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| ui.shadcn.com registry | OSS | Yes via CLI/MCP | Canonical source; copy-paste model |
| v0.dev | SaaS (Vercel) | Yes via API | Generates shadcn-styled JSX from prompts; pair with subagent for cleanup |
| 21st.dev | SaaS | Yes via MCP | Marketplace of shadcn-compatible blocks; MCP search returns components |
| Tweakcn | SaaS / OSS | Yes (export) | Visual theme editor producing CSS variable blocks |
| Storybook (Chromatic) | SaaS | Yes via API | Visual regression on variants — critical when agent edits ui/* |
| shadcn-svelte / shadcn-vue | OSS | Same workflow | Framework forks; same registry semantics |

## Templates & scripts
See `templates.md` for the per-component scaffold. Useful one-liner for agents to bulk-scaffold a feature's primitives:

```bash
#!/usr/bin/env bash
# Usage: ./scaffold.sh button card dialog form input label
# Adds shadcn primitives, then ensures displayName + a barrel export.
set -euo pipefail
for c in "$@"; do npx shadcn@latest add "$c" --yes; done
{
  echo "// auto-generated barrel — do not edit"
  for c in "$@"; do echo "export * from './$c';"; done
} > components/ui/index.ts
npx tsc --noEmit
echo "Scaffolded: $*"
```

## Best practices
- Pin shadcn registry version in `components.json` (`"$schema"` + lockfile commit) so an agent re-running `add` is deterministic.
- Treat `components/ui/*` as vendored code: tag the directory with a CODEOWNERS entry, gate via PR review.
- Co-locate Storybook stories with each ui primitive — agents validate variants visually before merging.
- Define design tokens in ONE place (`globals.css` `:root` + `.dark`); ban inline hex/`bg-[#...]` via an ESLint rule.
- Use `cva` `compoundVariants` for state combinations (`variant: "outline" + size: "sm"`) instead of new flat variants.
- Always export both the component and its `*Variants` CVA function — downstream code may want `cn(buttonVariants({ variant }))` for non-button elements.
- Add `displayName` immediately after `forwardRef`; otherwise React DevTools shows `_c2` and agent debugging breaks.

## AI-agent gotchas
- Agents love to "improve" `components/ui/*` files — protect via lint rule (`eslint-plugin-boundaries`) or a glob-restricted hook; require a separate explicit task to edit them.
- Copy-paste drift: when the agent re-runs `shadcn add button`, it overwrites your local edits silently. Force diff review (`git diff --check` after add).
- Class-name explosion: agents generate huge `className={cn(...20-classes)}` strings; require them to factor into CVA when length > 6 utilities.
- `asChild` confusion: agents wrap `<Slot>` children in extra divs, which breaks Radix asChild semantics. Lint rule: `<Slot>` must have exactly one React child.
- Tailwind v4 vs v3: agent fetches outdated examples and writes v3 `hsl(var(--x))` while config is v4. Keep version in `AGENTS.md` for the dir.
- Dark-mode mishandling: agents add `dark:bg-gray-800` instead of using semantic tokens. Enforce: only `--background`, `--foreground`, etc.
- Human-in-loop checkpoint: any change touching `components/ui/*` or `globals.css` token block requires a human review — these are blast-radius high.

## References
- https://ui.shadcn.com/docs
- https://ui.shadcn.com/docs/cli
- https://ui.shadcn.com/docs/mcp
- https://cva.style/docs
- https://www.radix-ui.com/primitives
- https://manupa.dev/blog/anatomy-of-shadcn-ui
- https://tailwindcss.com/docs/upgrade-guide (v3 → v4)
