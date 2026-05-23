# Service Ownership Map Template

## Summary

**One-sentence:** Service ownership map: per-service owning team, on-call contact, SLO link, runbook link, dependencies, current health badge — kept in version control.

**One-paragraph:** Service ownership map: per-service owning team, on-call contact, SLO link, runbook link, dependencies, current health badge — kept in version control. This methodology converts the inputs in Prerequisites into the artefact described in Output Contract, gated by the rules in 01-core-rules.xml and the decision tree in 06-decision-tree.xml.

**Ефективно для:** the kinds of tasks listed in 'Applies If' — primary use cases are teams shipping the artefact (`spec`) at a light complexity level, where the failure modes in 03-failure-modes.xml are realistic risks worth the methodology's overhead.

## Applies If (ALL must hold)

- Org has ≥5 services AND ≥3 owning teams.
- Incidents have suffered from 'who owns this?' confusion in last quarter.
- Backstage / equivalent catalogue is in use OR being considered.

## Skip If (ANY kills it)

- Single team owning everything — ownership map is trivial.
- <5 services — informal mapping suffices.
- Org already uses Backstage with the catalogue fully populated.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Service inventory | Spreadsheet / Backstage | infra |
| Team list + on-call contacts | Markdown | ops |
| SLO + runbook links | URLs | platform team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/software-architect/team-topologies-skills` | Team Topologies framing. |
| `geek/infra/oncall-handoff-protocol` | Owner team holds the on-call rotation. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 3-5 antipatterns with symptom/root-cause/fix | ~800 |
| `content/05-examples.xml` | medium | One end-to-end worked example | ~800 |
| `content/06-decision-tree.xml` | essential | Decision tree gating whether this methodology applies | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `inventory_fill` | haiku | Mechanical mapping from existing sources. |
| `dependency_synthesis` | sonnet | Read code + infra to derive service dependencies. |
| `orphan_resolution` | opus | Cross-team negotiation for orphan services. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ownership-map.md` | Markdown table per service. |
| `templates/backstage-catalog.yaml` | Backstage catalog-info.yaml shape. |
| `templates/orphan-resolution.md` | Decision template for unowned services. |
| `templates/_smoke-test.md` | Minimum-viable filled-in example (smoke test). |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-service-ownership-map-template.py` | Validate methodology output against `02-output-contract.xml` schema. | Pre-commit and CI before merge. |

## Related

- parent skill: `geek/infra/`
- `[[team-topologies-skills]]`
- `[[oncall-handoff-protocol]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether service-ownership-map-template applies: root question — "Does the org have ≥5 services AND multiple owning teams?". Branches lead to a specific core rule (e.g., `rule:r1`) when the methodology fits, or to a `skip-this-methodology` conclusion when it does not.
