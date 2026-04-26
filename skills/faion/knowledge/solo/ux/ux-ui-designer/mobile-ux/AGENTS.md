# Mobile UX Design Basics

## Summary

Mobile UX requires mobile-first design (smallest screen first, then enhance), touch targets of at least 44x44pt (iOS) or 48x48dp (Android), primary actions in the thumb zone (bottom third of screen), and Core Web Vitals targets of LCP &lt; 2.5s / CLS &lt; 0.1. Navigation defaults to bottom tab bar (3-5 items); hamburger menus are secondary. One primary action per screen is a hard constraint.

## Why

Desktop designs scaled down to mobile produce tiny targets, broken layouts, and slow load times that cause abandonment. Mobile context differs fundamentally: partial attention, variable connectivity, touch input, smaller screen. Mobile-first design forces prioritization of essential content and interaction, which also improves the desktop version. 53% of users abandon pages that take more than 3 seconds to load on mobile.

## When To Use

- Starting a product or feature that must run on mobile (apply mobile-first from the design phase)
- Auditing an existing web product for mobile usability issues before a campaign or launch
- Reviewing PRs that add UI components — verify touch targets, input types, thumb-zone placement
- Before App Store or Google Play submission — checklist sweep against HIG and Material guidelines
- Performance audit for mobile: LCP, FID, CLS targets are more critical on mobile than desktop

## When NOT To Use

- Internal tools used exclusively on desktop (admin panels, dashboards accessed via VPN)
- Projects where mobile is explicitly out of scope for the current phase
- Prototyping in high fidelity before mobile constraints are validated — wireframe mobile flows first
- Accessibility-only audits — mobile UX overlaps but is not a replacement for dedicated a11y review

## Content

| File | What's inside |
|------|---------------|
| `content/01-principles.xml` | Mobile-first approach, thumb zone model, touch target minimums, navigation patterns, form optimization, performance targets (LCP/FID/CLS/TTI) |
| `content/02-platform.xml` | iOS vs Android differences (navigation, modals, touch targets), gesture standards, progressive enhancement tiers, accessibility requirements |

## Templates

none

## Scripts

| File | Purpose |
|------|---------|
| `scripts/mobile-audit.sh` | Lighthouse mobile audit: runs mobile preset, extracts Core Web Vitals + failed audits. Usage: `bash scripts/mobile-audit.sh https://example.com` |
