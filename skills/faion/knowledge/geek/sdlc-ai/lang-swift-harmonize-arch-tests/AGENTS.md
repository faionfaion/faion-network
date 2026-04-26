# Swift Architecture as Tests via Harmonize + Swift Testing

## Summary

Encode Swift architecture rules (layer boundaries, no-import constraints, naming, protocol conformance) as actual `@Test`/`#expect` cases using Harmonize on top of SwiftSyntax, run alongside the rest of the suite via `swift test` / Xcode CI. Pair with `swift-format`, SwiftLint, and Swift Testing's interop with XCTest (ST-0021, accepted Mar 2026) so an agent's structurally wrong PR fails CI with a readable test name like `ViewModels_must_not_import_UIKit_failed`. Architecture-as-tests beats architecture-as-README because the agent's tool-use loop only reacts to executable failures — Harmonize gives Swift the equivalent of ArchUnit (Java) or Konsist (Kotlin), rules expressed as code that fails CI, not as prose that drifts. Xcode 26.3's agentic coding mode reads these signals natively.

## Why

SwiftLint is regex-based; `swift-format` only reshapes layout. Neither understands architectural intent like "ViewModels must not import UIKit", "Services must implement `Sendable`", or "Domain types must not depend on Network module". Harmonize parses the project with SwiftSyntax and exposes the AST as a query API; rules become test bodies. With Swift Testing now interoperating with XCTest under ST-0021, the architecture suite runs alongside unit tests in a single command (`swift test` or `xcodebuild test`). When an LLM agent generates a SwiftUI view that imports the wrong layer, the failing test name and location ride back through the agent's harness — the deterministic refusal channel Apple's agentic-coding write-up assumes.

## When To Use

- Multi-target Swift projects (SPM packages, Xcode workspaces with multiple frameworks).
- iOS apps following Clean / hexagonal / TCA architecture where layer leaks are the dominant regression class.
- Codebases where AI agents commit production code (Xcode 26.3 agentic mode, Cursor-Swift, Claude Code via SwiftAgents).
- Greenfield Swift packages where pinning architecture early prevents drift cheaply.

## When NOT To Use

- Single-file SwiftUI playgrounds or tutorials.
- Apps with one module and no internal layering — Harmonize adds overhead without preventing anything.
- Pre-Swift-5.9 codebases where SwiftSyntax's stable macros / parser contract is missing.

## Content

| File | What's inside |
|------|---------------|
| `content/01-harmonize-arch-rules.xml` | Architecture rules as `@Test` cases, scope/predicate API, layered package examples. |
| `content/02-swift-testing-floor.xml` | swift-format + SwiftLint + Swift Testing + XCTest interop wiring (ST-0021). |

## Templates

| File | Purpose |
|------|---------|
| `templates/Package.swift` | SPM package adding Harmonize and Swift Testing as test deps. |
| `templates/.swiftformat` | swift-format config used by the deterministic floor. |
