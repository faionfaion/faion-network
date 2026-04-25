# Agent Integration — Tailwind Patterns

## When to use
- Building or maintaining a React / Vue / Svelte / Astro / Next.js component library where utility-first CSS is the default.
- Implementing a design system on top of `tailwind.config.js` tokens (colors, spacing, typography, radii) instead of bespoke SCSS.
- Migrating from CSS-in-JS (Emotion, styled-components) to a build-time, server-render-friendly stack.
- LLM-driven UI generation: agents are reliable when the styling vocabulary is closed (utility class names) and predictable (Tailwind v3+ JIT).
- shadcn/ui, daisyUI, or headless-UI workflows — Tailwind is the substrate.

## When NOT to use
- Static brochureware where Tailwind's CSS bundle and toolchain outweigh value; vanilla CSS or Pico/Tachyons may suffice.
- Apps with deep theming requirements that don't map to design tokens (e.g., per-tenant runtime themes with hundreds of colors).
- Email templates — utility classes mostly don't survive email clients; use MJML / react-email instead.
- Teams that strongly prefer scoped CSS or BEM and won't tolerate `class="flex items-center …"` strings.
- Projects whose component output must be CSS-class-free (web components without Shadow DOM-bound utilities).

## Where it fails / limitations
- Class-name soup: long `className` strings hide intent; without `cva` / `cn` helpers, diffs become unreadable.
- Style drift: agents and humans copy classes between components instead of extracting; design tokens silently fork.
- Dark mode and theming: `dark:` modifier covers basic cases but breaks down with multi-theme (light/dark/system + brand themes).
- Arbitrary values (`w-[37px]`) are an escape hatch agents abuse, defeating the design system.
- Purge / content-config errors: dynamically generated class names get stripped from the build, causing runtime style misses.
- Plugin sprawl: each plugin (typography, forms, container queries, animation) adds rules that conflict; debugging cascade order is hard.
- Specificity surprises with `@apply` and component layers — order of import in `globals.css` matters.
- Tailwind v4 (Oxide engine) changes config and auto-content discovery; older docs and agent training data lag.

## Agentic workflow
A three-stage flow. (1) **Token sync**: an agent reads design tokens (Figma export, Style Dictionary JSON) and writes `tailwind.config.ts`; refuses arbitrary values that don't map to a token. (2) **Component generation**: agent emits a component using `cva` for variants, `cn`/`twMerge` for class merging, and explicit base/variant/size patterns; ESLint + `eslint-plugin-tailwindcss` enforces ordering and forbids unknown classes. (3) **Audit / refactor**: a periodic agent finds duplicated class strings (>3 uses), extracts them into reusable variants, and runs visual regression (Chromatic / Percy) to verify no pixel diff. Pair with `shadcn-ui-architecture` for primitive selection.

### Recommended subagents
- `faion-sdd-executor-agent` — gates: no arbitrary values without comment, no inline class duplication > 3 occurrences, design token diff matches Figma export.
- A **token-sync** subagent (worth creating): consumes Figma → `style-dictionary` output → writes `tailwind.config.ts`; opens PR diffing tokens.
- A **class-linter** subagent: runs `eslint-plugin-tailwindcss`, `prettier-plugin-tailwindcss`, and `tailwind-merge` checks; outputs PASS/FAIL per file.
- `faion-feature-executor` (skill) — sequence component spec → primitives → variants → stories → visual snapshot.
- `password-scrubber-agent` — irrelevant here unless component snapshots include real customer data.

### Prompt pattern
Component scaffold:
```
You are a UI engineer. Generate a <ComponentName> React component
using Tailwind v3 + cva. Variants: <list>. Sizes: <list>. Use cn() for
class merging (tailwind-merge + clsx). All colors/spacing must use
tokens defined in tailwind.config.ts (no arbitrary values). Add
focus-visible styles, disabled state, and a dark: variant. Output:
the .tsx file plus a Storybook story exercising every variant×size.
```

