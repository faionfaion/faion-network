# SDLC + AI Methodologies

Geek-tier knowledge base of methodologies that wire AI coding agents (Claude Code, Cursor, Codex, aider, Windsurf) into the deterministic SDLC floor: language toolchains, lint/format, tests, trackers, knowledge bases, task lifecycle, merge automation, incident response, security, governance.

## Scope

Each methodology is a self-contained folder with `CLAUDE.md`, `AGENTS.md`, `content/*.xml`, optional `templates/` and `scripts/`. Routing is via the methodology `AGENTS.md` (under 80 lines, strict shape per `docs/skill-authoring.md`).

## Categories

| Prefix | Domain | Target |
|--------|--------|--------|
| `lang-` | Language / package mgmt / build | 10 |
| `lint-` | Linters, formatters, hooks | 6 |
| `test-` | Testing frameworks and tactics | 6 |
| `tracker-` | Issue trackers + agent integration | 5 |
| `kb-` | Knowledge base, docs, agent memory | 4 |
| `task-` | Task / spec / branch lifecycle | 5 |
| `mr-` | Merge request / PR review automation | 5 |
| `inc-` | Incident response, on-call | 4 |
| `sec-` | Supply chain + SAST + secrets | 3 |
| `gov-` | Governance, audit, identity | 4 |

## How To Use

1. Pick the category by the active task — language work → `lang-`, hook fix → `lint-`, etc.
2. List the matching methodology folders.
3. Read each candidate's `AGENTS.md` (cheap — under 80 lines).
4. Load only the `content/*.xml` files relevant to the decision.
5. Apply, then run the deterministic checks named in the methodology.

## Full Methodology Index

Every methodology folder, grouped by category prefix.

**`lang-` — Language / package mgmt / build:**
- `lang-csharp-roslyn-analyzer-errors`: Roslyn analyzer errors as floor
- `lang-go-tygo-frontend-contract`: Go → TS contract via tygo
- `lang-jvm-jreleaser-tag-release`: JVM tag-release via JReleaser
- `lang-php-phpstan9-psalm-taint`: PHPStan 9 + Psalm taint floor
- `lang-ruby-sorbet-strict-floor`: Ruby Sorbet strict floor
- `lang-swift-harmonize-arch-tests`: Swift arch test harmonization
- `pnpm-catalogs`: pnpm catalogs for monorepo versioning
- `pyproject-single-source`: pyproject.toml as single version source
- `ts-strict-isolated`: TS strict + isolatedModules floor
- `uv-lockfile-floor`: `uv.lock` as Python lockfile floor

**`lint-` — Linters, formatters, hooks:**
- `lint-autofix-vs-flag-decision-rule`: When to autofix vs flag
- `lint-megalinter-polyglot`: MegaLinter for polyglot repos
- `lint-precommit-floor`: pre-commit as deterministic floor
- `lint-ruff-and-biome-as-default`: Ruff + Biome as defaults
- `lint-shellcheck-hadolint-iac-floor`: Shell / Docker / IaC floor
- `lint-staged-only-not-whole-tree`: Lint staged, not the tree

**`test-` — Testing frameworks and tactics:**
- `test-consumer-contract-from-spec`: Consumer contracts from spec
- `test-golden-master-legacy-rewrite`: Golden master for rewrites
- `test-mutation-feedback-loop`: Mutation testing feedback loop
- `test-property-based-llm-invariants`: Property tests for LLM invariants
- `test-self-healing-locators-audited`: Self-healing locators with audit
- `test-tdd-red-green-split-agents`: TDD with split red / green agents

**`tracker-` — Issue trackers + agent integration:**
- `tracker-ai-triage-classify-route`: AI triage and routing
- `tracker-github-copilot-workspace`: GitHub Copilot Workspace
- `tracker-gitlab-duo-developer-flow`: GitLab Duo developer flow
- `tracker-jira-rovo-mcp-agents`: Jira + Rovo MCP agents
- `tracker-linear-agent-as-assignee`: Linear agent as assignee

**`kb-` — Knowledge base, docs, agent memory:**
- `kb-agents-md-context-pyramid`: AGENTS.md context pyramid
- `kb-codebase-rag-symbol-chunked`: Codebase RAG, symbol-chunked
- `kb-symbol-index-fresh-tags`: Fresh symbol index (ctags)
- `kb-versioned-agent-memory-files`: Versioned agent memory files

**`task-` — Task / spec / branch lifecycle:**
- `task-agent-drafts-spec-before-coding`: Agent drafts spec first
- `task-agent-fixable-triage-gate`: Triage gate for agent fixes
- `task-plan-mode-locked-execution`: Plan-mode locked execution
- `task-spec-kit-three-step`: spec-kit three-step flow
- `task-worktree-runtime-isolation`: Worktree runtime isolation

**`mr-` — Merge request / PR review automation:**
- `mr-codemod-refactor-agent`: Codemod refactor agent
- `mr-error-tracker-draft-pr`: Error tracker drafts PR
- `mr-graph-vs-diff-reviewer`: Graph-aware vs diff-only reviewer
- `mr-renovate-ai-handoff`: Renovate → AI handoff
- `mr-slash-command-surface`: Slash-command surface for MR ops

**`inc-` — Incident response, on-call:**
- `inc-postmortem-auto-draft-no-publish`: Auto-draft postmortems, no auto-publish
- `inc-read-only-investigation-default`: Read-only by default during incidents
- `inc-runbook-as-markdown-tagged-steps`: Runbooks as tagged markdown
- `inc-tool-tier-approval-gate`: Tool-tier approval gate

**`sec-` — Supply chain + SAST + secrets:**
- `sec-codeql-autofix-on-pr`: CodeQL autofix on PR
- `sec-secrets-defense-in-depth`: Secrets defense in depth
- `sec-trivy-pinned-supply-chain-scan`: Trivy pinned supply-chain scan

**`gov-` — Governance, audit, identity:**
- `gov-approval-token-signed-jwt`: Approval tokens as signed JWT
- `gov-conventional-commits-enforced`: Conventional commits enforced
- `gov-license-compliance-scan`: License compliance scan
- `gov-sonarqube-ai-code-gate`: SonarQube AI-code gate

## Related

- Sibling: `geek/ai/ai-agents/` (agent-construction methodologies)
- Sibling: `geek/ai/llm-integration/semantic-xml-content/` (closed XML tag glossary)
- Spec: `docs/skill-authoring.md` (methodology folder structure)
