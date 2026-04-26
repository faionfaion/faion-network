# Mobile Responsive Design

## Summary

Mobile-first responsive design: base styles unconditional, `min-width` queries layer up. Breakpoints are derived from content, not device names. `clamp()` replaces stepwise media queries for typography and spacing. Container queries (`@container`) replace viewport queries inside components. Touch targets meet WCAG 2.5.8 minimum of 44x44 CSS px.

## Why

Desktop-first CSS requires complex `max-width` overrides that accumulate bugs on every layout change. `clamp()` fluid typography eliminates 30-50% of media queries. Container queries decouple component layout from viewport size, making components portable across different page regions. Agents routinely break mobile by lifting breakpoint values from Bootstrap or omitting `container-type: inline-size`.

## When To Use

- Greenfield site/app — set viewport meta, mobile-first base CSS, container queries from the first commit.
- Auditing an existing layout for breakpoint regressions, touch-target sizes, and CLS on small screens.
- Migrating from viewport-based to container-query-based responsive design.
- Configuring Tailwind breakpoints to match real content breakpoints, not device widths.

## When NOT To Use

- App is locked to a single device class (kiosk, tablet-only internal tool) — fixed layout is simpler.
- Framework already enforces mobile-first and the site passes Lighthouse mobile — adding breakpoints is busywork.

## Content

| File | What's inside |
|------|---------------|
| `content/01-mobile-first-css.xml` | Viewport meta, min-width query order, fluid clamp() typography/spacing, responsive images srcset/sizes. |
| `content/02-container-queries.xml` | container-type rule, @container syntax, touch-target floor, iOS dvh fix, responsive navigation pattern. |
| `content/03-antipatterns.xml` | Desktop-first overrides, device breakpoints, tiny touch targets, user-scalable=no a11y violation, srcset misuse. |

## Templates

| File | Purpose |
|------|---------|
| `templates/playwright-devices.ts` | Playwright config extract with mobile-chrome, mobile-safari, tablet, desktop projects. |

## Scripts

none
