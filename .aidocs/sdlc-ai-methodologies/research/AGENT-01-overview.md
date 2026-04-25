# AGENT-01: SDLC+AI Overview, Agentic IDEs, AGENTS.md/CLAUDE.md, SDD

Research subagent 1 of 10. Focus: how AI agents fit across plan -> spec -> design -> build -> test -> deploy -> monitor -> incident; agentic IDEs (Cursor, Windsurf, Zed, JetBrains AI, Aider, opencode, Claude Code); AGENTS.md/CLAUDE.md conventions; spec-driven development; deterministic CI vs AI agent boundary.

Category prefix legend: `lang-` language/style | `lint-` linters/formatters | `test-` testing | `tracker-` issue trackers | `kb-` knowledge base / docs / memory | `task-` task lifecycle | `mr-` merge / PR review | `inc-` incident / on-call | `sec-` security | `gov-` governance / policy.

---

## M-01: agents-md-as-single-source-of-agent-truth
**Category:** kb-
**Sources:**
- https://agents.md/
- https://developers.openai.com/codex/guides/agents-md
- https://github.com/agentsmd/agents.md
- https://www.infoq.com/news/2025/12/agentic-ai-foundation/
**Rule:** Place a Markdown `AGENTS.md` at every repo root and at every monorepo subpackage that owns a deployable or build target; the agent must use the closest `AGENTS.md` to the file it is editing as authoritative project context (build commands, test commands, code style, security notes, PR conventions). README.md stays human-facing.
**When to use:** Any repository touched by a coding agent (Codex, Cursor, Windsurf, Claude Code, Devin, Jules, Gemini CLI, Aider, opencode). Especially monorepos where each subpackage has its own toolchain.
**When NOT to use:** Single-script throwaway repos, vendored read-only mirrors, archived repos. Do not duplicate human onboarding content already in README.md - link instead.
**Example:** Root `AGENTS.md` lists `pnpm build`, `pnpm test`, ESLint config path, commit style "type: short description", forbids `--no-verify`. A nested `apps/api/AGENTS.md` overrides with `uv run pytest` and a Django-specific lint set. The agent edits `apps/api/views.py` and reads the API-package file, not the root one.
**Why it works:** As of Dec 2025 AGENTS.md is stewarded by the Agentic AI Foundation (Linux Foundation) under OpenAI/Anthropic/Block donation, with 60k+ projects adopting it; it is the only context-file convention currently honored by all major coding agents simultaneously. Closest-file-wins resolves monorepo conflicts deterministically without per-agent config sprawl.

---

## M-02: claude-md-loader-and-agents-md-delegate
**Category:** kb-
**Sources:**
- https://code.claude.com/docs/en/best-practices
- https://amitray.com/claude-md-vs-agents-md-memory-md-skills-md-context-md-guide-2026/
- https://github.com/shanraisshan/claude-code-best-practice/blob/main/reports/claude-agent-memory.md
**Rule:** In Claude Code projects, keep `CLAUDE.md` minimal (an `@AGENTS.md` import plus Claude-specific overrides) and put cross-agent rules in `AGENTS.md`. Each `CLAUDE.md` and each `AGENTS.md` stays under ~200 lines; everything longer goes into `.claude/rules/*.md` or `.agents/*.md` with an `INDEX.md`. Hierarchical resolution: nearest-CLAUDE.md plus all parent CLAUDE.md files merge top-down.
**When to use:** Any repo where Claude Code is one of several agents in rotation (Cursor + Claude Code + Codex). Required when you need both Claude-specific tuning (skills, hooks, plan mode) and portable rules.
**When NOT to use:** Single-agent shops that only ever use one tool - then a single `AGENTS.md` with no `CLAUDE.md` indirection is simpler.
**Example:** `CLAUDE.md` is one line: `@AGENTS.md`. `AGENTS.md` holds project rules. `.claude/rules/security.md`, `.claude/rules/migrations.md` carry deeper detail loaded on demand. `.claude/agents/*.md` defines specialized subagents.
**Why it works:** Above ~200 lines Claude's instruction-following degrades, so the 2026 best practice is index-and-link rather than monolithic. The CLAUDE.md -> AGENTS.md indirection lets the same repo serve every agent with one canonical file.

---

