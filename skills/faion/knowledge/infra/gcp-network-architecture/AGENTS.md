# GCP Network Architecture

## Summary

**One-sentence:** Network spec for GCP: Shared VPC topology, CIDR allocation for GKE secondary ranges, Private Service Connect, Cloud NAT and hierarchical firewall policy.

**One-paragraph:** Network spec for GCP: Shared VPC topology, CIDR allocation for GKE secondary ranges, Private Service Connect, Cloud NAT and hierarchical firewall policy. Use it whenever the `Applies If` preconditions all hold; the methodology produces a single `spec` artefact that conforms to `content/02-output-contract.xml` and is verified by `scripts/validate-gcp-network-architecture.py` before publication.

**Ефективно для:**

- Дизайн Shared VPC для організації з 5+ проектами.
- Розрахунок CIDR під GKE pod / service ranges.
- Налаштування Cloud NAT + hierarchical firewall.

## Applies If (ALL must hold)

- Input matches the methodology scope (gcp-network-architecture) — not an adjacent workload.
- All artefacts in `Prerequisites` are present and within their freshness window.
- Owner is identified and can review the produced `spec` before publication.

## Skip If (ANY kills it)

- Input is an adjacent workload covered by a more specific methodology in `[[Related]]`.
- Required prerequisite artefact is unavailable or older than the documented freshness window.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Environment list with /16 budget | env → required IP space | architecture review |
| Service-project list | service projects that attach to host VPC | gcp-landing-zone |
| Egress requirements | domain allow-list + bandwidth target | security team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[gcp]] | upstream context likely already loaded when this methodology fires |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | ~900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input/action/output/gate per step | ~800 |
| `content/05-examples.xml` | essential | Full worked example end-to-end | ~900 |
| `content/06-decision-tree.xml` | essential | Root-question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| gather-and-validate-inputs | haiku | Mechanical inventory + freshness check. |
| apply-core-rules | sonnet | Rule-by-rule reasoning over the inputs. |
| draft-spec-artefact | sonnet | Template filling with bounded judgement. |
| validate-and-publish | haiku | Script-driven validation + traceability wiring. |

## Templates

| File | Purpose |
|------|---------|
| `templates/spec.md` | Spec skeleton with scope / components / decisions / risks sections |
| `templates/_smoke-test.md` | Minimum viable filled-in version of the template used by `--self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-gcp-network-architecture.py` | Validate the artefact against the 02-output-contract schema | CI on each artefact change; pre-commit; before publish step in procedure |

## Related

- [[gcp]]
- [[gcp-landing-zone]]
- [[gcp-gke-architecture]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts at `Are all preconditions satisfied?`; the negative branch terminates with `skip-this-methodology` and the positive branch routes via `scope_explicit` to either `shared-vpc-default` (apply end-to-end) or a guarded entry. Use it whenever the input source or scope is ambiguous.
