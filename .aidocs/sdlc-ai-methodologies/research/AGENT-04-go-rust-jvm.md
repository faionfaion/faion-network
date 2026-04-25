# AGENT-04 — Go, Rust, Java, Kotlin tooling for AI-augmented SDLC

**Summary (2 lines):** AI-generated code in compiled languages must hit the deterministic floor (format/lint/vuln/types) before any LLM eyeball; mutation/property tests close the "tests pass but logic is wrong" gap that pattern-matching agents create.
Each entry below is a concrete, citable rule mapped to `lang-` / `lint-` / `test-` / `sec-` with when-to / when-NOT and a snippet.

State: April 2026. Languages: Go, Rust, Java, Kotlin. Focus: rules an AI agent (claude-code, aider, Cursor) can be made to obey via `CLAUDE.md`/`.cursorrules`/pre-commit, not vibes.

---

## 1. `lint-go-golangci-lint-v2-default` — golangci-lint v2 as Go's deterministic floor

**Rule:** Every Go module MUST have `.golangci.yml` with `version: "2"` and `linters.default: standard` (or `all` for greenfield), plus the `comments`, `std-error-handling`, `common-false-positives` exclusion presets enabled. AI agents run `golangci-lint run --fix` before producing any diff.

**Source:** <https://golangci-lint.run/docs/configuration/file/> · <https://golangci-lint.run/docs/product/migration-guide/> · v2 release notes <https://ldez.github.io/blog/2025/03/23/golangci-lint-v2/>

**When to use:** Every Go repo larger than a single `main.go`. v2 replaces `enable-all`/`disable-all` with a single `default:` field and ships migration via `golangci-lint migrate`.
**When NOT to use:** `tinygo` / WASI builds where some linters miss-flag generics — use `default: fast` + selective enables.

**Snippet:**
```yaml
# .golangci.yml
version: "2"
linters:
  default: standard
  enable: [errcheck, govet, ineffassign, staticcheck, unused, gofumpt, gosec, revive, copyloopvar]
  exclusions:
    presets: [comments, std-error-handling, common-false-positives]
formatters:
  enable: [gofumpt, goimports]
```

---

## 2. `lint-go-gofumpt-strict-format` — gofumpt over gofmt for AI patches

**Rule:** Replace `gofmt` with `gofumpt` (≥ v0.9.2, requires Go 1.24+) in pre-commit and editor save. gofumpt is a strict superset that removes 20+ stylistic ambiguities so AI-generated diffs are byte-stable across re-renders.

**Source:** <https://github.com/mvdan/gofumpt>

**When to use:** Anywhere you want zero style drift between human and AI commits. Critical when several agents (claude-code + Cursor) edit the same file — gofmt accepts variants, gofumpt collapses them to one.
**When NOT to use:** Codebases that vendor third-party Go tools requiring exact gofmt output (rare).

**Snippet:**
```bash
# pre-commit hook
gofumpt -l -w .
golangci-lint run --fix
```

---

## 3. `sec-go-govulncheck-call-graph` — call-graph–aware vuln scanning

**Rule:** Run `govulncheck ./...` in CI on every PR; fail the build only when the vulnerable symbol is reachable from your code (this is govulncheck's default — unlike npm audit it doesn't fire on unused transitive imports). For binary releases, also run `govulncheck -mode=binary ./bin/app`.

**Source:** <https://go.dev/doc/security/vuln/> · <https://pkg.go.dev/golang.org/x/vuln/cmd/govulncheck>

**When to use:** All Go modules; preferred over Dependabot for Go because of reachability filtering.
**When NOT to use:** Don't replace govulncheck with Snyk/Trivy alone — those don't do Go call-graph reachability and produce 5-10× noise.

**Snippet:**
```yaml
# .github/workflows/vuln.yml
- run: go install golang.org/x/vuln/cmd/govulncheck@latest
- run: govulncheck -show=verbose ./...
```

---

## 4. `test-go-table-driven-with-tcleanup` — table-driven + `t.Cleanup` for AI-readable tests

**Rule:** Every Go test that mocks an interface uses table-driven cases + `t.Cleanup(func() { mock.AssertExpectations(t) })`. Mocks generated via `mockery` from `.mockery.yml`, never hand-written. AI agents read the table, identify the missing case, and append rows.

**Source:** <https://go.dev/wiki/TableDrivenTests> · <https://github.com/stretchr/testify> · <https://vektra.github.io/mockery/>

