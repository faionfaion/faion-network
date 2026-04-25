# Agent Integration — W3C Design Tokens Standard

## When to use
- Authoring a token source-of-truth that must round-trip between Figma, Style Dictionary, and code without lossy mapping.
- Migrating a legacy Style Dictionary, Theo, or Tokens Studio file to a vendor-neutral DTCG-compliant JSON.
- Setting up a token pipeline shared across multiple front-ends (web, iOS, Android, RN) that needs one canonical schema.
- Preparing for tooling that already implements DTCG: Tokens Studio for Figma, Specify, Supernova, Style Dictionary v4, Penpot.

## When NOT to use
- Single-platform single-app project — DTCG overhead is wasted; native CSS variables are enough.
- Fast spike or throwaway prototype — schema discipline slows you down with no payoff.
- The team has zero token discipline yet — fix naming and primitives/semantic split (`token-organization`) first; switching format does not fix structure.

## Where it fails / limitations
- Spec is a Community Group draft, not a W3C Recommendation — breaking changes still happen between versions of the format module.
- `$type` coverage is incomplete: gradients, typography composites, and motion still vary across implementations; expect tool-specific extensions under `$extensions`.
- Aliases (`{group.token}`) require resolver support; agents that hand-roll JSON often emit unresolved references that break Style Dictionary v4.
- Math/reference loops are not detected by the spec — runtime tools must catch cycles.

## Agentic workflow
Treat DTCG as the canonical artifact. Have one subagent extract tokens from existing source (Figma export, SCSS variables, Tailwind config), a second normalize them to DTCG with a strict JSON schema validator in the loop, and a third generate platform outputs via Style Dictionary v4. Always run schema validation before committing — LLMs silently invent `$type` values that no parser accepts.

### Recommended subagents
- `ui-token-extractor` — pulls raw values from Figma REST API or CSS/SCSS source.
- `dtcg-normalizer` — rewrites raw values into DTCG groups with `$type`/`$value`/`$description`; validates against schema.
- `style-dictionary-builder` — runs `style-dictionary build` and verifies platform outputs (CSS, iOS, Android) compile.

### Prompt pattern
```
You are normalizing tokens to DTCG. Output ONLY valid JSON matching
https://design-tokens.github.io/community-group/format/. Each leaf MUST have
$type and $value. Aliases use {group.subgroup.name}. Reject typography composites
unless $type is "typography". Validate with `npx style-dictionary build` before responding.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `style-dictionary` v4 | Build DTCG → CSS/iOS/Android/JSON | `npm i -D style-dictionary@4` · https://styledictionary.com |
| `@tokens-studio/sd-transforms` | Bridge Tokens Studio → DTCG → Style Dictionary | `npm i -D @tokens-studio/sd-transforms` |
| `cti-style-dictionary-utils` | DTCG transforms, references | https://github.com/lukasoppermann/style-dictionary-utils |
| `terrazzo` (`@terrazzo/cli`) | DTCG-first build pipeline alternative to Style Dictionary | `npm i -D @terrazzo/cli` · https://terrazzo.dev |
| `figma-export` | Pull tokens from Figma to JSON | `npm i -D @figma-export/cli` |
| `ajv` + DTCG schema | JSON-schema validation in CI | `npx ajv validate -s dtcg-schema.json -d tokens.json` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Tokens Studio for Figma | SaaS plugin | Yes (REST + GitHub sync) | Native DTCG export; pair with sd-transforms. |
| Specify | SaaS | Yes (CLI + API) | Pulls tokens from Figma/Storybook, emits DTCG. |
| Supernova | SaaS | Partial (API in beta) | Strong DTCG import/export, weaker programmatic control. |
| Penpot | OSS | Partial | Built-in design tokens module aligned with DTCG draft. |
| Knapsack | SaaS | Limited | Good UI, weaker headless control. |

## Templates & scripts
Inline minimal validator (≤30 lines) that catches the two errors LLMs make most often: missing `$type` and unresolved aliases.

```js
// dtcg-validate.js
import fs from "node:fs";
const tokens = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
const errors = [];
const refRe = /\{([^}]+)\}/g;
const walk = (node, path = []) => {
  if (node && typeof node === "object") {
    if ("$value" in node) {
      if (!("$type" in node)) errors.push(`missing $type at ${path.join(".")}`);
      if (typeof node.$value === "string") {
        for (const m of node.$value.matchAll(refRe)) {
          const ref = m[1].split(".");
          let cur = tokens;
          for (const seg of ref) cur = cur?.[seg];
          if (!cur || !("$value" in cur))
            errors.push(`unresolved ref ${m[0]} at ${path.join(".")}`);
        }
      }
    } else for (const [k, v] of Object.entries(node)) walk(v, [...path, k]);
  }
};
walk(tokens);
if (errors.length) { console.error(errors.join("\n")); process.exit(1); }
console.log("OK");
```

Run in CI: `node dtcg-validate.js tokens.json`.

## Best practices
- Pin to a specific draft version in `$schema` and CI; the spec moves and silent breakage is common.
- Keep primitives in one file, semantic aliases in another, component overrides in a third — mirrors `token-organization` hierarchy and reduces merge conflicts.
- Use `$description` aggressively — it survives transforms and becomes inline docs in Storybook.
- Place tool-specific data under `$extensions.<tool>` not at the root; keeps the file portable.
- Always emit a `tokens.lock.json` snapshot of resolved values; downstream consumers diff against it to catch silent renames.

## AI-agent gotchas
- LLMs invent fictional `$type` values (`shadow-x`, `gradient-linear`). Constrain to the spec list (color, dimension, fontFamily, fontWeight, duration, cubicBezier, number, strokeStyle, border, transition, shadow, gradient, typography) in the prompt.
- Models add trailing commas and JS-style comments to JSON; require validators with strict JSON parsing.
- Aliases are easy to write but hard to reason about — agents create cycles. Have a deterministic cycle-check step before the LLM finalizes the file.
- "Composite" tokens (typography, shadow) trip up agents: they emit nested `$value` objects with bare strings instead of typed dimensions. Force `$type: "dimension"` plus `$value: { value, unit }`.
- Human checkpoint: after first DTCG generation, designer reviews semantic alias map manually. Wrong aliases propagate into every platform output.

## References
- DTCG Format Module: https://tr.designtokens.org/format/
- Style Dictionary v4: https://styledictionary.com
- Tokens Studio docs: https://docs.tokens.studio
- Lukas Oppermann, "Design tokens specification" walkthrough: https://lukasoppermann.com/blog/design-tokens-spec
- W3C Design Tokens Community Group: https://www.w3.org/community/design-tokens/
