# Agent Integration — GitLab CI/CD

## When to use
- Repo lives on GitLab (SaaS or self-hosted) and the team already uses GitLab issues / MRs / Container Registry — pipeline lives next to the code.
- Need a single platform that bundles SCM + CI + registry + DAST/SAST + Pages + Kubernetes Agent without gluing 5 SaaS tools together.
- Pipelines need fan-out / parent-child / multi-project triggering — GitLab's `trigger:` and `include:` are first-class, simpler than reusable workflows in GHA for cross-repo use.
- Compliance environments where every stage must produce an artifact / SBOM / scan report attached to a pipeline that auditors can pull from one place.
- Self-hosted runners on K8s with the GitLab Runner Helm chart — autoscaling executor pods per job is painless.

## When NOT to use
- Codebase on GitHub or Bitbucket — using GitLab CI as an external runner via mirror/webhook is technically possible but creates a dual-source-of-truth headache.
- Tiny throwaway projects — `.gitlab-ci.yml` syntax has more surface area (rules, workflow, includes, extends) than a one-job GHA workflow.
- Teams that need OSS-friendly free tier matching GHA — GitLab.com free CI minutes are tighter; for public repos GHA is genuinely free.

## Where it fails / limitations
- `rules:` vs `only/except` confusion: agents copy old `only/except` snippets from blogs, which silently get overridden by `workflow:rules`. Force `rules:` only.
- Stages without `needs:` serialize the whole pipeline. Default templates in old projects do this and waste 60%+ of wall time.
- `dependencies:` vs `needs:artifacts:` — both pass artifacts but `needs` activates DAG. Mixing them produces non-obvious "where did my file go" bugs.
- Cache vs artifacts: agents reach for `artifacts:` when they want `cache:` (or vice versa). Artifacts are uploaded to GitLab on every job; caches are runner-local by default — cache key + policy matters.
- `extends:` plus YAML anchors (`&`/`*`) plus `include:` with overrides → final job spec is unreadable. Agents lose track of what actually runs. Always run `gitlab-ci-lint` and inspect the merged config.
- Protected branches / protected variables: secrets only flow on protected refs. Agents test on a feature branch, secret is empty, job fails with cryptic "permission denied".
- Self-hosted Docker executor with `dind` is slow and racy. Prefer Kubernetes executor with BuildKit, or use rootless `kaniko`/`buildah`.
- GitLab runner concurrency setting is per-runner-process, not per-project — easy to over-saturate a self-hosted box.

## Agentic workflow
Have one agent draft the pipeline structure (stages, jobs, DAG via `needs:`, env-aware `rules:`) as a Markdown table BEFORE writing YAML — this catches "this job has no real trigger" at design time. A second agent generates `.gitlab-ci.yml` using `extends:` for shared steps and a small `include:` library. Always pipe the result through `glab ci lint` (or `POST /ci/lint`) inside the agent loop; YAML that lints clean still fails on `rules:` semantics, so trigger a sandboxed run on a draft MR before merging. A reviewer agent inspects merged config (`glab ci config`) and the timing/parallelism actually achieved on first run.

### Recommended subagents
- `faion-sdd-executor-agent` — drives spec → impl → review with the quality gates that pipelines need (lint, dry-run, draft MR run).
- `password-scrubber-agent` — `.gitlab-ci.yml` is a magnet for tokens, registry creds, and `CI_DEPLOY_USER` style vars accidentally hard-coded.
- A custom `pipeline-dag-auditor` (Sonnet, read-only) — given the merged config, lists each job's `needs:`, flags any stage with sequential dependencies that could be parallel.

### Prompt pattern
```
Design a GitLab CI pipeline for <repo>. Inputs: language, deployable artifact (image / package / static site), target envs (dev/stage/prod), security scanners required.
Output: (1) job DAG as a Markdown table (job, needs[], trigger rule, runtime estimate), (2) `.gitlab-ci.yml` using `extends:` and `include:` for shared steps, (3) protected vs unprotected variables list, (4) cache vs artifact decisions per job, (5) worst-case wall time vs critical path.
Forbid: only/except, dind without rootless mitigation, untagged Docker image refs, cache without explicit key tied to lockfile, missing `rules:` (so jobs run on every event).
```

