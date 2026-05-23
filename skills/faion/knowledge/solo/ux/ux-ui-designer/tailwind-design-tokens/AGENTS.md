---
slug: tailwind-design-tokens
tier: solo
group: ux
domain: ux
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generate a tailwind.config.js + tokens.css + Style Dictionary config that bridges semantic design tokens to Tailwind utilities via CSS custom properties, with safelist coverage and RGB-channel opacity support.
content_id: "015e97fab8369c86"
complexity: medium
produces: config
est_tokens: 3700
tags: [tailwind, design-tokens, css-variables, theming, style-dictionary]
---
# Tailwind + Design Tokens

## Summary

**One-sentence:** Generate a tailwind.config.js + tokens.css + Style Dictionary config that bridges semantic design tokens to Tailwind utilities via CSS custom properties, with safelist coverage and RGB-channel opacity support.

**One-paragraph:** Map design tokens (colours, spacing, typography) to Tailwind's theme config via CSS custom properties so the design system and component library share a single source of truth. Inputs: Figma Variables export (or Style Dictionary input) + Tailwind major version. Output: a config bundle covering primitives (CSS vars), semantics (Tailwind theme references via `var(--token)`), dark-mode tokens, RGB-channel colours for opacity modifiers, and a safelist for dynamically assembled classes.

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- The project uses Tailwind (v3 or v4) and has a design-system requirement.
- A token source exists (Figma Variables, Style Dictionary input, or canonical CSS file).
- The Tailwind major version is known up front.

## Skip If (ANY kills it)

- Project does not use Tailwind — use Style Dictionary alone or raw CSS variables.
- Throwaway prototype where systematic tokens add cost without payoff.
- Design ops own tokens and code edits are locked.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Token source (Figma export / SD input / canonical CSS) | JSON / CSS | design ops |
| Tailwind major version (3 or 4) | doc | engineering |
| Dark-mode requirement | doc | PM |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/frontend-developer/component-architecture` | Components consume the tokens this config emits. |
| `solo/ux/ux-ui-designer/match-real-world` | Semantic token naming follows user mental model where possible. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules + skip-this-methodology fallback | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for the token-config bundle + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns with symptom + root-cause + fix | ~900 |
| `content/04-procedure.xml` | medium | 5-step procedure: source → primitives → semantics → dark-mode → safelist | ~600 |
| `content/05-examples.xml` | medium | Worked example: brand colour primitives + semantic mapping + dark mode | ~500 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `convert-figma-vars` | sonnet | Mechanical Figma-variable to SD-input mapping. |
| `compose-tailwind-config` | sonnet | Tailwind theme block composition with `var(--token)` refs. |
| `safelist-audit` | opus | Detect dynamically assembled class names that JIT cannot statically see. |

## Templates

| File | Purpose |
|------|---------|
| `templates/tailwind.config.js` | Tailwind theme skeleton referencing `var(--token-name)`. |
| `templates/tokens.css` | CSS custom-property layer (light + dark). |
| `templates/sd.config.js` | Style Dictionary build config. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-tailwind-design-tokens.py` | Validate the output artefact against the schema in `content/02-output-contract.xml`. | After subagent returns, before downstream consumer reads. |

## Related

- [[match-real-world]]
- [[wireframing]]
- [[visibility-of-system-status]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, Tailwind major version known, opacity modifiers required) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
