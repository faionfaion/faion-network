---
slug: docker-security-hardening
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Apply layered security to Docker containers: run as non-root users, drop Linux capabilities, enforce read-only filesystems, manage secrets via Docker Secrets or Vault, sign images, and scan for vulnerabilities with Trivy or Docker Scout in every CI pipeline.
content_id: "ea0e80859e1a73e0"
tags: [docker, security, hardening, vulnerability-scanning, non-root]
---
# Docker Security Hardening

## Summary

**One-sentence:** Apply layered security to Docker containers: run as non-root users, drop Linux capabilities, enforce read-only filesystems, manage secrets via Docker Secrets or Vault, sign images, and scan for vulnerabilities with Trivy or Docker Scout in every CI pipeline.

**One-paragraph:** Apply layered security to Docker containers: run as non-root users, drop Linux capabilities, enforce read-only filesystems, manage secrets via Docker Secrets or Vault, sign images, and scan for vulnerabilities with Trivy or Docker Scout in every CI pipeline.

## Applies If (ALL must hold)

- Any production container — apply non-root user and capability dropping by default.
- Multi-tenant environments — combine read-only filesystem, dropped capabilities, and seccomp profiles.
- CI/CD pipelines — add Trivy or Docker Scout scan step that fails on HIGH/CRITICAL CVEs.
- Containers handling secrets — use Docker Secrets, Vault agent, or cloud secret managers; never ENV vars in Dockerfile.
- Containers that do not need to write to the filesystem at runtime — use --read-only with tmpfs for /tmp.

## Skip If (ANY kills it)

- Development-only containers where iteration speed matters more than hardening — apply in staging/prod but not dev.
- Containers that legitimately require elevated privileges (e.g., syslog daemons, network monitors) — document the exception and limit the scope.
- Legacy apps that cannot run as non-root without significant refactoring — triage and fix the app, do not permanently exempt it.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `pro/infra/devops-engineer/`
