# Agent Integration — Consistency and Standards

## When to use
- During a design system audit to identify component divergence across a product
- When onboarding a new designer or developer who needs to understand established conventions
- Before merging two products or brands that each have their own design language
- When a product has grown organically across teams and inconsistencies are causing user complaints
- As a quality gate before any major release: run a consistency check against the design system

## When NOT to use
- As a replacement for usability testing — consistent UI can still be confusing if the conventions chosen are wrong
- When no design system exists yet — consistency audit will find only noise; build the system first
- When the product is a single-screen tool with fewer than 5 interactive elements — overhead is not justified
- When intentional variation exists for differentiation (e.g., marketing landing pages intentionally differ from app UI)

## Where it fails / limitations
- Automated visual consistency checks (Storybook, design linters) catch token violations but miss contextual misuse — a correct token applied in the wrong semantic context passes the linter
- Component library adoption is rarely 100% in production code; engineers sometimes diverge under time pressure without the audit catching it
- Verbal consistency is the hardest to enforce: terminology drift happens in copy, tooltips, and error messages that are outside the design system scope
- Cross-platform consistency (web vs. mobile vs. email) requires separate audits and different convention hierarchies
- Over-enforcing consistency suppresses legitimate accessibility accommodations (e.g., larger touch targets on mobile are intentional, not inconsistent)

## Agentic workflow
A Claude subagent can audit terminology consistency across a codebase or content set: given a list of strings (button labels, navigation items, error messages), the agent identifies duplicates with different wording, flags terminology not in the glossary, and recommends the canonical term. For visual consistency, agents work best when given structured design token output (JSON from Figma plugin or Style Dictionary) rather than screenshots — pixel-level comparison is not a reliable LLM task.

### Recommended subagents
- Any general-purpose Claude subagent (Sonnet) — terminology audit, glossary generation, audit report synthesis
- `faion-sdd-executor-agent` — implement design token changes or component standardization tasks from the audit findings

### Prompt pattern
```
You are a UX consistency auditor. Below is a list of UI strings extracted from our product (button labels, navigation items, error messages, form labels). 

Tasks:
1. Identify groups of strings that represent the same action or concept but use different wording
2. For each group, recommend one canonical term and explain the choice
3. Flag any terms that conflict with common platform conventions (web, iOS, or Android as relevant)
4. Return JSON: [{ concept, variants: [...], canonical, rationale, platform_conflict: bool }]

Platform: [web | iOS | Android | all]
Approved glossary (if any): [terms]
UI strings: [list]
```

```
You are reviewing a design token file for consistency. Given the JSON token set below:
1. Identify tokens that have the same value but different names (likely duplication)
2. Identify naming convention violations (e.g., mixed camelCase and kebab-case)
3. Identify semantic tokens that reference raw values instead of semantic aliases
Return: [{ issue_type, token_name, current_value, recommendation }]

Token JSON: [JSON]
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `style-dictionary` | Build and lint design token files; validate naming | `npm i -g style-dictionary` / [styledictionary.com](https://styledictionary.com) |
| `chromatic` | Visual regression testing against Storybook baseline | `npm i -D chromatic` / [chromatic.com](https://www.chromatic.com) |
| `eslint-plugin-jsx-a11y` | Lint JSX for accessibility convention violations | `npm i -D eslint-plugin-jsx-a11y` / [github](https://github.com/jsx-eslint/eslint-plugin-jsx-a11y) |
| `alex` | Lint written content for inconsistent or insensitive language | `npm i -g alex` / [alexjs.com](https://alexjs.com) |
| `textlint` | Enforce terminology rules in Markdown/HTML docs | `npm i -g textlint` / [textlint.github.io](https://textlint.github.io) |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Figma | SaaS | Yes — REST API | Agent can pull all text nodes and component usages via API for consistency check |
| Storybook | OSS | Yes | Run visual diffs via Chromatic; agents can generate story files for new components |
| Zeroheight | SaaS | Partial | Design system documentation; no programmatic write API |
| Supernova | SaaS | Yes — API | Design token sync from Figma to code; automation-friendly |
| Style Dictionary | OSS | Yes | Token transformation pipeline; fully scriptable |

## Templates & scripts
See `README.md` for the Consistency Audit and Design System Component templates.

Script — extract all unique button label strings from a React codebase for terminology audit:
```bash
#!/usr/bin/env bash
# Finds all Button component labels in JSX files
# Usage: bash extract-button-labels.sh ./src/
grep -r --include="*.tsx" --include="*.jsx" \
  -h "<Button" "${1:-.}" \
  | grep -oP '(?<=>)[^<]{1,60}(?=<\/Button>)' \
  | sort -u
```

## Best practices
- Establish a single source of truth for the approved glossary before auditing — without it, "canonical" choices become opinion battles
- Treat design tokens as the enforcement layer: if a value is not in the token file, it should not exist in production code; make this a lint rule
- Run consistency audits incrementally (per component or feature) rather than as a one-time big-bang exercise; ongoing audits catch drift earlier
- When resolving terminology conflicts, default to the platform convention (iOS HIG, Material Design, W3C) before internal preference
- Document decisions with rationale: "we use 'Delete' not 'Remove' because…" — undocumented decisions get re-litigated
- Assign a design system owner to triage new inconsistency reports; without an owner, findings accumulate without resolution

## AI-agent gotchas
- Agents cannot see rendered UI — they audit source code, token files, or exported strings; visual auditing still requires a human or a dedicated visual regression tool
- Terminology audit output will include false positives when the same word has legitimately different meanings in different contexts (e.g., "Archive" as action vs. "Archive" as section label)
- Agents may suggest overly rigid canonical terms that reduce clarity — always have a UX writer or product owner validate the recommendation before enforcing
- Do not ask an agent to both identify inconsistencies and generate the updated design system documentation in one call — scope creep degrades both outputs
- When auditing large codebases, the agent needs context about intentional variants (e.g., mobile vs. desktop button text) — provide an exclusion list or the output will flag valid differences

## References
- [Consistency and Standards Heuristic — NNG](https://www.nngroup.com/articles/consistency-and-standards/)
- [Design Systems Handbook — InVision](https://www.designbetter.co/design-systems-handbook)
- [Atomic Design — Brad Frost](https://atomicdesign.bradfrost.com/)
- [Style Dictionary Docs](https://styledictionary.com)
- [Material Design System](https://m3.material.io/)
