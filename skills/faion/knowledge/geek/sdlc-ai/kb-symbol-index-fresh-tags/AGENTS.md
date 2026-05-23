---
slug: kb-symbol-index-fresh-tags
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Maintain a committed, always-fresh symbol index (LSP-based: Serena, SourceGraph, or ctags) wired to pre-commit/CI so coding agents resolve symbols deterministically without re-grepping.
content_id: "2dfe313b119c11a1"
complexity: medium
produces: config
est_tokens: 3600
tags: [symbol-index, ctags, lsp, agent-lookup, navigation]
---
# Symbol Index as Always-Fresh LSP/ctags Artifact

## Summary

**One-sentence:** Maintain a committed, always-fresh symbol index (LSP-based: Serena, SourceGraph, or ctags) wired to pre-commit/CI so coding agents resolve symbols deterministically without re-grepping.

**One-paragraph:** Symbol Index as Always-Fresh LSP/ctags Artifact produces a config artefact for the sdlc-ai domain. It pins observable preconditions, scores candidate decisions against ≥5 testable rules, fails fast on disqualifiers, and emits a schema-validated output. The methodology routes between apply and skip-this-methodology via an explicit decision tree so downstream agents never run it on an unsuitable input.

**Ефективно для:**

- Coding agent needs O(1) symbol lookup, not O(file-count) grep.
- Refactor / rename refactor where every call site must be visible.
- Cross-file impact analysis when an agent edits a symbol.
- Repository where grep-by-keyword produces > 100 candidates for common identifiers.

## Applies If (ALL must hold)

- Repo ≥ 20 KLOC, multi-file dependencies common.
- Language has a working LSP or universal-ctags grammar.
- Pre-commit / CI exists to refresh the index on every change.
- Coding agent has a Bash or Read tool to query the index file.

## Skip If (ANY kills it)

- Repo < 5 KLOC — grep is fast enough.
- Language not supported by LSP or ctags (rare).
- Index regen > 60 s on full repo and incremental update broken.
- Team rejects committed binary indexes — use sparse text formats only.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| LSP/ctags binary | Serena / sourcegraph / universal-ctags installed | dev-env |
| Index location | .symbol-index/ at repo root | team agreement |
| Pre-commit hook slot | ability to add a fast index-refresh hook | lead |
| CI gate | stage that fails the build if index is stale | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[lint-precommit-floor]] | Hook framework is the carrier for the refresh |

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
| `index_build_command` | haiku | Pick the right CLI invocation. |
| `hook_wire_up` | sonnet | Pre-commit + CI integration. |
| `staleness_detector` | sonnet | Heuristic for stale index. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ctags-config.ctags` | ctags config example. |
| `templates/pre-commit-symbol-index.yaml` | Pre-commit hook entry. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-symbol-index-fresh-tags.py` | Validate index-config artefact against schema. | pre-merge of index config |

## Related

- [[kb-codebase-rag-symbol-chunked]]
- [[lint-precommit-floor]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (precondition flag, repo metric, capability flag) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on a rule that triggers the procedure or on `skip-this-methodology`.
