# AGENT-06 — Linters, Formatters, SAST, Secrets, IaC, License Scanning

**Summary (2 lines):**
The deterministic check floor — linters, SAST, secrets, IaC, license, SCA — runs without LLM input and produces objective pass/fail signals AI agents must respect.
Modern stack lets AI patch what is auto-fixable (formatters, ruff/biome rules, Semgrep autofix, Copilot Autofix) and forces flag-and-block on anything stateful (secrets, license, SCA, container CVE).

State as of April 2026. All entries map to `lint-`, `sec-`, or `gov-`.

---

## M1 — `lint-precommit-floor` — Pre-commit hooks as the non-negotiable merge floor

**Category:** lint-

**Rule:** Every repo MUST install a pre-commit framework (`pre-commit` for polyglot, `lefthook` for monorepos with parallel needs, `husky` for pure Node.js) that blocks commits on format/lint/secret/typecheck failures. Hooks run BEFORE the agent commits, not after. AI agents NEVER bypass with `--no-verify`; on failure they fix the root cause and recommit.

**Why it works:** Hooks are the cheapest gate (sub-second on a diff) and run on the developer's machine, not just CI. They turn "did you forget to lint?" into a structural impossibility. Lefthook (Go) is ~10x faster than husky (Node) and runs hooks in parallel — preferred for polyglot/monorepo. `pre-commit` (Python, by pre-commit.com) has the broadest ecosystem of pre-built checks (ruff, black, gitleaks, detect-secrets, eslint, prettier, terraform fmt, shellcheck) with full env isolation per hook.

**When to use:** Always. Mandatory floor for every repo with code in it.
**When NOT to use:** Single-file gist repos, archived/read-only repos.

**Agent integration:**
- Hooks are deterministic — agent must read failure output and fix, not bypass.
- Add hook list to AGENTS.md so the agent sees what will be enforced before writing code.
- Use `pre-commit autoupdate` quarterly; commit the bumps as a separate PR.

**Sources:**
- https://pre-commit.com
- https://github.com/evilmartians/lefthook
- https://github.com/typicode/husky
- https://www.pkgpulse.com/blog/husky-vs-lefthook-vs-lint-staged-git-hooks-nodejs-2026
- https://www.andymadge.com/2026/03/10/git-hooks-comparison/

---

## M2 — `lint-semgrep-rules-as-policy` — Semgrep as project security policy + autofix surface

**Category:** sec-

**Rule:** Every repo with non-trivial security surface (any HTTP API, any auth, any DB) MUST run Semgrep with (a) the `p/default` registry pack, (b) custom rules in `.semgrep/` codifying project-specific anti-patterns, and (c) `--autofix` enabled in pre-commit / agent loops for fixes that ship a `fix:` block. CI runs the full ruleset blocking; agent loops run only `--autofix`-capable subset and apply patches automatically.

**Why it works:** Semgrep rules are YAML pattern-matchers, not magic — every team can write them, and Semgrep Assistant (2026) can write rules from a "we hit this bug, prevent it" prompt. Rules with a `fix:` field auto-rewrite the AST. Coverage: Java, JS/TS, Python, Go, Ruby, PHP, C/C++, Kotlin, Scala, Swift, Terraform, Dockerfile, Bash. Semgrep Assistant in 2026 also does AI-powered triage (false-positive ranking) and ties AI usage to credit limits with org-level governance.

**When to use:** Every codebase. Especially valuable when you hit a class of bug — write the rule before writing the fix.
**When NOT to use:** Pure data/notebook repos with no executable surface.

**Agent integration:**
- Agents call `semgrep --config .semgrep/ --autofix` after any code change; rerun until clean.
- New bug class found in code review → agent generates a Semgrep rule and adds to `.semgrep/`.
- Semgrep MCP server lets agents query findings directly inside Cursor/Claude Code.

**Sources:**
- https://semgrep.dev
- https://semgrep.dev/docs/semgrep-assistant/overview
- https://semgrep.dev/docs/semgrep-code/overview
- https://www.merito.com/resources/product-release-updates/semgrep-appsec-platform-update-april-2026-ai-detection-autofix-and-enterprise-governance

