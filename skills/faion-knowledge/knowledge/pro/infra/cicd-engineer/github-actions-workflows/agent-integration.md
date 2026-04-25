# Agent Integration — GitHub Actions Advanced Workflows

## When to use
- Repos already on GitHub where you've outgrown a one-job CI and need matrix builds, reusable workflows, multi-env deploys, or release automation.
- Multi-language / multi-OS test matrices (e.g. Node 18/20/22 × Linux/Win/Mac) — GHA's matrix is best-in-class.
- Cross-repo deploy orchestration via `workflow_call` reusable workflows + composite actions for shared steps.
- Cloud deploys via OIDC → AWS / GCP / Azure / HashiCorp Vault — short-lived creds, no long-lived secrets.
- Release pipelines (npm, PyPI, Docker images, GitHub Releases) triggered on tags with attestation/SBOM.

## When NOT to use
- Code on GitLab/Bitbucket — using GHA via mirrors is feasible but creates a dual source of truth and fragments PR review.
- Long-running batch (>6h job limit on GHA-hosted runners) — use self-hosted or a real workflow engine (Argo Workflows, Airflow).
- Pipelines that genuinely need stages with shared mutable state — GHA jobs are isolated runners; passing big state via artifacts is slow.
- Heavy parallel-fanout (1000+ jobs at once) — concurrency limits + queueing cause stalls; consider purpose-built systems (BuildKit cluster, Buildbarn).

## Where it fails / limitations
- **Action SHAs not pinned.** Agents use `actions/checkout@v4` then upstream tag is moved (Tj-actions incident, March 2025). Pin by SHA: `actions/checkout@b4ffde65f...`. Use Renovate to keep SHAs current.
- **`pull_request_target` misuse.** Runs in target repo context with secrets — agents wire it up for fork PRs and a malicious PR steals secrets. Use `pull_request` + minimal token scopes.
- **`GITHUB_TOKEN` over-permissioned.** Default permissions are write-all on classic; modern default read-only but old workflows lag. Always set `permissions:` explicitly per job.
- **OIDC audience drift.** Cloud role expects `aud: sts.amazonaws.com`; workflow sets a custom one and STS rejects, OR worse, uses default and trusts the wrong role.
- **Caching keys without lockfile hash.** `cache: ${{ runner.os }}-node` reuses stale deps across PRs. Always include `hashFiles('**/package-lock.json')`.
- **Cache cross-branch poisoning.** A malicious PR populates a cache key that main branch then restores. Scope caches per-branch or use `restore-keys:` carefully.
- **Matrix `fail-fast: true` (default).** First failure cancels everything — agents lose signal on Win/Mac when Linux fails. Set `fail-fast: false` for test matrices.
- **`needs:` graph missing.** Agents write 5 sequential jobs that could be parallel. Always model dependencies explicitly.
- **`continue-on-error` to "fix" flakes.** Hides real failures forever. Use `retry` action or fix the test.
- **Reusable workflow secret passing.** `secrets: inherit` passes ALL secrets — over-broad. Pass only what's needed.
- **Self-hosted runner registration.** `runs-on: self-hosted` without labels picks any runner; a malicious PR could target a privileged runner. Always require specific labels + ephemeral runners.
- **Concurrency mis-grouping.** `concurrency: ${{ github.workflow }}` cancels production deploys when staging deploy is queued. Group per-environment.
- **Workflow size limits.** 50MB workflow file, 50 jobs per workflow run, 256 nested matrix combos. Agents hit these silently.
- **Artifact retention default 90 days = storage bills.** Set `retention-days: 7` on intermediate artifacts.

## Agentic workflow
Treat workflow files as security-sensitive code. Have a planning agent map jobs as a DAG (with `needs:`) BEFORE writing YAML; classify each job by trust level (PR-context / main-context / release-context) and assign permissions accordingly. A second agent generates the workflow using composite actions for shared steps and reusable workflows for cross-repo patterns. A reviewer agent runs `actionlint` + a custom permissions auditor that flags any job with `permissions: write-all` or unpinned actions. For first deploy of a workflow that touches prod, require manual `workflow_dispatch` approval; only enable `push`-trigger after a clean dry run.

