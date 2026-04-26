# Architecture Decision Records

## Summary

ADRs capture significant architectural decisions with context, alternatives, and consequences. They prevent tribal knowledge loss and stop the same debates from recurring. Store ADRs in version control with code, not in wikis. Keep each ADR to 1-2 pages. Status lifecycle: Proposed → Accepted → Deprecated | Superseded. Never alter an accepted ADR — create a new one to supersede it.

## Why

Without ADRs, teams repeat the same architectural debates, new members lack context for existing design choices, and production incidents lack design rationale. ADRs are not design guides — they document the decision and why it was made, not how to implement it.

## When To Use

- Choosing frameworks, databases, or major dependencies
- Breaking API changes that require consumer migration
- Adopting architectural patterns (microservices, event-driven, CQRS)
- Quality attribute tradeoffs (security vs. performance, consistency vs. availability)
- Cross-team decisions affecting multiple services
- Making implicit standards explicit

## When NOT To Use

- Small, reversible decisions with low risk
- Implementation details that don't set a pattern
- Individual bug fixes or minor feature changes
- Items already covered by existing standards
- Single-developer, self-contained, minimal-risk choices

## Content

| File | What's inside |
|------|---------------|
| `content/01-adr-structure.xml` | Nygard format fields, status lifecycle, immutability principle, storage convention |
| `content/02-writing-process.xml` | Pre-writing gate, alternatives research, quality checks, agent limitations |

## Templates

| File | Purpose |
|------|---------|
| `templates/adr-template.md` | Nygard-format ADR stub (copy-paste) |
| `templates/new-adr.sh` | Shell script to create next-numbered ADR file |
