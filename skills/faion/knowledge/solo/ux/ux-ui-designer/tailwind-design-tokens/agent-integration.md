# Agent Integration — Tailwind + Design Tokens

## When to use
- Setting up a new project's design system foundation — define tokens once, use everywhere
- Migrating hardcoded hex values and magic numbers to a semantic token system
- Bridging a Figma design system (with Variables/Tokens) to a Tailwind CSS implementation
- Multi-brand or white-label products where the same component library needs per-tenant theming
- When a team uses both Tailwind utility classes and custom components and wants them to share the same values

## When NOT to use
- Projects with a single component and no design system requirements — raw Tailwind utilities suffice
- Teams not using Tailwind at all — use CSS custom properties directly or a dedicated token tool (Style Dictionary)
- Projects where design tokens are owned by a design ops team and not to be edited in code
- Prototype/throwaway work where systematic tokens add overhead with no payoff

## Where it fails / limitations
- Tailwind JIT purges unused classes — if token-mapped classes are constructed dynamically (string concatenation), they get purged; use safelist or full class names
- CSS variable-based tokens lose Tailwind's opacity modifier syntax (`bg-primary/50` doesn't work with `var(--color-primary)` without explicit alpha channel setup)
- Token naming conventions differ between Figma Variables, Style Dictionary, and Tailwind config — misalignment causes drift between design and code
- Dark mode with CSS variables requires careful scoping (`:root` vs `[data-theme="dark"]`) — Tailwind's built-in `dark:` variant may conflict
- Token inheritance (semantic → primitive → alias) flattens in `tailwind.config.js` unless structured deliberately

## Agentic workflow
An agent can generate a complete `tailwind.config.js` token layer from a token JSON file (W3C DTCG format or Style Dictionary output), enforce naming conventions across the codebase by scanning for hardcoded values, and scaffold per-theme CSS variable files. The primary human checkpoint is the token taxonomy decision (which token names are semantic vs. primitive) — this is a design decision agents should not make without design system specs. Agents should also not auto-merge generated configs without a design review of the visual output.

### Recommended subagents
- general code agent — scans codebase for hardcoded color/spacing values that should be replaced with token references
- `faion-usability-agent` — reviews component screenshots for token violations (inconsistent spacing, off-brand colors)

### Prompt pattern
```
Given this token JSON (W3C DTCG format), generate a tailwind.config.js `theme.extend` block.
Rules:
- Colors: map each token to `var(--color-<token-name>)`
- Spacing: map each token to `var(--spacing-<token-name>)`
- Typography: fontFamily, fontSize, lineHeight as separate sub-objects
- Do not hardcode any hex values in the config — all values must reference CSS variables
Output the config block and a companion globals.css with all CSS custom property declarations.
```

```
Search the following codebase files for hardcoded hex colors and pixel spacing values
that are NOT using Tailwind token-mapped classes. List each occurrence with file:line
and the equivalent token class it should use.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `style-dictionary` | Transform W3C token JSON to multiple platform outputs (CSS vars, Tailwind config, iOS/Android) | `npm i -g style-dictionary` / styledictionary.com |
| `tailwindcss` CLI | Build and inspect generated CSS; verify token-mapped utilities are present | `npm i -D tailwindcss` / tailwindcss.com/docs/installation |
| `token-transformer` | Convert Figma Tokens Plugin JSON to Style Dictionary format | `npm i -g token-transformer` / github.com/tokens-studio/token-transformer |
| `theo` | Salesforce token transformation tool, alternative to Style Dictionary | `npm i -g theo` / github.com/salesforce-ux/theo |
| `postcss-cli` | Process CSS variable files for production builds | `npm i -D postcss-cli` / postcss.org |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Tokens Studio (Figma plugin) | SaaS | Yes — exports JSON to Git | Best Figma-to-code token bridge; agent reads exported JSON and generates Tailwind config |
| Style Dictionary | OSS | Yes — Node.js API | De-facto standard for token transformation; agents invoke via Node script |
| Storybook | OSS | Partial — plugin API | Documents token usage in components; agent can generate addon-docs stories from token catalog |
| Chromatic | SaaS | Yes — CLI | Visual regression testing for token changes; catches unintended visual changes after token updates |
| Supernova | SaaS | Yes — REST API | Design token management platform with Tailwind export; good for large teams |
| Specify | SaaS | Yes — REST API | Token sync from Figma to code; agent can pull updated tokens via API |

## Templates & scripts
Style Dictionary build script for Tailwind + CSS variables (≤50 lines):
```javascript
// sd.config.js — run with: node sd.config.js
const StyleDictionary = require('style-dictionary');

