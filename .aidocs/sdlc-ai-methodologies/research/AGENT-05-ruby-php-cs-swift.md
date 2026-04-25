# AGENT-05 — Ruby, PHP, C#, Swift Tooling for AI-Augmented SDLC

**Summary line 1:** Each of Ruby, PHP, C#, Swift now ships an "AI-ready" floor — deterministic linters, type checkers, formatters, mutation tools — that AI agents must run BEFORE adding semantic value, plus an explicit agent surface (Ruby LSP MCP, Laravel Boost skills, Roslyn-grounded Copilot Testing, Xcode 26.3 agentic coding).
**Summary line 2:** The cross-language pattern: pin a strict deterministic gate (PHPStan L9, Sorbet `# typed: strict`, Roslyn analyzers as errors, Harmonize architecture tests), then expose tool output to agents via MCP / AGENTS.md / .editorconfig so the LLM is grounded in compiler semantics, not regex.

---

## Methodology candidates (12)

### M-05-01 — Sorbet `# typed: strict` + Tapioca RBI floor before AI edits Ruby
**Slug:** `lang-ruby-sorbet-strict-floor`
**Category:** lang-

**Rule:** Any Ruby file an agent is allowed to modify autonomously must be `# typed: true` or stricter, with Tapioca-generated RBIs for all gems. Agents pre-flight `bundle exec srb tc` and `bundle exec tapioca check-shims` before opening a PR; failures block.

**Why it works:** Sorbet is the typechecker Shopify built specifically because Ruby is dynamic enough to make any LLM hallucinate methods. Tapioca runtime-introspects Rails DSLs and emits static RBIs, giving Sorbet the "shape" of `has_many`, `scope`, etc. With a strict file, agent-generated method calls fail at typecheck — a deterministic refusal.
**When to use:** Rails monoliths > 100 KLOC; multi-team engineering orgs.
**When NOT to use:** Toy gems, Sinatra micro-services, scripts (overhead too high; use `# typed: false`).

**Sources:**
- https://sorbet.org/
- https://github.com/Shopify/tapioca
- https://shopify.engineering/adopting-sorbet
- https://blog.jez.io/type-aware-rubocop/

---

### M-05-02 — Ruby LSP + RuboCop MCP as the agent's "code sense" channel
**Slug:** `lang-ruby-lsp-mcp-agent`
**Category:** lang-

**Rule:** Configure Claude Code (or any MCP-aware agent) with both Ruby LSP and RuboCop MCP servers. Agent uses `goToDefinition`, `findReferences`, `callHierarchy` from Ruby LSP and structured RuboCop offenses (not raw stdout) to plan edits. RuboCop ≥ 1.85.0 (Feb 2026) ships experimental MCP.

**Why it works:** LLMs guessing at Ruby symbol locations is the #1 source of hallucinated Rails associations. Ruby LSP grounds the model in Shopify's compiler-aware index; RuboCop MCP gives offenses as JSON the model can `apply_correction` on, instead of re-reading text logs. Lower token cost, fewer wrong patches.
**When to use:** Any Ruby project with Claude Code/Cursor agents.
**When NOT to use:** Single-file scripts (LSP setup overhead not worth it).

**Sources:**
- https://www.damiangalarza.com/posts/2026-03-13-ruby-lsp-claude-code/
- https://allaboutcoding.ghinda.com/how-to-add-rubocop-mcp-to-claude-code-and-opencode
- https://github.com/st0012/ruby-skills
- https://st0012.dev/2026/01/24/ruby-skills-teaching-claude-code-about-ruby-tooling-and-ecosystem/

---

### M-05-03 — Brakeman + bundler-audit run on every agent PR (Rails)
**Slug:** `sec-ruby-brakeman-bundler-audit-pr`
**Category:** sec-

**Rule:** CI step blocks any agent-authored PR if Brakeman raises a Confidence:High warning OR bundler-audit reports any unfixed CVE in `Gemfile.lock`. No human override without security-team approval label.

