# Generative UI Design

## Summary

Methodology for using AI generation tools (v0 by Vercel, Claude Artifacts, Galileo, Uizard, Relume) to produce multiple UI variants rapidly in the ideation phase. The loop is: agent generates 3–5 variants → human selects and critiques → agent refines → human verifies accessibility → done. Generated output is a forcing function for critique, not a finished deliverable.

## Why

Blank-canvas paralysis and slow single-variant design cycles are the primary bottlenecks in early UI exploration. Generating 5–10 variants in parallel from a single brief reduces the cost of exploration to near-zero, surfaces the design space faster, and gives teams concrete artifacts to critique rather than abstract concepts to debate. Every variant must still be verified for accessibility and brand compliance before use.

## When To Use

- Rapid ideation: generating 5–10 UI variants from a brief to explore design space
- Prototyping flows for investor demos or usability tests where visual polish is secondary
- Generating React/HTML component code from design descriptions (v0, Claude Artifacts)
- Reducing blank-canvas paralysis on new projects
- Creating low-fidelity wireframe sets across multiple screen sizes in parallel

## When NOT To Use

- Brand-critical production interfaces — AI generation does not understand brand nuance reliably
- Accessibility-first projects — generative outputs routinely miss focus management, ARIA roles, contrast
- Design system contributions — generated components bypass token and variant governance
- When the design problem requires deep user research insight — generation amplifies assumptions
- Final developer handoff — generated code requires significant cleanup before production

## Content

| File | What's inside |
|------|---------------|
| `content/01-tools-and-workflow.xml` | Tool landscape, generation loop, quality rules, agent/human responsibility split |
| `content/02-agentic-workflow.xml` | Subagent patterns, prompt templates, batch generation script reference, gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/batch-generate.py` | Generate multiple UI variants via Claude API in a single batch |
| `templates/prompt-ui-variants.txt` | Prompt for generating 3 styled React component variants |
| `templates/prompt-ui-critique.txt` | Prompt for auditing generated UI for WCAG, ARIA, and brand violations |
