---
slug: lang-swift-harmonize-arch-tests
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Encode Swift architecture rules (layer boundaries, no-import constraints, naming, protocol conformance) as actual @Test/#expect cases using Harmonize on top of SwiftSyntax, run alongside the rest of the suite via swift test / Xcode CI.
content_id: "bd3e4747dd747dbe"
tags: [swift, harmonize, architecture-tests, swift-testing, swiftlint]
---
# Swift Architecture as Tests via Harmonize + Swift Testing

## Summary

**One-sentence:** Encode Swift architecture rules (layer boundaries, no-import constraints, naming, protocol conformance) as actual @Test/#expect cases using Harmonize on top of SwiftSyntax, run alongside the rest of the suite via swift test / Xcode CI.

**One-paragraph:** Encode Swift architecture rules (layer boundaries, no-import constraints, naming, protocol conformance) as actual @Test/#expect cases using Harmonize on top of SwiftSyntax, run alongside the rest of the suite via swift test / Xcode CI. Pair with swift-format, SwiftLint, and Swift Testing's interop with XCTest (ST-0021, accepted Mar 2026) so an agent's structurally wrong PR fails CI with a readable test name like ViewModels_must_not_import_UIKit_failed.

## Applies If (ALL must hold)

- Multi-target Swift projects (SPM packages, Xcode workspaces with multiple frameworks).
- iOS apps following Clean / hexagonal / TCA architecture where layer leaks are the dominant regression class.
- Codebases where AI agents commit production code (Xcode 26.3 agentic mode, Cursor-Swift, Claude Code via SwiftAgents).
- Greenfield Swift packages where pinning architecture early prevents drift cheaply.

## Skip If (ANY kills it)

- Single-file SwiftUI playgrounds or tutorials.
- Apps with one module and no internal layering — Harmonize adds overhead without preventing anything.
- Pre-Swift-5.9 codebases where SwiftSyntax's stable macros / parser contract is missing.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `geek/sdlc-ai/sdlc-ai/`
