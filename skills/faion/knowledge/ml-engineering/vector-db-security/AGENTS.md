# Vector Database Security Hardening

## Summary

**One-sentence:** Hardens a vector DB with authentication (API key / OIDC), TLS-in-flight, encryption at rest, private VPC, audit log, and PII handling — closing the default-open posture most vector DBs ship with.

**One-paragraph:** Vector DBs default to open: Qdrant binds 0.0.0.0:6333 with no auth, pgvector inherits Postgres permissions (often weak), Pinecone uses static API keys. Hardening requires: enable auth (API key or OIDC), enforce TLS on all listeners, restrict listener to private subnet, enable encryption at rest, log every admin + query call, and document the PII handling procedure (anonymise / redact / drop on request). Output: a `security-config.yaml` declaring auth + tls + network + encryption + audit + PII handling.

**Ефективно для:**

- Multi-tenant SaaS — auth + audit log = compliance baseline.
- PII-bearing corpora (medical, legal, finance) — encryption at rest + redact procedure = GDPR / HIPAA floor.
- Compliance-driven products — explicit security-config audit trail.
- Open-source self-host — closes the default-open posture before production exposure.

## Applies If (ALL must hold)

- Production deployment (any non-dev environment)
- DB contains real user / customer data
- Compliance regime applies (GDPR, HIPAA, SOC2, PCI)

## Skip If (ANY kills it)

- Pure dev / local sandbox with synthetic data
- DB in fully isolated air-gapped network (still consider, but priorities shift)

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| `network-topology.yaml` | YAML | infra (VPC, subnets, firewall rules) |
| `compliance-requirements.yaml` | YAML | legal / compliance |
| `secret-manager-config.yaml` | YAML | Vault / KMS / SSM Parameter Store |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `vector-databases` | DB chosen |
| `vector-db-setup-prod` | Prod deploy baseline |
| `vector-db-monitoring` | Monitoring needed to detect auth attacks |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: no anonymous, TLS everywhere, private network only, audit every admin call, PII handling procedure | 1100 |
| `content/02-output-contract.xml` | essential | security-config.yaml schema | 700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: open binding, plain HTTP, static key in code, no audit, no PII process | 900 |
| `content/04-procedure.xml` | essential | 5 steps: lock auth → TLS → network → encryption → audit + PII | 700 |
| `content/05-examples.xml` | essential | Worked example: Qdrant hardened deployment | 500 |
| `content/06-decision-tree.xml` | essential | Routes by compliance regime → required hardening level | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `threat_model_drafting` | sonnet | Synthesise threats |
| `security_review_drafting` | opus | Compliance + threat composition |
| `security_config_lint` | haiku | Schema check |

## Templates

| File | Purpose |
|------|---------|
| `templates/security-config.schema.yaml` | Schema |
| `templates/_smoke-test.yaml` | Minimum-viable spec |
| `templates/threat-model.md` | Threat model markdown skeleton |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-vector-db-security.py` | Lint security-config | Pre-commit |

## Related

- [[vector-databases]] · [[vector-db-setup-prod]] · [[vector-db-monitoring]]
- external: [Qdrant security docs](https://qdrant.tech/documentation/guides/security/) · [OWASP top 10 LLM](https://owasp.org/www-project-top-10-for-large-language-model-applications/)

## Decision tree

See `content/06-decision-tree.xml`. Routes by compliance regime (GDPR / HIPAA / SOC2 / none) to a required hardening level.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/security-config.schema.yaml`

```yaml
$schema: "http://json-schema.org/draft-07/schema#"
type: object
required: [auth, tls, network, encryption_at_rest, audit, pii]
properties:
  auth:
    type: object
    required: [enabled, method]
    properties:
      enabled: {type: boolean}
      method: {type: string, enum: [api-key, oidc, mtls]}
  tls:
    type: object
    required: [enabled, min_version]
    properties:
      enabled: {type: boolean}
      min_version: {type: string, enum: ["1.2", "1.3"]}
  network:
    type: object
    required: [binding, public_internet_exposed]
    properties:
      binding: {type: string}
      public_internet_exposed: {type: boolean}
  encryption_at_rest:
    type: object
    required: [enabled]
    properties:
      enabled: {type: boolean}
  audit:
    type: object
    required: [enabled, sink]
    properties:
      enabled: {type: boolean}
      sink: {type: string}
  pii:
    type: object
    required: [detection, redaction, retention_days, erasure_sla_hours]
    properties:
      retention_days: {type: integer, minimum: 1}
      erasure_sla_hours: {type: integer, minimum: 1, maximum: 720}
```

### `templates/_smoke-test.yaml`

```yaml
auth: {enabled: true, method: api-key}
tls: {enabled: true, min_version: "1.3"}
network: {binding: 10.20.30.40:6333, public_internet_exposed: false}
encryption_at_rest: {enabled: true}
audit: {enabled: true, sink: "s3://prod-audit/qdrant/"}
pii:
  detection: presidio
  redaction: pseudonymise
  retention_days: 365
  erasure_sla_hours: 168
```
