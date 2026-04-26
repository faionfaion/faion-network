# Mobile Responsive Design

## Summary

Mobile-first CSS design: start with styles for the smallest viewport, enhance progressively for larger screens. Use relative units (rem, %, clamp()), CSS Grid/Flexbox for layout, viewport meta tag, and touch targets of at least 44x44px. No fixed pixel widths above 1px borders.

## Why

Over 60% of web traffic comes from mobile devices. Desktop-first CSS generates complex mobile overrides that accumulate technical debt. Mobile-first produces simpler, more maintainable code and ensures the smallest-resource experience works correctly.

## When To Use

- Any web UI: mobile-first is the default, not an option.
- Auditing an existing site for mobile regressions after redesign.
- Generating Tailwind configs, Storybook stories, or component libraries.
- Any UI that must render correctly from 320px to 1920px.

## When NOT To Use

- Internal admin tools targeting fixed-resolution kiosks or desktop-only dashboards.
- Embedded WebViews where the host app fixes the viewport (e.g., Telegram WebApp pinned to mobile).
- Print stylesheets, PDF generators, static reports — different rendering model.
- Native mobile (React Native, Flutter, SwiftUI) — different layout primitives.

## Content

| File | What's inside |
|------|---------------|
| `content/01-css-rules.xml` | Viewport meta, mobile-first media queries, fluid typography with clamp(), responsive images, touch targets. |
| `content/02-components.xml` | Responsive navigation pattern (React + CSS), responsive tables, container queries. |
| `content/03-antipatterns.xml` | Fixed widths, desktop-first, device-specific breakpoints, tiny touch targets, horizontal scroll. |

## Templates

| File | Purpose |
|------|---------|
| `templates/responsive-check.ts` | Playwright script: screenshot at 3 viewports, detect horizontal scroll overflow. |