### Recommended subagents
- `faion-sdd-executor-agent` — drives spec → workflow → review; quality gate runs `actionlint` and a permissions check.
- `password-scrubber-agent` — `.github/workflows/*.yml` are a magnet for embedded tokens, registry creds, deploy keys.
- A custom `gha-permissions-auditor` (Sonnet, read-only) — given a workflow file, emits `{job, permissions, secrets_referenced[], oidc_aud, runs_on}` and flags any job with privileged `permissions:` or referencing prod secrets in a PR-trigger context.
- A custom `gha-action-pinner` — replaces `@vN` tag refs with current SHA + comment of version; integrates with Renovate for ongoing updates.

### Prompt pattern
```
Design a GitHub Actions workflow set for <repo>. Inputs: events (PR/push/tag/manual), build matrix, target envs, cloud provider for deploy, registry, package outputs.
Output: (1) DAG of jobs as Markdown table (job, needs[], trigger, runs-on, permissions, timeout), (2) YAML files split by trigger (ci.yml, cd.yml, release.yml, scheduled.yml), (3) reusable workflows under .github/workflows/_*.yml, (4) composite action for build/setup steps under .github/actions/, (5) per-env concurrency group + cancel-in-progress policy, (6) OIDC role ARNs and trust policy snippets.
Forbid: actions referenced by tag (must be by SHA), `permissions: write-all`, `pull_request_target` without env-protected job and explicit checkout of base ref, secrets in PR-trigger workflows, `continue-on-error: true` on critical jobs, missing timeout-minutes.
```

```
Audit: for every workflow file under .github/workflows/, parse YAML and emit JSON {workflow, jobs: [{job, runs_on, permissions, uses_actions: [{ref, pinned_to_sha}], secrets_referenced[], oidc_used, on_triggers[]}]}. Reject if any action ref is not a 40-char SHA, OR any prod-secret-referencing job triggers on a PR event from a fork.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh` | Official GitHub CLI: workflows, runs, artifacts, secrets | https://cli.github.com |
| `gh workflow run` / `gh run watch` | Trigger and tail workflow runs | built-in |
| `actionlint` | Static check workflows for syntax + common issues | https://github.com/rhysd/actionlint |
| `act` | Run GHA workflows locally in Docker | https://github.com/nektos/act |
| `gh attestation verify` | Verify build provenance attestations | https://docs.github.com/en/actions/security-guides/using-artifact-attestations |
| `gh secret` / `gh variable` | Manage secrets/vars from CLI; agent-friendly | built-in |
| `step-security/harden-runner` | Egress audit + block, replaces `harden-runner` GHA | https://github.com/step-security/harden-runner |
| `Renovate` | Bot to keep action SHAs current | https://docs.renovatebot.com |
| `Trivy` / `Grype` | Scan images built in workflow | https://github.com/aquasecurity/trivy |
| `cosign` + `gh attestation` | Sign + attest images, packages | https://docs.sigstore.dev/cosign |
| `octokit` SDKs (JS/Py) | Programmatic GHA control for agents | https://github.com/octokit |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub-hosted runners | SaaS | Yes | Default; pricing reduced 39% Jan 2026; ephemeral by default. |
| Self-hosted runners | OSS | Partial | Use only with `runner-controller` (ARC) on K8s for ephemeral pods; never long-lived VMs. |
| Actions Runner Controller (ARC) | OSS | Yes | K8s operator for ephemeral self-hosted runners; agent-friendly via Helm. |
| Larger / GPU runners | SaaS | Yes | `runs-on: ubuntu-latest-8-cores` etc; matters for ML jobs. |
| Reusable workflows + composite actions | OSS | Yes | Internal sharing across repos in same org. |
| GitHub Marketplace actions | OSS | Partial | Audit before use; pin by SHA always. |
| OIDC (AWS / GCP / Azure / Vault) | SaaS | Yes | Replace long-lived secrets; mandatory for any prod deploy. |
| Step Security Harden Runner | SaaS / OSS | Yes | Network egress filtering, file integrity — defends against malicious dependency. |
| GitHub Environments | SaaS | Yes | Approval gates, env-scoped secrets, deployment timelines. |
| Codespaces / dev containers | SaaS | Partial | Useful for `act`-equivalent local runs. |
| ChatOps via `peter-evans/slash-command-dispatch` | OSS | Yes | Agents trigger workflows from PR comments. |

## Templates & scripts
See `templates.md` and `examples.md` for full multi-env CD pipeline. Permissions auditor (≤30 lines) — agents should run on every PR that touches `.github/`:

