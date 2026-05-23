# Pre-Commit Hooks as the Non-Negotiable Merge Floor

## Summary

**One-sentence:** Every repo with code MUST install a pre-commit framework (pre-commit, lefthook, husky) running format + lint + secret-scan + type-check on staged files BEFORE the commit is created.

**One-paragraph:** Pre-Commit Hooks as the Non-Negotiable Merge Floor produces a config artefact for the sdlc-ai domain. It pins observable preconditions, scores candidate decisions against ≥5 testable rules, fails fast on disqualifiers, and emits a schema-validated output. The methodology routes between apply and skip-this-methodology via an explicit decision tree so downstream agents never run it on an unsuitable input.

**Ефективно для:**

- Any code repo where humans + agents both commit.
- Repo where CI catches lint after push, wasting cycles.
- Team that has had a secret leak from forgotten `.env` commits.
- Multi-language repo where each language needs its own format/lint.

## Applies If (ALL must hold)

- Repo has code (not pure docs).
- Team agrees on a single hook framework.
- CI also runs the same checks as a safety net.
- Languages in repo have working linters / formatters.

## Skip If (ANY kills it)

- Repo is pure prose (use markdownlint via different path).
- Team rejects local hooks (controversial — push back).
- Hook framework not installable on the dev machines (Windows blockers).
- Single-author throwaway — overhead > value.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| .pre-commit-config.yaml or lefthook.yml | committed config | lead |
| Local install script | make hooks / setup.sh | platform |
| CI mirror | same checks run in CI | ci-eng |
| Secret scanner | trufflehog / gitleaks integrated | security |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[lint-staged-only-not-whole-tree]] | Hook discipline complement |

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
| `framework_pick` | sonnet | pre-commit vs lefthook vs husky. |
| `hook_set_draft` | sonnet | Per-language entries. |
| `ci_mirror` | haiku | CI workflow that runs the same. |

## Templates

| File | Purpose |
|------|---------|
| `templates/.pre-commit-config.yaml` | Sample pre-commit config. |
| `templates/lefthook.yml` | Sample Lefthook config. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-precommit-floor.py` | Validate hook-config artefact. | pre-merge of hook config |

## Related

- [[lint-staged-only-not-whole-tree]]
- [[lint-ruff-and-biome-as-default]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (precondition flag, repo metric, capability flag) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on a rule that triggers the procedure or on `skip-this-methodology`.
