---
slug: secret-consumer-discovery
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: "Enumerate every consumer of a given secret across repos, services, CI jobs, schedulers, and runtime configs before initiating rotation."
content_id: "b753f08903bcb4a3"
tags: [secret-consumer-discovery, infra, pro]
---
# Secret Consumer Discovery

## Summary

**One-sentence:** A repeatable procedure to enumerate every consumer of a named secret across the entire stack before a rotation kicks off.

**One-paragraph:** Secret-storage and rotation primitives are well documented in faion-network, but the missing step — knowing every consumer of a given secret — is what turns a routine rotation into a Saturday-night incident. This methodology defines the discovery sweep: code search across all repos with the secret's logical name AND obfuscated variants, secret-store audit-log query, CI/CD env-var inventory, scheduled-job/cron parse, runtime config snapshots across all environments, and a signed consumer registry that becomes the input to the rotation runbook. Output: `secrets/<name>/consumers.yaml` versioned in the secrets repo.

## Applies If (ALL must hold)

- a specific named secret is scheduled for rotation, revocation, or scope change
- you have read access to every repo, CI system, secret-store audit log, and runtime config the org uses
- output will gate the rotation runbook execution
- tier == pro or higher

## Skip If (ANY kills it)

- the secret is consumed by exactly one service and the consumer is unambiguous (single-binary deployment)
- you are doing a "burn it all" rotation where downstream breakage is acceptable (declared incident response)
- a fresh consumer registry already exists (<7 days old) and the change boundary has not moved

## Prerequisites

- the secret's logical name AND every known alias (env-var spelling, file path, KMS key alias, store path)
- read-only credentials for: all repos, CI/CD platform, secret-store audit log, scheduler/cron host, runtime config (k8s ConfigMaps, .env mounts, etc.)
- a place to write the consumer registry (secrets repo or wiki)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/secrets-rotation-end-to-end` | downstream consumer of this discovery output |
| `pro/infra/devops-engineer` | parent role/operating context |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable discovery rules + 1 worked example | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `grep_repos` | haiku | bounded ripgrep over known alias list |
| `parse_ci_jobs` | sonnet | YAML/JSON parse with alias matching |
| `consolidate_registry` | sonnet | merge dedupe + dependency tagging |

## Related

- parent skill: `pro/infra/`
- `pro/infra/secrets-rotation-end-to-end`
- upstream playbook: `role-devops-engineer/Secret rotation execution`