**When to use:** Any function with ≥ 2 distinct branches or any mocked dependency. Tables make AI-driven test expansion trivial: "add a row for the timeout case" is a 4-line diff.
**When NOT to use:** Single-branch helpers — tables add overhead. Don't generate mocks for stable third-party interfaces (use real fakes instead).

**Snippet:**
```go
func TestParse(t *testing.T) {
    cases := []struct{ name, in string; want int; wantErr bool }{
        {"empty", "", 0, true},
        {"valid", "42", 42, false},
    }
    for _, tc := range cases {
        t.Run(tc.name, func(t *testing.T) {
            t.Parallel()
            got, err := Parse(tc.in)
            require.Equal(t, tc.wantErr, err != nil)
            require.Equal(t, tc.want, got)
        })
    }
}
```

---

## 5. `test-go-native-fuzz` — `testing.F` fuzz over hand-rolled property tests

**Rule:** For any parser, decoder, or boundary-input function add a `FuzzXxx(f *testing.F)` test with at least 3 `f.Add(...)` seeds. Run `go test -fuzz=FuzzXxx -fuzztime=60s` nightly in CI; check failing corpus into `testdata/fuzz/`.

**Source:** <https://go.dev/doc/security/fuzz/> · <https://go.dev/doc/tutorial/fuzz>

**When to use:** Parsers, validators, marshallers, anything taking `[]byte` or `string` from outside. AI agents are excellent at writing property invariants ("round-trip Marshal/Unmarshal must equal input").
**When NOT to use:** Pure side-effect code (handlers, schedulers) — fuzzing here yields noise, prefer integration tests.

**Snippet:**
```go
func FuzzRoundtrip(f *testing.F) {
    f.Add([]byte(`{"a":1}`))
    f.Fuzz(func(t *testing.T, b []byte) {
        var v map[string]any
        if json.Unmarshal(b, &v) != nil { return }
        out, err := json.Marshal(v)
        require.NoError(t, err)
        require.NotNil(t, out)
    })
}
```

---

## 6. `lang-go-tygo-frontend-contract` — Go→TypeScript types via tygo as the single source

**Rule:** API DTOs live in Go; TypeScript types are generated via `tygo generate` from `tygo.yaml`. Never hand-write the TS counterpart. CI fails if generated `.d.ts` differs from committed file (`git diff --exit-code`).

**Source:** <https://github.com/gzuidhof/tygo>

**When to use:** Go BE + TS FE monorepos where contract drift is the #1 source of "AI hallucinated this field" bugs.
**When NOT to use:** OpenAPI-first projects (use `oapi-codegen` instead — single source is the spec, not Go).

**Snippet:**
```yaml
# tygo.yaml
packages:
  - path: github.com/me/api/dto
    output_path: web/src/types/api.ts
    type_mappings:
      time.Time: "string"
      uuid.UUID: "string"
```

---

## 7. `lint-rust-clippy-deny-pedantic` — clippy as a build gate

**Rule:** `cargo clippy --all-targets --all-features -- -D warnings -W clippy::pedantic -W clippy::nursery` runs in CI and as `pre-commit`. AI agents are forbidden from adding `#[allow(clippy::*)]` without an inline comment naming the lint and the reason.

**Source:** <https://doc.rust-lang.org/clippy/> · <https://github.com/rust-lang/rust-clippy> · Effective Rust Item 29 <https://effective-rust.com/clippy.html>

**When to use:** Every Rust crate. `pedantic` catches AI-typical patterns: needless clones, suboptimal iterator chains, redundant `.to_string()`.
**When NOT to use:** Don't enable `clippy::restriction` wholesale — it's mutually contradictory; cherry-pick rules instead.

**Snippet:**
```toml
# clippy.toml
disallowed-methods = [
  { path = "std::env::var", reason = "use config crate" },
  { path = "std::process::exit", reason = "return Result" },
]
```

---

## 8. `sec-rust-cargo-deny-supply-chain` — cargo-deny licenses + advisories + sources

**Rule:** Every Rust workspace ships `deny.toml` with four checks enabled: `licenses` (allowlist), `advisories` (RustSec), `bans` (forbid yanked / multiple versions of same crate), `sources` (only crates.io + your registry). CI runs `cargo deny check` on every PR.