StyleDictionary.registerTransform({
  name: 'css/var-name',
  type: 'name',
  transformer: (token) =>
    `--${token.path.join('-').toLowerCase().replace(/\s+/g, '-')}`
});

StyleDictionary.registerFormat({
  name: 'tailwind/tokens',
  formatter: ({ dictionary }) => {
    const colors = {};
    const spacing = {};
    dictionary.allTokens.forEach(token => {
      const varName = `var(--${token.name})`;
      if (token.path[0] === 'color') {
        colors[token.path.slice(1).join('-')] = varName;
      } else if (token.path[0] === 'spacing') {
        spacing[token.path.slice(1).join('-')] = varName;
      }
    });
    return `module.exports = ${JSON.stringify({ colors, spacing }, null, 2)}`;
  }
});

module.exports = {
  source: ['tokens/**/*.json'],
  platforms: {
    css: {
      transforms: ['attribute/cti', 'css/var-name', 'color/hsl'],
      buildPath: 'src/styles/',
      files: [{ destination: 'tokens.css', format: 'css/variables' }]
    },
    tailwind: {
      transforms: ['attribute/cti', 'css/var-name'],
      buildPath: 'src/',
      files: [{ destination: 'tw-tokens.js', format: 'tailwind/tokens' }]
    }
  }
};
```

## Best practices
- Separate primitive tokens (raw values: `#1A73E8`) from semantic tokens (`color.action.primary`) — Tailwind config should only expose semantic tokens
- Use CSS custom properties as the bridge: Tailwind `theme` references `var(--token)`, CSS defines the actual value — enables runtime theming without rebuilding
- Add Tailwind's `safelist` for any token-based classes assembled dynamically to prevent JIT purge
- Run visual regression tests (Chromatic or Percy) after every token update — a single spacing token change can affect hundreds of components
- Document token usage in Storybook with a dedicated "Design Tokens" page showing swatches and spacing scale
- Keep token names consistent with Figma Variables names — one-to-one mapping reduces translation errors
- Version tokens independently from component code when supporting multiple design system versions

## AI-agent gotchas
- Agents regenerating `tailwind.config.js` from tokens may overwrite manual theme customizations (e.g., custom `screens` breakpoints) — always merge, never replace the full config
- Tailwind v3 vs. v4 config format differs significantly; confirm version before generating (v4 uses CSS-first config, not `tailwind.config.js`)
- Agents do not know which token changes are breaking vs. additive — a color token rename is a breaking change if hardcoded class names exist in templates
- CSS variable opacity modifiers (`text-primary/50`) require the token value to be in RGB channels format, not hex — agents often miss this constraint
- Generated token files need human visual review — agents cannot verify that `--color-primary` actually looks correct on screen

## References
- https://tailwindcss.com/docs/theme
- https://styledictionary.com/
- https://www.smashingmagazine.com/2022/05/you-dont-need-ui-framework/
- https://tokens.studio/ (Tokens Studio for Figma)
- https://www.w3.org/community/design-tokens/ (W3C DTCG token spec)
- https://tailwindcss.com/docs/customizing-colors#using-css-variables
