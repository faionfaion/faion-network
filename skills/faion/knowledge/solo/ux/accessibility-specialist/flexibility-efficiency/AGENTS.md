# Flexibility and Efficiency of Use

## Summary

Nielsen Heuristic #7: design for both novice and expert users simultaneously by providing accelerators (keyboard shortcuts, bulk operations, templates) that novices can ignore but experts use daily, plus progressive disclosure and multiple paths for the same goal.

## Why

Interfaces tuned only for beginners frustrate power users who repeat the same tasks hundreds of times per day. Interfaces tuned only for experts overwhelm newcomers. Layered flexibility — visible affordances plus hidden accelerators — lets one interface serve the full user spectrum without cognitive overload at either end.

## When To Use

- Designing or auditing productivity tools, admin panels, developer tools, or any app with repeat-use workflows
- Adding keyboard shortcut coverage to an existing web application
- Auditing whether an interface serves both novice onboarding and power-user acceleration
- Planning customization features (saved layouts, quick actions, pinned items) for SaaS products
- Evaluating CLI tools or APIs for efficiency affordances

## When NOT To Use

- One-time-use flows (checkout, onboarding wizard, password reset) — shortcuts add no value here
- Consumer apps with mostly casual, infrequent users — shortcut investment is wasted
- Early prototype stages before task flows are validated — optimizing efficiency before correctness is premature
- Accessibility-first flows where additional modalities must be layered carefully to avoid screen reader conflicts

## Content

| File | What's inside |
|------|---------------|
| `content/01-rules.xml` | Core flexibility rules: keyboard shortcuts, multiple paths, progressive disclosure, customization, bulk operations |
| `content/02-examples.xml` | Good examples (Figma, VS Code, Gmail) and antipatterns (no shortcuts, expert-only, no customization) |

## Templates

| File | Purpose |
|------|---------|
| `templates/flexibility-audit.md` | Audit table for shortcuts, customization options, alternative paths, and power-user features |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/find-shortcuts.sh` | Grep-based script to extract keyboard shortcut bindings from a JS/TS codebase |
