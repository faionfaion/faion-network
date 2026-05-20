---
slug: 1on1-template-managers
tier: geek
group: pm
domain: project-manager
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Reusable template for 1on1 template managers that codifies the structure, named fields, and decision points so each new instance ships in minutes instead of being re-invented.
content_id: "9c348d335fda2bd9"
tags: [1on1, pm, template]
---
# 1on1 Template Managers

## Summary

**One-sentence:** Reusable template for 1on1 template managers that codifies the structure, named fields, and decision points so each new instance ships in minutes instead of being re-invented.

**One-paragraph:** Reusable template for 1on1 template managers that codifies the structure, named fields, and decision points so each new instance ships in minutes instead of being re-invented. Once team is 5+ people the founder/PM does 4-8 weekly 1:1s. Faion has no template (agenda, growth-question rotation, blocker-escalation hand-off, doc-as-you-go). Adjacent to `feedback` in comms but that's about giving feedback, not running the meeting itself.

## Applies If (ALL must hold)

- You are starting a new instance of the artefact addressed by 1on1 template managers (kickoff, contract, brief, deck).
- The instance has a named owner and a target review date.
- Filled fields will be read by humans outside the author's team (clients, contractors, executives).
- Sensitive data (contract terms, salary, IP) is captured but redacted before broad sharing.

## Skip If (ANY kills it)

- First instance ever, no comparable past work — write freeform, extract a template after.
- One-off bespoke artefact (M&A doc, lawsuit, novel R&D) — template constrains the wrong axes.
- Localized cultural or regulatory context the template does not encode — start from local norms.

## Prerequisites

- Empty instance of the artefact created and named (filename, doc ID).
- Required input metadata reachable (parties, dates, scope, budget).
- Reviewer identified with deadline acknowledged.

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/pm/project-manager/AGENTS.md` | Parent skill context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | The 4 testable rules every application enforces | ~900 |
| `content/02-output-contract.xml` | essential | Required output schema, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 5 detector + repair clauses for known agent failures | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `structural_fill` | haiku | Slot in known fields from inputs |
| `ambiguity_resolution` | sonnet | Resolve open fields against context |
| `stakeholder_voice` | opus | Write narrative sections coherent with strategy |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema for the methodology's required output |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-output.py` | Enforce the output-contract before main agent accepts | After subagent returns, before commit/publish |

## Related

- parent skill: `geek/pm/project-manager/`
- peer methodologies: see siblings under `geek/pm/project-manager/`
- external: industry references cited inline in `content/01-core-rules.xml`
