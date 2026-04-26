# Agent Integration — Design Tokens Implementation

## When to use
- Multi-platform product (web + iOS + Android + macOS) needing one source of truth for color, typography, spacing
- Migrating ad-hoc CSS variables / Sass `$color-*` maps to a token-driven pipeline (Style Dictionary, W3C Design Tokens spec)
- Wiring Tailwind theme, CSS custom properties, iOS Asset Catalogs, Android XML, JS object outputs from one JSON source
- Light/dark/high-contrast/brand modes via semantic tokens (alias layer)
- Connecting Figma Variables → Tokens Studio → Style Dictionary → app codegen

## When NOT to use
- Single-app projects with one platform and stable styling (over-engineering for solos)
- Prototype/MVP UIs where design churn outpaces token churn
- Static marketing sites with no design system to maintain

## Where it fails / limitations
- Style Dictionary v3 → v4 breaking changes: `formatter` → `format` function shape; agents trained on v3 emit broken configs
- W3C Design Tokens Format Module (DTCG) is still draft; agents may emit non-standard shapes that Tokens Studio can't parse
- Token reference resolution (`{color.brand.500}`): cycles between aliases crash the build with cryptic errors
- Multi-mode (light/dark) tokens duplicated across mode files drift; without a single semantic alias layer per mode, contrast pairs break
- iOS / Android codegen requires platform-specific transforms; agents skip the `transforms` chain and ship invalid `.xml`/`.swift`
- Tailwind v4 prefers CSS-native `@theme` over JS config; pipelines that emit `tailwind.config.js` only need to also emit a CSS theme block
- Tokens Studio JSON ≠ Style Dictionary native JSON; needs `@tokens-studio/sd-transforms` or the build silently drops styles

## Agentic workflow
Token edits never happen in app code: agent edits the `tokens/` source (JSON or DTCG), runs `style-dictionary build`, then runs visual regression tests against Storybook to catch unintentional shifts. A review subagent diffs generated outputs (CSS, JS, XML, Swift) — if a non-token-related file changed, fail. Pair the codegen with a CI publish step that bumps an `@org/design-tokens` package, and downstream apps lock to a semver range.

### Recommended subagents
- General-purpose subagent — token JSON authoring, Style Dictionary config, transform/format authoring
- `faion-feature-executor` — sequence: edit tokens → build → publish package → bump consumers → visual regression
- `faion-sdd-execution` — gates: token JSON validates against schema, no broken `{...}` references, generated files diff-clean
- Visual-regression subagent (Chromatic / Percy / Loki) — Storybook snapshots gate token changes
- Review subagent — diffs the generated outputs against the lockfile and asserts non-source files weren't hand-edited

### Prompt pattern
```
Add a `bg-surface-elevated` semantic token mapped to:
  light → color.gray.50
  dark  → color.gray.900
1. Edit tokens/semantic/surface.json with the alias layer.
2. Update mode files tokens/modes/{light,dark}.json.
3. Run `pnpm sd build`; commit only the *.json sources, not generated artifacts (those rebuild in CI).
4. Add a Storybook story showing both modes; run `pnpm chromatic` and report the diff URL.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `style-dictionary` | Token transform/codegen pipeline | `npm i -D style-dictionary` |
| `@tokens-studio/sd-transforms` | Tokens Studio → SD transforms | `npm i -D @tokens-studio/sd-transforms` |
| `terrazzo` (`@terrazzo/cli`) | Modern DTCG-native build (alternative to SD) | `npm i -D @terrazzo/cli` |
| `@cobalt-ui/cli` | DTCG token CLI | `npm i -D @cobalt-ui/cli` |
| `figma-tokens` / Tokens Studio | Figma plugin export | https://tokens.studio/ |
| `chromatic` / `percy` / `loki` | Visual regression on token changes | `npm i -D chromatic` |
| `tinacms` / `theo` (Salesforce, legacy) | Older token tooling | reference only |
| `style-dictionary-utils` | Common DTCG-aligned formats/transforms | `npm i -D style-dictionary-utils` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Tokens Studio (Figma plugin) | SaaS | Partial | Sync to GitHub via the plugin's GitHub action |
| Supernova | SaaS | Yes (CLI + API) | Token management with multi-platform export |
| Specify | SaaS | Yes (CLI) | Design-API serving DTCG tokens |
| Knapsack | SaaS | Partial | Documentation + tokens hub |
| Storybook + Chromatic | OSS + SaaS | Yes | Visual regression gating; agents trigger via `chromatic --auto-accept-changes=false` |
| Style Dictionary (built into design-token monorepos) | OSS | Yes | The default for solo/agency teams |
| GitHub Actions | SaaS | Yes | `tokens.json` change → build → publish `@org/tokens@X.Y.Z` |

## Templates & scripts
See `templates.md` for full Style Dictionary config, custom transforms, and DTCG examples. Pipeline GitHub Action sketch (≤50 lines):

```yaml
name: design-tokens
on:
  push:
    branches: [main]
    paths: ['tokens/**']
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v3
        with: { version: 9 }
      - uses: actions/setup-node@v4
        with: { node-version: 20, cache: pnpm }
      - run: pnpm install --frozen-lockfile
      - run: pnpm sd build
      - run: pnpm test
      - name: bump version
        run: pnpm changeset version && pnpm changeset publish
        env:
          NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Best practices
