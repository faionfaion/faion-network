---
slug: image-digest-pinning-policy
tier: pro
group: infra
domain: devops-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Team-level policy for pinning container images by SHA256 digest instead of floating tag, with documented update + rotation discipline.
content_id: "28cf925a3b124ede"
tags: [containers,supply-chain,digest-pinning,helm,docker,sbom]
---
# Image Digest Pinning Policy

## Summary

**One-sentence:** Team-level policy for pinning container images by SHA256 digest instead of floating tag, with documented update + rotation discipline.

**One-paragraph:** Container scanning and supply-chain methodologies exist as topics, but the team-level policy for digest pinning versus floating tags is rarely documented — leaving each engineer to ad-hoc choose. This methodology defines the binding rules: production manifests pin by `@sha256:` digest, staging may use immutable tags, dev may use floating tags ONLY with documented exceptions. Mechanism: a digest-update workflow (renovate or in-house bot), a quarterly rotation discipline for base images, a CI lint that rejects floating tags in production manifests, and a runbook for emergency unpins when supply-chain incidents demand rapid rollback. Primary output: a `digest-policy.md` checked into the platform repo with per-environment rules and an automation hookup that enforces them.

## Applies If (ALL must hold)

- team runs containerized workloads on Kubernetes / ECS / Cloud Run / Nomad / Docker Swarm
- production environment exists and is customer-facing
- team uses ≥ 1 third-party base image (not solely first-party builds)
- registry supports SHA256 digest references (Docker Hub, ECR, GCR, GHCR, Harbor, Quay)
- container scanning tool produces SBOM or CVE reports

## Skip If (ANY kills it)

- workloads are pure first-party builds with internal-only registry AND mandatory in-registry signature verification — pinning policy already exists
- single-user demo / sandbox environment with no production blast radius
- regulated environment requires only signed releases (signature pinning supersedes digest pinning)
- platform forces digest-pinning by default (e.g., GKE Autopilot + Binary Authorization)

## Prerequisites (must be true before starting)

- inventory of base images in use across services
- registry access patterns documented (pull credentials, mirror configuration)
- CI pipeline can run a lint step before merge
- a renovation / digest-bumper bot is selectable (Renovate, Dependabot, in-house)
- on-call team understands how to unpin in an incident

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer/iac-pr-review-checklist` | Image digest checks fold into the secrets / supply-chain axis |
| `pro/infra/infrastructure-engineer/k8s-security-hardening` | Pairs with image-policy admission controllers |
| `pro/infra/devops-engineer/container-scanning` | Provides CVE feed for prioritized digest updates |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: prod-digest-only, immutable-tag staging, quarterly rotation, lint gate, emergency unpin | ~1000 |
| `content/02-output-contract.xml` | essential | Digest-policy doc schema, per-env rules, automation hookup | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes (floating tag in prod, stale digests, lint-bypass, etc.) | ~1100 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `manifest_scanner` | haiku | Find every container image reference + classify pinning style |
| `digest_freshness_report` | sonnet | Compare current digests vs latest CVE-clean digest |
| `lint_rule_authoring` | sonnet | Generate CI lint config for production-tag detection |
| `emergency_unpin_runbook_drafter` | sonnet | Draft incident playbook |

## Templates

| File | Purpose |
|------|---------|
| `templates/digest-policy.md` | Per-environment policy template (prod/staging/dev rules) |
| `templates/renovate-config.json` | Renovate bot config tuned for digest-bumping |
| `templates/ci-lint-snippet.yaml` | CI lint snippet rejecting floating tags in prod manifests |
| `templates/emergency-unpin-runbook.md` | Incident playbook for rapid unpin |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/scan-manifests.py` | Find all image refs in repo + emit per-env compliance report | Quarterly + PR-time |
| `scripts/digest-freshness.py` | Compare pinned digests to latest tag at registry, flag stale | Quarterly review |

## Related

- parent skill: `pro/infra/devops-engineer/`
- peer methodology: `iac-pr-review-checklist`, `container-scanning`
- external: [OCI Image Spec](https://github.com/opencontainers/image-spec/blob/main/manifest.md) · [Renovate docs](https://docs.renovatebot.com/)