## M-03: spec-driven-development-with-spec-kit
**Category:** task-
**Sources:**
- https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/
- https://github.com/github/spec-kit
- https://github.com/github/spec-kit/blob/main/spec-driven.md
- https://speckit.org/
**Rule:** Before any agent writes code, run the `/speckit.specify` -> `/speckit.plan` -> `/speckit.tasks` chain so the workflow produces three versioned artifacts in this order: spec.md (WHAT/WHY, with `[NEEDS CLARIFICATION]` markers), plan.md (HOW + tech rationale), tasks.md (parallelizable work items). Code is generated only from tasks.md; the spec, not the code, is the source of truth.
**When to use:** Any non-trivial feature, especially multi-file or multi-service changes. Required for high-stakes domains (payments, auth, migrations) and any change traceable to a regulator or contract.
**When NOT to use:** True one-line bugfixes, typo fixes, dependency bumps, exploratory spike branches that will be thrown away. Do not spec-kit your way through a `npm audit fix`.
**Example:** Engineer says "add OAuth Google login". `/speckit.specify` produces a spec with user stories + AC + 4 NEEDS-CLARIFICATION markers. PM resolves them. `/speckit.plan` writes plan.md choosing Authlib, naming the redirect URI rules, marking constitution gates passed. `/speckit.tasks` emits 11 tasks with `[P]` markers for those that can run in parallel.
**Why it works:** The spec kit constitution enforces nine immutable principles (library-first, test-first, simplicity gate, anti-abstraction, integration-first testing, etc.) as automated gates inside templates, so the LLM is constrained toward higher-quality output. The spec acts as a deterministic anchor that survives LLM context swaps and model upgrades.

---

