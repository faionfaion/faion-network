---
slug: lint-shellcheck-hadolint-iac-floor
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Every repository with shell scripts, Dockerfiles, Compose files, GitHub Actions workflows, Kubernetes manifests, Terraform, or YAML configuration MUST run a per-format infrastructure linter at the same hook tier as code linters.
content_id: "8b27d28f7af23a58"
tags: [shellcheck, hadolint, iac, linting, infrastructure]
---
# Infrastructure-as-Code Lint Floor (shellcheck, hadolint, yamllint, actionlint, tflint)

## Summary

**One-sentence:** Every repository with shell scripts, Dockerfiles, Compose files, GitHub Actions workflows, Kubernetes manifests, Terraform, or YAML configuration MUST run a per-format infrastructure linter at the same hook tier as code linters.

**One-paragraph:** Every repository with shell scripts, Dockerfiles, Compose files, GitHub Actions workflows, Kubernetes manifests, Terraform, or YAML configuration MUST run a per-format infrastructure linter at the same hook tier as code linters. The minimum set is shellcheck for *.sh and bash-shebanged files, hadolint for any Dockerfile*, yamllint for .yaml/.yml, actionlint for .github/workflows/, and tflint (plus terraform validate) for HCL. Findings block at the same level as code-lint findings; hooks run pre-commit on the staged file set and CI runs the whole tree once per PR. AI agents fix flagged issues at the source (pin apt versions, drop latest tags, quote shell variables) rather than disabling the rule.

## Applies If (ALL must hold)

- Every repository that contains at least one Dockerfile, shell script, GitHub Actions workflow, Kubernetes manifest, Terraform file or non-trivial YAML config (i.e., effectively every production repo).
- Polyglot monorepos where app-code linters skip the IaC tree entirely.
- Repos with self-hosted CI or community-contributed workflows where action injection is a real attack surface.
- Hardening sprints after an incident traceable to a shell or Dockerfile bug.

## Skip If (ANY kills it)

- Pure prose / Markdown / asset repos with no scripts, no CI workflows, no IaC — there is nothing for these tools to see.
- Throwaway prototype repos where the operational surface is hand-managed and never deployed automatically.
- Repos under active migration where IaC is being rewritten — schedule a one-shot baseline reset, then turn the hooks back on.

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

- parent skill: `geek/sdlc-ai/sdlc-ai/`
