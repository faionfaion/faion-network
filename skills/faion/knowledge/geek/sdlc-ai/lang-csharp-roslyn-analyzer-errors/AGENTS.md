---
slug: lang-csharp-roslyn-analyzer-errors
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: For every recurring class of LLM-introduced bug in a.
content_id: "8fbce158ab3fd37f"
tags: [csharp, roslyn, analyzer, dotnet, public-api]
---
# C# Roslyn Analyzers as Compile Errors + Public API Lock

## Summary

**One-sentence:** For every recurring class of LLM-introduced bug in a.

**One-paragraph:** For every recurring class of LLM-introduced bug in a .NET codebase (null deref, async-void, missing ConfigureAwait, accidental public-API break), enable the corresponding Roslyn analyzer with severity error in .editorconfig and ship Microsoft.CodeAnalysis.PublicApiAnalyzers against checked-in PublicAPI.Shipped.txt + PublicAPI.Unshipped.txt files. The build refuses to compile until each failure mode is fixed, so Copilot/Claude-Code edits cannot land code that violates a known-bad pattern.

## Applies If (ALL must hold)

- Production .NET libraries (NuGet packages, internal SDKs) where a SemVer-major break is expensive.
- .NET services with Copilot/Claude/Codex authoring code regularly.
- Codebases that have suffered repeated incidents from a single bug class (null deref, async-void, blocking .Result).
- Multi-target frameworks (net8.0;net9.0) where consistency under all TFMs matters.

## Skip If (ANY kills it)

- Throwaway scripts, scratch console apps, sample/demo projects — bootstrap cost dominates.
- Internal apps with no public API surface — skip PublicApiAnalyzers, keep the bug-class analyzers.
- Greenfield prototypes still churning the API every day — pin the analyzer set after the first stable release.

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
