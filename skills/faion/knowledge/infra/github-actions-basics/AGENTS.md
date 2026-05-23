# GitHub Actions — Basics

## Summary

**One-sentence:** Generates an entry-level GHA config (single repo workflow with trigger + permissions + a canonical 2-job pipeline + cache + artifact) that pre-installs the discipline of the later methodologies.

**One-paragraph:** Generates an entry-level GHA config (single repo workflow with trigger + permissions + a canonical 2-job pipeline + cache + artifact) that pre-installs the discipline of the later methodologies. The methodology pins the artefact shape, ties every conclusion to a rule, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Перший GHA workflow в репо: lint + test + small artifact.
- Onboarding eng-team на GHA з безпечним baseline.
- Прототип pipeline що еволюціонує у складніший CD.
- Internal tooling repos де треба швидкий CI з мінімумом ceremony.

## Applies If (ALL must hold)

- Repository hosted on GitHub with Actions available.
- Code has a runnable test or lint step (`npm test`, `pytest`, etc.).
- Owner exists who will maintain the workflow.
- Standard project layout (one main branch + PRs).

## Skip If (ANY kills it)

- Repo already has a hardened GHA setup — jump to specific methodology (security/matrix/cd).
- Tests don't run — fix the test setup before adding CI.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Test command | string | Eng team |
| Default branch name | string (main / master) | GitHub admin |
| Build output path | string | Eng team |
| Owner email | string | Eng team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/cicd-engineer/AGENTS.md` | Parent skill context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source + skip rule | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end with decision gates | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-github-actions-basics` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config.yaml` | YAML config skeleton conforming to the output contract |
| `templates/config-instance.json` | JSON instance of a filled config artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-github-actions-basics.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/infra/cicd-engineer/AGENTS.md`
- [[finops-framework]]
- [[gitops-core-principles]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
