---
slug: lint-autofix-vs-flag-decision-rule
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: A coding agent may apply a linter / scanner autofix automatically iff: (1) fix is purely syntactic, (2) tool has explicit --fix, (3) tests still pass, (4) diff < 50 lines OR a single rule ID. Otherwise flag-only.
content_id: "bb6468c06642e1aa"
complexity: medium
produces: decision-record
est_tokens: 3500
tags: [lint, autofix, agent-policy, sast, security]
---
# Autofix-vs-Flag Decision Rule for Coding Agents

## Summary

**One-sentence:** A coding agent may apply a linter / scanner autofix automatically iff: (1) fix is purely syntactic, (2) tool has explicit --fix, (3) tests still pass, (4) diff < 50 lines OR a single rule ID. Otherwise flag-only.

**One-paragraph:** Autofix-vs-Flag Decision Rule for Coding Agents produces a decision-record artefact for the sdlc-ai domain. It pins observable preconditions, scores candidate decisions against ≥5 testable rules, fails fast on disqualifiers, and emits a schema-validated output. The methodology routes between apply and skip-this-methodology via an explicit decision tree so downstream agents never run it on an unsuitable input.

**Ефективно для:**

- Coding agent decides what to do with a linter / SAST finding.
- Policy gate for `ruff --fix` vs `semgrep --autofix` vs `eslint --fix`.
- Multi-agent setup where autofix authority is governed.
- CI bot that opens PRs for fixable issues — pick fix vs flag deterministically.

## Applies If (ALL must hold)

- Agent has access to linter / scanner output as structured data.
- Test suite is the source of truth for behavioural regression.
- Tool has machine-readable autofix support.
- Repo has a policy for what counts as an acceptable autofix scope.

## Skip If (ANY kills it)

- No tests exist — autofix can silently break behaviour.
- Tool autofix is known-buggy (e.g. eslint --fix on old configs).
- Diff diff > 50 lines across > 1 rule — change becomes a refactor.
- Single-author repo where the human always reviews — agent autonomy = 0.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Linter / scanner integrated in CI | JSON output | platform |
| Test suite | fast green path | team |
| Decision-rule doc | this methodology | lead |
| Audit log location | repo dir for decisions.jsonl | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[lint-precommit-floor]] | Hook framework where autofix may fire |
| [[lint-staged-only-not-whole-tree]] | Scope discipline upstream |

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
| `apply_decision_rule` | sonnet | Run the 4-clause rule against a finding. |
| `decision_log_emit` | haiku | Emit decisions.jsonl entry. |
| `test_smoke_after_fix` | haiku | Run focused test set. |

## Templates

| File | Purpose |
|------|---------|
| `templates/decision.json` | One agent decision record. |
| `templates/decisions-log.jsonl` | Append-only audit log. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-autofix-vs-flag-decision-rule.py` | Validate the decision-record artefact. | per-decision append |

## Related

- [[lint-precommit-floor]]
- [[lint-staged-only-not-whole-tree]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (precondition flag, repo metric, capability flag) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on a rule that triggers the procedure or on `skip-this-methodology`.
