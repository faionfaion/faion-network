---
slug: retro-adr-workflow
tier: pro
group: software-architect
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "6d1a94dbe2132d84"
summary: Sanctioned no-blame workflow for capturing architectural decisions AFTER code has already shipped — Retroactive ADRs — so undocumented decisions become audit-able without freezing delivery.
tags: [adr, architecture, documentation, retro, no-blame]
---

# Retroactive ADR Workflow

## Summary

**One-sentence:** No-blame workflow for capturing architectural decisions retroactively (Retro-ADRs) when code has shipped ahead of docs, so undocumented choices become auditable without stalling delivery.

**One-paragraph:** ADR (Architecture Decision Records) methodology assumes decisions are written before the code lands. In practice — especially in fast solo / agency / startup teams — code routinely ships ahead of any written decision. The result is months of "tribal knowledge" that nobody admits to and nobody captures. Generic ADR docs offer no sanctioned path to write an ADR after the fact, so people don't. This methodology pins the Retro-ADR pattern: identify undocumented decisions via signal (PR comments, repeated questions, surprise behaviour), batch them in a 90-minute weekly capture, write the ADR using a constrained template that distinguishes intent-at-time vs reconstructed-now, and adopt with explicit `status: accepted-retroactively`. No blame, no rewriting history. Mechanism: a recurring ritual + a template + a discovery signal. Primary output: ADRs that close the documentation gap without demanding heroic memory work.

## Applies If (ALL must hold)

- codebase already has architectural decisions that ship undocumented OR partially documented
- team has authority to adopt the ADR pattern in this repo
- ≥1 senior engineer or architect is available 90 min/week for the capture ritual
- repo has a `docs/adr/` or equivalent location for decision records
- the team accepts retroactive documentation is valuable (not just forward-looking)

## Skip If (ANY kills it)

- team is greenfield with no shipped code — use the standard ADR-from-the-start methodology
- team explicitly rejects ADRs as a practice — fix that conversation first
- the codebase has ≥3 architects who actively disagree about decisions — Retro-ADR amplifies the disagreement; resolve the architecture-review process first
- nobody can remember the original intent of any decision — write Decision-Archaeology notes instead and rebuild a baseline

## Prerequisites

- ADR template adopted (MADR, Nygard, or similar)
- a place to publish: `docs/adr/`, `architecture/decisions/`, Confluence space, etc.
- discovery signals enabled: PR-comment scraper, repeated-question detector in chat, or simple a backlog of "things we never wrote down"
- agreement that retroactive status is honest, not lesser than forward-looking ADRs

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/software-architect/adr-canonical-template` | The base template Retro-ADRs extend |
| `pro/dev/software-architect/architecture-fitness-functions` | Fitness checks reference recently-captured decisions |
| `pro/dev/software-architect/architecture-review-cadence` | Retro-ADR capture is one item on the review agenda |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: no-blame framing, retroactive status field, intent vs reconstruction, weekly cadence, single-owner sign-off | ~1000 |
| `content/02-output-contract.xml` | essential | Retro-ADR template, frontmatter schema, status enum, traceability fields | ~800 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: blame-leak, retro-as-rewrite, batch overload, stale capture, conflict between authors, etc. | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `discovery_from_pr_comments` | sonnet | Cluster PR threads referencing undocumented decisions |
| `retro_adr_first_draft` | sonnet | Draft from PR thread + commit history + chat snippets |
| `intent_vs_reconstruction_split` | opus | Distinguish what was decided then vs reconstructed now |
| `adr_lint` | haiku | Frontmatter + status check |

## Templates

| File | Purpose |
|------|---------|
| `templates/retro-adr.md` | Retro-ADR template with intent + reconstruction fields |
| `templates/discovery-signal-rubric.md` | How to score undocumented decisions for capture priority |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/discover-undocumented-decisions.py` | Scan PR comments + chat exports for repeated architectural questions | Weekly cron before capture ritual |
| `scripts/lint-retro-adr.py` | Verify retro-status is set, sources cited, owner named | Pre-commit hook in docs/adr/ |

## Related

- parent skill: `pro/dev/software-architect/`
- peer methodologies: `adr-canonical-template`, `architecture-fitness-functions`, `architecture-review-cadence`, `decision-archaeology`
- external: [Michael Nygard original ADR](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) · [MADR template](https://adr.github.io/madr/) · [ThoughtWorks ADR tech radar](https://www.thoughtworks.com/radar/techniques/lightweight-architecture-decision-records)