```python
# scripts/gha-audit.py
import sys, yaml, re, json, pathlib
SHA = re.compile(r"^[0-9a-f]{40}$")
issues = []
for path in pathlib.Path(".github/workflows").glob("*.y*ml"):
    wf = yaml.safe_load(path.read_text())
    for job_name, job in (wf.get("jobs") or {}).items():
        perms = job.get("permissions", wf.get("permissions", "default"))
        if perms == "write-all" or (isinstance(perms, dict) and perms.get("contents") == "write" and "pull_request" in (wf.get("on") or {})):
            issues.append({"file": str(path), "job": job_name, "issue": "broad_permissions_on_pr_trigger"})
        for step in job.get("steps", []):
            uses = step.get("uses", "")
            if "@" in uses:
                ref = uses.rsplit("@", 1)[1]
                if not SHA.match(ref):
                    issues.append({"file": str(path), "job": job_name, "issue": "unpinned_action", "ref": uses})
print(json.dumps(issues, indent=2))
sys.exit(1 if issues else 0)
```

## Best practices
- Pin every `uses:` to a 40-char SHA, not a tag. Renovate keeps them fresh.
- Set `permissions:` explicitly at workflow OR job level — never rely on org default.
- Use OIDC for all cloud auth: GH OIDC issuer + cloud STS / Vault. Zero long-lived `*_ACCESS_KEY` secrets.
- Reusable workflows for cross-repo patterns; composite actions for shared steps within a repo.
- One concurrency group per `(workflow, env)`; `cancel-in-progress: true` for PR builds, `false` for prod deploys.
- `timeout-minutes:` on every job — default 360 is too long; use 15-30 for tests, 60 for builds, 120 for deploys.
- Cache with `actions/cache@v4`: key on lockfile hash; restore-keys for graceful fallback; one cache per language ecosystem.
- GitHub Environments for prod with required reviewers + wait timer + branch protection.
- Artifact retention 7 days for intermediate, 90 default only for releases.
- Add `step-security/harden-runner@<sha>` as first step on every job — egress audit catches supply-chain compromise.
- Always sign + attest releases with `actions/attest-build-provenance` + cosign.

## AI-agent gotchas
- Agents copy public marketplace actions referenced by tag; tag gets force-moved (March 2025 supply-chain incident affecting `tj-actions/changed-files`). SHA-pin is non-negotiable.
- `pull_request_target` looks like `pull_request` — agents wire it up to "get secrets working for fork PRs" and create a code-execution-with-secrets vulnerability. Forbid PR-target unless behind environment + base-ref-only checkout.
- `${{ ... }}` interpolation in `run:` is shell-injection: `run: echo "${{ github.event.pull_request.title }}"` — a PR title `"; rm -rf /` runs. Use env vars + reference `$TITLE`, not `${{ ... }}`.
- GHA's `secrets` inheritance via `secrets: inherit` in reusable workflows passes everything; agents do this for convenience and over-expose.
- Concurrency cancellation kills in-flight prod deploys when a new commit lands. Agents set `cancel-in-progress: true` globally; deploys must be `false`.
- `outputs:` from a job require `id:` on the producing step AND `outputs:` mapping at job level — agents miss one half and the consumer job sees empty string.
- Matrix exclusions / inclusions order: `include:` after `matrix:` adds; `exclude:` first removes. Agents mis-order and end up with phantom combos.
- Self-hosted runner with `runs-on: self-hosted` and no labels: a fork PR can run on the priv runner. Use `runs-on: [self-hosted, repo-name, ephemeral]` and ARC.
- Human-in-loop checkpoints (mandatory): adding a new `secrets:` entry, granting a new OIDC trust policy, enabling self-hosted runners on a public repo, lowering env protection rules. All credential-equivalent.
- Caching is global per repo — a malicious PR populates `node_modules` cache; main branch restores it next run. Scope caches by branch or invalidate on lockfile change.
- `actions/cache@v4` API change in Feb 2025 — agents using v3 silently fail. Bump version and verify cache hits in logs.

## References
- GitHub Actions docs — https://docs.github.com/en/actions
- Security hardening — https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions
- OIDC with cloud providers — https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect
- Reusable workflows — https://docs.github.com/en/actions/using-workflows/reusing-workflows
- `actionlint` — https://github.com/rhysd/actionlint
- `act` (local runner) — https://github.com/nektos/act
- StepSecurity blog — https://www.stepsecurity.io/blog
- Tj-actions incident postmortem — https://www.stepsecurity.io/blog/harden-runner-detection-tj-actions-changed-files-action-is-compromised
- ARC for self-hosted runners — https://github.com/actions/actions-runner-controller
- Artifact attestations — https://docs.github.com/en/actions/security-guides/using-artifact-attestations