**Source:** <https://embarkstudios.github.io/cargo-deny/> · <https://github.com/EmbarkStudios/cargo-deny>

**When to use:** All production Rust services and any crate published to crates.io. Replaces `cargo-audit` + a license tool + manual checks.
**When NOT to use:** Throwaway prototypes — bootstrap cost (~1 hour to tune `deny.toml`) isn't worth it.

**Snippet:**
```toml
# deny.toml
[licenses]
allow = ["MIT", "Apache-2.0", "BSD-3-Clause", "ISC"]
confidence-threshold = 0.93
[advisories]
yanked = "deny"
[bans]
multiple-versions = "warn"
```

---

## 9. `test-rust-nextest-junit-ci` — cargo-nextest for parallel + JUnit reports

**Rule:** Replace `cargo test` with `cargo nextest run --profile ci` in CI. Profile emits JUnit XML for GitHub/GitLab dashboards and runs tests in process-isolated parallel groups (3-5× faster on large workspaces).

**Source:** <https://nexte.st/> · <https://nexte.st/docs/configuration/>

**When to use:** Workspaces with > 100 tests or any flaky-test problem (nextest retries). AI agents see structured failure output instead of cargo's ANSI soup.
**When NOT to use:** Doctests — nextest doesn't run them; keep `cargo test --doc` separately.

**Snippet:**
```toml
# .config/nextest.toml
[profile.ci]
fail-fast = false
retries = 2
[profile.ci.junit]
path = "junit.xml"
```

---

## 10. `test-rust-proptest-and-mutants` — property + mutation as a pair

**Rule:** For pure-logic crates use `proptest!` for invariants, then run `cargo mutants --in-place --jobs 4` weekly. A mutation that survives all property tests is a missing invariant — AI is asked to propose the new property.

**Source:** <https://github.com/proptest-rs/proptest> · <https://mutants.rs/> · <https://github.com/sourcefrog/cargo-mutants>

**When to use:** Parsers, state machines, financial math, anything with explicit invariants. cargo-mutants is the Rust counterpart to PIT — Mutagen is unmaintained, do not use.
**When NOT to use:** Async / I/O code — mutation testing thrashes on it; restrict via `--package` to pure crates.

**Snippet:**
```rust
proptest! {
    #[test]
    fn roundtrip(s in "\\PC*") {
        let enc = encode(&s);
        prop_assert_eq!(decode(&enc).unwrap(), s);
    }
}
```

---

## 11. `lint-rust-miri-undefined-behavior` — Miri for unsafe-touching code

**Rule:** Any crate with `unsafe` blocks runs `cargo +nightly miri test` in CI (separate job, allowed-to-fail flagged tests). Miri detects out-of-bounds, use-after-free, data races that escape clippy and the borrow checker.

**Source:** <https://github.com/rust-lang/miri> · <https://doc.rust-lang.org/nightly/unstable-book/compiler-flags/miri.html>

**When to use:** FFI bindings, hand-rolled allocators, lock-free data structures, anywhere `unsafe` lives.
**When NOT to use:** Pure-safe crates — Miri adds 10-50× test runtime; don't pay it without `unsafe`. Also skip async heavy code (Miri's tokio support is partial).

**Snippet:**
```bash
cargo +nightly miri test --package my-ffi --lib
```

---

## 12. `lint-java-errorprone-nullaway` — Error Prone + NullAway as the compile-time gate

**Rule:** Wire Error Prone (500+ checks) and NullAway into `javac` for every Java module. Treat selected checks (`@RestrictedApi`, `MissingCasesInEnumSwitch`, `NullAway:AnnotatedPackages`) as `ERROR` so the compile fails. AI agents see the failure during edit, not at PR review.

**Source:** <https://errorprone.info/bugpatterns> · <https://github.com/uber/NullAway> · <https://errorprone.info/docs/installation>

