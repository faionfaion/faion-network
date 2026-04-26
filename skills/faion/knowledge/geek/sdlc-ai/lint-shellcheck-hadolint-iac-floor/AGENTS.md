# Infrastructure-as-Code Lint Floor (shellcheck, hadolint, yamllint, actionlint, tflint)

## Summary

Every repository with shell scripts, Dockerfiles, Compose files, GitHub Actions workflows, Kubernetes manifests, Terraform, or YAML configuration MUST run a per-format infrastructure linter at the same hook tier as code linters. The minimum set is `shellcheck` for `*.sh` and bash-shebanged files, `hadolint` for any `Dockerfile*`, `yamllint` for `.yaml`/`.yml`, `actionlint` for `.github/workflows/`, and `tflint` (plus `terraform validate`) for HCL. Findings block at the same level as code-lint findings; hooks run pre-commit on the staged file set and CI runs the whole tree once per PR. AI agents fix flagged issues at the source (pin apt versions, drop `latest` tags, quote shell variables) rather than disabling the rule.

## Why

App-code linters (ruff, biome) cannot see infrastructure code. Production failures routinely originate in shell quoting (Shellshock-class), Dockerfile rootful images and unpinned `latest` tags, GitHub Actions privilege misuses (especially `pull_request_target` paired with checkout of head SHA), Compose port leaks and Terraform plan drift. The IaC linter set is mature and maintained: `shellcheck` is the de-facto Haskell-based shell analyzer (MIT), `hadolint` codifies the Docker best-practice catalog, `yamllint` guards spec-compliant YAML, `actionlint` is the GitHub-published linter that also runs `shellcheck` against `run:` blocks, and `tflint` adds provider-aware Terraform rules above `terraform validate`. Skipping any of them lets a known class of outage land at runtime instead of pre-merge.

## When To Use

- Every repository that contains at least one Dockerfile, shell script, GitHub Actions workflow, Kubernetes manifest, Terraform file or non-trivial YAML config (i.e., effectively every production repo).
- Polyglot monorepos where app-code linters skip the IaC tree entirely.
- Repos with self-hosted CI or community-contributed workflows where action injection is a real attack surface.
- Hardening sprints after an incident traceable to a shell or Dockerfile bug.

## When NOT To Use

- Pure prose / Markdown / asset repos with no scripts, no CI workflows, no IaC — there is nothing for these tools to see.
- Throwaway prototype repos where the operational surface is hand-managed and never deployed automatically.
- Repos under active migration where IaC is being rewritten — schedule a one-shot baseline reset, then turn the hooks back on.

## Content

| File | What's inside |
|------|---------------|
| `content/01-iac-tool-baseline.xml` | The mandatory tool-per-format mapping and the rule that IaC findings block at the same severity as code findings. |
| `content/02-agent-fix-not-disable.xml` | Agent contract: fix the source (pin versions, quote vars, drop root) before reaching for `# shellcheck disable` or `# hadolint disable`. |

## Templates

| File | Purpose |
|------|---------|
| `templates/iac-precommit.yaml` | `.pre-commit-config.yaml` snippet wiring shellcheck, hadolint, yamllint, actionlint, tflint to the right file globs. |
| `templates/iac-ci.yml` | GitHub Actions matrix job running the full IaC linter set whole-tree on PR open. |