## M-04: plan-mode-then-execute-with-locked-plan
**Category:** task-
**Sources:**
- https://www.agentic-patterns.com/patterns/plan-then-execute-pattern/
- https://smartscope.blog/en/generative-ai/chatgpt/codex-plan-mode-complete-guide/
- https://www.mindstudio.ai/blog/claude-code-agentic-workflow-patterns
- https://kilo.ai/articles/beyond-autocomplete
**Rule:** For any change that touches more than ~3 files or runs longer than ~5 minutes, the agent must first enter Plan Mode (read-only, no edits, no shell side effects), produce an explicit plan with steps + verification + out-of-scope list, get human approval, then execute the locked plan. The agent is forbidden from re-planning silently mid-execution; deviations require a new plan.
**When to use:** Multi-file refactors, schema migrations, anything with security or data implications, anything where the human will not review every diff line. Default for autonomous/long-running runs.
**When NOT to use:** Trivial single-line edits, autocomplete in inline mode, throwaway scratch sessions. Heavy plan ceremony on a typo wastes tokens.
**Example:** User: "extract auth into its own service". Agent enters Plan Mode, lists 14 steps grouped by phase, lists 3 out-of-scope items (don't change session DB schema, don't touch frontend, don't refactor tests), defines 4 verification commands. User approves. Agent executes step-by-step, marks each complete in a TODO file, reports at end.
**Why it works:** Anthropic's published research (Boris Cherny) reports Plan Mode raises success rates 2-3x; the broader plan-then-execute literature shows tool-use accuracy moving from 72% to 94%. Locking the plan also closes the prompt-injection window during the execution phase, since untrusted data cannot rewrite the agreed steps.

---

## M-05: deterministic-hooks-as-the-ai-ci-boundary
**Category:** lint-
**Sources:**
- https://liviaerxin.github.io/blog/agentic-vs-deterministic-orchestration
- https://briandouglas.me/posts/2025/08/27/pre-commit-hooks-are-back-thanks-to-ai/
- https://circleci.com/blog/test-hooks-ai-development/
- https://www.ayautomate.com/blog/best-claude-code-hooks
**Rule:** Anything that must happen on every change runs as a deterministic hook (pre-commit, pre-push, agent lifecycle hook), not as an instruction in CLAUDE.md/AGENTS.md. Agents are never trusted to "remember" to lint, format, run tests, or update the changelog. Hooks fail closed; agents may not skip them with `--no-verify`.
**When to use:** Lint/format (ruff, eslint, prettier), typecheck, secret-scan, changelog enforcement, doc-drift detection, license headers, debug-statement detection (T20), forbidden-import checks. Anything you can express as "must be true on every commit".
**When NOT to use:** Subjective rules ("write idiomatic code"), context-dependent decisions ("decide if this needs a migration"), anything that needs to read intent. Those stay in the agent's judgement layer.
**Example:** `.pre-commit-config.yaml` runs `ruff check --fix`, `ruff format`, `gitleaks`, and a custom `changelog-required.py` that blocks the commit if `CHANGELOG.md` did not change. A Claude Code `PostToolUse` hook on `Write|Edit` also runs `ruff check` on the touched file so failures surface immediately, not at commit time.
**Why it works:** LLMs are non-deterministic; CI is. The 2026 industry consensus (state-machine-guided agents, hybrid orchestration) puts the deterministic skeleton outside the model and lets the model only operate within those bounds. This makes the system auditable and reproducible.

---

## M-06: one-task-one-branch-one-worktree-one-agent
**Category:** task-
**Sources:**
- https://www.augmentcode.com/guides/git-worktrees-parallel-ai-agent-execution
- https://devcenter.upsun.com/posts/git-worktrees-for-parallel-ai-coding-agents/
- https://docs.bswen.com/blog/2026-03-18-ai-agent-worktree-isolation/
- https://www.penligent.ai/hackinglabs/git-worktrees-need-runtime-isolation-for-parallel-ai-agent-development/
**Rule:** Each parallel agent run gets its own git worktree, its own branch, its own scoped file ownership manifest, AND its own runtime sandbox (ports, DB, cache, secrets). One task -> one branch -> one worktree -> one agent. The agent is forbidden from editing files outside its declared scope; conflicts are resolved at merge time, not at edit time.
**When to use:** Any time more than one agent runs concurrently on the same repo (multi-feature parallel build, fan-out subagent dispatch, comparison/arena mode). Standard pattern in Claude Code, Cursor, Windsurf Wave 13 (parallel agents).
**When NOT to use:** A single agent doing sequential work. Pure read-only research subagents that never write files (a shared sandbox is fine).
**Example:** Top-level agent splits a 5-task plan. It runs `git worktree add ../wt-feat-a feat-a`, sets `CLAUDE.md` scope to `apps/billing/**`, dispatches a subagent with `PORT=4001 DATABASE_URL=...billing_a` env. Four worktrees in parallel, each on its own port; merges back via PRs.
**Why it works:** Worktrees share the `.git` object store but isolate working trees, eliminating index-lock contention and silent overwrites. Adding runtime sandboxing closes the second-class isolation gap (the published failure mode of 2026: worktrees alone do not stop port/DB/cache collisions).

---

## M-07: progressive-disclosure-skills-and-subagents
**Category:** kb-
**Sources:**
- https://code.claude.com/docs/en/skills
- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- https://levelup.gitconnected.com/a-mental-model-for-claude-code-skills-subagents-and-plugins-3dea9924bf05
- https://dev.to/owen_fox/claude-code-hooks-subagents-and-skills-complete-guide-hjm
**Rule:** Domain knowledge is packaged as skills with three tiers - metadata (~100 tokens, always loaded), instructions (<5k tokens, loaded only when matched), bundled resources (loaded on demand). Heavy or one-off work runs in subagents that fork their own context window. Never put domain knowledge directly into the main agent's CLAUDE.md once the project has more than ~3 distinct domains.
**When to use:** Multi-domain repos (auth + billing + media + infra), repeated workflows (release, migration, security review), context-window-pressured sessions. Any time main-context tokens are scarce.
**When NOT to use:** Tiny single-domain projects where one CLAUDE.md fits everything. Tasks that need the main agent's already-built context (forking loses it).
**Example:** A `release` skill: 80-token metadata `description`, 1.2k-token SKILL.md with the release checklist, and 4 bundled scripts loaded only when the skill activates. A `code-reviewer` subagent forks a fresh context for PR review so the planning agent stays clean.
**Why it works:** Context windows fill fast; progressive disclosure keeps the always-loaded surface tiny while making 50+ domains addressable. Subagents trade extra orchestration cost for clean separation, which empirically beats one giant context for long-horizon work.

---

## M-08: agent-friendly-tracker-with-mcp-and-spec-sync
**Category:** tracker-
**Sources:**
- https://linear.app/integrations/jira
- https://www.theregister.com/2026/03/26/linear_agent/
- https://prommer.net/en/tech/guides/linear-vs-jira-vs-trello/
- https://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/
**Rule:** The issue tracker exposes itself to agents over MCP (first-party server, not a screen-scrape) and the tracker's issue ID is the canonical link between spec.md, branch name, PR, and incident. Agents create/update issues only via MCP with scoped tokens, never via human-facing GraphQL/REST keys with broad scopes.
**When to use:** Any team where agents triage, draft specs, open PRs, or run on-call. Required when agents must round-trip status from CI/PR back into the tracker.
**When NOT to use:** Solo projects with no tracker. Trackers without an MCP server or scoped-token model (legacy Jira on-prem with global API tokens) - fix the auth model first.
**Example:** Linear MCP server is wired into Claude Code with scope `team:engineering, action:create_issue,update_issue`. Branch name is `eng-1234-add-google-oauth`; spec.md front-matter has `linear: ENG-1234`; PR template auto-links. The Linear Agent (in beta as of April 2026) takes a Slack thread and emits a draft spec back into ENG-1234.
**Why it works:** MCP became the de facto integration standard in 2026 (97M monthly SDK downloads, OpenAI/Google/Microsoft/Cloudflare adoption); a native MCP server avoids brittle scrapers and gives the agent a typed, auditable surface. Anchoring everything on the tracker ID gives a single join key across spec, code, deploy, and incident.

---

## M-09: ai-sre-as-co-pilot-not-pager-owner
**Category:** inc-
**Sources:**
- https://incident.io/ai-sre
- https://www.infoq.com/news/2026/01/opsworker-ai-sre/
- https://rootly.com/sre/top-5-ai-powered-incident-management-platforms-2026
- https://www.datadoghq.com/blog/bits-ai-sre/
**Rule:** AI SRE agents narrow the search space, gather context, draft timelines, propose probable cause, and write the postmortem - but humans hold the pager and own remediation decisions. Every agent action in incident is logged with a correlation ID; the agent never executes destructive remediation without explicit human approval.
**When to use:** Triage, log/trace correlation, "is this familiar from a past incident?", drafting status updates, generating postmortems with timeline + contributing factors + follow-ups. Any time MTTR is dominated by context-gathering, not decision-making.
**When NOT to use:** Single-engineer shops where the AI overhead exceeds the benefit. Highly novel incidents where the model has no prior data. Hard-failure scenarios that need an immediate human decision (rollback now, page the CEO).
**Example:** Pager fires on `api-prod` 5xx spike. Bits AI SRE / incident.io AI SRE pulls related deploys, opens a draft incident with timeline, links the suspect commit, suggests rollback, drafts the customer comms. On-call human approves rollback. Postmortem draft is auto-generated with timeline, AC violations, follow-up items linked back into the tracker.
**Why it works:** Reported 2026 results show MTTR cuts up to ~70% when AI handles the tedious context-gathering layer while humans keep judgment. The "human-centred AI for SRE" pattern (InfoQ Jan 2026) is the consensus design: multi-agent assistance, single human authority.

---

## M-10: governed-agent-with-least-privilege-and-evidence-trail
**Category:** gov-
**Sources:**
- https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ai-agents/governance-security-across-organization
- https://www.beyondtrust.com/blog/entry/ai-agent-identity-governance-least-privilege
- https://techcommunity.microsoft.com/blog/linuxandopensourceblog/agent-governance-toolkit-architecture-deep-dive-policy-engines-trust-and-sre-for/4510105
- https://www.kiteworks.com/cybersecurity-risk-management/ai-agent-data-governance-why-organizations-cant-stop-their-own-ai/
**Rule:** Every coding/operating agent runs under its own scoped identity (not a human's PAT), with permissions narrowed to the minimum tool/path/resource set; a runtime policy engine classifies each tool call as allow / require-approval / block; every action emits an audit record (who/what/when/why/correlation-id) retained to the org's compliance bar.
**When to use:** Any agent with write access to production, secrets, customer data, or money-moving systems. Regulated environments (EU AI Act enforcement broadens Aug 2 2026; SOC2/GDPR audits now scrutinize agent access patterns).
**When NOT to use:** Pure local dev sandboxes with no shared resources. Hobby projects with no compliance bar (still good hygiene though).
**Example:** A deploy agent has identity `agent-deploy@company`, with role allowing only `kubectl apply -f manifests/staging/*` plus rollback. Policy engine classifies `kubectl delete` as require-approval, `aws iam *` as block. Each call is logged to a tamper-evident audit store with the originating spec/PR/issue ID. `--no-verify`, secret env injection, and tool-call escalation are blocked at the harness layer.
**Why it works:** The published 2026 governance pattern (Microsoft Agent Governance Toolkit, BeyondTrust, Oracle runtime governance) converges on identity + policy engine + audit trail, exactly the same shape that has secured production systems for decades. Audit-trail quality is the single strongest predictor of AI governance maturity in current surveys; without it, regulators and customers cannot verify controls.

---

## Notes for cross-agent merge

- M-01 and M-02 compose: M-02 is the Claude-specific dialect of the M-01 cross-agent standard.
- M-03 (spec-kit) feeds M-04 (plan mode): spec-kit produces the plan that plan mode locks.
- M-05 (hooks) and M-10 (policy engine) are the deterministic boundary at two different layers (local commit vs runtime tool call).
- M-06 (worktrees) is what makes M-07 (subagents) actually safe in practice.
- M-08 (tracker MCP) is what makes M-03's spec discoverable and M-09's incident threadable to the rest of the SDLC.
