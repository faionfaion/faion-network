# Agent Integration — AI-Enhanced Design Systems

## When to use
- A mature design system exists with well-defined tokens and component structure, and you want AI to scale it (variants, documentation, consistency checks)
- Automating component documentation generation from existing component code and usage examples
- Detecting token usage inconsistencies across a large codebase where manual audit is impractical
- Generating component variant permutations (size, state, density) from a seed component definition
- Producing design token suggestions when a system is evolving (new brand palette, dark mode addition)

## When NOT to use
- The design system has no defined tokens, no naming conventions, and no systematic component structure — AI amplifies deficiencies, it does not fix them
- You need AI to create the foundational design system from scratch — this requires human-led system design first
- The component library has <10 components — manual documentation is faster than setting up AI automation
- The team's primary problem is design-engineering alignment, not documentation scale — that is a process problem, not an AI problem

## Where it fails / limitations
- AI-generated component variants inherit semantic errors from the seed component — bad foundations produce bad variants at scale
- Token suggestion quality degrades without color theory constraints in the prompt — AI will produce accessible ratios if asked, but defaults to aesthetically arbitrary values
- Inconsistency detection requires the agent to have access to the full codebase; partial context produces incomplete results
- Documentation generation for stateful components (focus, hover, disabled, error) requires the agent to understand interaction semantics, not just visual appearance
- AI does not understand the human/team adoption problem — a technically correct component that breaks existing usage patterns will be ignored

## Agentic workflow
A Claude subagent (Haiku) reads the existing component library source (Storybook stories, CSS/Tailwind classes, Figma export JSON) and generates Markdown documentation stubs for each component including props table, usage examples, accessibility notes, and do/don't guidance. A Sonnet subagent performs token audit across the codebase, finds hardcoded values (hex colors, px values) that should be token references, and produces a replacement report. Human design system leads review both outputs before merging to the system.

### Recommended subagents
- General Claude subagent (Haiku) — component documentation generation, token stub population
- General Claude subagent (Sonnet) — inconsistency detection, variant generation review, token suggestion critique

### Prompt pattern
```
You are a design system engineer. Given this component definition:
[component code + existing props + Storybook story]

Generate documentation with these sections:
1. Component purpose (1 sentence)
2. Props table (name | type | default | description)
3. Usage examples (3 code snippets: basic, with variants, with accessibility props)
4. Accessibility notes (keyboard, ARIA roles, screen reader behavior)
5. Do / Don't (2 examples each)
6. Token references (list which design tokens this component uses)
Do not invent props that are not in the component code.
```

```
You are auditing a codebase for design token compliance.
Given these files: [file list with content]
Find all hardcoded values that should be token references:
- Hex colors not using CSS custom properties
- Hardcoded px/rem spacing values not using spacing tokens
- Hardcoded font sizes not using typography tokens
For each finding: { file, line, hardcoded_value, suggested_token, confidence: High/Med/Low }
Flag Low confidence items for human review.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `style-dictionary` | Build token transforms across platforms (CSS vars, iOS, Android) | `npm install style-dictionary` / amzn.github.io/style-dictionary |
| `storybook` | Component documentation host; agent can generate stories | `npx storybook init` / storybook.js.org |
| `token-transformer` | Transform Figma Tokens plugin output to Style Dictionary format | `npm install token-transformer` |
| `chromatic` | Visual regression testing for design system components | `npm install chromatic` / chromatic.com |
| `eslint-plugin-import` | Detect direct color/spacing imports bypassing token layer | `npm install eslint-plugin-import` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Figma | SaaS | Yes — REST API | Read token/component data; agent can extract design specs programmatically |
| Figma Tokens plugin | SaaS plugin | Yes — JSON export | Export token JSON for Style Dictionary pipeline |
| Storybook | OSS | Yes — MDX/JSON | Agent generates .stories.tsx and .mdx docs files |
| Chromatic | SaaS | Yes — CLI + API | Visual diff detection for component changes |
| Supernova | SaaS | Yes — REST API | Design token management with multi-platform export |
| Specify | SaaS | Yes — REST API | Design asset + token sync between Figma and code |
| Zeroheight | SaaS | Partial — embed | Documentation host; agent can generate content, not publish directly |

## Templates & scripts
See `templates.md` for the component documentation template and token audit report template.

Token audit script (finds hardcoded hex colors in CSS/SCSS):
```bash
#!/usr/bin/env bash
# audit-hardcoded-tokens.sh
# Finds hardcoded hex colors and common px values not using CSS custom properties
set -euo pipefail

echo "=== Hardcoded Hex Colors ==="
grep -rn --include="*.css" --include="*.scss" --include="*.tsx" \
  -E '#[0-9a-fA-F]{3,8}(?![0-9a-fA-F])' \
  --exclude-dir=node_modules \
  . | grep -v 'var(--' | head -50

echo ""
echo "=== Hardcoded Spacing (px not in token pattern) ==="
grep -rn --include="*.css" --include="*.scss" \
  -E '[^-](\d{1,3}px)' \
  --exclude-dir=node_modules \
  . | grep -v 'var(--\|1px\|2px' | head -50
```

## Best practices
- Feed AI the token JSON and naming convention document as context before asking for any token suggestions — without it, AI invents names that violate the system's conventions
- Require the agent to reference existing token names when generating documentation — never allow it to create new token names without human approval
- Use AI for documentation first pass, not final text — component documentation must be verified by the engineer who built the component
- Set up Style Dictionary as the single source of truth before enabling AI variant generation — without it, AI variants will drift from the actual token values
- Run Chromatic visual regression testing on every AI-generated variant before merging — AI-generated code often has subtle visual differences from the design spec
- Documentation generation works best on components with good prop types (TypeScript) — poorly typed components produce poor documentation regardless of AI quality

## AI-agent gotchas
- AI-generated Storybook stories often use deprecated Storybook API (CSF 2 vs CSF 3) — specify the exact version in the prompt
- Token suggestion agents frequently confuse semantic tokens (--color-action-primary) with primitive tokens (--color-blue-500) — require explicit semantic/primitive distinction in the prompt
- Component variant generation requires the agent to understand disabled state, focus state, and error state independently — a prompt that only says "generate variants" produces only visual variants, missing interaction states
- Inconsistency detection on large codebases (>500 files) exceeds single-prompt context — chunk by directory and aggregate results
- Human-in-loop checkpoint: design system lead must review all AI-generated documentation and token suggestions before merging to the published system — inaccurate system docs cause widespread misuse

## References
- Style Dictionary: https://amzn.github.io/style-dictionary/
- Storybook: https://storybook.js.org/
- W3C Design Tokens Community Group: https://www.w3.org/community/design-tokens/
- NNGroup AI in design systems: https://www.nngroup.com/articles/ai-design-systems/
- Smashing Magazine AI design systems: https://www.smashingmagazine.com/2025/01/ai-design-systems/
