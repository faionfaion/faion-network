# Design System Success Factors

## Summary

Four pillars that determine whether a design system succeeds: clear ownership (single DRI per pillar, not a committee), usable components (actually adoptable at v0), strong documentation (discoverable, non-decaying), and real adoption (measured across product, brand, and marketing). Ship lean, stress-test, gather feedback, grow iteratively. Tie adoption metrics to perf/a11y baselines so 100% coverage cannot hide quality regressions.

## Why

Most design system failures trace to one of the four pillars: no owner means nobody fixes drift; unusable components mean teams re-create UI off-system; missing documentation means discoverable only by word-of-mouth; adoption not measured means leadership defunds the work. Brad Frost's Atomic Design research and NNG adoption studies both show that governance and measurability predict long-term survival better than component quality.

## When To Use

- Diagnosing why a design system has low adoption (components built but unused).
- Bootstrapping a new system and choosing what to ship in v0 vs v1.
- Establishing adoption metrics and instrumentation before a design-ops review.
- Drafting governance/ownership models when multiple product teams contribute components.

## When NOT To Use

- Component-level decisions (button anatomy, color contrast, motion specs) — those need their own methodologies.
- Tooling-only choices (Figma vs Penpot, Storybook vs Histoire) — covered by tools methodologies.
- Pure brand/marketing systems with no engineering tie-in — adoption metrics assume product UI.

## Content

| File | What's inside |
|------|---------------|
| `content/01-four-pillars.xml` | Definitions, rules, and anti-patterns for each of the four success pillars. |
| `content/02-metrics-and-agents.xml` | Adoption metrics, agentic audit loop, recommended subagents, prompt patterns, gotchas. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ds-adoption.sh` | Shell script that counts design-system component usage vs raw HTML across TSX files. |
| `templates/pillar-critic-prompt.txt` | Structured-output prompt for a ds-pillar-critic subagent scoring all four pillars. |

## Scripts

none
