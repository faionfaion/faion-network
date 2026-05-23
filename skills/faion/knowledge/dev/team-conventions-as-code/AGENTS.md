# Team Conventions as Code

## Summary

**One-sentence:** Encode team conventions (naming, file layout, test required-coverage, PR-template fields) as enforced lint rules / pre-commit hooks / CI gates, not Confluence pages.

**One-paragraph:** Encode team conventions (naming, file layout, test required-coverage, PR-template fields) as enforced lint rules / pre-commit hooks / CI gates, not Confluence pages. The methodology pins the artefact shape via a JSON Schema (see `content/02-output-contract.xml`), ties every conclusion in the decision tree to a rule id in `content/01-core-rules.xml`, and gates output via `scripts/validate-team-conventions-as-code.py` (stdlib-only, `--self-test` available). Apply when preconditions in Applies-If hold; route to `skip-this-methodology` otherwise. The output artefact is versioned (semver), owner-signed (named human, never 'team' / 'we'), and consumable by a downstream agent or human reviewer without re-deriving the rationale.

**Ефективно для:**

- Team ≥4 devs з конвенціями, що drift щомісяця через PRs.
- Production-readiness gates на PR level (test coverage, ADR-link, security checklist).
- Onboarding bottleneck: new devs ламають конвенції бо не прочитали Confluence.
- CI infrastructure (GitHub Actions, GitLab CI) здатна gate'ити merge на violations.

## Applies If (ALL must hold)

- Team ≥3 devs and conventions drift across PRs
- CI infrastructure can block merge on lint / hook / gate failures
- Conventions are non-trivial (>5 rules) and re-explained in PR reviews
- Existing Confluence/wiki conventions doc that nobody reads

## Skip If (ANY kills it)

- Solo dev / pair team — convention drift solved by direct conversation
- Conventions still in flux (changing weekly) — code them once stable
- No CI gate authority — encoding without enforcement is theatre
- Convention is a one-time choice (e.g. license header) — set it once, no automation needed

## Prerequisites

| Trigger artefact | format | author / source |
|---|---|---|
| Task brief | Markdown | requester |
| Named owner | string | requester / RACI |
| Prior artefact (if updating) | repo path | artefact store |
| Constraint inputs (budget, SLA, compliance) | structured | requester / policy |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/INDEX.xml` | Parent domain context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip-this-methodology, each with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end with decision gates | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application — light judgement on preconditions vs skip-if. |
| `draft-team-conventions-as-code` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config.json` | JSON instance matching the output contract |
| `templates/config.yaml` | YAML config skeleton matching the output contract |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-team-conventions-as-code.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/dev/INDEX.xml`
- [[team-rfc-process-for-devs]]
- [[test-suite-audit-rubric]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
