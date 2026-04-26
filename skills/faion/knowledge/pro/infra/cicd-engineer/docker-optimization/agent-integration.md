# Agent Integration — Docker Optimization

## When to use
- Image is bigger than 200 MB and pull/push latency or storage cost is real (CI minutes, edge deploys, K8s pod start time).
- CVE / supply-chain pressure: need to reduce attack surface, switch to distroless / Chainguard, sign + attest.
- Build times have crept past 5 minutes and BuildKit cache mounts / multi-stage refactor would actually help.
- Multi-arch builds (linux/amd64 + linux/arm64) for ARM laptops + Graviton/Ampere production.
- Compliance requirement to run as non-root, read-only filesystem, no shell.

## When NOT to use
- Hobby projects, internal-only single-tenant apps where image size genuinely doesn't matter — premature optimization burns more dev time than it saves.
- Already-distroless image being "optimized" further by switching base every quarter — diminishing returns.
- Apps that need a shell + package manager at runtime (debugging-heavy services). Going scratch/distroless creates ops drag.
- Build that's slow because TESTS are slow, not because the image is bloated. Profile before optimizing.

## Where it fails / limitations
- **Multi-stage stripping that breaks runtime.** Agents copy only the binary but forget timezone data, CA certs, locale files. Container starts, then breaks on first TLS call.
- **Distroless + dynamic linking.** `gcr.io/distroless/static` for a Go binary built with cgo links to glibc → segfault. Must use `distroless/base` or static-build the binary.
- **Alpine + glibc apps.** Python / Node wheels compiled against glibc fail on Alpine's musl. Result: silent ABI errors. Use `python:3.12-slim` (Debian) instead.
- **Layer order ignored.** Agents `COPY . .` before `RUN pip install` → every code change busts the dep cache. Order: deps file → install → app code.
- **`apt-get update` without cleanup.** Layer keeps the apt cache; image grows by 50MB. Always `apt-get update && apt-get install -y --no-install-recommends X && rm -rf /var/lib/apt/lists/*` in one RUN.
- **Cache mounts not enabled.** Without `# syntax=docker/dockerfile:1.7` and `--mount=type=cache,target=/root/.cache/...`, BuildKit cache mounts are ignored.
- **`.dockerignore` missing or wrong.** `.git/`, `node_modules/`, build outputs, IDE configs land in build context → 500MB context for a 10MB project. Build is slow before it even starts.
- **Root user as default.** Even when not malicious, K8s `runAsNonRoot: true` PSP rejects the pod. Always `USER 65532:65532`.
- **`COPY --chown=` after layer cache invalidation.** Each chown rewrites the layer; large `node_modules` chowned in one COPY = 200MB layer.
- **Hardcoded image tags (`python:3.12`).** Agents update Python; tag floats and breaks. Pin by digest: `python:3.12-slim@sha256:...`.
- **Buildx multi-arch without QEMU emulation in CI.** Cross-arch build is 10x slower; agents enable it without realizing the cost.
- **Health-check shell expansion.** `HEALTHCHECK CMD curl -f http://localhost:8080/h || exit 1` requires a shell — distroless has none. Use exec form + the binary itself.
- **`CMD ["sh", "-c", "..."]` in distroless.** Crashes — no shell. Use exec form `CMD ["/app", "--flag", "value"]`.

## Agentic workflow
Treat the Dockerfile as a layered cache program, not just a recipe. Have a planning agent classify the build (compiled binary / interpreted with deps / static assets / mixed) and pick a base accordingly (scratch / distroless / chainguard / slim) BEFORE writing the Dockerfile. A second agent writes the Dockerfile with explicit layer ordering, BuildKit cache mounts, multi-stage build, non-root user, and digest-pinned base. A reviewer agent runs `hadolint`, `dive`, and `trivy image` on the built artifact and emits a per-layer breakdown. For prod images, agents also generate SBOM (`syft`) and sign with `cosign`. The build pipeline must produce an attestation; downstream deploys verify it.

### Recommended subagents
- `faion-sdd-executor-agent` — drives Dockerfile spec → impl → review; quality gate must include hadolint + trivy + dive layer summary.
- `password-scrubber-agent` — Dockerfiles attract `ARG SECRET_KEY` / hardcoded npm tokens / `RUN curl -u ...` patterns.
- A custom `dockerfile-layer-auditor` (Sonnet, read-only) — given a Dockerfile, emits per-layer estimated size + cache-hit-rate + flags ordering issues.
- A custom `image-cve-gate` — runs trivy/grype on built image; blocks merge if any HIGH/CRITICAL with available fix.

