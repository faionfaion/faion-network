# Agent Integration — GitHub Actions Basics

## When to use
- Repos hosted on GitHub: GHA is the path of least resistance for CI.
- Open source projects — public repos run free, including Linux/Win/Mac matrix.
- Teams that want PR checks, status badges, and release automation tied directly to GitHub events.
- Simple-to-medium pipelines (build, test, lint, deploy) — most workflows fit comfortably in a single `.github/workflows/ci.yml`.
- First CI/CD setup for a project: GHA's marketplace + minimal config gets a green build in minutes.

## When NOT to use
- Code on GitLab/Bitbucket — the native CI is a better fit.
- Complex multi-team multi-repo orchestration where reusable workflows / composite actions strain — at that point evaluate true workflow engines.
- Heavy long-running batch (>6h on hosted runners; >35 days on self-hosted with ARC). Use Argo Workflows / Airflow / Prefect.
- Deeply customized agents needing persistent state — GHA runners are ephemeral; engineering around that is more work than picking a different tool.

## Where it fails / limitations
- **Default permissions.** New repos default to read-only `GITHUB_TOKEN`, but old workflows still inherit write-all. Always set `permissions:` explicitly.
- **`actions/checkout@v4` with default settings** fetches with `persist-credentials: true` — credentials persist on disk, accessible to subsequent steps. Force `persist-credentials: false` unless needed.
- **`workflow_dispatch` inputs unsanitized** in `run:` steps — `${{ inputs.tag }}` interpolation = shell injection. Always pass via env var.
- **`schedule:` triggers run on default branch only.** Agents put scheduled jobs on a feature branch and wonder why they never fire.
- **Free-tier minutes burn on private repos.** A test matrix multiplies fast: 3 OSes × 4 versions × 5 minutes = 60 minutes per push. 2000 free min/month exhausted in days.
- **`runs-on: ubuntu-latest`** drifts: a workflow stable for months breaks when GHA rolls a new image (Node ABI change, glibc bump). Pin `ubuntu-22.04` for stability.
- **Action Marketplace risk.** Anyone can publish an action. Tag refs (`@v3`) can be moved silently (Tj-actions, March 2025). Always pin to SHA.
- **Concurrency without environment scoping.** `concurrency: ${{ github.workflow }}-${{ github.ref }}` cancels in-progress runs on same ref — desirable for PRs, dangerous for `main` deploys. Group correctly.
- **Self-hosted runner exposure.** `runs-on: self-hosted` on a public repo allows fork PRs to execute on your runner. Always pair with org-level approval requirement + ephemeral ARC pods.
- **Cache size limits.** 10 GB per repo; old caches evicted LRU. Agents cache `node_modules` plus `.next/cache` plus `.docker` and the cache thrashes — net slowdown.
- **`needs:` fan-out limit.** Hard limit ~256 jobs in a workflow run. Big matrix + per-platform deploy hits it.
- **Reusable workflow + secrets.** Default does NOT pass secrets; either explicit list or `secrets: inherit`. Agents pick `inherit` for convenience and over-share.

## Agentic workflow
Start small. Have one agent generate a single `ci.yml` (build + test + lint) covering the actual matrix needed and nothing else; classify what's CI vs. CD vs. release and split into multiple workflows only when you have a reason. Pin all action SHAs from day one (Renovate keeps them current). A reviewer agent runs `actionlint` + a permissions check on every change to `.github/`. For deploys, prefer `workflow_dispatch` (manual) before automating; only graduate to push triggers after a clean dry run. Agents must never put long-lived cloud creds in repo secrets — wire OIDC instead, even for "basic" workflows.

### Recommended subagents
- `faion-sdd-executor-agent` — quality gate runs `actionlint` + checks all `uses:` are SHA-pinned + verifies `permissions:` is explicit.
- `password-scrubber-agent` — workflow files attract embedded tokens, deploy keys, registry creds.
- A custom `gha-cost-projector` (Haiku) — given a workflow file, estimates monthly minutes from matrix size × trigger frequency × average duration.
- A custom `gha-permissions-auditor` (Sonnet) — flags any workflow with broad permissions on PR triggers, secrets referenced in fork-context jobs.

