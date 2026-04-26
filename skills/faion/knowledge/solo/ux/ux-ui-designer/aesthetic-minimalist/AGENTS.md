# Aesthetic and Minimalist Design

## Summary

Nielsen Heuristic #8: every element in an interface competes with every other element for user attention. Classify all elements as Primary (essential for task completion), Secondary (helpful but not critical), Tertiary (nice-to-have, rarely needed), or Remove (no value). Apply progressive disclosure — show summaries, reveal details on demand. Define the screen's single primary task before auditing; all classification is relative to that task.

## Why

Cluttered interfaces increase cognitive load, slow task completion, and bury important content in visual noise. Every extra element added to a screen dilutes the relative visibility of every other element — this is not aesthetic preference but an empirically measured attention cost. Minimalist interfaces reduce decision fatigue, speed first-click success, and lower error rates. The constraint also forces product discipline: removing rarely-used features exposes which features actually matter.

## When To Use

- Evaluating a near-finished UI for visual noise and clutter before shipping
- Auditing a feature that has accumulated too many options after incremental additions
- Generating prioritized element-removal recommendations from a screenshot or design spec
- Pre-launch heuristic sweep as part of a broader usability review
- After each major feature addition — lightweight regression check for creeping complexity

## When NOT To Use

- Data-dense tools (analytics dashboards, trading platforms, IDEs) where density is the feature
- Early exploration or wireframing phases — minimalism audits are premature without final content
- When the root problem is information architecture, not visual presentation — fix IA first
- As a substitute for user testing — agent opinions on "noise" are not user behavior data

## Content

| File | What's inside |
|------|---------------|
| `content/01-principles.xml` | Content hierarchy (Primary/Secondary/Tertiary/Remove), visual hierarchy rules, progressive disclosure pattern, white space usage, techniques (remove/hide/organize/shrink) |
| `content/02-examples.xml` | Good examples (Google homepage, Apple product pages), bad examples (cluttered dashboards, feature overload), balance signals (too cluttered vs too minimal) |

## Templates

| File | Purpose |
|------|---------|
| `templates/content-audit.md` | Content audit table: element, purpose, user need, priority (P1-P3), action (keep/remove/hide); sections for visual elements and information density |
