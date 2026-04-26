# Accessibility

## Summary

WCAG 2.1/2.2 AA compliance methodology for web UIs. Covers semantic HTML, ARIA usage (first rule: don't use ARIA), keyboard navigation, focus management, color contrast, form labeling, live regions, and automated testing with axe-core. Treat AA as the minimum for all public-facing work.

## Why

Automated tools (axe, Lighthouse) catch only 30-40% of accessibility issues; the remainder requires structural patterns — proper semantics, focus traps, live regions, keyboard support. Building in these patterns from the start costs far less than retrofitting them. EU EAA (June 2025) and US Section 508 create legal exposure for non-compliance in many product categories.

## When To Use

- All web development — treat WCAG 2.1 AA as the default minimum
- Public-facing applications, e-commerce, fintech, healthcare, government, education
- Components in a design system or library (fix once, benefit everywhere)
- Any flow tied to revenue — accessibility bugs convert into lost sales

## When NOT To Use

- Internal one-off scripts used by 1-2 people who do not use assistive tech (low ROI, still worth doing if cheap)
- Throwaway experimental prototypes — defer until validated
- "Skip a11y" is rarely correct; the question is always which effort level, not whether

## Content

| File | What's inside |
|------|---------------|
| `content/01-rules.xml` | Semantic HTML, ARIA usage rules, keyboard nav, focus management, color contrast |
| `content/02-checklist.xml` | Phase-by-phase implementation checklist: HTML, ARIA, forms, keyboard, color, images, testing |

## Templates

none
