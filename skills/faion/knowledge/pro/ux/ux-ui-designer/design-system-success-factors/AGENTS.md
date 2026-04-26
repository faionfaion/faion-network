# Design System Success Factors

## Summary

A framework for evaluating and growing design systems around four measurable pillars: clear ownership (dedicated responsible person/team), usable components (adoptable API and quality), strong documentation (findable and current), and real adoption (measured component coverage across products). Each pillar must be explicitly healthy for the system to succeed — any collapsed pillar predicts system abandonment.

## Why

Design systems fail most often not from technical debt but from governance and adoption gaps: no single owner, documentation that drifts from source, components teams work around. The four-pillar model makes failure modes explicit and measurable, enabling quarterly health checks and OKR-setting for platform teams.

## When To Use

- Standing up a new design system or evaluating build vs. adopt vs. wrap.
- Quarterly health check on an existing system: ownership, adoption, contribution, debt.
- Diagnosing why a system is being ignored (low component coverage, parallel snowflake CSS).
- Pre-merger or rebrand audit when two systems must be unified.
- Setting OKRs/KPIs for a platform team.

## When NOT To Use

- One-off marketing landing pages — a tokens file + Tailwind config is sufficient.
- Pre-product-market-fit prototyping — the pillars optimize for adoption, which assumes stable surface area.
- Teams with fewer than 3 designers and 1 frontend engineer — ownership pillar collapses, overhead exceeds value.
- Pure motion or brand-illustration systems — adoption metrics are not meaningful.

## Content

| File | What's inside |
|------|---------------|
| `content/01-pillars.xml` | Four pillars defined, MVP launch sequence, adoption metrics table |
| `content/02-agent-patterns.xml` | Agent audit workflow, coverage probe prompt, gotchas, tooling reference |

## Templates

| File | Purpose |
|------|---------|
| `templates/ds-coverage.mjs` | AST-based Node script: counts system vs snowflake primitive usage across consumer apps |

## Scripts

none