### Prompt pattern
```
Optimize Dockerfile for <app>. Inputs: language + framework, runtime needs (TLS, timezone, fonts, etc.), target arch list, prod or dev image, max acceptable size MB, CVE budget (none/low/medium-or-below).
Output: (1) base image choice + rationale (scratch/distroless/chainguard/slim), (2) full Dockerfile with `# syntax=docker/dockerfile:1.7`, multi-stage, BuildKit cache mounts, digest-pinned base, non-root USER, .dockerignore, (3) expected size delta vs. current, (4) hadolint clean output, (5) trivy summary expected.
Forbid: ADD when COPY suffices, root user, `apt-get install` without cleanup, COPY of .git or node_modules, base by floating tag, `latest` tag, missing HEALTHCHECK in exec form, dev tools (curl, vim) in prod image.
```

```
Build & audit: `docker buildx build --platform linux/amd64,linux/arm64 --sbom=true --provenance=true -t test:audit .` ; then run `hadolint`, `dive --json test:audit`, `trivy image --severity HIGH,CRITICAL --exit-code 1 test:audit`. Emit JSON {size_mb, layer_count, hadolint_warnings[], cves: {critical, high, fixable}, dive_efficiency, layers_over_50mb[]}. Reject if size_mb > BUDGET OR fixable critical/high CVEs > 0.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `docker buildx` | Multi-arch + BuildKit-native build | https://docs.docker.com/buildx/ |
| `hadolint` | Dockerfile linter — agent's first quality gate | https://github.com/hadolint/hadolint |
| `dive` | TUI/JSON layer analysis: spot waste, find fat layers | https://github.com/wagoodman/dive |
| `trivy image` / `grype` | CVE scan on built image | https://github.com/aquasecurity/trivy |
| `docker scout` | Docker's built-in CVE + recommendations | https://docs.docker.com/scout/ |
| `syft` | SBOM generator (SPDX, CycloneDX) | https://github.com/anchore/syft |
| `cosign` | Sign + verify images, attest SBOM | https://docs.sigstore.dev/cosign |
| `docker-slim` (slim toolkit) | Auto-minify image by tracing runtime usage | https://github.com/slimtoolkit/slim |
| `crane` | Container registry / image manipulation | https://github.com/google/go-containerregistry/tree/main/cmd/crane |
| `regctl` | Inspect / copy / mutate manifests in registry | https://github.com/regclient/regclient |
| `buildah` | Daemonless image build (rootless friendly) | https://buildah.io |
| `kaniko` | In-cluster image build, no Docker daemon | https://github.com/GoogleContainerTools/kaniko |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Docker Hub | SaaS | Yes | Free public; rate-limited pulls; mirror via cache for CI. |
| GitHub Container Registry (GHCR) | SaaS | Yes | Free for public, tight GHA integration, OIDC auth. |
| AWS ECR | SaaS | Yes | Cross-account replication; ECR Public for OSS. |
| GCP Artifact Registry | SaaS | Yes | Workload Identity Federation = no static keys. |
| Azure Container Registry | SaaS | Yes | ACR Tasks for in-cloud builds. |
| Harbor | OSS | Yes | Self-hosted with replication, vulnerability scan, signing. |
| Chainguard Images | SaaS / OSS | Yes | Zero-CVE base images; `cgr.dev/chainguard/<lang>` . |
| Distroless (Google) | OSS | Yes | `gcr.io/distroless/static`/`base`/`cc`/`python3` etc. |
| Wolfi (Chainguard's distro) | OSS | Yes | Underlies Chainguard images; build your own. |
| BuildKit (CI cluster) | OSS | Yes | Shared remote cache via `type=registry` for fast CI builds. |
| Sigstore / Rekor | OSS | Yes | Public transparency log for signed images. |
| Earthly / Dagger / Bazel rules_oci | OSS | Partial | Higher-level build DSLs; agents can use but harder to debug. |

## Templates & scripts
See `templates.md` and `examples.md` for language-specific templates. Reference Python multi-stage Dockerfile (≤45 lines) — agent's safe default:

```dockerfile
# syntax=docker/dockerfile:1.7

ARG PY_VER=3.12-slim-bookworm
ARG PY_DIGEST=sha256:replace_with_actual_digest

FROM python:${PY_VER}@${PY_DIGEST} AS builder
ENV PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1
WORKDIR /build
RUN --mount=type=cache,target=/root/.cache/pip,sharing=locked \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    pip install --prefix=/install -r requirements.txt

FROM python:${PY_VER}@${PY_DIGEST} AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/install/bin:$PATH" \
    PYTHONPATH="/install/lib/python3.12/site-packages"

RUN groupadd -g 65532 app && useradd -u 65532 -g 65532 -s /sbin/nologin -d /app app \
 && mkdir -p /app && chown -R 65532:65532 /app

COPY --from=builder --chown=65532:65532 /install /install
COPY --chown=65532:65532 ./src /app

USER 65532:65532
WORKDIR /app
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD ["python", "-c", "import urllib.request,sys;sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/health',timeout=2).status==200 else 1)"]

ENTRYPOINT ["python", "-m", "myapp"]
CMD ["serve"]
```

```bash
# .dockerignore must exist; minimal sane default:
.git
.github
.venv
.pytest_cache
__pycache__
*.pyc
node_modules
dist
build
*.log
.env*
.vscode
.idea
docs
README.md
```

## Best practices
- Multi-stage by default. One stage for build deps, one for runtime; only the runtime stage ships.
- Pin base by digest (`python:3.12-slim@sha256:...`); Renovate updates the digest weekly.
- Order layers least-to-most-volatile: ARG/ENV → system pkgs → lang runtime → deps file → deps install → app code.
- BuildKit cache mounts for package managers (`pip`, `npm`, `apt`, `cargo`, `go mod`).
- Always non-root: explicit `USER` with high UID/GID, `runAsNonRoot: true` in K8s.
- HEALTHCHECK in exec form (no shell), short timeouts, retries.
- `.dockerignore` aggressively — your build context should be < 10MB unless legit.
- Multi-arch via buildx with native runners or QEMU; cache per-arch.
- SBOM + provenance attestation on every prod build; verify in deploy step with cosign.
- Trivy/Grype gate in CI; fail merge on fixable HIGH/CRITICAL.
- Read-only root filesystem in K8s with explicit `emptyDir` mounts for any writable paths.

## AI-agent gotchas
- Agents copy `FROM ubuntu:latest` from old samples; produces 70MB+ baseline and floating tag. Force slim/distroless and digest pinning.
- `RUN curl -fsSL https://... | bash` — supply-chain risk + non-reproducible. Agents do this to install tools; require pinned packages or verified checksums.
- Distroless has no shell, no `bash`, no `sh`. Agent's `RUN echo "..." > /etc/...` fails late; use ConfigMap/env at runtime.
- `COPY --link` (BuildKit) is faster but breaks if subsequent layer modifies the same paths. Agents use it everywhere blindly.
- `ENV PIP_INDEX_URL` to a private mirror with credentials → leaks via `docker history`. Use BuildKit secret mounts.
- Multi-stage final stage `FROM scratch` requires explicit copy of CA certs (`COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/`); agents miss this and TLS calls fail.
- Buildx + GHA cache: `cache-from: type=gha,scope=...` requires matching `cache-to` and a non-default scope per workflow; agents share scopes and cause cache thrash.
- `--platform=linux/amd64,linux/arm64` in `FROM` is wrong — that's for build platform, not target. Use `--platform=$TARGETPLATFORM` in multi-arch builds.
- Image size measurement confusion: `docker images` shows uncompressed; registry pull size is compressed. Agents optimize the wrong number.
- Human-in-loop checkpoints: switching base image family (Alpine→Debian, Debian→Distroless) MUST run full integration tests; don't auto-merge.
- Trivy false positives on dev dependencies: agents add `--ignore-unfixed` and skip fixable issues. Configure ignore via `.trivyignore` with explicit reason + expiry.
- Removing `apt-get` packages doesn't shrink the image — they're still in the layer. Use `--no-install-recommends` and clean caches in the same RUN.

## References
- Docker build best practices — https://docs.docker.com/build/building/best-practices/
- BuildKit features — https://docs.docker.com/build/buildkit/
- Multi-stage builds — https://docs.docker.com/build/building/multi-stage/
- Distroless — https://github.com/GoogleContainerTools/distroless
- Chainguard Images — https://www.chainguard.dev/chainguard-images
- Hadolint rules — https://github.com/hadolint/hadolint/wiki
- Dive — https://github.com/wagoodman/dive
- Trivy — https://aquasecurity.github.io/trivy/
- Sigstore / cosign — https://docs.sigstore.dev/
- OWASP Docker Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html
- Slim Toolkit — https://github.com/slimtoolkit/slim
- BuildKit cache backends — https://docs.docker.com/build/cache/backends/
