# Accessibility-First Design

## Summary

A design-phase methodology that prevents 70-80% of WCAG 2.2 issues before engineering begins. Enforce contrast ratios (4.5:1 body, 3:1 large/UI), touch targets (44x44px), visible focus states, semantic HTML structure, and motion controls at the design token and component-spec level. Issues caught at design time cost 5-10x less than post-launch remediation.

## Why

Most accessibility defects are traceable to decisions made during design: color choices, layout spacing, animation defaults. Catching them at the Figma/handoff stage removes them from the code-review and QA cycle entirely. Embedding a11y constraints in design tokens and component approval criteria makes compliance structural rather than manual.

## When To Use

- Starting a new product, design system, or major redesign.
- Establishing design-token contrast rules and focus-state baselines for a component library.
- Onboarding new designers — the checklist is the working agreement.
- Pre-handoff QA: validating Figma frames before engineering begins.

## When NOT To Use

- Pure code-fix sprints where designs are frozen — code-level a11y patterns (semantic HTML, ARIA, focus management) are the right tool.
- Marketing landing pages with one-off visual gimmicks — apply principles but don't gate launch on WCAG 2.2 AAA.
- When the design hasn't started — load design first; applying checklists too early constrains ideation.

## Content

| File | What's inside |
|------|---------------|
| `content/01-rules.xml` | Contrast ratios, touch-target minimums, focus-visible requirements, semantic structure rules, motion controls |
| `content/02-agent-patterns.xml` | Figma-API audit workflow, subagent roles, JSON output schema, gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/a11y_quick.ts` | Contrast ratio calculator + WCAG AA/AAA level check + touch-target size validator |

## Scripts

none
