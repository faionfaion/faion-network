# Generative UI Design

## Summary

Use AI tools (Galileo, Uizard, v0, Claude Artifacts, Relume) to generate multiple UI layout variants from a feature brief, then have a human select and refine. Generative UI accelerates ideation and rapid prototyping; it does not produce production-ready output. Claude Artifacts is the only agent-native path — the agent generates the artifact inline, the human reviews it, and the agent iterates based on feedback.

## Why

Manual UI creation is slow for early ideation when the team is undecided on layout patterns. Generating 3–5 variants simultaneously compresses the decision cycle. The key constraint: no tool produces accessible markup, correct component library usage, or brand-compliant output by default — human refinement is always required before production.

## When To Use

- Rapid ideation: generating 5–10 UI layout variants from a feature brief before any human design work starts
- Converting a written product spec into interactive prototypes for early stakeholder feedback
- Producing low-fidelity wireframe candidates that a designer then refines
- Generating alternative component implementations (card, list, grid) when the team is undecided
- Bootstrapping a new screen when design system tokens are already defined

## When NOT To Use

- Final, production-ready UI is expected — generative output requires significant designer refinement
- Strict brand compliance is mandatory from the first iteration — AI tools ignore brand guidelines unless explicitly constrained
- Component must integrate with an existing codebase — generated code often uses different component libraries
- WCAG AA/AAA accessibility is non-negotiable from day one — generated UIs consistently miss aria attributes and focus management
- The client or legal team cannot review IP of AI-generated design artifacts

## Content

| File | What's inside |
|------|---------------|
| `content/01-workflow.xml` | Tool comparison, AI design workflow stages, quality rules |
| `content/02-agent-integration.xml` | Agent-native path, prompt patterns, service catalog, gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/ui-generation-prompt.txt` | Structured prompt template for React/Tailwind UI generation |
| `templates/gen-ui.sh` | Batch v0 CLI generation script from a prompts file |
