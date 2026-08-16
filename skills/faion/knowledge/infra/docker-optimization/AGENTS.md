# Docker Image Optimization (size + cache + supply chain)

## Summary

**One-sentence:** Generates an optimized Dockerfile (multi-stage + BuildKit cache mounts + distroless/Wolfi base + pinned digest + non-root) targeting <200MB images and zero-CVE base.

**One-paragraph:** Docker Image Optimization (size + cache + supply chain) — applied when the preconditions below hold. The methodology pins the artefact shape via `content/02-output-contract.xml`, anchors testable rules in `content/01-core-rules.xml`, and routes ambiguous cases through `content/06-decision-tree.xml` to a concrete rule or to `skip-this-methodology`. Failure modes in `content/03-failure-modes.xml` describe the antipatterns this methodology eliminates. The output is a config that the downstream agent can verify with the included validator.

**Ефективно для:**

- Production container image larger than 500MB or rebuilding > 10x per day.
- Supply-chain hardening required (image signing, SBOM, digest pinning).
- Multi-language project where build deps should not bleed into runtime image.

## Applies If (ALL must hold)

- Production container image larger than 500MB or rebuilding > 10x per day.
- Supply-chain hardening required (image signing, SBOM, digest pinning).
- Multi-language project where build deps should not bleed into runtime image.

## Skip If (ANY kills it)

- Throwaway dev image for one-shot experiments — optimization overhead exceeds value.
- Image already meets size + CVE + cache targets; no rework needed.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Task signal / spec | text / Markdown | user |
| Domain context | XML | `pro/infra/cicd-engineer/AGENTS.md` |
| Inventory of in-scope resources | list / JSON | infra catalog |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[cicd-cert-rotation-pipeline]] | Sibling methodology — shared vocabulary and patterns. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules (multi-stage-build, distroless-or-wolfi-runtime, digest-pinned-base, non-root-user, buildkit-cache-mounts, hadolint-and-scan, skip-this-methodology) | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the config + valid + invalid + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree from observable signals to a `<conclusion ref="rule-id">` | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-docker-optimization` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/Dockerfile.optimized` | Multi-stage Dockerfile with cache mounts + distroless + non-root + digest-pinned base |
| `templates/dockerignore` | .dockerignore skeleton excluding common bloat |
| `templates/backup-config.example.json` | Filled config artefact |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-docker-optimization.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- Parent: `pro/infra/cicd-engineer/`
- [[cicd-cert-rotation-pipeline]]
- [[elk-stack-logging]]
- [[dora-metrics]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/Dockerfile.optimized`

```text
# syntax=docker/dockerfile:1.7
FROM gcr.io/distroless/static-debian12 AS runtime
USER 10001
COPY app /app
ENTRYPOINT ["/app"]
```

### `templates/dockerignore`

```text
.git
node_modules
.venv
__pycache__
*.pyc
.cache
```

### `templates/backup-config.example.json`

```json
{
  "multi_stage": true,
  "runtime_base": "distroless",
  "digest_pinned": true,
  "user_uid": 1,
  "cache_mounts": true,
  "scanners": [
    "hadolint",
    "trivy"
  ],
  "target_size_mb": 1
}
```
