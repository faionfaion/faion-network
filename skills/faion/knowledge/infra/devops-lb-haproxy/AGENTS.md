# HAProxy / Nginx Load Balancer Configuration

## Summary

**One-sentence:** Generates a production-ready HAProxy (or Nginx) load-balancer config — frontend/backend separation, ACL path routing, sticky cookies, stick-table rate-limiting, L4 DB mode, SSL termination, and Docker Compose bundle.

**One-paragraph:** Generates a production-ready HAProxy (or Nginx) load-balancer config — frontend/backend separation, ACL path routing, sticky cookies, stick-table rate-limiting, L4 DB mode, SSL termination, and Docker Compose bundle. The methodology pins the artefact shape, ties every conclusion to a rule, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Self-hosted LB на Hetzner / bare-metal без managed ALB.
- ACL-based routing (`/api` → API pool, `/static` → CDN pool).
- Per-IP rate-limit через stick tables (DDoS mitigation light).
- L4 mode для MySQL/PostgreSQL з protocol-aware health checks.

## Applies If (ALL must hold)

- Workload runs on self-hosted infrastructure (bare-metal, VMs, Docker hosts) — managed cloud LB is unavailable or not chosen.
- Operator owns the HAProxy/Nginx config file (Git-controlled, not ad-hoc UI).
- Production traffic flows through this LB (or will within 30 days).

## Skip If (ANY kills it)

- Workload is cloud-native and a managed ALB/NLB is the better choice.
- Only one LB instance is in scope — SPOF without HA pair (apply `devops-lb-high-availability` first).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Backend pool list | table (host, port, weight, role) | SRE |
| Cert bundle path | PEM bundle | Cert team |
| Rate-limit policy | RPM per IP | Security |
| Routing map | ACL → backend | Application team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer/devops-lb-algorithms/AGENTS.md` | Algorithm decision upstream |

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
| `draft-devops-lb-haproxy` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config.yaml` | YAML config skeleton conforming to the output contract |
| `templates/config-instance.json` | JSON instance of a filled config artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-devops-lb-haproxy.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/infra/devops-engineer/AGENTS.md`
- [[devops-lb-algorithms]]
- [[devops-lb-ssl-tls]]
- [[devops-lb-high-availability]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
