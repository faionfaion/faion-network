# Mobile UX Basics

## Summary

A mobile-first design methodology covering touch target sizing, thumb-zone placement, navigation patterns, form optimization, performance budgets, and platform conventions (iOS vs Android). Start with the smallest screen, expose only essential features, then enhance for larger viewports. Touch targets must be at least 44x44pt (iOS) or 48x48dp (Android) with 8px spacing between them.

## Why

Desktop designs scaled down fail on mobile: touch targets are too small, primary actions fall outside the thumb zone, and 53% of users abandon pages that load in over 3 seconds. Mobile context (partial attention, short sessions, variable network) demands a distinct design approach, not a responsive rescaling of a desktop layout.

## When To Use

- Auditing an existing mobile experience for thumb-zone, touch-target, performance, and platform-convention compliance.
- Pre-launch checklist enforcement before each mobile release: Lighthouse mobile score, accessibility, touch-target sizes.
- Code review for mobile-affecting PRs: flagging small touch targets, hidden navigation, blocking JS, missing input types.
- Cross-platform parity reviews: same flow on iOS vs Android — list of platform-convention divergences.

## When NOT To Use

- Greenfield strategic mobile design — start with research (interviews, diary studies) before applying basics; this knowledge is downstream.
- Native-only platform-specific work where Apple HIG / Material 3 are the primary reference — load those directly.
- Single-component visual polish — that is UI/visual design feedback, not mobile-UX methodology.
- No mobile users in the product's audience — effort is wasted on unused contexts.

## Content

| File | What's inside |
|------|---------------|
| `content/01-principles.xml` | Mobile-first thinking, mobile context factors, five key principles, platform differences (iOS vs Android). |
| `content/02-design-rules.xml` | Touch target rules, thumb zone, navigation patterns, form best practices, gesture guidelines, accessibility requirements. |
| `content/03-performance.xml` | Core Web Vitals targets (LCP, FID/INP, CLS), optimization techniques, testing methods and device matrix. |

## Templates

| File | Purpose |
|------|---------|
| `templates/touch-target-audit.js` | Playwright script that flags tap targets smaller than 44x44 at iPhone 13 viewport. |
