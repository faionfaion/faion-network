# Agent Integration — Cross-Platform Token Distribution

## When to use
- Single source of truth for design tokens that ship to Web (CSS/SCSS), iOS (Swift/UIKit/SwiftUI), Android (XML/Compose), React Native.
- Replacing hand-maintained brand colors/spacing/type scales scattered across repos.
- Wiring Figma → repo via Tokens Studio, Specify, or Supernova.
- Adding theming (light/dark/high-contrast) and brand variants without per-platform forks.

## When NOT to use
- One platform only and one product — Style Dictionary overhead is not worth it.
- Tokens that are not values (animation easing curves, motion specs) — use platform-native specs.
- Highly dynamic runtime theming driven by API responses — use a runtime tokens service instead.
- A team without a versioning + CI culture — token drift is worse than no system.

## Where it fails / limitations
- Naming collisions when multiple Figma libraries merge into one Style Dictionary tree.
- Platform transforms diverge: rgba vs hex8, dp vs sp on Android, points vs pixels on iOS.
- Semantic tokens depending on alias chains break silently when a primitive is renamed.
- Dark-mode tokens on iOS need `UIColor(dynamicProvider:)` wrappers — not a flat hex map.
- Compose vs XML on Android: same token, two outputs, drift if generators are not co-versioned.

## Agentic workflow
Use a subagent to read the Tokens Studio JSON export, validate W3C Design Tokens Community Group schema, generate Style Dictionary config and platform transforms, then run the build and diff outputs against the previous release. A second agent inspects the diff for breaking renames and writes a migration note. Humans review the generated CSS/Swift/Kotlin files for naming and tone before merge.

### Recommended subagents
- `faion-sdd-executor-agent` — wires Style Dictionary configs, runs `style-dictionary build`, commits outputs.
- `faion-usability-agent` — reviews semantic token names for clarity and consistency.

### Prompt pattern
```
Read tokens.json (W3C DTCG format). Generate style-dictionary
config that emits: css/variables, scss/maps, ios-swift/class.swift,
android/resources, compose/object. Use category-type-item naming.
List any token without a $type as a blocker.
```

```
Diff the previous build/ outputs against current. List renamed,
removed, type-changed tokens. Output a CHANGELOG entry and a
codemod plan for consumers.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `style-dictionary` | Token transform engine | `npm i -D style-dictionary`; styledictionary.com |
| `tokens-studio-cli` | Sync Figma token sets to disk | tokens.studio/docs/sync |
| `specify` CLI | Pull tokens from Specify projects | specifyapp.com/docs/cli |
| `supernova-cli` | Export from Supernova design system | supernova.io/docs |
| `theo` (Salesforce) | Legacy token transformer | github.com/salesforce-ux/theo |
| `terrazzo` | W3C DTCG-first transformer | terrazzo.dev |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Tokens Studio (Figma) | SaaS plugin | Yes — JSON export, GitHub sync | Best for designer-driven workflows. |
| Specify | SaaS | Yes — REST API + CLI | Distributes tokens, icons, assets across platforms. |
| Supernova | SaaS | Partial — exporters are JS, scriptable | Strong for documentation generation. |
| Knapsack | SaaS | Partial — config-driven | Bundles tokens with component docs. |
| Style Dictionary | OSS | Yes — fully scriptable | Industry standard; latest v4 supports DTCG natively. |
| Terrazzo | OSS | Yes — DTCG-first | Modern alternative to Style Dictionary. |

## Templates & scripts
See `templates.md` and `examples.md` for the pipeline. Inline minimal `style-dictionary.config.js`:

```js
module.exports = {
  source: ["tokens/**/*.json"],
  platforms: {
    css: {
      transformGroup: "css",
      buildPath: "build/css/",
      files: [{ destination: "vars.css", format: "css/variables" }],
    },
    ios: {
      transformGroup: "ios-swift",
      buildPath: "build/ios/",
      files: [{ destination: "Tokens.swift", format: "ios-swift/class.swift",
                options: { className: "Tokens" } }],
    },
    android: {
      transformGroup: "android",
      buildPath: "build/android/",
      files: [
        { destination: "colors.xml", format: "android/colors" },
        { destination: "dimens.xml", format: "android/dimens" },
      ],
    },
  },
};
```

## Best practices
- Pin to W3C Design Tokens Community Group (DTCG) format — `$value` / `$type` / `$description`.
- Three layers: primitives (hex/px) → semantic (intent) → component (specific). Agents alias upward only.
- Generate outputs in CI; never commit hand-edited build outputs — pre-commit hook should diff.
- Version tokens with semver: rename = major, value tweak = minor, addition = patch.
- Emit a `tokens.json` for downstream consumers (web RN, marketing sites) alongside per-platform files.
- Maintain a CODEOWNERS rule on `tokens/` so designers gate changes, engineers gate generators.

## AI-agent gotchas
- Agents invent token names that don't exist in the Figma library — ground via DTCG schema validation.
- LLMs round colors (#3B82F6 → #3b82f5); enforce exact-match diff and lint.
- Path aliasing (`{color.primary}`) breaks on case sensitivity — Linux CI catches what macOS misses.
- iOS Swift output shadows existing UIKit names if the className is generic — pick `BrandTokens`.
- Agents over-emit semantic tokens; cap at one alias per primitive per surface to keep the system mappable.
- Dark mode: agent must emit both light and dark values per token, not duplicate the file.

## References
- W3C Design Tokens Format Module — design-tokens.github.io/community-group/format/
- Style Dictionary docs — styledictionary.com
- Tokens Studio for Figma — tokens.studio/docs
- Specify docs — specifyapp.com/docs
- Nathan Curtis, "Naming Tokens in Design Systems" — medium.com/eightshapes-llc/naming-tokens-in-design-systems-9e86c7444676
- Salesforce Lightning Design System token architecture — lightningdesignsystem.com/design-tokens/