- Three-layer token hierarchy: **primitives** (raw colors, hex), **semantic** (`bg.surface.default`), **component** (`button.primary.bg`). App code consumes only semantic + component layers.
- Validate token JSON against a JSON schema in CI; catches typos in references before build
- Generated artifacts (CSS, JS, XML) live in `dist/` and are committed only when this is the published artifact; otherwise `.gitignore` and rebuild in CI
- Mode tokens stay in separate files per mode (`light.json`, `dark.json`); never inline `{ light: ..., dark: ... }` per token unless your tooling supports it
- Use the W3C DTCG `$value` / `$type` shape for new projects; gives portability to Cobalt UI, Terrazzo, future tools
- Lock the token package version per app (semver `^`) so feature branches don't pull surprise color changes
- Prefer CSS custom properties over Sass / JS for runtime theme switching; faster than re-rendering on theme change
- Document each semantic token's intent (`bg.surface.elevated: cards floating above the canvas`) in JSON `$description` — feeds future agent context

## AI-agent gotchas
- Style Dictionary v3 vs v4 API: agents emit `formatter: function({dictionary, file})` (v3) into v4 projects expecting `format: ({dictionary, options}) => ...`. Lock the major version explicitly.
- Agents flatten the primitive→semantic→component hierarchy "for simplicity"; that destroys the alias layer and makes mode-switching impossible to add later
- DTCG vs Tokens Studio JSON divergence: Tokens Studio uses `value` and `type` (no `$`); needs `@tokens-studio/sd-transforms` to convert. Agents miss this and ship empty CSS.
- Hex color references break when an upstream primitive changes — Style Dictionary resolves at build time, not at runtime, so consumers must rebuild + redeploy
- Agents commit generated CSS into the same repo as sources; on the next build CI generates the same file, marks the repo dirty, fails. Use `.gitignore`.
- Multi-mode contrast: agent updates dark mode but forgets light mode pair → WCAG fails on one theme. Pair every mode change with an a11y check (`@testing-library/jest-dom`, axe).
- Human-in-loop required for: brand color changes, semantic naming refactors (`bg.surface` → `surface.background`), introducing a new mode
- Token JSON files >50KB feed slowly into LLM context; chunk by group (color, typography, spacing) when prompting

## References
- Style Dictionary: https://amzn.github.io/style-dictionary/
- W3C Design Tokens Community Group spec: https://design-tokens.github.io/community-group/format/
- Tokens Studio: https://tokens.studio/
- `@tokens-studio/sd-transforms`: https://github.com/tokens-studio/sd-transforms
- Terrazzo: https://terrazzo.app/
- Cobalt UI: https://cobalt-ui.pages.dev/
- "Design Tokens" (Smashing Magazine, Lukas Oppermann): https://www.smashingmagazine.com/2021/04/managing-design-tokens-style-dictionary/
- Tailwind theming via tokens: https://tailwindcss.com/docs/customizing-colors
