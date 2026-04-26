# Agent Integration — Consistency and Standards

## When to use
- Auditing a codebase or design system for visual, functional, and verbal inconsistencies before a release
- Generating a terminology glossary by scanning all UI copy across a product and surfacing synonym clusters
- Reviewing a new component or screen against an existing design system to flag deviations
- Enforcing design token usage in code (ensuring no hardcoded color/spacing values bypass the token system)
- Checking that action labels (Save, Delete, Edit) are used uniformly across all pages in a product

## When NOT to use
- Intentional divergence from convention for brand differentiation — consistency auditing is not the tool to adjudicate that decision
- Brand-new products with no existing design system; there is nothing to be consistent against yet
- Single-screen tools where cross-screen consistency is irrelevant

## Where it fails / limitations
- Automated consistency audits of visual design require design file access (Figma API or exported tokens); agents working from screenshots or descriptions have low recall
- Terminology audits on large codebases miss UI strings buried in i18n JSON files unless the agent explicitly searches those paths
- Platform convention violations (e.g., breaking iOS back-button behavior) require platform-specific knowledge the agent may not have; validate against platform HIG manually
- Design drift happens continuously — a one-time audit goes stale within weeks without a governance process to enforce it
- Agents cannot distinguish intentional exceptions ("this is a special one-time pattern") from accidental inconsistencies without context

## Agentic workflow
A Claude agent reads all UI copy from i18n files, component templates, or scraped live pages, and groups synonym clusters for the same UX concept (e.g., Save / Submit / Confirm / Apply for the same action type). It then produces a terminology audit report with a recommended canonical term per concept. Separately, an agent can scan a codebase for hardcoded CSS color and spacing values that bypass design tokens, generating a migration list. Both outputs feed into a design system backlog.

### Recommended subagents
- `faion-sdd-executor-agent` — enforces consistency ACs in feature specs (checks that new component specs reference the design system, not ad-hoc values)

### Prompt pattern
```
You are a UX consistency auditor. Given the following list of button labels found across the product UI:
[Save, Submit, Done, Confirm, Apply, OK, Update, Store]

Group these by the underlying UX action they represent. For each group:
- Recommended canonical term (prefer the most widely used or most conventional for this platform)
- Labels that should be replaced
- Screens/contexts where each variant was found

Output as a terminology audit table.
```

```
Review this React component file for hardcoded color or spacing values that bypass design tokens.
Flag any hex codes, rgb(), pixel values outside the 8px grid, or font-size literals.
For each finding: file, line, current value, recommended token replacement.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `stylelint` | Enforce design token usage in CSS/SCSS; catch hardcoded values | `npm i -g stylelint` / stylelint.io |
| `eslint-plugin-no-hardcoded-colors` | Flag literal color values in JSX/TSX | npm / community plugin |
| `grep` / `ripgrep` | Search i18n files and templates for synonym clusters | `apt install ripgrep` |
| `chromatic` | Visual regression testing — catches unintended visual changes between builds | `npm i -g chromatic` / chromatic.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Figma (Variables/Tokens) | SaaS | Yes — REST API | Read design token values; compare component usage across pages |
| Storybook | OSS | Yes | Enforce that all component variants are documented and tested; visual diff on deploy |
| Chromatic | SaaS | Yes — CI integration | Automated visual regression; flags consistency breaks on each PR |
| Token Studio (Figma plugin) | OSS | Partial | Exports design tokens as JSON; agent can diff between branches |
| Lokalise / Phrase | SaaS | Yes — API | Manages i18n strings; agent can query for synonym clusters across locales |
| Supernova | SaaS | Yes — API | Design system documentation; exposes component usage rules via API |

## Templates & scripts
See `templates.md` for the Consistency Audit template and Design System Component template.

```bash
#!/bin/bash
# Scan a project for hardcoded hex colors outside design tokens
# Usage: bash audit_colors.sh src/

DIR="${1:-src}"
echo "Scanning $DIR for hardcoded hex colors..."
rg --type tsx --type ts --type css \
  -n '#[0-9a-fA-F]{3,6}' "$DIR" \
  | grep -v '\.tokens\.' \
  | grep -v 'colors\.ts' \
  | awk -F: '{print $1 ":" $2 " → " $3}'
```

## Best practices
- Establish a design token system before writing component code — retrofitting tokens is 5x the work of starting with them
- Limit synonyms by documenting canonical terms in a shared glossary that both design and engineering reference; a single source of truth prevents drift
- Run a consistency audit at the start of each major feature cycle, not at the end — fixing inconsistencies mid-feature is cheaper than post-release
- For verbal consistency, pick the most common term in existing usage as the canonical, not the "best" term — migration cost of changing widespread usage is high
- Consistency checks in CI (Chromatic visual diff + stylelint token enforcement) are cheaper and faster than manual audits

## AI-agent gotchas
- Agents scanning i18n JSON for synonym clusters will false-positive on locale-specific idiomatic differences (e.g., "Submit" in en-US vs. "Send" in en-GB may both be correct) — scope audits to a single locale first
- LLMs proposing "canonical" terms may not know your platform conventions; always validate recommendations against platform HIG (Apple, Material, Windows Fluent)
- Visual consistency audits from screenshots are unreliable — agents see JPEG artifacts, not actual pixel values; use Figma API or computed CSS instead
- Agents tend to recommend the most common term as canonical, but "most common" in legacy code may be the wrong term — human final call required on canonical selection
- Consistency enforcement is a governance problem as much as a tooling problem; agent tooling without human review cycles will not prevent future drift

## References
- https://www.nngroup.com/articles/consistency-and-standards/
- https://www.designbetter.co/design-systems-handbook
- https://atomicdesign.bradfrost.com/
- https://material.io/design/introduction
- https://www.smashingmagazine.com/design-systems-book/