```
Lint and dry-run: `glab ci lint --json .gitlab-ci.yml`. Then for each job emit JSON: {job, stage, needs, when, will_run_on_branch_push, will_run_on_mr, will_run_on_tag, secrets_required[]}. Reject if any job's secrets_required is non-empty AND its trigger fires on unprotected refs.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `glab` | Official GitLab CLI: pipelines, MRs, vars, lint | https://gitlab.com/gitlab-org/cli |
| `glab ci lint` | Validate `.gitlab-ci.yml` against the project's merged config | https://docs.gitlab.com/ee/api/lint.html |
| `glab ci view` / `glab ci status` | Watch a running pipeline, get failed job logs | https://gitlab.com/gitlab-org/cli/-/blob/main/docs/source/ci/view.md |
| `gitlab-runner exec docker <job>` | Run a single job locally in Docker | https://docs.gitlab.com/runner/commands/#gitlab-runner-exec |
| `python-gitlab` / `ruby-gitlab` SDK | Programmatic pipeline mgmt for agents | https://python-gitlab.readthedocs.io |
| `yamllint` + `pre-commit` GitLab hook | Catch YAML errors before push | https://yamllint.readthedocs.io |
| `kaniko` / `buildah` / `BuildKit` | Container builds without privileged dind | https://github.com/GoogleContainerTools/kaniko |
| `cosign` | Sign images produced by pipeline; verify in deploy job | https://docs.sigstore.dev/cosign |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitLab.com | SaaS | Yes | REST + GraphQL APIs are complete; `glab` covers 90% of agent needs. |
| GitLab Self-Managed (CE/EE) | OSS / Commercial | Yes | Same APIs; agent code is portable. EE adds compliance + protected env approvals. |
| GitLab Runner (Kubernetes executor) | OSS | Yes | Helm chart, autoscaling per job, supports IAM via projected SA token. |
| GitLab Runner (Docker autoscaler) | OSS | Yes | Replacement for `docker-machine` executor (deprecated). |
| HashiCorp Vault | OSS / SaaS | Yes | First-class JWT auth (`id_tokens:`) — short-lived secrets per job, no static `CI_VARS`. |
| AWS / GCP / Azure OIDC | SaaS | Yes | `id_tokens:` → cloud STS, no long-lived keys in protected vars. |
| Renovate / Dependabot-on-GitLab | OSS | Yes | Bot-driven MRs that pipelines validate. |
| Sigstore / cosign / Rekor | OSS | Yes | Sign + attest images; verify on deploy. |
| GitLab Pages | SaaS / Self-managed | Yes | Use `pages:` job for previews / docs from MR. |
| Auto DevOps | Built-in | Partial | Magic templates speed start but hide real config; agents struggle to debug. Prefer explicit pipelines. |

## Templates & scripts
See `templates.md` and `examples.md` for full pipelines. Minimal DAG-style starter (≤45 lines) the agent should use as a default skeleton:

```yaml
# .gitlab-ci.yml
include:
  - template: Security/SAST.gitlab-ci.yml
  - template: Security/Secret-Detection.gitlab-ci.yml

workflow:
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
    - if: $CI_COMMIT_TAG

variables:
  DOCKER_IMAGE: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA

stages: [build, test, scan, deploy]

.go: &go
  image: golang:1.22-alpine
  cache:
    key:
      files: [go.sum]
    paths: [.gocache/]
  variables:
    GOMODCACHE: $CI_PROJECT_DIR/.gocache

build:
  <<: *go
  stage: build
  script: [go build -o app ./cmd/...]
  artifacts: { paths: [app], expire_in: 1 day }

test:
  <<: *go
  stage: test
  needs: [build]
  script: [go test -race -coverprofile=cov.out ./...]

deploy:stage:
  stage: deploy
  needs: [build, test]
  rules: [{ if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH }]
  environment: { name: staging, url: https://stage.example.com, auto_stop_in: 24 hours }
  id_tokens:
    AWS_TOKEN: { aud: https://sts.amazonaws.com }
  script: [./deploy.sh]
```

## Best practices
- One source of truth for triggers: `workflow:rules`. Job-level `rules:` only narrow further. Never mix `only/except` with `rules:`.
- Replace stage-only ordering with `needs:` everywhere reasonable — flatten the DAG; aim for critical path = max(slowest_chain), not sum(all_jobs).
- Cache key = lockfile hash + runner OS. `cache:policy: pull` on consumer jobs to avoid useless re-uploads.
- Use `id_tokens:` + Vault/AWS OIDC; delete every long-lived `AWS_ACCESS_KEY_ID` from protected variables.
- Mark every prod-bound variable as Protected + Masked + Hidden (GitLab 17+). Verify via `glab variable list --json`.
- Run pipelines in MR scope (`merge_request_event`) and on default branch — not both for the same job, or you double-charge minutes.
- Tag every runner; tag every job. Untagged runners pick up jobs they should not — common cause of leaked secrets onto a shared runner.
- Pin image refs by digest (`alpine@sha256:...`) for build determinism; bot/agent updates them via Renovate.
- Cap pipeline length: kill anything > 30 min by splitting parent/child or moving slow tests to nightly schedule.

## AI-agent gotchas
- Agents copy `image: docker:dind` patterns from outdated blogs. Force BuildKit / Kaniko / rootless Buildah and explicit `services:` if dind is truly needed.
- `extends:` chains: agents extend a job that itself extends another and overrides `script:` — the resulting `script:` is the deepest `script:`, not concatenated. Document this and emit a "merged effective config" preview for human review.
- Variables precedence (project → group → instance → file → job) is a real source of incidents. Agents add a project var that gets masked by a group var. Always print effective vars from `glab ci view` on first run.
- Long pipelines hit the 1MB log cap; agents see "log truncated" and chase ghosts. Add `set -x` only behind a flag.
- Multi-project pipelines (`trigger:`) cross-project secrets do NOT propagate. Agents wire a `deploy` trigger across projects and wonder why the deploy job has no creds.
- Human-in-loop checkpoints: any new protected variable, new ID-token audience, or new self-hosted runner registration MUST go through human approval — these are credential-equivalent operations.
- GitLab 18 immutable artifact tags are great but break agents that re-tag during retries. Coordinate retry policy with the immutability flag.

## References
- GitLab CI/CD reference — https://docs.gitlab.com/ee/ci/yaml/
- Pipeline efficiency — https://docs.gitlab.com/ee/ci/pipelines/pipeline_efficiency.html
- ID tokens & OIDC — https://docs.gitlab.com/ee/ci/secrets/id_token_authentication.html
- GitLab Runner Helm chart — https://docs.gitlab.com/runner/install/kubernetes.html
- `glab` CLI — https://gitlab.com/gitlab-org/cli
- Rules vs only/except — https://docs.gitlab.com/ee/ci/jobs/job_rules.html
