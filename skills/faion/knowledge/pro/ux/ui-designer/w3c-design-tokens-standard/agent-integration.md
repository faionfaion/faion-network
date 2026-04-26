# Agent Integration — W3C Design Tokens Standard

## When to use
- Migrating an existing token set (Tokens Studio, custom JSON) to the W3C draft format (`$type` + `$value`).
- Greenfield design system aiming for vendor-neutral, future-proof token files.
- Auditing token files for compliance with the latest community-group draft.
- Generating Style Dictionary / Cosmos transforms that consume W3C-formatted source.

## When NOT to use
- Locked into a vendor format (Adobe Spectrum, IBM Carbon, Material 3) that has its own dialect; conversion is overhead.
- Pre-MVP product where token contract is unstable — chasing a moving spec wastes cycles.
- Single-platform design system where standardization gives no portability win.
- Agencies producing one-off campaign tokens — interchange isn't worth it.

## Where it fails / limitations
- The format is still a Community Group draft; no W3C Recommendation, breaking changes possible.
- Tooling support is partial: Style Dictionary v4 supports it; Tokens Studio export is close-but-not-exact.
- Composite types (typography, transition, gradient, shadow) have evolving sub-schemas — older files break newer parsers.
- `$ref` style aliases (`{color.brand}`) resolve differently across implementations.
- No standard motion / animation type yet — vendor-specific extensions remain necessary.

## Agentic workflow
Use Claude as a "format migrator + validator": it ingests legacy token JSON, emits W3C-compliant output (`$type`, `$value`, `$description`), preserves alias graphs, and produces a JSON Schema-based validator. A second pass diffs old-vs-new render output (CSS, Swift, XML) to verify semantic preservation. The agent maintains a tracking issue listing draft-format deltas so that periodic re-validation catches spec evolution.

### Recommended subagents
- `general-purpose` Claude subagent — format migration + validator scaffolding.
- `faion-sdd-executor-agent` — SDD task to swap legacy source for W3C source in the build pipeline.
- A "schema-validator" prompt — run draft-format JSON Schema against token files in CI.

### Prompt pattern
```
Migrate this Tokens Studio export (input.json) to W3C draft format.
Preserve alias graph with $ref notation. Add $type for color, dimension,
fontFamily, fontWeight, shadow. Emit a JSON Schema for validation.
```

```
Validate tokens.json against the latest W3C draft (date: <YYYY-MM>).
List violations with path, expected $type, actual value, and severity.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `style-dictionary` v4+ | Native W3C source format support | `npm i -g style-dictionary@latest` |
| `@design-tokens/format-validator` (community) | JSON Schema validator | https://github.com/design-tokens/community-group |
| `ajv-cli` | Generic JSON Schema validation | `npm i -g ajv-cli` |
| `jq` | Path-level inspection of token files | `apt install jq` |
| `cosmos-config` | Multi-platform build with W3C source | https://cosmos.jetbrains.com/ |
| `tokens-studio-cli` (community) | Export Figma plugin data → JSON | https://docs.tokens.studio/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Style Dictionary v4 | OSS | Yes (Node API) | First-class W3C support |
| Tokens Studio | SaaS plugin | Partial | Export close to W3C; gaps in composite types |
| Supernova | SaaS | Partial | Roadmap mentions W3C alignment |
| Specify | SaaS | Partial | Similar story |
| Knapsack | SaaS | Partial | Adoption in progress |
| design-tokens.org reference | OSS | Yes (schemas + examples) | Canonical source |

## Templates & scripts
See `templates.md` for example W3C JSON. Inline draft validator:

```bash
#!/usr/bin/env bash
# w3c-tokens-validate.sh — gate CI on W3C draft compliance
set -euo pipefail
SCHEMA="${SCHEMA_URL:-https://design-tokens.github.io/community-group/format/schema.json}"
FILE="${1:?path to tokens.json required}"
curl -sSL "$SCHEMA" -o /tmp/dt.schema.json
ajv validate -s /tmp/dt.schema.json -d "$FILE" --strict=false \
  || { echo "FAIL: not W3C-compliant"; exit 1; }
echo "OK: $FILE conforms to W3C draft"
```

## Best practices
- Pin a draft snapshot date in your repo; don't auto-pull `main` of the format spec — breaking changes happen.
- Always include `$description` on semantic tokens; it's the only place to record intent.
- Use `$ref` aliases for the primitive→semantic→component layering, not value duplication.
- Validate in CI on every PR; add a "format date" check to flag when the upstream spec moved.
- Treat current files as draft-compliant, not standard-compliant; communicate this in design-system docs.
- Pair migration with a rendered-output snapshot test to catch silent semantic drift.

## AI-agent gotchas
- Claude conflates W3C draft with Tokens Studio dialect — they share `$type` but differ on composite types and aliases.
- Generated `$type` values may use older names (`type` instead of `$type`); enforce the `$`-prefixed form.
- LLM may flatten alias chains and embed primitive values — defeats the migration purpose; require alias preservation.
- Composite types (shadow, gradient, typography) are commonly malformed; lint each composite against its sub-schema.
- Agent will assume v4 Style Dictionary syntax without checking project version; pin in prompt.
- Don't auto-replace legacy tokens in production without a snapshot diff — visual changes can sneak in.

## References
- https://www.w3.org/community/design-tokens/
- https://design-tokens.github.io/community-group/format/
- https://tr.designtokens.org/format/
- https://github.com/design-tokens/community-group
- https://styledictionary.com/info/dtcg/
- https://www.designsystems.com/w3c-tokens/
