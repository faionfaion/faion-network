# WCAG 2.2 Compliance

## Summary

Delta methodology for upgrading from WCAG 2.0/2.1 to 2.2 (published October 2023). Covers all 9 new success criteria, the removal of 4.1.1 Parsing, and the 5 new AA-level criteria most teams miss: 2.4.11 Focus Not Obscured, 2.5.7 Dragging Movements, 2.5.8 Target Size (24x24 CSS px minimum), 3.3.7 Redundant Entry, and 3.3.8 Accessible Authentication.

## Why

WCAG 2.2 is the emerging compliance baseline for 2025-2026 (EU EAA, ADA Title II follow-up). The delta from 2.1 is small but specific: drag alternatives, focus visibility with sticky headers, auth without cognitive tests, and no repeated form entry. Automated tools cover only a subset of 2.2 criteria; the rest require structured manual checks. Agents frequently confuse the WCAG 2.2 AA target size (24x24 CSS px) with the iOS HIG or AAA target (44x44 px).

## When To Use

- Auditing or upgrading a product from WCAG 2.0/2.1 to 2.2.
- Implementing WCAG 2.2 AA criteria in new components (drag, auth, multi-step forms).
- Writing acceptance criteria that reference 2.2 SC numbers.
- Future-proofing for ADA Title II extensions and EU EAA (EN 301 549 will incorporate 2.2).

## When NOT To Use

- General a11y triage on a new codebase — start with `a11y-testing` or `a11y-basics`.
- AT runtime testing — use `testing-with-assistive-technology`.
- Compliance paperwork / VPAT — use `regulatory-compliance-2026`.
- XR/spatial products — use `spatial-accessibility`; WCAG 2.2 does not fully cover them.

## Content

| File | What's inside |
|------|---------------|
| `content/01-new-criteria.xml` | All 9 new WCAG 2.2 SC with level, requirement, pass/fail examples, and implementation notes. |
| `content/02-migration-checklist.xml` | Quick-win vs. moderate vs. high-effort items; 4.1.1 Parsing removal; axe-core version requirements. |

## Templates

| File | Purpose |
|------|---------|
| `templates/target-size-playwright.js` | Playwright + axe test for 2.5.8 target size (24x24 CSS px) and 2.5.7 drag alternatives. |