---

## M3 — `sec-codeql-autofix-on-pr` — CodeQL + Copilot Autofix as the PR-time SAST gate

**Category:** sec-

**Rule:** GitHub repos enable Code Scanning with CodeQL on push + PR. PRs that introduce a CodeQL alert are blocked from merge. Copilot Autofix runs automatically on alerts and posts an AI-generated patch as a PR suggestion — humans accept/reject, never auto-merge. Hybrid AI-detection covers ecosystems CodeQL doesn't (Bash, Dockerfile, Terraform/HCL, PHP).

**Why it works:** CodeQL is a semantic dataflow engine (not regex), catches injection/SSRF/auth-bypass that pattern matchers miss. Copilot Autofix (GA 2024, expanded 2026) covers >90% of alert types in JS/TS/Java/Python and resolves >2/3 of findings with little/no editing — median fix time dropped from 1.5h manual to 28 min. As of 2026 the engine is "hybrid": CodeQL for compiled/typed code, AI detections for shell/Docker/Terraform/PHP.

**When to use:** Any repo on GitHub with paid Advanced Security (or public OSS — free).
**When NOT to use:** Self-hosted Git not on GitHub — use Semgrep or SonarQube instead.

**Agent integration:**
- Agents read the SARIF output via `gh api` and treat alerts as blocking.
- Agents can run CodeQL CLI locally before push to get the same signal.
- Autofix patches are SUGGESTIONS — agents review the diff for correctness, never blindly apply.

**Sources:**
- https://github.com/github/codeql
- https://docs.github.com/en/code-security/responsible-use/responsible-use-autofix-code-scanning
- https://github.blog/news-insights/product-news/found-means-fixed-introducing-code-scanning-autofix-powered-by-github-copilot-and-codeql/
- https://github.blog/security/application-security/github-expands-application-security-coverage-with-ai-powered-detections/

---

## M4 — `sec-secrets-defense-in-depth` — Two-layer secret scanning (gitleaks pre-commit + trufflehog CI verify)

**Category:** sec-

**Rule:** Layer 1: `gitleaks` runs as pre-commit hook (sub-second, MIT, 150+ patterns) — blocks the local commit before secret hits any history. Layer 2: `trufflehog` runs in CI on every PR with `--results=verified` — actively calls the issuing service (AWS, GitHub, Stripe…) to confirm the secret is *live*. Treat verified findings as P0 incidents (rotate first, then revert). Maintain a `.secrets.baseline` (detect-secrets) for any historic findings being phased out.

**Why it works:** No single tool wins. Gitleaks is fast and local but no verification → false positives. TruffleHog covers 800+ types and verifies → confirms live threats but is slower, doesn't suit pre-commit. Run both. detect-secrets (Yelp, Apache-2) shines as the gradual-introduction path: baseline existing secrets, block only NEW ones, ratchet down the baseline over time. GitGuardian's 2026 sprawl report: 29M new secrets leaked publicly in 2025, 81% surge in AI-service leaks specifically — agents leaking API keys is a leading attack surface now.

**When to use:** Always. Even single-developer repos — a leaked AWS key costs more than the project's revenue.
**When NOT to use:** Never skip; only the depth (1 layer vs 2) varies.

**Agent integration:**
- Agents that handle secrets MUST set them via env vars / secret managers, never inline.
- If pre-commit blocks a "secret", agent investigates whether it's a real secret or a false positive — if real, agent rotates immediately (calling 1Password CLI / vault), then scrubs from diff.
- Add `*.env`, `*.pem`, `*.key`, `credentials.json` to `.gitignore` AND `.gitleaks.toml` allowlist as defense-in-depth.

**Sources:**
- https://github.com/gitleaks/gitleaks
- https://github.com/trufflesecurity/trufflehog
- https://github.com/Yelp/detect-secrets
- https://www.gitguardian.com/state-of-secrets-sprawl-report-2026
- https://appsecsanta.com/sast-tools/gitleaks-vs-trufflehog
- https://blog.gitguardian.com/secret-scanning-tools/

---

