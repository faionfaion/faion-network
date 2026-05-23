---
slug: role-cheatsheet-generator
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates a deterministic per-role one-pager (`cheatsheet-<role>.md`) listing the top-10 faion methodologies for that role, filtered to the org's tier, derived from corpus role-tag metadata + priority signals.
content_id: "b5e16e55fea38611"
complexity: medium
produces: report
est_tokens: 3300
tags: [role-cheatsheet-generator, sdlc-ai, geek, corpus-tools]
---
# Role Cheatsheet Generator

## Summary

**One-sentence:** Generates a deterministic per-role one-pager (`cheatsheet-<role>.md`) listing the top-10 faion methodologies for that role, filtered to the org's tier, derived from corpus role-tag metadata + priority signals.

**One-paragraph:** When a team adopts faion org-wide, each role (PM / Architect / QA / DevOps) opens a different faion path for the same situation. This methodology produces a regeneratable, tier-aware top-10 cheatsheet per role: input = (corpus version, role, tier); output = byte-identical `cheatsheet-<role>.md` ordered by priority signal → role-tag-match → slug. Manual overrides live in a separate `cheatsheet-<role>.overrides.md` so the regenerate-from-scratch property survives.

**Ефективно для:**

- Team-wide faion adoption, де PM/Architect/QA відкривають різні шляхи.
- Onboarding: одна канонічна сторінка per role.
- Audit: cheatsheet diff across corpus releases показує, що змінилось.
- Tier-gated org: cheatsheet не містить content вище за org-tier.

## Applies If (ALL must hold)

- Corpus has role-tag metadata on ≥80% of methodologies for the target role.
- A tier policy is set (cheatsheet must not list content above org tier).
- Generator output is consumed by humans during work, not by an LLM at runtime.
- Tier == geek (internal tool, not customer-facing content).

## Skip If (ANY kills it)

- Role-tag coverage &lt;80% — generate tags first; partial cheatsheet teaches the wrong defaults.
- Org already maintains a hand-curated cheatsheet reviewed every release — extend it, do not replace.
- Role does not yet have ≥10 distinct methodologies in the corpus.
- Customer-facing context — methodology content is CLI-only by policy.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Corpus index | XML / JSON | faion-network |
| Role-tag metadata | per-methodology frontmatter `role:` list | corpus |
| Priority signal | blocks_count or flagged_by_units | corpus |
| tier-manifest snapshot | JSON | faion-network |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[mr-graph-vs-diff-reviewer]] | Corpus-graph traversal pattern reused here. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip-rule + rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | 700 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns (symptom/root-cause/fix) | 600 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with decision gates | 500 |
| `content/05-examples.xml` | essential | Worked report example end-to-end | 400 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion ref=rule-id | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `corpus_filter` | haiku | Mechanical filter by role-tag + tier. |
| `priority_rank` | haiku | Sort by priority signal + tie-breakers. |
| `overrides_merge` | sonnet | Light judgement merging human override file. |

## Templates

| File | Purpose |
|------|---------|
| `templates/cheatsheet-skeleton.md` | Generated cheatsheet skeleton with header + numbered list of 10 methodologies. |
| `templates/cheatsheet-overrides-skeleton.md` | Override skeleton — pinned entries that survive regenerate. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-role-cheatsheet-generator.py` | Validate generated cheatsheet artefact + verify tier-gating + deterministic header. | Pre-merge of every regenerate |

## Related

- [[mr-graph-vs-diff-reviewer]]
- [[task-agent-drafts-spec-before-coding]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from observable signals (role-tag coverage, role methodology count, tier policy) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether to invoke the generator — the tree terminates either on the active rule or on `skip-this-methodology`.
