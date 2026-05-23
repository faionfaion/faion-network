# ADR Decay Detector Agent

## Summary

**One-sentence:** Agent that scans ADRs against current code and emits a decay report: ADRs contradicted by code, deprecated by other ADRs, missing referenced artifacts.

**One-paragraph:** Architecture Decision Records (ADRs) rot the moment the decision changes but the markdown doesn't. This methodology installs a weekly agent that scans every ADR against current code, checks for: contradiction (ADR says use Postgres, code uses MongoDB), supersession (later ADR overrides earlier without link), missing artifacts (ADR references a script that no longer exists). Output is a decay report keyed by ADR + decay category + remediation, suitable for a weekly architecture review.

**Ефективно для:**

- Team maintains ≥10 ADRs in repo (e.g. `docs/adr/`).
- ADRs reference concrete artifacts (file paths, modules, libraries) that can be checked against current code.
- There is a weekly or monthly architecture review cadence to act on findings.

## Applies If (ALL must hold)

- Team maintains ≥10 ADRs in repo (e.g. `docs/adr/`).
- ADRs reference concrete artifacts (file paths, modules, libraries) that can be checked against current code.
- There is a weekly or monthly architecture review cadence to act on findings.

## Skip If (ANY kills it)

- Team has <5 ADRs — manual review suffices.
- ADRs are pure prose with no concrete artifact references — nothing to check.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| ADR directory | md | Repo at `docs/adr/` |
| Repo index | files | Current git HEAD |
| ADR template + linkage convention | md | Repo at `docs/adr/TEMPLATE.md` |

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
| `content/04-procedure.xml` | essential | 6-step procedure end-to-end | ~900 |
| `content/05-examples.xml` | essential | Worked example trace + final artefact | ~700 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-kb-adr-decay-detector-agent` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/decay-report.json` | Decay report skeleton |
| `templates/ci-cron.yml` | GitHub Actions weekly cron |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-kb-adr-decay-detector-agent.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `geek/sdlc-ai/AGENTS.md`
- [[kb-agents-md-context-pyramid]]
- [[gov-conventional-commits-enforced]]
- [[inc-read-only-investigation-default]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
