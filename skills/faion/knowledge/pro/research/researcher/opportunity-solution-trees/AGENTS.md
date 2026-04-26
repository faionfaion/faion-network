# Opportunity Solution Trees

## Summary

A visual discovery framework (Teresa Torres) that connects a single business Outcome to Opportunities (customer needs, grounded in evidence), Solutions (3+ per opportunity for compare-and-contrast), and Assumption Tests (one falsifiable experiment per solution). Stored as YAML/JSON in git; visual tools (Vistaly, Miro) are render targets only.

## Why

Without an OST, teams jump to solutions before understanding the problem space, or maintain flat idea backlogs that cannot be prioritized by evidence. The tree structure enforces opportunity-first thinking, requires evidence citations per node, and separates "compare and contrast" from "commit" — reducing the risk of building the wrong thing confidently.

## When To Use

- Translating a single OKR or KPI into a discovery backlog of customer-rooted opportunities.
- Synthesizing user-research artifacts (interview notes, JTBD, tickets, NPS verbatims) into a navigable structure.
- Aligning PM/design/engineering on in-scope sub-problems before any solution is committed.
- Deciding between competing solution ideas under a fixed opportunity.
- Maintaining a living artifact during continuous discovery (weekly interviews, ongoing experiments).

## When NOT To Use

- Pure delivery/sprint planning — use a roadmap or Jira board instead.
- Compliance or contract-driven work where the opportunity is fixed and only execution remains.
- Single-developer side projects where outcome-to-solution distance is trivial.
- Crisis/incident response where speed beats discovery rigor.
- When you have zero customer evidence — an OST built from assumptions is a confident-looking lie.

## Content

| File | What's inside |
|------|---------------|
| `content/01-ost-structure.xml` | OST components, node types, evidence rules, compare-and-contrast requirement. |
| `content/02-agentic-pipeline.xml` | Subagent roles (synthesizer, solution-generator, experiment-designer, critic), prompt patterns. |
| `content/03-gotchas-and-tools.xml` | Failure modes, CLI tools, services, best practices for agent runs. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ost.yaml` | Canonical OST schema: outcome, opportunities, solutions, experiments with stable IDs. |
| `templates/ost-render.sh` | Converts ost.yaml → Mermaid diagram → SVG via mmdc. |

## Scripts

none
