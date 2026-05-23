# AI-Generated IaC Review Red-Flags

## Summary

**One-sentence:** Red-flag checklist for AI-generated Terraform / Pulumi / CloudFormation: hard-coded credentials, open security groups, public S3 buckets, missing tags, no state lock — emits gated JSON report.

**One-paragraph:** AI agents author IaC that compiles but encodes catastrophic defaults — public S3 buckets, 0.0.0.0/0 ingress, hard-coded ARNs, no state lock, missing tags. This methodology fixes a 10-item red-flag list run before any `terraform apply` / `pulumi up`. Output is a structured JSON report keyed by file + resource, with severity + remediation, suitable as a PR check that blocks merge on any high-severity finding.

**Ефективно для:**

- AI-authored Terraform, OpenTofu, Pulumi, or CloudFormation changes are in the PR.
- The target environment has production blast radius (publicly reachable, holds real customer data, or signs releases).
- CI runs `plan` + reviews before merge — there is a gate to insert this check into.

## Applies If (ALL must hold)

- AI-authored Terraform, OpenTofu, Pulumi, or CloudFormation changes are in the PR.
- The target environment has production blast radius (publicly reachable, holds real customer data, or signs releases).
- CI runs `plan` + reviews before merge — there is a gate to insert this check into.

## Skip If (ANY kills it)

- The change is a pure refactor with no `plan` diff (variable rename, comment).
- The target is a personal sandbox with auto-destroy and no shared data.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| IaC files | tf/yaml/ts | PR diff |
| `terraform plan` JSON | json | `terraform show -json plan.out` |
| Tag policy | yaml | team `infra/tag-policy.yaml` |

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
| `content/04-procedure.xml` | essential | 4-step procedure end-to-end | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-ai-generated-iac-review-redflags` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/redflag-report.json` | JSON skeleton for the validator output |
| `templates/ci-gate.yml` | GitHub Actions snippet that runs the validator and gates merge |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-generated-iac-review-redflags.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `geek/sdlc-ai/AGENTS.md`
- [[kb-agents-md-context-pyramid]]
- [[gov-conventional-commits-enforced]]
- [[inc-read-only-investigation-default]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
