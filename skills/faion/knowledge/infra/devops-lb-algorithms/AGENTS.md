# Load Balancer Types and Algorithm Selection

## Summary

**One-sentence:** Generates a load-balancer architecture decision record: chosen LB layer (L4/L7/DNS/Global), algorithm (round-robin / least-conn / weighted / IP-hash / consistent-hash), and session-affinity strategy.

**One-paragraph:** Generates a load-balancer architecture decision record: chosen LB layer (L4/L7/DNS/Global), algorithm (round-robin / least-conn / weighted / IP-hash / consistent-hash), and session-affinity strategy. The methodology pins the artefact shape, ties every conclusion to a rule, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Перший дизайн LB — вибір L4 vs L7 і алгоритму під workload.
- Heterogeneous backends (різна capacity) — обґрунтований Weighted Least Connections.
- Caching tier (Varnish / Redis cluster) — Consistent Hashing з rationale.
- Migration з sticky-IP на cookie-based affinity.

## Applies If (ALL must hold)

- Horizontal scaling across ≥2 backend instances is in scope.
- Traffic profile (HTTP vs TCP, request length variance, session semantics) is documented.
- Decision must be defended in an architecture review (ADR).

## Skip If (ANY kills it)

- Single-instance deployment with no HA requirement.
- Decision is already pinned by managed cloud LB defaults that team has accepted.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Traffic profile | table (RPS, p50/p99 duration, protocol) | Product / SRE |
| Backend capacity table | list (instance, capacity weight) | SRE |
| Session semantics | free-form note (stateless / sticky / sharded) | Application owner |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer/AGENTS.md` | Parent skill context |

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
| `draft-devops-lb-algorithms` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config-instance.json` | JSON instance of a filled config artefact |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-devops-lb-algorithms.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- Parent: `pro/infra/devops-engineer/AGENTS.md`
- [[devops-lb-haproxy]]
- [[devops-lb-health-checks]]
- [[devops-lb-high-availability]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/config-instance.json`

```json
{
  "layer": "L7",
  "algorithm": "weighted_least_connections",
  "session_affinity": "cookie",
  "rationale": "API backend with heterogeneous instance sizes and long-lived WebSocket connections; least-conn rebalances under variance while weights match measured RPS capacity.",
  "backends": [
    {
      "host": "api1.internal",
      "weight": 100
    },
    {
      "host": "api2.internal",
      "weight": 100
    },
    {
      "host": "api3.internal",
      "weight": 50
    }
  ],
  "owner": "sre@acme.io",
  "last_reviewed": "2026-05-23"
}
```
