# Docker Compose (CI/CD)

## Summary

**One-sentence:** Generates a CI-only Docker Compose override — no port bindings, health-check waits, teardown discipline — so integration test stacks run reliably under CI runners.

**One-paragraph:** Generates a CI-only Docker Compose override — no port bindings, health-check waits, teardown discipline — so integration test stacks run reliably under CI runners.

**Ефективно для:**

- Solo team running integration tests in CI against real DB + cache.
- Pipeline that builds + tests stack before pushing image.
- CI runner with limited resources where teardown discipline matters.

## Applies If (ALL must hold)

- Integration test stack spins up in CI (≥2 services).
- CI runner is single-host (GitHub Actions / GitLab CI / Drone).
- Tests need a fresh stack per run.
- Secrets come from CI env vars (not .env files).

## Skip If (ANY kills it)

- Production zero-downtime — use Kubernetes rolling updates.
- Multi-host CI — use test clusters or Testcontainers.
- Single-container pipeline — docker run is simpler.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| compose.yaml | yaml | primary compose file |
| compose.ci.yaml | yaml | CI override (this methodology produces it) |
| Service health-check definitions | yaml | per-service healthcheck blocks |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| docker-compose-devops | Base infra compose patterns. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-no-host-ports-in-ci, r2-wait-for-healthy, r3-teardown-always, r4-secrets-from-env, r5-named-owner | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the Docker Compose (CI/CD) artefact + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: flaky-port-conflicts, orphan-volumes, secrets-in-cache | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure for end-to-end application | 800 |
| `content/06-decision-tree.xml` | essential | Maps observable inputs to rule ids in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-docker-compose` | opus | High-stakes synthesis — sets the artefact baseline. |
| `validate-docker-compose` | sonnet | Bounded structural check against the output contract. |
| `review-docker-compose` | sonnet | Per-section critique against rules + failure modes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/docker-compose.json` | JSON skeleton matching the output contract. |
| `templates/docker-compose.md` | Markdown skeleton with required fields. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-docker-compose.py` | Validate Docker Compose (CI/CD) output JSON against the schema. | After subagent returns, before downstream consumer reads. |

## Related

- [[docker-compose-devops]]
- [[docker-compose-infrastructure]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input fields to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, the verdict label, and which template variant to fill.