Refactor pass:
```
Find all className strings in <dir> appearing in ≥3 files. For each,
propose either: (a) extract into cva variant in the closest primitive,
(b) move into globals.css @layer components if it represents a real
pattern, or (c) leave alone with justification. Output diff blocks; do
not auto-apply.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `tailwindcss` CLI | Build / watch / minify | `npm i -D tailwindcss` ; https://tailwindcss.com/docs/installation |
| `prettier-plugin-tailwindcss` | Auto-sort class names | `npm i -D prettier-plugin-tailwindcss` |
| `eslint-plugin-tailwindcss` | Lint unknown / mis-ordered classes | `npm i -D eslint-plugin-tailwindcss` |
| `tailwind-merge` | Resolve conflicts at runtime | `npm i tailwind-merge` |
| `class-variance-authority` | Type-safe variant API | `npm i class-variance-authority` |
| `clsx` | Conditional class composer | `npm i clsx` |
| `style-dictionary` | Token pipeline (Figma → CSS / Tailwind) | `npm i -D style-dictionary` |
| `headlessui` / `radix-ui` | A11y primitives that pair with Tailwind | https://headlessui.com / https://www.radix-ui.com |
| `shadcn-ui` CLI | Pull copy-paste components into repo | `npx shadcn@latest add button` |
| `chromatic` / `percy` | Visual regression on stories | https://www.chromatic.com |
| `tailwind-variants` | cva-like API with slots / responsive | https://www.tailwind-variants.org |
| `unocss` | Drop-in alternative + analyzer (good for migration) | https://unocss.dev |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Tailwind UI | Paid templates | Partial | Static HTML/JSX patterns; agents can adapt. |
| Tailwind Plus / Catalyst | Paid components | Partial | React component sets. |
| shadcn/ui | OSS | Yes — CLI | Copy-paste components on top of Radix; ideal for agents. |
| Hero Icons / Lucide | OSS icons | Yes — package | Token-aligned icons. |
| Headless UI | OSS | Yes — package | A11y primitives by Tailwind Labs. |
| Radix UI | OSS | Yes — package | A11y primitives; default for shadcn. |
| Storybook | OSS | Yes — CLI | Visual catalog; pairs with Chromatic. |
| Chromatic | SaaS | Yes — CLI | Visual regression CI. |
| Percy | SaaS | Yes — CLI | Visual regression CI. |
| Tokens Studio | SaaS + Figma plugin | Yes — sync API | Figma → JSON tokens → style-dictionary → Tailwind config. |
| Penpot | OSS | Partial | Open-source design tool with token export. |

## Templates & scripts
See `templates.md` for the full Button + variant scaffolding. Inline class-string deduper (≤50 lines):

```bash
#!/usr/bin/env bash
# tw-dupes.sh — find Tailwind class strings duplicated across components.
set -euo pipefail
ROOT="${1:-src}"
node - "$ROOT" <<'JS'
const fs = require('fs'), path = require('path');
const root = process.argv[2];
const re = /className\s*=\s*["'`]([^"'`]+)["'`]/g;
const map = new Map();
function walk(d){
  for (const f of fs.readdirSync(d, {withFileTypes:true})){
    const p = path.join(d, f.name);
    if (f.isDirectory()) walk(p);
    else if (/\.(tsx|jsx|astro|svelte|vue)$/.test(f.name)){
      const src = fs.readFileSync(p,'utf8');
      let m; while ((m = re.exec(src))){
        const norm = m[1].split(/\s+/).filter(Boolean).sort().join(' ');
        if (norm.split(' ').length < 3) continue;
        if (!map.has(norm)) map.set(norm, []);
        map.get(norm).push(p);
      }
    }
  }
}
walk(root);
const dupes = [...map.entries()].filter(([,v]) => new Set(v).size >= 3);
dupes.sort((a,b) => b[1].length - a[1].length);
for (const [cls, files] of dupes.slice(0, 30)){
  console.log(`# ${files.length}x  ${cls}`);
  for (const f of [...new Set(files)]) console.log(`  ${f}`);
}
process.exit(dupes.length ? 1 : 0);
JS
```

Wire into a weekly job that opens an SDD task with the dupe list for refactor.

## Best practices
- Configure `tailwind-merge` (or `tailwind-variants`) on every component that accepts a `className` prop — without it, prop overrides silently lose.
- Use `cva` (or `tailwind-variants`) for any component with > 1 variant axis. Inline ternaries multiply class strings and tank readability.
- Pin tokens in `tailwind.config.ts` and reject arbitrary values (`w-[37px]`) in PR review unless commented with rationale.
- Add `eslint-plugin-tailwindcss` (`classnames-order`, `no-custom-classname`, `no-contradicting-classname`) and `prettier-plugin-tailwindcss` to the toolchain.
- Co-locate Storybook stories with components; require a story per variant for visual regression.
- Use design-token sources of truth (Figma → Style Dictionary → Tailwind config) and regenerate on token PRs; manual sync drifts.
- Dark mode via `class` strategy plus a system-pref toggle; CSS-variable theming inside the same Tailwind setup for runtime themes.
- Encapsulate global patterns (typography defaults, prose) in `@layer components`, not ad-hoc files; ordering matters.
- Optimize purge with explicit `content` globs covering MDX, Storybook, and any content rendered at runtime — dynamic class names need a safelist.
- Keep `@apply` rare. It's fine for `prose-*`-style abstractions but easy to abuse into "Tailwind-as-SCSS".

## AI-agent gotchas
- Agents emit arbitrary values (`text-[#1a1a1a]`) and ignore tokens — they regenerate plausible hex codes from training data. Forbid arbitrary values via lint and reject on PR.
- LLMs duplicate base styles into every variant instead of putting them in the cva `base`. Provide an example with the base/variant/size split.
- Class ordering drifts and creates noisy diffs. `prettier-plugin-tailwindcss` fixes this — keep it on.
- Conflicting classes (`p-4 p-2`) — agents append instead of merging. `tailwind-merge` is required at runtime; lint catches obvious cases.
- Dark-mode coverage: agents add `bg-white` without `dark:bg-zinc-900`. Require a dark-mode pair in lint or a snapshot test.
- Dynamic class names (`bg-${color}-500`) get purged. Use full class names with conditional logic, or add to `safelist`.
- Tailwind v4 vs v3: training data is mostly v3; agents may emit `tailwind.config.js` for a v4 project. Pin major version in the prompt and verify.
- shadcn copy-paste: agents add new shadcn components but skip the token migration step in `tailwind.config.ts` (CSS variables, base colors). Provide the post-add checklist.
- Accessibility regressions: agents drop `focus-visible:` styles or remove `sr-only` for "cleanup". Lock these in the cva base and require a11y test.
- Human-in-loop checkpoint: any change to `tailwind.config.ts` token values must be human-approved — token diffs cascade across the entire app.

## References
- Tailwind CSS v3+ docs — https://tailwindcss.com/docs
- Tailwind CSS v4 (Oxide) — https://tailwindcss.com/blog/tailwindcss-v4-alpha
- Adam Wathan — "CSS Utility Classes and 'Separation of Concerns'". https://adamwathan.me/css-utility-classes-and-separation-of-concerns/
- shadcn/ui — https://ui.shadcn.com
- class-variance-authority — https://cva.style
- tailwind-variants — https://www.tailwind-variants.org
- Tokens Studio — https://tokens.studio
- Style Dictionary — https://amzn.github.io/style-dictionary/
- Sibling methodologies in this repo: `tailwind-architecture/`, `shadcn-ui-architecture/`, `design-tokens/`, `ui-component-library/`, `react-component-architecture/`.
