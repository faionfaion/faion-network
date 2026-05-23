# Conventional Commits Enforced at the Hook

## Summary

**One-sentence:** Every repo enforces Conventional Commits 1.0.0 via commitlint commit-msg hook + CI PR-title check; release-please/semantic-release/changesets derive changelog + semver bump from the log.

**One-paragraph:** Every repo enforces Conventional Commits 1.0.0 (`feat`, `fix`, `chore`, `refactor`, `docs`, `test`, `perf`, `build`, `ci`, `style`, `revert`; optional scope; optional `!` for breaking; mandatory `BREAKING CHANGE:` footer when `!` is used) via a `commitlint` `commit-msg` hook plus a CI PR-title check. The CHANGELOG, semver bump, and release notes are derived deterministically from the log; agents never freeform commit subjects. Non-conformant messages are rejected at hook time, before they reach the remote.

**Ефективно для:**

- Any team repo that produces releases (libraries, services with semver, monorepos with independent package versions).
- Repos where AI agents create commits autonomously and a human curator does not edit every subject line.
- Projects with downstream consumers expecting semver-correct changelogs (npm, PyPI, NuGet, Maven Central, Helm charts).

## Applies If (ALL must hold)

- Any team repo that produces releases (libraries, services with semver, monorepos with independent package versions).
- Repos where AI agents create commits autonomously and a human curator does not edit every subject line.
- Projects with downstream consumers expecting semver-correct changelogs (npm, PyPI, NuGet, Maven Central, Helm charts).

## Skip If (ANY kills it)

- Single-developer scratch repos and throwaway prototypes.
- Mirror / vendored repos where commits are imported verbatim from upstream.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| commitlint config | cjs | Repo at `commitlint.config.cjs` |
| commit-msg hook installer | yaml/json | lefthook / husky / pre-commit |
| Release tool config | yaml | release-please / semantic-release / changesets |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/sdlc-ai/AGENTS.md` | Parent domain context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 testable rules with rationale + source + skip rule | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-gov-conventional-commits-enforced` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/commitlint.config.cjs` | commitlint config |
| `templates/lefthook.yml` | lefthook hook config |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-gov-conventional-commits-enforced.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `geek/sdlc-ai/AGENTS.md`
- [[kb-agents-md-context-pyramid]]
- [[inc-read-only-investigation-default]]
- [[ci-eval-gate-config]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
