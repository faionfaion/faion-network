# Agent Integration — Semantic Tokens and Modes

## When to use
- Building a token system that supports light/dark, high-contrast, density, brand themes, or per-platform overrides.
- Migrating from raw color/spacing tokens to a semantic layer (`surface.primary`, `text.muted`).
- Wiring Figma Variables ↔ Style Dictionary ↔ runtime CSS/JS so designers and engineers see the same source of truth.
- Adding a new mode (e.g., AAA contrast, a white-label brand) without doubling component code paths.

## When NOT to use
- One-theme apps where adding modes adds cost without payoff — start with raw tokens, promote to semantic when the second theme arrives.
- Print/static asset pipelines where modes do not apply.
- Pure animation/motion tokens where mode-switching is rarely meaningful.

## Where it fails / limitations
- Mode explosion: 4 color modes × 3 density modes × 5 brands = 60 effective configurations. Methodology does not bound combinatorial growth.
- Figma Variables have hard limits (collection size, mode count per plan); methodology does not surface those.
- iOS/Android/Web have different runtime mode-switching semantics (system colorScheme vs CSS media query vs Compose `LocalConfiguration`); naming alone does not guarantee parity.
- "Semantic" is subjective — `text.primary` means different things to different designers; without governance the layer rots.
- High-contrast and AAA contrast modes are not free additions — they require ratio testing on every alias before claiming support.

## Agentic workflow
Agents are well-suited to mechanical token operations: alias generation, mode-matrix expansion, contrast checks, format conversion. Keep humans on naming/semantics. Pipeline: (1) ingest Figma Variables export, (2) `token-aliaser` agent maps primitive → semantic with deterministic rules, (3) `mode-validator` checks every alias resolves in every mode and meets contrast/spec rules, (4) `multi-platform-emitter` runs Style Dictionary to write CSS, iOS, Android, JSON. Rerun on every Figma library version bump in CI.

### Recommended subagents
- `token-aliaser` — haiku; deterministic mapping primitive→semantic from a rules file.
- `mode-validator` — haiku; verifies every (alias × mode) cell has a value and passes contrast/spec checks.
- `token-diff-reporter` — sonnet; summarizes additions/removals/breaking changes between two token snapshots for release notes.
- `figma-syncer` — sonnet; handles Figma Variables REST mutations with idempotent payloads.

### Prompt pattern
```
You are mode-validator. Given <tokens.json> with collection.modes structure,
verify each alias has a value in every declared mode. For color aliases also
compute WCAG contrast vs declared partner aliases (text-on-surface pairs).
Output JSON: {missing:[{alias,mode}], contrast_failures:[{pair,mode,ratio,required}]}.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `style-dictionary` | Multi-platform token build (CSS, iOS, Android, JSON) | `npm i -g style-dictionary` · amzn.github.io/style-dictionary |
| `theo` (Salesforce) | Token transforms similar to Style Dictionary | github.com/salesforce-ux/theo |
| `tokens-studio` plugin + sync CLI | Figma Variables ↔ JSON sync | tokens.studio |
| `figma-api-exporter` (community) | Pull Figma Variables via REST | github.com/figma/api-spec |
| `culori` | Programmatic color manipulation, contrast | `npm i culori` · culorijs.org |
| `axe-core` CLI | Contrast/a11y validation on rendered modes | `npm i -g @axe-core/cli` |
| `chroma.js` | Color conversion, palettes | gka.github.io/chroma.js |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Figma Variables | SaaS | Yes — REST `/v1/files/:key/variables/local` | Source of truth in many teams |
| Tokens Studio | OSS plugin + SaaS sync | Yes — JSON repo + CLI | Git-backed token sync |
| Supernova | SaaS | Yes — REST | Tokens, themes, doc gen |
| Specify | SaaS | Yes — REST + CLI | Token distribution to multiple targets |
| Knapsack | SaaS | Yes — REST | Multi-brand theming |
| Penpot | OSS | Limited — REST evolving | OSS Figma alternative with token plugin |
| Zeroheight | SaaS | Yes — REST | Token doc surfacing |

## Templates & scripts
See `templates.md` for naming convention and mode matrix. Mode coverage check:

```python
# mode_coverage.py — fail if any alias missing a value in any declared mode
import json, sys

def check(path: str) -> int:
    data = json.load(open(path))
    missing = []
    for col_name, col in data["collections"].items():
        modes = col.get("modes", [])
        for alias_name, alias in col.get("aliases", {}).items():
            values = alias.get("values", {})
            for m in modes:
                if m not in values or values[m] in (None, ""):
                    missing.append((col_name, alias_name, m))
    for row in missing:
        print("missing:", *row)
    return 1 if missing else 0

if __name__ == "__main__":
    sys.exit(check(sys.argv[1]))
```

## Best practices
- Three-tier naming: primitive (`color.blue.500`) → semantic (`color.action.primary`) → component (`button.primary.bg`). Components reference semantic, never primitive.
- Reserve one mode per axis as the default (light, default-density, brand-A) and document the inheritance rules — consumers of unset modes fall back deterministically.
- Treat a token rename as a breaking API change. Use codemods or alias deprecation periods, not silent removals.
- Co-locate contrast partner pairs in the token spec (e.g., `text.on-surface-primary` declares its surface). Validation needs both halves.
- Generate runtime CSS custom properties at build time, not at app boot — boot-time JS theming flickers and hurts perf.
- Per-platform deltas (iOS 14px button padding) belong in separate platform-prefixed tokens, not as `ios:` overrides on a shared token; overrides become invisible to designers.

## AI-agent gotchas
- LLMs invent token names confidently. Pin the agent to a closed enumeration loaded from a manifest; reject outputs with unknown identifiers.
- Color math regressions are silent: agent may emit `oklch()` values that look fine but fail contrast in dark mode. Always run `mode-validator` post-generation.
- Figma Variables REST API uses `tempId` for newly-created variables in the same call. Agents must capture and reuse those IDs in dependent operations or risk dangling refs.
- Mode counts are per-collection; agents that flatten across collections can lose mode info. Preserve collection scope end-to-end.
- Avoid agent-driven "auto-promotion" of primitives to semantic without human review — semantic naming is the one place humans add real meaning.
- Cache invalidation: when tokens change, downstream artifacts (Storybook stories, Tailwind config, iOS asset catalog) must rebuild. Drive with file hashes, not timestamps.
- Style Dictionary transforms run in declared order; an agent reordering them silently can break platform output. Lock the order in the agent's tooling spec.

## References
- Style Dictionary docs — amzn.github.io/style-dictionary.
- Figma Variables guide — help.figma.com/hc/en-us/articles/15339657135383.
- W3C Design Tokens Format Module — design-tokens.github.io/community-group/format/.
- Nathan Curtis, "Naming tokens in design systems" — medium.com/eightshapes-llc.
- "Theming with design tokens" — Smashing Magazine theme-tokens article.
