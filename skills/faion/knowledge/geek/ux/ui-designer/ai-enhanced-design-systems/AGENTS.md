# AI-Enhanced Design Systems

## Summary

AI scales a mature design system by automating component documentation, detecting hardcoded token violations, and generating variant permutations — but only when the system already has well-defined tokens, systematic component structure, and clear naming conventions. AI amplifies the existing foundation; it does not create one.

## Why

Scaling design systems manually requires significant effort per component (props documentation, usage examples, accessibility notes, do/don't guidance). AI documentation generation and token audit scripts reduce this to minutes per component, while Chromatic visual regression catches AI-generated variant drift before merge.

## When To Use

- A mature design system exists with defined tokens and component structure; you want AI to scale it
- Automating component documentation generation from existing component code and stories
- Detecting token usage inconsistencies across a large codebase where manual audit is impractical
- Generating component variant permutations (size, state, density) from a seed component
- Producing design token suggestions when the system is evolving (new brand palette, dark mode)

## When NOT To Use

- The design system has no defined tokens, naming conventions, or systematic component structure — AI amplifies deficiencies
- You need AI to create the foundational design system from scratch — requires human-led design first
- The component library has fewer than 10 components — manual documentation is faster
- The primary problem is design-engineering alignment, not documentation scale — that is a process problem

## Content

| File | What's inside |
|------|---------------|
| `content/01-ai-capabilities.xml` | AI amplification principle; prerequisites; capability table; tool landscape |
| `content/02-workflow.xml` | Documentation generation pipeline; token audit workflow; variant generation rules |
| `content/03-anti-patterns.xml` | Semantic/primitive token confusion, deprecated Storybook API, interaction state gaps, gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/audit-hardcoded-tokens.sh` | Bash script: find hardcoded hex colors and px spacing not using CSS custom properties |
| `templates/prompt-document-component.txt` | Haiku prompt: component code + stories → full documentation with props table and a11y notes |
| `templates/prompt-audit-tokens.txt` | Sonnet prompt: codebase files → hardcoded value report with suggested token replacements |