**When to use:** Every JDK 11+ project; replaces ad-hoc `@Nullable` discipline with enforcement.
**When NOT to use:** Pure Kotlin codebases (use detekt's null rules); legacy projects until you've fixed the existing N nullness errors.

**Snippet:**
```xml
<!-- pom.xml fragment -->
<compilerArgs>
  <arg>-Xplugin:ErrorProne -XepDisableWarningsInGeneratedCode</arg>
  <arg>-Xplugin:ErrorProne -Xep:NullAway:ERROR -XepOpt:NullAway:AnnotatedPackages=com.me</arg>
</compilerArgs>
```

---

## 13. `lint-java-spotbugs-pmd-checkstyle-trio` — three tools, three roles

**Rule:** Run all three in CI but for distinct purposes: **Checkstyle** = formatting + naming, **PMD** = best-practices + duplication, **SpotBugs** (with FindSecBugs plugin) = bytecode-level bug detection. Use `gradle-static-analysis-plugin` to aggregate. AI agents must pass all three before opening a PR.

**Source:** <https://spotbugs.github.io/> · <https://pmd.github.io/> · <https://checkstyle.sourceforge.io/> · <https://gradleup.com/static-analysis-plugin/>

**When to use:** Long-lived Java services; gives layered coverage Error Prone alone misses (e.g., bytecode-level resource leaks).
**When NOT to use:** Greenfield projects under 5k LoC — start with Error Prone + Checkstyle, add the rest at scale. SpotBugs is slow on huge JARs (> 200 MB); split modules instead.

**Snippet:**
```groovy
// build.gradle
staticAnalysis {
    penalty { maxErrors = 0; maxWarnings = 0 }
    checkstyle { toolVersion = '10.21.0' }
    pmd { toolVersion = '7.10.0' }
    spotbugs { toolVersion = '4.8.6'; ignoreFailures = false }
}
```

---

## 14. `test-java-pit-mutation-incremental` — PITest `scmMutationCoverage` per PR

**Rule:** Add `pitest-maven` (or `gradle-pitest-plugin`) and run `mvn -DwithHistory pitest:scmMutationCoverage -Danalyse=lastCommit` on every PR. Threshold: ≥ 70% mutation coverage on changed files; build fails otherwise. AI-written tests historically score 30-50% — this rule forces real assertions.

**Source:** <https://pitest.org/quickstart/maven/> · <https://gradle-pitest-plugin.solidsoft.info/> · 1.19.x release <https://github.com/hcoles/pitest/releases>

**When to use:** Anywhere line coverage is being gamed by `assertNotNull`/`assertTrue(true)` patterns from AI agents. `scmMutationCoverage` keeps PR runtime under 2 minutes.
**When NOT to use:** Pure DTO modules (no logic to mutate); UI/Selenium suites (mutation is meaningless on click handlers).

**Snippet:**
```xml
<plugin>
  <groupId>org.pitest</groupId>
  <artifactId>pitest-maven</artifactId>
  <configuration>
    <mutationThreshold>70</mutationThreshold>
    <historyInputFile>target/pit-history.bin</historyInputFile>
    <historyOutputFile>target/pit-history.bin</historyOutputFile>
  </configuration>
</plugin>
```

---

## 15. `test-java-testcontainers-singleton` — singleton containers for JUnit 5

**Rule:** Use Testcontainers with JUnit 5 via a singleton pattern (`static` block + JVM-shutdown stop), NOT `@Testcontainers + @Container`. The annotation pair stops containers per-class causing "connection refused" cascades when sharing fixtures. AI agents copy-pasting tutorials almost always get this wrong — pin the rule in `CLAUDE.md`.

**Source:** <https://java.testcontainers.org/test_framework_integration/junit_5/> · <https://testcontainers.com/guides/testcontainers-container-lifecycle/>

**When to use:** Integration test suites with > 5 classes hitting the same DB/Kafka. ~10× faster than per-class containers.
**When NOT to use:** When tests must NOT share state (security boundary tests). Then accept the per-class cost.

**Snippet:**
```java
abstract class IntegrationTestBase {
    static final PostgreSQLContainer<?> PG = new PostgreSQLContainer<>("postgres:16-alpine")
        .withReuse(true);
    static { PG.start(); }
    @BeforeEach void clean() { jdbc.update("TRUNCATE accounts CASCADE"); }
}
```

---

## 16. `test-java-jqwik-property` — JQwik for property-based JUnit 5

**Rule:** Add JQwik alongside JUnit 5 for any pure-function module. `@Property` replaces hand-written corner-case tables with generators. Pair with PIT (rule 14) — properties kill mutants tables miss.

**Source:** <https://jqwik.net/> · <https://jqwik.net/docs/current/user-guide.html>

**When to use:** Validators, encoders, business invariants ("balance never negative"). AI is excellent at proposing properties from spec text.
**When NOT to use:** Side-effecty controllers; tests that need very specific seeded data — properties produce noise.

**Snippet:**
```java
@Property
boolean reverseTwiceEqualsOriginal(@ForAll String s) {
    return reverse(reverse(s)).equals(s);
}
```

---

## 17. `lint-kotlin-detekt-plus-ktlint-ksp` — detekt = bugs, ktlint = style, KSP = codegen

**Rule:** Every Kotlin module enables: detekt (200+ rules, bug/complexity/smell), ktlint via the detekt formatting plugin (style + import order), and KSP for any annotation processing (KAPT is deprecated). Three separate concerns, three tools, all wired into `./gradlew check`.

**Source:** <https://detekt.dev/> · <https://github.com/pinterest/ktlint> · <https://kotlinlang.org/docs/ksp-overview.html> · 2026 overview <https://blog.allegro.tech/2026/03/static-code-analysis-kotlin.html>

**When to use:** Every Kotlin module — JVM, Android, Multiplatform. AI agents that produce sloppy formatting trip ktlint instantly.
**When NOT to use:** Don't enable detekt + ktlint as TWO separate plugins — use detekt's ktlint wrapper to avoid double-fix loops.

**Snippet:**
```kotlin
// build.gradle.kts
detekt {
    config.setFrom("$rootDir/detekt.yml")
    buildUponDefaultConfig = true
    autoCorrect = true
}
dependencies { detektPlugins("io.gitlab.arturbosch.detekt:detekt-formatting:1.23.7") }
```

---

## 18. `test-kotlin-konsist-architecture` — Konsist for architecture as unit tests

**Rule:** Architecture rules (layering, naming, no-cycles, framework-leak prevention) are encoded as Kotest/JUnit tests using Konsist, NOT documented in a README. They run as part of `./gradlew test` and AI agents see violations as failing tests, not after-the-fact lint.

**Source:** <https://docs.konsist.lemonappdev.com/> · <https://github.com/LemonAppDev/konsist> · ArchUnit comparison <https://proandroiddev.com/archunit-vs-konsist-why-did-we-need-another-linter-972c4ff2622d>

**When to use:** Multi-module Kotlin projects, hexagonal/clean-arch codebases. Konsist understands Kotlin features (sealed, data, suspend) ArchUnit misses.
**When NOT to use:** Single-module libraries — overkill. Pure Java codebases — use ArchUnit instead, it's more mature for Java idioms.

**Snippet:**
```kotlin
@Test
fun `domain must not depend on infrastructure`() {
    Konsist.scopeFromModule("domain")
        .files
        .assertFalse { it.hasImport { i -> i.name.startsWith("com.me.infra") } }
}
```

---

## 19. `test-kotlin-kotest-mockk-relaxed` — Kotest spec + MockK with `clearMocks`

**Rule:** Use Kotest `BehaviorSpec`/`FunSpec` with MockK; reset mocks in `beforeTest { clearMocks(*mocks) }` (NOT in the constructor — that pattern silently shares state across tests). AI agents producing flaky `verify` failures are usually missing this hook.

**Source:** <https://kotest.io/docs/framework/integrations/mocking.html> · <https://mockk.io/>

**When to use:** Any Kotlin unit test with > 1 mocked dependency. `relaxed = true` for collaborators you don't care about; explicit mocks for the system-under-test contract.
**When NOT to use:** Don't relax mocks for the SUT's main collaborator — you'll miss missing-call assertions.

**Snippet:**
```kotlin
class OrderServiceTest : BehaviorSpec({
    val repo = mockk<OrderRepo>()
    val svc = OrderService(repo)
    beforeTest { clearMocks(repo) }
    Given("a paid order") {
        every { repo.save(any()) } returns Unit
        When("ship") { svc.ship(orderOf(paid = true)) }
        Then("repo saved once") { verify(exactly = 1) { repo.save(any()) } }
    }
})
```

---

## 20. `lang-jvm-jreleaser-one-tag-release` — JReleaser as the single release pipeline

**Rule:** Replace ad-hoc `mvn deploy`/`gradle publish` + manual changelog with `jreleaser.yml`. A git tag triggers one workflow that signs, uploads to Maven Central + GitHub Releases + Homebrew, and writes the changelog from conventional commits. AI agents never need to touch deploy YAML.

**Source:** <https://jreleaser.org/> · <https://github.com/jreleaser/jreleaser>

**When to use:** Libraries publishing to Maven Central, CLIs distributed via brew/scoop/sdkman. Works for non-JVM artifacts too (Go, Rust binaries) — useful for polyglot repos.
**When NOT to use:** Single-artifact internal libraries to a private registry — over-engineered. Use `mvn deploy` directly.

**Snippet:**
```yaml
# jreleaser.yml
project: { name: mylib, version: 1.4.0, license: Apache-2.0 }
release: { github: { owner: me, name: mylib } }
deploy:
  maven:
    mavenCentral:
      sonatype:
        active: ALWAYS
        url: https://central.sonatype.com/api/v1/publisher
```

---

## 21. `lint-ai-claude-md-language-floor` — `CLAUDE.md`/`AGENTS.md` encodes the deterministic floor

**Rule:** Every repo's root `AGENTS.md` (loaded by claude-code, OpenCode, Cursor via `agents.md` standard) MUST list the language's floor commands AI is required to run before producing any diff. For Go: `golangci-lint run --fix && go test ./...`. For Rust: `cargo clippy -- -D warnings && cargo nextest run`. For Java: `./gradlew check`. For Kotlin: `./gradlew detekt test`.

**Source:** <https://agents.md/> · claude-code memory docs <https://docs.anthropic.com/en/docs/claude-code/memory> · awesome-agent-skills <https://github.com/VoltAgent/awesome-agent-skills>

**When to use:** Every repo any AI agent touches. The agent runtime reads this file automatically — it's the cheapest way to enforce hygiene without per-prompt nagging.
**When NOT to use:** Don't list flaky/slow commands here (e.g., full mutation runs) — agents will skip them and learn to ignore the file.

**Snippet:**
```markdown
# AGENTS.md
## Pre-commit floor (MUST run before any diff)
- `golangci-lint run --fix`
- `gofumpt -l -w .`
- `go test ./... -race`
- `govulncheck ./...`
## Test floor
- New code requires table-driven tests + a row for the error path.
- Public parsers require a Fuzz_<Name> test with ≥ 3 seeds.
```

---

## Coverage map

| Category | Methodologies |
|----------|--------------|
| `lang-` | 6, 20 |
| `lint-` | 1, 2, 7, 12, 13, 17, 21 |
| `test-` | 4, 5, 9, 10, 14, 15, 16, 18, 19 |
| `sec-` | 3, 8, 11 |

21 methodologies across Go (6), Rust (5), Java (5), Kotlin (3), polyglot/AI (2). All have URLs, when-to/when-NOT, runnable snippet.

---

## Sources (consolidated)

- golangci-lint v2: <https://golangci-lint.run/docs/configuration/file/> · <https://ldez.github.io/blog/2025/03/23/golangci-lint-v2/>
- gofumpt: <https://github.com/mvdan/gofumpt>
- govulncheck: <https://go.dev/doc/security/vuln/>
- testify / mockery: <https://github.com/stretchr/testify> · <https://vektra.github.io/mockery/>
- Go fuzzing: <https://go.dev/doc/security/fuzz/>
- tygo: <https://github.com/gzuidhof/tygo>
- clippy: <https://doc.rust-lang.org/clippy/> · <https://effective-rust.com/clippy.html>
- cargo-deny: <https://embarkstudios.github.io/cargo-deny/>
- cargo-nextest: <https://nexte.st/>
- proptest: <https://github.com/proptest-rs/proptest>
- cargo-mutants: <https://mutants.rs/>
- Miri: <https://github.com/rust-lang/miri>
- Error Prone: <https://errorprone.info/bugpatterns>
- NullAway: <https://github.com/uber/NullAway>
- SpotBugs/PMD/Checkstyle: <https://spotbugs.github.io/> · <https://pmd.github.io/> · <https://checkstyle.sourceforge.io/>
- PIT: <https://pitest.org/>
- Testcontainers: <https://java.testcontainers.org/test_framework_integration/junit_5/>
- JQwik: <https://jqwik.net/>
- detekt: <https://detekt.dev/>
- ktlint: <https://github.com/pinterest/ktlint>
- KSP: <https://kotlinlang.org/docs/ksp-overview.html>
- Konsist: <https://docs.konsist.lemonappdev.com/>
- Kotest / MockK: <https://kotest.io/> · <https://mockk.io/>
- JReleaser: <https://jreleaser.org/>
- agents.md standard: <https://agents.md/>
