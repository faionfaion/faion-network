---
slug: architect-skill-index-geek-tier
tier: geek
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "46a609b78e4c229f"
summary: A thin, opinionated geek-tier architect index that re-anchors the 50+ geek/sdlc-ai entries (spec-kit, plan-mode, RAG, graph reviewer) from the software architect's point of view — closing the perceived coverage gap without authoring new content.
tags: [index, software-architect, sdlc-ai, geek, navigation]
---
# Geek-Tier Software Architect Skill Index

## Summary

**One-sentence:** A thin, opinionated index that re-anchors the existing 50+ `geek/sdlc-ai/` entries (spec-kit, plan-mode, RAG reviewer, graph-vs-diff reviewer, governance rules) from the software architect's point of view — five role-shaped lenses that close the perceived coverage gap without authoring new content.

**One-paragraph:** Geek tier ships dozens of methodologies useful to architects, but they are organised by SDLC stage (lang, lint, test, mr, inc, sec, gov) — not by role. An architect entering the tier sees no `geek/dev/software-architect/` index and concludes "geek has nothing for me", missing actually-relevant content. This methodology is the missing index: five architect-shaped lenses (specification, plan-mode discipline, knowledge-base and RAG, merge-request review automation, governance + audit) that point into the relevant sibling methodologies in `geek/sdlc-ai/`. Output: a one-page navigation doc the architect reads on day 1 of geek-tier adoption, plus a per-lens reading order so adoption is incremental, not overwhelming.

## Applies If (ALL must hold)

- Reader is a software architect (or senior engineer with architecture responsibilities).
- Reader has access to geek tier.
- Reader is adopting AI-assistant tooling in their architecture practice.
- Existing `geek/sdlc-ai/` methodologies are loaded in the knowledge base.

## Skip If (ANY kills it)

- Reader is a generalist developer (use `pro/dev/software-architect/` first).
- Geek-tier `sdlc-ai` group has migrated or restructured — index references break; rebuild.
- Reader is using a different role-shaped index (e.g. ML engineer) — different lens.
- Reader prefers stage-shaped navigation already provided by `geek/sdlc-ai/AGENTS.md`.

## Prerequisites

- Geek tier access confirmed via tier-manifest.
- Reader has skim-read `geek/sdlc-ai/AGENTS.md` and recognises the stage groups.
- Reader has at least one concrete architecture task in flight (spec, ADR, review, audit).

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/sdlc-ai/AGENTS.md` (the group index) | The stage-shaped view; this methodology re-projects it. |
| `pro/dev/software-architect/SKILL.md` | Pro-tier architect skill; the geek-tier index complements it. |
| `geek/ai/claude-code/SKILL.md` | Tooling foundation referenced by several entries. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: index immutability, every entry must reference real methodology, reading-order discipline, lens cap, quarterly refresh | ~1100 |
| `content/02-output-contract.xml` | essential | Index file schema, per-lens reading order, navigation surface | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: broken refs, lens sprawl, stale ordering | ~1000 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `lens-validate` | haiku | Mechanical: confirm each lens entry points to a real path |
| `reading-order-suggest` | sonnet | Bounded judgement: given a task, suggest the lens + first 2 entries |
| `quarterly-refresh-audit` | sonnet | Walk the geek/sdlc-ai/ tree; flag new methodologies for inclusion |

## Templates

| File | Purpose |
|------|---------|
| `templates/architect-index.md` | The 5-lens index file the architect reads day 1 |
| `templates/lens-entry.json` | Schema for a single lens-entry record |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-index.py` | Walk the index; assert each entry's path exists | Pre-publish + quarterly |
| `scripts/quarterly-refresh.py` | Diff geek/sdlc-ai/ tree against the index; emit candidate-additions list | Quarterly |

## Related

- parent skill: `geek/dev/software-developer/`
- peer methodologies: cross-references the entire `geek/sdlc-ai/` group from an architect angle
- external: [Mark Richards architecture content](https://www.developertoarchitect.com/) · [Gregor Hohpe enterprise integration](https://www.enterpriseintegrationpatterns.com/)
