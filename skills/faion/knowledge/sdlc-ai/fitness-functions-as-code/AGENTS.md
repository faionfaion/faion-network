# Fitness Functions as Code

## Summary

**One-sentence:** Codify evolutionary architecture fitness functions as executable tests: per-axis (modularity, latency, security posture) tests that fail the build when architecture drifts beyond bounds.

**One-paragraph:** Evolutionary architecture (Ford, Parsons, Kua) treats architectural characteristics as fitness functions — executable tests that fail when modularity, latency, security posture, or coupling drift beyond agreed bounds. Most teams know the concept; few install it. This methodology turns the abstract idea into per-axis Python/TypeScript test files (`tests/fitness/test_modularity.py`, `test_latency_p95.py`, `test_no_circular_deps.py`) that run as part of CI and gate merge.

**Ефективно для:**

- Codebase has ≥3 services or ≥30 modules — architectural drift is a real risk.
- Team has agreed an architectural decision record (ADR) listing the characteristics to preserve.
- CI infrastructure can run static analysis (deps graph) and performance smoke tests (load harness).

## Applies If (ALL must hold)

- Codebase has ≥3 services or ≥30 modules — architectural drift is a real risk.
- Team has agreed an architectural decision record (ADR) listing the characteristics to preserve.
- CI infrastructure can run static analysis (deps graph) and performance smoke tests (load harness).

## Skip If (ANY kills it)

- Codebase is a single-file script — architecture is trivial.
- Team has no ADR + no agreement on which characteristics matter — fitness functions need a target.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| ADR list | md | Repo at `docs/adr/*.md` |
| Dep graph tooling | binary | `tach`, `pydeps`, `madge`, or `dependency-cruiser` |
| Load harness | yaml | Repo at `loadtests/*.yaml` |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/sdlc-ai/AGENTS.md` | Parent domain context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules with rationale + source + skip rule | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-fitness-functions-as-code` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/test_no_circular_deps.py` | Modularity fitness function reference test |
| `templates/test_p95_under_500ms.py` | Latency fitness function reference test |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-fitness-functions-as-code.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `geek/sdlc-ai/AGENTS.md`
- [[kb-agents-md-context-pyramid]]
- [[gov-conventional-commits-enforced]]
- [[inc-read-only-investigation-default]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
