---
slug: refactoring-patterns
tier: free
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-net]
summary: Produces a refactor playbook (Extract Method, Replace Conditional with Polymorphism, Introduce Parameter Object, Rename for Clarity) executed one-at-a-time with green tests as the only gate.
content_id: "2b95c58304d49a1b"
complexity: medium
produces: playbook-step
est_tokens: 4000
tags: [refactoring, code-quality, patterns, maintainability, fowler]
---
# Refactoring Patterns

## Summary

**One-sentence:** Catalogues structural transformations (Extract Method, Replace Conditional with Polymorphism, Introduce Parameter Object, Decompose Conditional, Rename) applied one-at-a-time with green tests as the sole gate.

**One-paragraph:** "Two-hat rule" (Kent Beck): never refactor and add behaviour in the same commit. This methodology packages Fowler's catalogue into agent-executable steps: each refactor names the input shape, names the output shape, names the verification ("tests stay green"), and names the rollback. Refactors are bounded — `refactor:` commits touching >5 files are blocked by a pre-commit hook; large structural moves go through `[[code-decomposition-patterns]]` instead. Output is a JSON list of refactor steps with before/after pointers and test-run evidence.

**Ефективно для:**

- Підготовка legacy-модуля до додавання тесту: extract seams, make-the-change-easy before make-the-easy-change.
- Чистка дублікатів, виявлених jscpd / pylint duplicate-code / similar.
- Зниження cyclomatic complexity / function length warnings від lint.
- Перейменування на чистих іменах перед merge — рев'ю-комент про naming рішити одним коммітом.

## Applies If (ALL must hold)

- Existing test suite green; affected paths have coverage OR characterisation tests will be added first.
- Behaviour stays unchanged — refactor commit fixes no bugs and adds no features.
- Change is bounded to a single transformation; chained refactors go into separate commits.

## Skip If (ANY kills it)

- Same change also modifies behaviour — split into two commits, refactor first.
- Tests do not cover the affected code paths AND no characterisation tests added — refactor without coverage = silent regression.
- Hot paths where the "messy" form is intentional (manual loop unrolling, allocation reuse).
- Right before a release window — defer to next cycle.
- Generated code, vendored libraries, or migration scripts.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Failing-lint output | text / JSON | `ruff`, `eslint`, `jscpd`, `radon cc` |
| Test runner config | repo-native | `pyproject.toml` / `package.json` |
| Coverage report | lcov / coverage.xml | latest CI run |
| Change-bounded file list | path list | `git diff --name-only` from current branch |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[code-decomposition-patterns]] | Larger structural moves (Extract Class, Move Module) live there; this methodology handles fine-grained transformations. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: two-hat, tests-green-gate, one-transform-per-commit, scope-cap-5-files, rename-by-tooling, prefer-derivation | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for refactor-step playbook + verification evidence | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: refactor-mixed-with-feature, ide-rename-without-test, premature-abstraction, scope-creep | 700 |
| `content/04-procedure.xml` | essential | 5-step procedure: pick transform → branch → tests-green → apply → re-test | 700 |
| `content/05-examples.xml` | optional | Worked example: 30-line god-function → 3 extracted methods | 700 |
| `content/06-decision-tree.xml` | essential | Routing: smell → transform mapping (long method / conditional / duplication / magic number) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `smell_detect` | haiku | Lint output parse; deterministic. |
| `pick_transform` | sonnet | Mapping smell → catalogue entry; needs source context. |
| `apply_transform` | sonnet | Per-file code rewrite; small scope. |
| `architectural_move` | opus | Cross-file Move Class / Extract Module — delegate to [[code-decomposition-patterns]]. |

## Templates

| File | Purpose |
|------|---------|
| `templates/refactor-scope-guard.sh` | Pre-commit hook blocking `refactor:` commits touching >5 files |
| `templates/refactor-playbook.example.json` | Reference playbook artefact populating the output-contract schema |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-refactoring-patterns.py` | Validate refactor-playbook JSON against schema | After playbook generation, before commit |

## Related

- [[code-decomposition-patterns]] — larger structural moves.
- [[code-coverage]] — characterisation tests precondition for safe refactor.
- [[code-review-process]] — refactor PRs go through review.

## Decision tree

See `content/06-decision-tree.xml`. Tree maps detected smell to canonical transform: long method → Extract Method; complex conditional → Replace Conditional with Polymorphism OR Decompose Conditional; long parameter list → Introduce Parameter Object; magic number → Replace Magic Number with Symbolic Constant; unclear name → Rename for Clarity. All leaves reference rules from `01-core-rules.xml`.
