# Agent Integration — Cross-Platform Token Distribution

## When to use
- Setting up a Style Dictionary / Tokens Studio / Supernova / Specify pipeline that emits CSS, SCSS, iOS Swift, Android XML, and React Native.
- Migrating a one-platform token set (CSS only) to multi-platform.
- Auditing drift between Figma tokens and shipped artifacts.
- Generating CI jobs that fail when token outputs are out of date.

## When NOT to use
- Single-platform product (web-only marketing site) — Style Dictionary adds friction with no payoff.
- Pre-design-system phase where token contract isn't stable; pipeline churn outpaces value.
- Brand assets that change every campaign — distribution overhead exceeds reuse benefit.
- Closed mobile app with one developer who hand-edits XML — overhead > saved minutes.

## Where it fails / limitations
- Style Dictionary transforms are unit-and-platform-aware but trip on edge cases (rem in iOS, dp in CSS).
- Tokens Studio JSON dialect drifts from W3C draft; round-tripping breaks references.
- Vendor SaaS (Supernova, Specify) lock outputs behind paid plans and undocumented field names.
- Semantic-token aliasing across platforms is fragile — Android XML resolves only one level deep without custom resolvers.
- Animation, motion, elevation tokens have no standard cross-platform mapping yet.

## Agentic workflow
Use Claude as a "transform pipeline author": given a Tokens Studio export and a list of target platforms, it generates the Style Dictionary `config.json`, custom transforms (e.g., px→dp, color→UIColor), build script, and a per-platform output checker. A second pass writes a CI job that diff-checks committed outputs vs. fresh build, blocking PRs on drift. The agent also produces a README explaining how designers add tokens without breaking transforms.

### Recommended subagents
- `general-purpose` Claude subagent — pipeline scaffolding + transform code.
- `faion-sdd-executor-agent` — execute SDD task implementing the pipeline as repo.
- A "design-token-validator" prompt — diff Figma export vs. Style Dictionary output, list mismatches.

### Prompt pattern
```
Targets: web (CSS vars + SCSS), iOS (Swift UIColor + CGFloat), Android (colors.xml + dimens.xml).
Source: tokens.json (Tokens Studio v0.5 export).
Output: style-dictionary config.json + custom transforms for px→dp and color formats + npm build script.
```

```
Given the diff between commit A and commit B of tokens.json,
list which platform output files are stale and the exact npm
script to rebuild them.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `style-dictionary` | Token transform engine (de-facto standard) | `npm i -g style-dictionary` |
| `tokens-studio-cli` (community) | Export Figma Tokens Studio JSON in CI | https://docs.tokens.studio/ |
| `supernova-cli` | Pull tokens from Supernova platform | `npm i -g @supernovaio/cli` |
| `specify-cli` | Specify token sync | `npm i -g @specifyapp/cli` |
| `cosmos-config` | Multi-platform token build (JetBrains) | https://cosmos.jetbrains.com/ |
| `theo` (Salesforce, legacy) | Predecessor of Style Dictionary | https://github.com/salesforce-ux/theo |
| `tinacms tina-tokens` | Visual token editor → JSON | https://tina.io/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Style Dictionary | OSS | Yes (Node API) | Pipeline core |
| Tokens Studio for Figma | SaaS plugin | Limited (export JSON) | Designer-side authoring |
| Supernova | SaaS | Yes (CLI + REST) | Full lifecycle but pricey |
| Specify | SaaS | Yes (CLI + REST) | Distribution-focused |
| Knapsack | SaaS | Yes (REST API) | Component + token co-management |
| zeroheight | SaaS | Limited (Figma sync) | Documentation-first |
| Chromatic | SaaS | Indirect | Visual regression for token impact |
| Penpot | OSS | Limited | Open-source Figma alternative |

## Templates & scripts
See `templates.md` for `config.json` skeleton. Inline drift-detector for CI:

```bash
#!/usr/bin/env bash
# tokens-drift-check.sh — fail CI if outputs diverge from source
set -euo pipefail
git stash --include-untracked --quiet || true
npx style-dictionary build --config tokens/config.json
if ! git diff --quiet -- 'platforms/'; then
  echo "FAIL: token outputs are stale. Run 'npm run tokens:build' and commit."
  git diff --stat -- 'platforms/'
  exit 1
fi
git stash pop --quiet 2>/dev/null || true
echo "OK: token outputs in sync."
```

## Best practices
- Treat Tokens Studio JSON as the single source of truth; no platform should hand-edit outputs.
- Commit generated outputs (CSS, Swift, XML) to the repo — never resolve at app runtime.
- Run the build in CI on every PR; block merges on drift.
- Use Style Dictionary `transformGroup` per platform; only override individual transforms when truly needed.
- Validate against W3C draft format on every export so future tooling stays compatible.
- Snapshot-test rendered components after token changes; raw value diffs miss visual regressions.

## AI-agent gotchas
- Claude often writes Style Dictionary `transforms` against the deprecated v3 API; pin v4+ in the prompt.
- Generated SCSS maps may use a syntax that newer Dart Sass deprecates (`!default` placement); lint after generation.
- Color-space mismatches (sRGB vs. P3) are silently lost in token transform; require explicit color-space metadata.
- Agent will sometimes invent capability for Tokens Studio (e.g., "math expressions"); validate features against current docs.
- Auto-applying token PRs is risky — a wrong primary color rebrands the product instantly across platforms.
- Don't let an agent prune "unused" tokens automatically; static analysis misses runtime / theming references.

## References
- https://styledictionary.com/
- https://tokens.studio/
- https://www.supernova.io/
- https://specifyapp.com/
- https://design-tokens.github.io/community-group/format/
- Brad Frost, *Atomic Design* (2016)
- https://css-tricks.com/what-are-design-tokens/
