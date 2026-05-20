---
slug: role-cheatsheet-generator
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: Role Cheatsheet Generator: auto-builds a per-role one-pager of the top-N faion methodologies from corpus + role-tag metadata so every PM/Architect/QA/DevOps opens the same path.
content_id: "43612aea9d2d89f5"
tags: [role-cheatsheet-generator, sdlc-ai, geek]
---
# Role Cheatsheet Generator

## Summary

**One-sentence:** Generate a per-role one-pager (PM, Architect, QA, DevOps, etc.) listing the top-N faion methodologies for that role, derived deterministically from the corpus and role-tag metadata so every team member opens the same canonical path.

**One-paragraph:** When a team adopts faion org-wide, the team-wide-methodology-base pain ("each dev googles differently") returns at the next layer up: each role opens a different faion path for the same situation. This methodology defines how to auto-generate a `cheatsheet-<role>.md` artefact from (a) corpus-wide role-tag metadata, (b) blocks_count / flagged_by_units priority signals, and (c) the org's tier so the cheatsheet only references content the team can actually read. Output is a stable, regeneratable, tier-aware top-10 list that can ship as `faion cheatsheet --role architect` and be diffed across releases.

## Applies If (ALL must hold)

- the corpus has role-tag metadata (role-product-manager, role-software-architect, role-devops-engineer, role-qa, etc.) on at least 80% of methodologies for the target role
- a tier policy is set (the cheatsheet must not list content above the org's tier)
- the generator output is consumed by humans opening it during work, not by an LLM at runtime
- tier == geek (the generator is an internal tool, not customer-facing content)

## Skip If (ANY kills it)

- role-tag coverage is below 80% — generate tags first; a partial cheatsheet teaches the wrong defaults
- the org already maintains a hand-curated cheatsheet that is actively reviewed every release — extend it, do not replace
- the role does not yet have ≥10 distinct methodologies in the corpus (output would be padding)

## Prerequisites

- corpus index with per-methodology role tags
- tier-manifest.json snapshot
- priority signal: blocks_count or flagged_by_units count per methodology
- target role name (must match a known role-tag slug)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/sdlc-ai/kb-agents-md-context-pyramid` | corpus-as-context pattern this generator implements |
| `geek/sdlc-ai/team-mode-cli-flag` | tier and team-mode awareness for output gating |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: deterministic-ordering, tier-gated, role-tag-source-of-truth, regeneratable-not-edited, top-n-cap | ~1100 |

## Related

- parent skill: `geek/sdlc-ai/`
- upstream playbook: `p6-product-dev-team/Adopt faion org-wide and override with company patterns`
- adjacent methodology: `geek/sdlc-ai/kb-symbol-index-fresh-tags`