**Why it works:** Brakeman traces params → controller → view to find injection sinks; bundler-audit cross-references `Gemfile.lock` against the ruby-advisory-db. Together they catch the two largest Rails attack surfaces an LLM agent can introduce: unsanitized user input and a vulnerable transitive dep update. Brakeman v8.0.2 (Feb 2026) is the standard.
**When to use:** Any Rails app with agents authoring PRs.
**When NOT to use:** Pure-library gems with no controllers (Brakeman doesn't apply; keep bundler-audit).

**Sources:**
- https://brakemanscanner.org/
- https://www.helpnetsecurity.com/2026/01/26/brakeman-open-source-vulnerability-scanner-ruby-on-rails/
- https://vulehuan.com/en/blog/2024/6/secure-your-ruby-on-rails-app-brakeman-vs-grype-vs-bundler-audit-axkoAXLpVXz

---

### M-05-04 — VCR cassette = first-class artifact for agent-replayable HTTP tests
**Slug:** `test-ruby-vcr-deterministic`
**Category:** test-

**Rule:** All RSpec tests that hit external APIs must use VCR with `record: :once` and FactoryBot factories that pin sequence-generated values to fixed strings. Cassettes are checked into the repo. Agents may NOT re-record cassettes without an explicit `vcr_rerecord:` label on the PR.

**Why it works:** Without pinning, FactoryBot sequences mutate every run, VCR fails to match the cassette, agent "fixes" by deleting + re-recording → flake-bypass. Pinned factories + `:once` mode make the test deterministic and the agent fail loudly on real change.
**When to use:** Any Ruby test suite with HTTP-dependent specs.
**When NOT to use:** WebMock-only stubs are sufficient for trivial cases.

**Sources:**
- https://fabioperrella.github.io/10_tips_to_help_using_the_VCR_gem_in_your_ruby_test_suite.html
- https://github.com/vcr/vcr
- https://elitedev.in/ruby/essential-ruby-gems-for-production-ready-testing-/

---

### M-05-05 — PHPStan level 9 + Psalm taint-mode dual gate before agent merge
**Slug:** `lang-php-phpstan9-psalm-taint`
**Category:** lang-

**Rule:** CI runs PHPStan at level 9 (or 10 for libs) AND Psalm with `--taint-analysis` on every agent PR; both must be green. PHPStan catches type errors, Psalm catches SQLi/XSS/command-injection taint flow that PHPStan does not model.

**Why it works:** PHPStan 2.1.34 (early 2026) added 25-40% faster reflection-cache analysis, making L9 affordable in CI. Psalm uniquely tracks tainted data through methods. Together they are the "Information Gain" floor referenced in 2026 PHP+AI literature: deploy LLM only where these two tools are silent. PHPStan L9 also forbids `mixed`, which is exactly the type LLMs love to emit.
**When to use:** Any Symfony/Laravel/Drupal codebase with agent contributors.
**When NOT to use:** Greenfield prototypes (start at L5, ratchet up).

**Sources:**
- https://appsecsanta.com/sast-tools/phpstan-vs-psalm
- https://appsecsanta.com/phpstan
- https://meh.dev/php-static-analysis-tools
- https://devqube.com/ai-in-legacy-php-code-review/

---

### M-05-06 — Rector recipes as the only "auto-modernize" channel for legacy PHP
**Slug:** `lang-php-rector-modernize-pipeline`
**Category:** lang-

**Rule:** Refactors that change PHP syntax (PHP version upgrade, dead-code removal, type-hint backfill) MUST go through Rector with a checked-in `rector.php` config. Agents may propose new rule sets but cannot hand-edit the same transformation by hand-rolling sed/regex.

**Why it works:** Rector is AST-driven; sed/regex is not. Agents asked to "upgrade this codebase to PHP 8.4" without Rector reliably break complex syntax (named args, enums, readonly). With Rector, the agent's job is to pick rule sets, run, review the diff — a much narrower failure surface. Pairs with PHPStan as a deterministic floor.
**When to use:** Any PHP project doing version migrations or framework upgrades.
**When NOT to use:** Tiny bug fixes — overkill.

**Sources:**
- https://github.com/netresearch/php-modernization-skill
- https://meh.dev/php-static-analysis-tools
- https://www.artiphp.com/2026/laravel-13-migration-checklist/

---

### M-05-07 — Laravel Boost skills mounted in agent context (Laravel-specific KB)
**Slug:** `kb-php-laravel-boost-skills`
**Category:** kb-

**Rule:** Every Laravel project running an AI agent installs Laravel Boost; Boost 2.0 (Jan 2026) loads modular Skills (Livewire, Pest, Eloquent, Filament, Inertia, etc.) on-demand via `SupportsSkills` contract. Agents read `composer require laravel/boost` artifacts to learn the project's exact Laravel version idioms — not generic outdated training data.

**Why it works:** Static AGENTS.md bloats context. Boost Skills load only the relevant subset (Pest skill loads only when writing tests). The Laravel Skills directory (skills.laravel.cloud) ships community skills that map agent intent → Laravel best practice. Pairs with `composer audit` (Composer 2.9 auto-blocks vulnerable deps).
**When to use:** Laravel ≥ 11.
**When NOT to use:** Pure Symfony / vanilla PHP — no Boost equivalent.

**Sources:**
- https://laravel.com/docs/13.x/boost
- https://laravel-news.com/laravel-skills
- https://sadiqueali.medium.com/laravel-boost-2-0-ships-skills-ai-agents-now-understand-your-laravel-app-at-a-package-level-22cc7db6ecfa
- https://freek.dev/3006-my-current-setup-for-laravel-php-and-ai-development-2026-edition

---

### M-05-08 — Pest + Behat split: Pest for unit, Behat for AI-readable BDD specs
**Slug:** `test-php-pest-behat-split`
**Category:** test-

**Rule:** Unit and feature tests use Pest (closure DSL, `it('does X')`). Acceptance specs that double as product documentation use Behat with Gherkin `.feature` files. AI agents may auto-generate Pest tests but must NOT auto-write `.feature` files — those require human PM/PO sign-off.

**Why it works:** Pest's expressive syntax produces tests close to natural language → LLMs both read and write them well. Gherkin scenarios are the contract with non-engineers; LLM-generated `.feature` files drift from product intent silently. The split keeps determinism for code, human review for spec.
**When to use:** Mid/large Laravel/Symfony with cross-functional teams.
**When NOT to use:** Solo CRUD apps — Pest alone is enough.

**Sources:**
- https://pestphp.com/
- https://www.phpeveryday.com/articles/testing-php-2026-phpunit-10-pest-code-coverage/
- https://testautomationtools.dev/top-5-php-testing-frameworks/

---

### M-05-09 — Roslyn analyzers as compile-error class to make LLM bugs structurally impossible
**Slug:** `lang-csharp-roslyn-analyzer-compile-error`
**Category:** lang-

**Rule:** For each LLM-introduced bug class (null-deref, async-void, missing `ConfigureAwait`, public-API break) add or enable a Roslyn analyzer with severity `error` in `.editorconfig`. Use `Microsoft.CodeAnalysis.PublicApiAnalyzers` to lock the public surface (`PublicAPI.Shipped.txt` + `PublicAPI.Unshipped.txt`).

**Why it works:** The Microsoft .NET team's stated 2026 pattern: "identify the class of mistake, make it a compile-time impossibility, then let Copilot continue knowing that failure mode is structurally ruled out." Roslyn is a deterministic gate. Public API analyzer prevents an agent from accidentally widening or breaking a library surface — a frequent failure mode in autonomous PRs.
**When to use:** Any production .NET library or service.
**When NOT to use:** Throwaway scripts, scratch projects.

**Sources:**
- https://devblogs.microsoft.com/dotnet/github-copilot-testing-for-dotnet/
- https://learn.microsoft.com/en-us/visualstudio/code-quality/roslyn-analyzers-overview?view=vs-2022
- https://medium.com/workleap/preventing-breaking-changes-in-net-class-libraries-e61ae93b1b46
- https://github.com/dotnet/roslyn-analyzers

---

### M-05-10 — `@Test` Copilot agent + Stryker.NET mutation gate for C# test quality
**Slug:** `test-csharp-copilot-stryker-quality`
**Category:** test-

**Rule:** Use GitHub Copilot Testing for .NET (`@Test` agent in VS 2026 v18.3) to generate xUnit/NUnit/MSTest tests at file/project/git-diff scope, then run Stryker.NET; require mutation score ≥ 70% on changed files. Tests with mutation score < threshold are rejected even if all green.

**Why it works:** `@Test` is grounded in Roslyn + MSBuild semantics — it reads the type system, not text. But LLM tests notoriously over-mock and under-assert. Stryker mutates operators, conditions, return values; surviving mutants reveal weak assertions the model wrote. The combo (AI generates volume, mutation testing enforces rigor) outperforms either alone.
**When to use:** C# code with non-trivial business logic.
**When NOT to use:** DTOs, plain data classes (mutation noise high).

**Sources:**
- https://devblogs.microsoft.com/dotnet/github-copilot-testing-for-dotnet-available-in-visual-studio/
- https://learn.microsoft.com/en-us/dotnet/core/testing/mutation-testing
- https://stryker-mutator.io/docs/stryker-net/introduction/
- https://github.com/stryker-mutator/stryker-net

---

### M-05-11 — Hybrid Roslyn + Azure OpenAI code-review pipeline (deterministic + reasoning split)
**Slug:** `mr-csharp-roslyn-llm-hybrid-review`
**Category:** mr-

**Rule:** Code-review automation for .NET PRs runs in two stages: (1) Roslyn extracts AST diff + analyzer findings; (2) Azure OpenAI / Claude reasons over the structured artifact (NOT the raw diff). Comments are posted only when both Roslyn flagged a structural concern AND the LLM scored confidence ≥ X.

**Why it works:** Pure-LLM code review hallucinates issues that the compiler already accepts. Pure-Roslyn misses intent. Roslyn provides "shape and accuracy"; LLM provides "meaning and intention". Feeding the LLM a typed AST view dramatically lowers false-positive rate vs. raw-diff review.
**When to use:** .NET teams that already run Roslyn analyzers in CI.
**When NOT to use:** Tiny repos (< 5k LOC) — overhead exceeds value.

**Sources:**
- https://developersvoice.com/blog/ai-development/building-hybrid-ai-code-reviewer-with-roslyn/
- https://devblogs.microsoft.com/dotnet/github-copilot-testing-for-dotnet/

---

### M-05-12 — Swift floor: SwiftLint + swift-format + Harmonize architecture tests + Swift Testing
**Slug:** `lang-swift-arch-test-harmonize`
**Category:** lang-

**Rule:** A Swift project's deterministic floor before agent edits: `swift-format` (Apple-shipped, in Xcode 16+ toolchain) for layout, SwiftLint for style/idioms, Harmonize for architecture rules expressed as XCTest/Swift Testing assertions, and Swift Testing (`@Test` + `#expect`) as the default test framework with XCTest interop via ST-0021 (accepted Mar 2026). All four run pre-merge.

**Why it works:** SwiftLint is regex; SwiftFormat is layout — neither understands architecture (e.g. "ViewModels must not import UIKit", "Services must implement Protocol X"). Harmonize uses SwiftSyntax to write architecture rules as actual unit tests, so an agent's structurally wrong PR fails CI with a real test name like `ViewModels_must_not_import_UIKit_failed`. ST-0021 lets legacy XCTest cases live alongside new `#expect` tests, so migration doesn't block. Xcode 26.3 agentic coding (Claude/Codex) reads these signals natively.
**When to use:** Any Swift app with > 1 module or shared codebase.
**When NOT to use:** Scratch SwiftUI playgrounds.

**Sources:**
- https://github.com/realm/SwiftLint
- https://github.com/perrystreetsoftware/Harmonize
- https://forums.swift.org/t/we-built-harmonize-a-modern-open-source-linter-for-swift-that-enforces-architecture-as-unit-tests/79508
- https://forums.swift.org/t/accepted-st-0021-targeted-interoperability-between-swift-testing-and-xctest/85331
- https://www.apple.com/newsroom/2026/02/xcode-26-point-3-unlocks-the-power-of-agentic-coding/
- https://sundayswift.com/posts/preparing-ios-codebase-for-ai-agents/
- https://github.com/twostraws/SwiftAgents

---

## Cross-cutting observations

| Theme | Ruby | PHP | C# | Swift |
|-------|------|-----|----|-------|
| Type floor | Sorbet `# typed: strict` + Tapioca | PHPStan L9 + Psalm taint | Roslyn analyzers as errors | Swift compiler + SwiftLint + Harmonize |
| Agent surface | Ruby LSP MCP, RuboCop MCP, ruby-skills plugin | Laravel Boost Skills, AGENTS.md | Copilot `@Test` (Roslyn-grounded) | Xcode 26.3 agentic mode + AGENTS.md (SwiftAgents) |
| Test rigor add-on | VCR pinning, FactoryBot fixed sequences | Pest + Behat split | Stryker.NET mutation | Harmonize architecture tests, Swift Testing |
| Security gate | Brakeman + bundler-audit | composer audit (2.9 auto-block) + Psalm taint | PublicApiAnalyzers + analyzer rules | Apple sandbox + SwiftLint custom rules |
| Determinism rule | Sorbet typecheck must pass | PHPStan + Psalm both green | Roslyn `error` severity | Harmonize tests + swift-format |

**Universal pattern:** Each language now has (a) a deterministic floor agents must pass before semantic LLM steps, (b) a structured agent-ingestion channel (MCP / Skills / AGENTS.md / Roslyn AST), (c) an instrumentation layer that converts agent output into something the deterministic floor can re-judge. Methodologies that don't honor (a) → (b) → (c) flow tend to produce drift.

---

## References (consolidated)

- Ruby — Sorbet: https://sorbet.org/ ; Tapioca: https://github.com/Shopify/tapioca ; Ruby LSP + Claude Code: https://www.damiangalarza.com/posts/2026-03-13-ruby-lsp-claude-code/ ; ruby-skills: https://github.com/st0012/ruby-skills ; Brakeman v8: https://www.helpnetsecurity.com/2026/01/26/brakeman-open-source-vulnerability-scanner-ruby-on-rails/
- PHP — PHPStan 2.1.34: https://appsecsanta.com/phpstan ; Psalm vs PHPStan: https://appsecsanta.com/sast-tools/phpstan-vs-psalm ; Laravel Boost 2.0: https://laravel.com/docs/13.x/boost ; Laravel Skills directory: https://laravel-news.com/laravel-skills ; Pest: https://pestphp.com/ ; Composer audit: https://blog.packagist.com/discover-security-advisories-with-composers-audit-command/
- C# — Copilot Testing GA: https://devblogs.microsoft.com/dotnet/github-copilot-testing-for-dotnet-available-in-visual-studio/ ; Roslyn analyzers: https://github.com/dotnet/roslyn-analyzers ; PublicApiAnalyzers: https://github.com/dotnet/roslyn-analyzers/blob/main/src/PublicApiAnalyzers/Microsoft.CodeAnalysis.PublicApiAnalyzers.md ; Stryker.NET: https://stryker-mutator.io/docs/stryker-net/introduction/ ; Hybrid review: https://developersvoice.com/blog/ai-development/building-hybrid-ai-code-reviewer-with-roslyn/
- Swift — SwiftLint: https://github.com/realm/SwiftLint ; Harmonize: https://github.com/perrystreetsoftware/Harmonize ; Swift Testing ST-0021: https://forums.swift.org/t/accepted-st-0021-targeted-interoperability-between-swift-testing-and-xctest/85331 ; Xcode 26.3 agents: https://www.apple.com/newsroom/2026/02/xcode-26-point-3-unlocks-the-power-of-agentic-coding/ ; SwiftAgents: https://github.com/twostraws/SwiftAgents ; AI-ready iOS codebases: https://sundayswift.com/posts/preparing-ios-codebase-for-ai-agents/
