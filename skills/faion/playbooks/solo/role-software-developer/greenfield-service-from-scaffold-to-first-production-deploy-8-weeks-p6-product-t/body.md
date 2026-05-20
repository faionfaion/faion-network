# Greenfield service from scaffold to first production deploy (8 weeks)

## Context

In-house dev or small squad ships a greenfield service across 8 weeks. Covers scaffold + AGENTS.md, architecture, contracts, infra, security, tests, observability, and first deploy. Done when the service is live with metrics + health checks and a published changelog.

## Outcome

Empty repo -> first user-facing deploy with conventions, infra, and observability live. In-house dev or small squad takes a greenfield service from zero to first user-facing deploy with own conventions, infra, and observability.

## Steps

1. **Scaffold + AGENTS.** Set up for LLM-friendly + human-friendly contributions. Tasks: Bootstrap the repo with standard structure; Add AGENTS.md + CLAUDE.md per module; Wire pnpm catalogs / pyproject single source.
2. **Architecture + ADRs.** Decide before coding. Tasks: Pick architecture pattern (hexagonal / onion); Make build-vs-buy + stack decisions explicit; Capture ADRs.
3. **Contract + API.** API contract first, no surprises later. Tasks: Draft OpenAPI spec; Add contract tests; Define rate limiting + auth.
4. **Domain model + DB.** Codify the domain explicitly. Tasks: Model aggregates + value objects + repositories; Design DB schema; Optimize critical queries.
5. **Tests + perf.** Layers of testing + a perf smoke. Tasks: Unit + integration tests via TDD; Add test fixtures + factories; Run a perf smoke test; Split TDD red-green between agents.
6. **Security.** Bake security in. Tasks: Wire CodeQL autofix on PRs; Run Trivy supply-chain scans on pinned deps; Apply secrets defense-in-depth; Add security-focused tests; Add circuit breakers for downstream services.
7. **Observability.** You can see the service from outside. Tasks: Wire metrics + logs + traces; Add health checks + alerts; Wire docker-compose for local + smoke.
8. **First deploy.** Ship to users. Tasks: Wire CD pipeline + tagged release; Deploy behind feature flag for a small audience; Verify post-deploy with smoke + alerts.

## Decision points

- **After Scaffold + AGENTS:** Advance only when scaffold builds clean.
- **After Architecture + ADRs:** Advance only when ADRs cover the major decisions.
- **After Contract + API:** Advance only when contract tests are green.
- **After Domain model + DB:** Advance only when domain model is reviewed.
- **After Tests + perf:** Advance only when perf smoke passes.
- **After Security:** Advance only when scans pass.
- **After Observability:** Advance only when health checks + metrics + alerts are wired.
- **After First deploy:** Done when deploy is verified and changelog is published.

## References

- `faion/knowledge/free/dev/devtools-developer/github-repo-bootstrap`
- `faion/knowledge/free/dev/software-developer/integration-testing`
- `faion/knowledge/free/dev/software-developer/tdd-workflow`
- `faion/knowledge/free/dev/software-developer/test-fixtures`
- `faion/knowledge/free/dev/software-developer/unit-testing`
- `faion/knowledge/geek/dev/software-developer/claude-md-creation`
- `faion/knowledge/geek/dev/software-developer/llm-friendly-architecture`
- `faion/knowledge/geek/sdlc-ai/pnpm-catalogs`
- `faion/knowledge/geek/sdlc-ai/pyproject-single-source`
- `faion/knowledge/geek/sdlc-ai/sec-codeql-autofix-on-pr`
- `faion/knowledge/geek/sdlc-ai/sec-secrets-defense-in-depth`
- `faion/knowledge/geek/sdlc-ai/sec-trivy-pinned-supply-chain-scan`
- `faion/knowledge/geek/sdlc-ai/test-tdd-red-green-split-agents`
- `faion/knowledge/pro/dev/backend-systems/go-layout-directory-structure`
- `faion/knowledge/pro/dev/backend-systems/nosql-redis-patterns`
- `faion/knowledge/pro/dev/backend-systems/sql-optimization`
- `faion/knowledge/pro/dev/code-quality/clean-architecture`
- `faion/knowledge/pro/dev/software-developer/api-monitoring-alerting`
- `faion/knowledge/pro/dev/software-developer/api-monitoring-health-checks`
- `faion/knowledge/pro/dev/software-developer/api-monitoring-logging`
- `faion/knowledge/pro/dev/software-developer/api-monitoring-metrics`
- `faion/knowledge/pro/dev/software-developer/ddd-aggregates`
- `faion/knowledge/pro/dev/software-developer/ddd-repositories`
- `faion/knowledge/pro/dev/software-developer/ddd-value-objects`
- `faion/knowledge/pro/dev/software-developer/microservices-circuit-breaker`
- `faion/knowledge/solo/dev/api-developer/api-contract-first`
- `faion/knowledge/solo/dev/api-developer/api-openapi-spec`
- `faion/knowledge/solo/dev/api-developer/api-rate-limiting`
- `faion/knowledge/solo/dev/api-developer/api-rest-design`
- `faion/knowledge/solo/dev/automation-tooling/cd-pipelines`
- `faion/knowledge/solo/dev/automation-tooling/continuous-delivery`
- `faion/knowledge/solo/dev/automation-tooling/perf-test-tools`
- `faion/knowledge/solo/dev/software-architect/arch-pattern-hexagonal`
- `faion/knowledge/solo/dev/software-architect/arch-pattern-onion`
- `faion/knowledge/solo/dev/software-architect/database-selection`
- `faion/knowledge/solo/dev/software-architect/decision-tree-build-vs-buy`
- `faion/knowledge/solo/dev/software-architect/decision-tree-tech-stack`
- `faion/knowledge/solo/dev/software-architect/trade-off-decision-matrix`
- `faion/knowledge/solo/dev/software-developer/api-authentication`
- `faion/knowledge/solo/dev/software-developer/database-design`
- `faion/knowledge/solo/dev/software-developer/go-project-structure`
- `faion/knowledge/solo/dev/software-developer/performance-testing`
- `faion/knowledge/solo/dev/software-developer/security-testing`
- `faion/knowledge/solo/dev/software-developer/sql-optimization`
- `faion/knowledge/solo/infra/devops-engineer/docker-compose`
- Related: `feature-from-spec-to-production-3-weeks-p4-client-rules-edition`