### Prompt pattern
```
Generate a starter GHA workflow for <repo>. Inputs: language, test framework, OS+version matrix, lint tools, deploy target (or "none"), public-or-private repo.
Output: (1) `.github/workflows/ci.yml` with explicit `permissions:`, SHA-pinned actions, matrix with `fail-fast: false`, `timeout-minutes: 15`, lockfile-keyed cache, (2) optional `cd.yml` (only if deploy target given) with OIDC auth and environment protection, (3) `.github/dependabot.yml` for action updates, (4) projected monthly minutes at current PR + main commit cadence.
Forbid: actions referenced by tag (must be SHA), `permissions: write-all`, secrets in PR-trigger jobs, `runs-on: ubuntu-latest` in production workflow (pin to specific version), `${{ ... }}` interpolation inside `run:` (use env vars).
```

```
Audit: parse `.github/workflows/*.yml`. For each workflow emit JSON {file, on[], jobs: [{name, runs_on, permissions, uses_actions: [{ref, sha_pinned}], secrets_referenced[], oidc_used, on_pr_or_pr_target}]}. Reject if any (uses ref not 40-char SHA) OR (permissions == "write-all") OR (secrets referenced AND on includes pull_request_target without environment protection).
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh` | Official GitHub CLI: workflows, runs, secrets, env | https://cli.github.com |
| `gh workflow run <name> -f input=value` | Manual trigger via CLI; agent-driven runs | built-in |
| `gh run list` / `gh run watch` / `gh run view --log` | Tail workflow runs from CLI | built-in |
| `actionlint` | Static analysis of workflow files (catches 90% of bugs) | https://github.com/rhysd/actionlint |
| `act` | Run GHA workflows locally in Docker for fast iteration | https://github.com/nektos/act |
| `gh secret set` / `gh variable set` | Manage repo/env secrets and variables | built-in |
| `gh attestation verify` | Verify build provenance / SBOM attestations | https://docs.github.com/en/actions/security-guides/using-artifact-attestations |
| `Renovate` / `dependabot` | Bot for action SHA updates | https://docs.renovatebot.com |
| `step-security/harden-runner` | Egress filter on workflow runners | https://github.com/step-security/harden-runner |
| `yamllint` + `pre-commit` GHA hook | Catch YAML errors before push | https://yamllint.readthedocs.io |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub-hosted runners | SaaS | Yes | Default, ephemeral, 4-vCPU/16GB; price reduced 39% Jan 2026. |
| Larger runners (8/16/32-vCPU + GPU) | SaaS | Yes | `runs-on: ubuntu-latest-8-cores`; matters for ML / compile. |
| Self-hosted runners + ARC | OSS | Partial | K8s-based ephemeral runners; never long-lived VMs on public repos. |
| GitHub Marketplace actions | OSS / SaaS | Partial | Audit + SHA-pin every action; treat unknown publishers as risk. |
| Reusable workflows | OSS | Yes | `workflow_call` for cross-repo / cross-job sharing. |
| Composite actions | OSS | Yes | Local `.github/actions/foo/action.yml` for shared steps. |
| GitHub Environments | SaaS | Yes | Approval gates, env secrets, branch protection. |
| OIDC providers (AWS/GCP/Azure/Vault) | SaaS | Yes | Default for cloud auth; replaces static `*_ACCESS_KEY` secrets. |
| GitHub Container Registry (GHCR) | SaaS | Yes | Free for public; OIDC-auth in workflows trivially. |
| Codecov / SonarCloud / similar | SaaS | Yes | Standard PR-comment integrations. |
| Step Security Harden Runner | SaaS / OSS | Yes | Audit / block egress; defense against malicious deps. |

## Templates & scripts
See `templates.md` and `examples.md` for full templates. Minimal-but-correct starter (≤40 lines) — agents should copy this and only add what's needed:

```yaml
# .github/workflows/ci.yml
name: CI
on:
  pull_request:
  push:
    branches: [main]

permissions:
  contents: read

concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true

jobs:
  test:
    runs-on: ubuntu-22.04
    timeout-minutes: 15
    strategy:
      fail-fast: false
      matrix:
        node: [20, 22]
    steps:
      - uses: step-security/harden-runner@0080882f6c36860b6ba35c610c98ce87d4e2f26f # v2.10.2
        with:
          egress-policy: audit
      - uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11 # v4.1.1
        with:
          persist-credentials: false
      - uses: actions/setup-node@1e60f620b9541d16bece96c5465dc8ee9832be0b # v4.0.3
        with:
          node-version: ${{ matrix.node }}
          cache: npm
      - run: npm ci
      - run: npm test
      - run: npm run lint
```

## Best practices
- One workflow per concern (`ci.yml`, `cd.yml`, `release.yml`, `scheduled.yml`); don't cram everything into one giant file.
- `permissions: contents: read` at workflow level; expand per-job only when needed.
- Pin every `uses:` to a 40-char SHA + version comment. Renovate keeps them fresh.
- `actions/checkout@<sha>` with `persist-credentials: false` unless a later step needs git operations.
- Pin runner OS (`ubuntu-22.04`, not `ubuntu-latest`) for reproducibility.
- `concurrency` per `(workflow, ref)`; cancel-in-progress for PRs, off for prod deploys.
- `timeout-minutes:` on every job (15-30 typical, 60 max for builds).
- `fail-fast: false` on test matrices so all platforms report.
- Cache with lockfile-hash key + restore-keys fallback; one cache per ecosystem.
- Use OIDC for cloud auth from day one; never put `AWS_ACCESS_KEY_ID` as a secret.
- Add `step-security/harden-runner` as the first step of every job — at least `audit` mode.
- GitHub Environments for prod with required reviewer + branch protection; secrets scoped to env.
- `Dependabot` or `Renovate` enabled for `github-actions` ecosystem to keep SHAs current.

## AI-agent gotchas
- Agents copy `actions/checkout@v4` everywhere — tag refs are mutable. Force SHA pinning from the very first PR.
- `${{ github.event.pull_request.title }}` (or any user input) inside `run:` = shell injection. Always pass through `env:` and reference `$VAR`.
- `pull_request_target` looks innocent but runs in target repo context with secrets — agents enable it for fork PRs and create RCE-with-secrets. Forbid unless the workflow has env protection + base-ref-only checkout + read-only token.
- Reusable workflow `secrets: inherit` over-shares; agents use it because it "just works". Pass explicit list only.
- Cron `schedule:` runs on default branch — agents test on feature branch and never see it fire. Document in PR description.
- Cache hit ≠ correctness: a cached `node_modules` from before a `package.json` engines bump will install but break at runtime. Always include lockfile hash in cache key.
- Self-hosted runner registration on a public repo + fork PR = remote code execution on your infra. Use ARC ephemeral runners or org-level approval.
- `${{ secrets.X }}` in PR-triggered workflows for forks: secrets are NOT passed to fork PRs by default — agents debug "why is my deploy step empty" and don't realize this is intentional.
- GHA cache writes from PR can poison caches restored by `main`. Scope cache keys per branch when threat model demands.
- Human-in-loop checkpoints: enabling self-hosted runners, granting new OIDC trust, lowering env protection, adding org-level secrets. All credential-equivalent.
- Workflow files in `.github/workflows/` from a fork PR run on hosted runners only by default — but `pull_request_target` flips this. Read the docs every time.
- `${{ env.X }}` vs. `${{ vars.X }}` vs. `${{ secrets.X }}` — agents conflate them, exposing repo variables thinking they're secrets, or vice versa.

## References
- GitHub Actions docs — https://docs.github.com/en/actions
- Security hardening — https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions
- OIDC overview — https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect
- Reusable workflows — https://docs.github.com/en/actions/using-workflows/reusing-workflows
- `actionlint` — https://github.com/rhysd/actionlint
- `act` — https://github.com/nektos/act
- StepSecurity blog — https://www.stepsecurity.io/blog
- Tj-actions postmortem — https://www.stepsecurity.io/blog/harden-runner-detection-tj-actions-changed-files-action-is-compromised
- ARC for self-hosted runners — https://github.com/actions/actions-runner-controller
- GitHub Pricing 2026 — https://github.blog/changelog/2025-12-16-coming-soon-simpler-pricing-and-a-better-experience-for-github-actions/