## M5 — `sec-trivy-iac-and-container-scan` — Trivy as the universal supply-chain scanner

**Category:** sec-

**Rule:** Every Dockerfile / Helm chart / Terraform module / Kubernetes manifest passes through `trivy fs` (filesystem) and `trivy image` (container) in CI. Failing on HIGH/CRITICAL CVEs blocks merge. Generate SBOM (CycloneDX or SPDX) on every release tag and attach to GitHub release. Pin `trivy` to a known-clean version (NOT 0.69.4, which was supply-chain-compromised March 2026 — last clean was 0.69.3, then >=0.70 with new signing).

**Why it works:** Trivy is the de-facto multi-purpose scanner — vulns, misconfigs, secrets, SBOM — across containers, Kubernetes, IaC, code repos, cloud, OS packages. Single tool replaces 4-5. Active community, weekly DB updates. 2026 caveat: aquasecurity/trivy-action and a `trivy` 0.69.4 release were compromised in March 2026 ("TeamPCP" supply-chain attack); pin versions explicitly and verify signatures.

**When to use:** Any container, any IaC, any release artifact.
**When NOT to use:** Pure docs / SPA-only repos with no container or IaC.

**Agent integration:**
- Agents bumping a base image MUST run `trivy image <new-tag>` before opening the PR.
- SBOM diff posted as PR comment — agents verify the new dependency set is intentional.
- For Terraform, also chain `tflint` (provider-specific) + `checkov` (cloud-policy: 750+ rules across AWS/GCP/Azure/K8s) for layered coverage.

**Sources:**
- https://github.com/aquasecurity/trivy
- https://trivy.dev/
- https://www.stepsecurity.io/blog/trivy-compromised-a-second-time---malicious-v0-69-4-release
- https://www.checkov.io/
- https://github.com/terraform-linters/tflint

---

## M6 — `lint-megalinter-polyglot` — MegaLinter as one-call multi-language quality umbrella

**Category:** lint-

**Rule:** Polyglot repos (≥3 languages, e.g., Python+TS+Terraform+Markdown) run MegaLinter in CI as a single GitHub Action / GitLab job. It auto-detects languages and dispatches 100+ linters in parallel (multiprocessing) and reports unified SARIF. Choose a flavor (`security`, `python`, `javascript`, `terraform`, `dotnet`, etc.) to keep the image lean. Don't run as pre-commit — too heavy; reserve for CI.

**Why it works:** MegaLinter (oxsecurity, fork of GitHub Super-Linter, parallel via Python multiprocessing) covers 69 languages, 23 formats, 21 tooling formats — handles ESLint, ruff, hadolint, terraform fmt, ansible-lint, yamllint, markdownlint, shellcheck, golangci-lint, rubocop, php-cs-fixer, sql-lint, dotenv-linter, etc. in one shot. Faster than Super-Linter's sequential bash. For pure JS/TS, prefer `biome` (Rust, ESLint+Prettier in one, 491 rules, used by AWS/Cloudflare/Discord/Vercel) over chaining ESLint+Prettier.

**When to use:** Polyglot repos, CI quality umbrella, monorepos with multiple stack zones.
**When NOT to use:** Single-language repos (use the native tool: ruff for Python, biome for JS/TS, golangci-lint for Go).

