# Swift Architecture as Tests via Harmonize + Swift Testing

## Summary

**One-sentence:** Encode Swift architecture rules (layer boundaries, no-import constraints, naming, protocol conformance) as @Test/#expect cases using Harmonize on SwiftSyntax — run alongside the rest of the suite in CI.

**One-paragraph:** Swift Architecture as Tests via Harmonize + Swift Testing produces a config artefact for the sdlc-ai domain. It pins observable preconditions, scores candidate decisions against ≥5 testable rules, fails fast on disqualifiers, and emits a schema-validated output. The methodology routes between apply and skip-this-methodology via an explicit decision tree so downstream agents never run it on an unsuitable input.

**Ефективно для:**

- Swift app where layer / module boundaries keep eroding.
- Team adopting Swift Testing and wanting arch rules as first-class tests.
- iOS / macOS / server-side Swift codebase ≥ 30 KLOC.
- Pair with SwiftLint for surface style and Harmonize for structural rules.

## Applies If (ALL must hold)

- Swift 5.9+ with Swift Testing available.
- SwiftPM or Xcode project can pull in Harmonize.
- CI runs `swift test` / Xcode test plan.
- Team agrees on layer rules to encode.

## Skip If (ANY kills it)

- Swift < 5.9 — Swift Testing unavailable.
- Project too small to benefit from arch tests.
- Team uses ArchUnit-like tool already.
- Arch rules are aspirational, not enforced — tests will be skipped.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Package.swift / Xcode project | test target available | iOS lead |
| Harmonize dep | Swift package | platform |
| Arch rule list | 1-paragraph rules per layer | architect |
| CI gate | `swift test` in matrix | ci-eng |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[lint-precommit-floor]] | Hook framework can run swift test on staged files |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip-rule + rationale + source | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | 800 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns (symptom/root-cause/fix) | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with decision gates | 700 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion ref=rule-id | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `arch_rule_capture` | sonnet | Convert prose rules to Harmonize. |
| `test_target_wire_up` | haiku | Add test target dependency. |
| `ci_gate_wire` | haiku | Add `swift test` step. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ArchTests.swift` | Sample Harmonize arch test file. |
| `templates/Package.swift.fragment` | Harmonize SPM dependency fragment. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-swift-harmonize-arch-tests.py` | Validate the arch-test-config artefact. | pre-merge of arch config |

## Related

- [[lint-precommit-floor]]
- [[mr-graph-vs-diff-reviewer]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (precondition flag, repo metric, capability flag) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on a rule that triggers the procedure or on `skip-this-methodology`.
