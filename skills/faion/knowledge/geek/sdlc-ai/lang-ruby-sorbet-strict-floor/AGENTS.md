---
slug: lang-ruby-sorbet-strict-floor
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: For any Ruby file an AI agent may modify autonomously, declare # typed: true (or stricter), generate Tapioca RBIs for every gem + Rails DSL, and gate the PR on `srb tc` + `tapioca check-shims`.
content_id: "7c5cf570e4459468"
complexity: medium
produces: config
est_tokens: 3700
tags: [ruby, sorbet, tapioca, static-types, rails]
---
# Ruby Sorbet Strict Floor with Tapioca RBI

## Summary

**One-sentence:** For any Ruby file an AI agent may modify autonomously, declare # typed: true (or stricter), generate Tapioca RBIs for every gem + Rails DSL, and gate the PR on `srb tc` + `tapioca check-shims`.

**One-paragraph:** Ruby Sorbet Strict Floor with Tapioca RBI produces a config artefact for the sdlc-ai domain. It pins observable preconditions, scores candidate decisions against ≥5 testable rules, fails fast on disqualifiers, and emits a schema-validated output. The methodology routes between apply and skip-this-methodology via an explicit decision tree so downstream agents never run it on an unsuitable input.

**Ефективно для:**

- Rails monolith with AI agents authoring controllers / models.
- Ruby library publisher needing type-checked surface.
- Codebase where dynamic dispatch keeps causing runtime errors agents miss.
- Team adopting types incrementally per-file.

## Applies If (ALL must hold)

- Ruby 3.0+, Bundler-managed gems.
- Repo can commit sorbet/ directory with RBIs.
- CI can run `srb tc` + `tapioca check-shims`.
- Team accepts per-file `# typed:` sigils.

## Skip If (ANY kills it)

- Ruby < 2.7 — Sorbet support patchy.
- Project relies on heavy meta-programming Sorbet can't model.
- Team has Steep/RBS as standard — don't mix two type systems.
- Throwaway script — overhead > value.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| sorbet/config | committed Sorbet config | lead |
| Tapioca RBIs | checked-in gem RBIs | lead |
| CI gate | `srb tc` + `tapioca check-shims` | ci-eng |
| Per-file sigils policy | agreement on minimum level | team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[lint-precommit-floor]] | Hook framework can run srb tc on staged files |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip-rule + rationale + source | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | 800 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns (symptom/root-cause/fix) | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with decision gates | 700 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion ref=rule-id | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `sigil_strategy` | sonnet | Pick minimum sigil per directory. |
| `rbi_regeneration` | haiku | Run tapioca; commit deltas. |
| `ci_wire_up` | sonnet | Add `srb tc` step. |

## Templates

| File | Purpose |
|------|---------|
| `templates/sorbet-config` | Sorbet config file. |
| `templates/tapioca-config.yml` | Tapioca config. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ruby-sorbet-strict-floor.py` | Validate the Sorbet-config artefact. | pre-merge of sorbet config |

## Related

- [[lint-precommit-floor]]
- [[mr-codemod-refactor-agent]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (precondition flag, repo metric, capability flag) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on a rule that triggers the procedure or on `skip-this-methodology`.