**Agent integration:**
- Agent sees MegaLinter SARIF, fixes per-file using each native tool (not MegaLinter directly — it's a dispatcher).
- For autofixable rules, run native tool with `--fix` (`ruff check --fix`, `biome check --write`).
- Update MegaLinter quarterly to match latest linter versions.

**Sources:**
- https://github.com/oxsecurity/megalinter
- https://megalinter.io/
- https://biomejs.dev/
- https://github.com/biomejs/biome
- https://www.programming-helper.com/tech/biome-2026-rust-toolchain-web-development

---

## M7 — `lint-ruff-and-biome-as-default` — Rust-based unified linter+formatter as default per language

**Category:** lint-

**Rule:** For Python, use `ruff` (replaces black, flake8, isort, pyupgrade, autoflake, pydocstyle — 900+ rules, 10-100x faster) as the SOLE linter+formatter. For JS/TS/JSX/CSS/GraphQL, use `biome` (replaces ESLint + Prettier — 491 rules, single config) as the SOLE linter+formatter. Both have `--fix`/`--write` flags that agents call after every code edit. No more black+flake8+isort or ESLint+Prettier+import-sort chains.

**Why it works:** Single Rust binary per language → no `node_modules` overhead, no Python plugin chaos. ruff covers 900+ rules including Django (`DJ`), bugbear (`B`), pyupgrade (`UP`), no-print (`T20`), pyflakes (`F`), pycodestyle (`E/W`), isort (`I`), simplify (`SIM`). biome v2 (Biotype, Feb 2026) added type-aware lints, multi-file project understanding, and is replacing ESLint+Prettier in production at AWS/Google/Microsoft/Cloudflare/Coinbase/Discord/Slack/Vercel. Faion-network already enforces this for backend (ruff) — extend to dag and any new TS package.

**When to use:** Default for every new Python or JS/TS project.
**When NOT to use:** Legacy projects with deeply customized ESLint configs that haven't been migrated yet — migrate incrementally.

**Agent integration:**
- After ANY Python code edit: `ruff check --fix && ruff format`.
- After ANY TS/JS code edit: `biome check --write`.
- Agents NEVER manually format — always defer to the formatter.
- Add ruff/biome to pre-commit hooks AND CI to catch human commits too.

**Sources:**
- https://github.com/astral-sh/ruff
- https://docs.astral.sh/ruff/
- https://astral.sh/blog/ruff-v0.15.0
- https://biomejs.dev/
- https://github.com/biomejs/biome

---

## M8 — `gov-sonarqube-quality-gate-for-ai-code` — SonarQube quality gate qualified for AI code

**Category:** gov-

**Rule:** Repos with significant AI-generated code (per Sonar 2025: 42% of all committed code is AI-generated) MUST run SonarQube/SonarCloud with the "Sonar way for AI Code" quality gate (or a custom gate marked Qualified for AI Code Assurance). The gate enforces stricter thresholds on cognitive complexity, duplication, hotspot density, and "trust score" for AI code. PRs not passing the gate cannot merge. SonarQube MCP server connects to Claude Code/Cursor so the agent iteratively rewrites until it passes.

**Why it works:** AI-generated code has different defect profiles from human code (more lookalike bugs, more dead code, more shallow tests). A gate tuned for AI code (vs the default "Sonar way") catches these. Sonar's MCP server lets the agent itself loop until pass — turning the gate into a productive constraint, not a blocker.

**When to use:** Any team with >25% AI-authored code, regulated industries (finance, healthcare), enterprise-scale teams needing dashboards.
**When NOT to use:** Tiny solo projects — overhead exceeds value; ruff+biome+semgrep cover most of it cheaper.

**Agent integration:**
- Agent calls Sonar MCP to fetch findings, fixes locally, re-runs until clean.
- Treat gate fail as blocking; never override.
- For solo / OSS, Codacy is a lighter alternative (SAST + SCA + duplication + AI guardrails); Code Climate covers maintainability only (no SAST/SCA), so pair it with Snyk/Semgrep.

**Sources:**
- https://docs.sonarsource.com/sonarqube-cloud/standards/ai-code-assurance/quality-gates-for-ai-code
- https://docs.sonarsource.com/sonarqube-cloud/ai-capabilities/ai-code-assurance
- https://blog.codacy.com/sonarqube-alternatives
- https://securityboulevard.com/2026/03/how-to-optimize-sonarqube-for-reviewing-ai-generated-code/

---

## M9 — `sec-snyk-or-semgrep-supply-chain-on-pr` — Reachability-aware SCA on every PR

**Category:** sec-

**Rule:** Every PR runs SCA (Snyk Open Source / Snyk Code, OR Semgrep Supply Chain, OR OWASP Dependency-Check + Dependabot/Renovate) blocking on HIGH/CRITICAL CVEs in *reachable* code paths. Agents bumping deps must see the diff in vulnerability surface BEFORE merging. SBOM produced per release (SPDX or CycloneDX) for EU CRA compliance (mandatory Sep 2026 reporting, full Dec 2027). For dep updates, Renovate (60+ ecosystems, Bazel/Helm/Compose/Ansible Galaxy) or Dependabot (GitHub-native, free).

**Why it works:** Plain CVE matching has 70%+ false-positive rate (vulnerable function never called). Reachability analysis (Snyk, Semgrep) cuts noise. EU Cyber Resilience Act now MANDATES SBOMs for software shipped to EU — this is regulatory, not optional. Snyk Agent Fix autonomously generates and validates patches; Snyk DeepCode AI explains the data-flow path. OWASP Dependency-Check (free, NVD-based) is the OSS fallback when budget is zero.

**When to use:** Any project with third-party deps (i.e., ~all of them).
**When NOT to use:** Hermetic vendor-only codebases.

**Agent integration:**
- Agent reads Snyk/Semgrep JSON output, decides: (a) bump version if patch exists, (b) replace dep, (c) flag for human if no fix path.
- Agent NEVER ignores via inline `# noqa` for CVEs — adds documented exception with sunset date in `.snyk` / equivalent.
- Renovate config: groupName updates, auto-merge patch CVEs only, manual review for major bumps.

**Sources:**
- https://snyk.io/platform/
- https://snyk.io/solutions/secure-ai-generated-code/
- https://owasp.org/www-project-dependency-check/
- https://docs.renovatebot.com/
- https://rafter.so/blog/sca-tools-comparison
- https://nesbitt.io/2026/03/19/the-fragmented-world-of-dependency-policy.html

---

## M10 — `gov-license-compliance-fossa-or-licensee` — License obligations as a build-blocker

**Category:** gov-

**Rule:** Every release pipeline runs license scanning. For OSS-shipped products: GitHub's `licensee` (Ruby, free, used by GitHub itself for repo license detection) on the source. For commercial SaaS or shipped binaries: FOSSA (99.8% accuracy across 17+ langs, 20+ build systems, SBOM in SPDX/CycloneDX, deny/flag/approve policy engine) or Black Duck. Block on copyleft (GPL/AGPL) appearing in proprietary builds; require attribution NOTICE file regenerated per release.

**Why it works:** License violations are legal liability, not just security. AGPL inadvertently pulled into a SaaS = source-disclosure obligation for the entire stack. Manual review is hopeless at scale. FOSSA scans on every PR, posts deltas, generates attribution, and exposes a "policy denied" gate. Continuous "living SBOM" approach replaces one-time legal sign-off — required for EU CRA, US Executive Order 14028 SBOM mandates, and most enterprise procurement.

**When to use:** Any product distributed externally (SaaS, downloadable, OSS published). Any enterprise procurement context.
**When NOT to use:** Internal-only tools with no redistribution.

**Agent integration:**
- Agent adding a new dep checks license against allowlist BEFORE adding (e.g., MIT/Apache/BSD/MPL OK, GPL/AGPL blocked for proprietary).
- Agent regenerates `NOTICE` / `THIRD_PARTY.md` on dep changes.
- License changes between versions (e.g., HashiCorp BSL switch) trigger a flag → human escalation.

**Sources:**
- https://fossa.com/
- https://github.com/licensee/licensee
- https://fossa.com/blog/best-practices-generating-high-quality-sboms/
- https://appsecsanta.com/sca-tools/open-source-license-compliance

---

## M11 — `gov-conventional-commits-enforced` — Commit-message linting as deterministic changelog source

**Category:** gov-

**Rule:** Every repo enforces Conventional Commits (`feat:`, `fix:`, `chore:`, `refactor:`, `docs:`, `test:`, `perf:`, optional scope, optional `!` for breaking) via `commitlint` + Husky/lefthook `commit-msg` hook. CI also lints PR title (`commitlint-github-action`). Generated CHANGELOG.md flows from commits (`conventional-changelog`, `release-please`, `semantic-release`). Blocks non-conformant commits at hook time.

**Why it works:** Deterministic commit grammar = deterministic release notes, deterministic semver bumps, deterministic changelog. AI agents (which produce many small commits) NEED a hard format or the log becomes noise. commitlint validates before commit; commitizen prompts a wizard for humans who forget. The faion-network repo's pre-commit hook requiring CHANGELOG.md is a downstream of this principle.

**When to use:** Any team repo, any monorepo with multiple packages requiring independent versioning.
**When NOT to use:** Throwaway prototype repos.

**Agent integration:**
- Agents prefix every commit type per the spec — never freeform `"updates"` / `"fixes"`.
- One logical change per commit (matches existing faion-net `feedback_granular_commits.md` memory).
- Breaking changes use `!` AND `BREAKING CHANGE:` footer for tooling to pick up the major bump.

**Sources:**
- https://www.conventionalcommits.org/en/v1.0.0/
- https://github.com/conventional-changelog/commitlint
- https://commitizen-tools.github.io/commitizen/
- https://www.deployhq.com/blog/conventional-commits-a-standardized-approach-to-commit-messages

---

## M12 — `lint-autofix-vs-flag-decision-rule` — Crisp autofix-vs-flag policy for agents

**Category:** lint-

**Rule:** Agents apply an autofix automatically iff ALL hold:
1. The fix is purely syntactic (formatter, import sort, type annotation, dead-code removal).
2. The tool ships an explicit `fix:` / `--fix` / `--write` mechanism (ruff, biome, eslint --fix, semgrep --autofix where rule has `fix:`, prettier).
3. Tests still pass after the fix.
4. The diff is < 50 lines or all changes match a single rule ID.

Agents FLAG (do not auto-apply) when:
- Finding is from CodeQL / Semgrep without `fix:` / Snyk → propose patch as PR suggestion, human reviews.
- Finding is a secret (gitleaks/trufflehog) → ROTATE first, then human-reviewed cleanup.
- Finding is a CVE with no patch version → human picks: replace dep, accept risk, defer.
- Finding is a license conflict → ALWAYS human escalation.
- Finding is a SonarQube cognitive-complexity hotspot → propose refactor as draft PR; human approves.

**Why it works:** Confuses fewer humans, lets agents go fast on cheap fixes, blocks them from making "creative" decisions on stateful or legal issues. Mirrors what Factory.ai calls "lint green" as the agent merge gate, and what BitsAI-Fix academic work confirmed: pure-syntax fixes near-100% safe, anything semantic needs verification + retry. CodeMender (DeepMind 2025) and Snyk Agent Fix specifically validate fixes by running tests before submitting — same loop applies.

**When to use:** Always — this is the policy spine for any agent that touches code.
**When NOT to use:** N/A — this is a meta-rule.

**Agent integration:** This IS the agent integration. Encode as a checklist in the agent's system prompt and as logic in the CI agent.

**Sources:**
- https://factory.ai/news/using-linters-to-direct-agents
- https://arxiv.org/html/2508.03487v1 (BitsAI-Fix)
- https://deepmind.google/blog/introducing-codemender-an-ai-agent-for-code-security/
- https://dagger.io/blog/automate-your-ci-fixes-self-healing-pipelines-with-ai-agents/
- https://www.docker.com/blog/how-to-fix-eslint-violations-with-ai-assistance/

---

## Cross-cutting principles (for the brainstorm phase)

- **Determinism first, AI second.** Every methodology above runs WITHOUT AI and produces a hard signal. AI extends (autofix, triage, custom rule generation) but never replaces the gate.
- **Two-layer pattern recurs:** local (pre-commit, fast, MIT) + CI (slow, deep, verifying). Secrets, lint, SAST all follow this. Agents respect both.
- **AI-code-specific gates:** Sonar AI Code Assurance, Snyk Agent Fix, Semgrep AI rules — 2026 added a dedicated tier for "AI authored this, hold to a higher bar."
- **Supply-chain pinning is mandatory.** Trivy 0.69.4 and aquasecurity/trivy-action were both compromised in March 2026. Pin actions by SHA, verify signatures (cosign), enable StepSecurity / hardened runners.
- **Per-language native tool beats umbrella for small repos:** ruff (Py) and biome (JS/TS) — single Rust binary per repo wins over MegaLinter when scope is one language.
