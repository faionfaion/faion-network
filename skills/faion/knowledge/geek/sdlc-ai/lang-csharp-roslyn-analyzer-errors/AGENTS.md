# C# Roslyn Analyzers as Compile Errors + Public API Lock

## Summary

For every recurring class of LLM-introduced bug in a .NET codebase (null deref, async-void, missing `ConfigureAwait`, accidental public-API break), enable the corresponding Roslyn analyzer with severity `error` in `.editorconfig` and ship `Microsoft.CodeAnalysis.PublicApiAnalyzers` against checked-in `PublicAPI.Shipped.txt` + `PublicAPI.Unshipped.txt` files. The build refuses to compile until each failure mode is fixed, so Copilot/Claude-Code edits cannot land code that violates a known-bad pattern. This is the Microsoft .NET team's stated 2026 pattern — make the failure structurally impossible, then let the agent continue.

## Why

Pure-LLM review hallucinates concerns; pure regex linters miss intent. Roslyn analyzers run inside the compiler with full type and flow information, so they reject exactly the syntactic shapes that produced past production incidents — not vague "best practices". When severity is `error`, the agent's tool-use loop sees a build failure, reads the diagnostic, and self-corrects; when it is `warning`, the agent learns to ignore it. PublicApiAnalyzers additionally pin the library's public surface: any agent-added `public` type or method that is not in `PublicAPI.Unshipped.txt` is a build error, preventing accidental SemVer-major breakage. Together they convert the most common LLM regressions in C# from "spotted in review" to "never typed".

## When To Use

- Production .NET libraries (NuGet packages, internal SDKs) where a SemVer-major break is expensive.
- .NET services with Copilot/Claude/Codex authoring code regularly.
- Codebases that have suffered repeated incidents from a single bug class (null deref, async-void, blocking `.Result`).
- Multi-target frameworks (`net8.0;net9.0`) where consistency under all TFMs matters.

## When NOT To Use

- Throwaway scripts, scratch console apps, sample/demo projects — bootstrap cost dominates.
- Internal apps with no public API surface — skip `PublicApiAnalyzers`, keep the bug-class analyzers.
- Greenfield prototypes still churning the API every day — pin the analyzer set after the first stable release.

## Content

| File | What's inside |
|------|---------------|
| `content/01-analyzer-as-error.xml` | `.editorconfig` severity escalation, bug-class lock-in, agent feedback loop. |
| `content/02-public-api-lock.xml` | PublicApiAnalyzers, Shipped/Unshipped files, breaking-change refusal. |

## Templates

| File | Purpose |
|------|---------|
| `templates/.editorconfig` | Severity escalation snippet for the canonical LLM bug classes. |
| `templates/Directory.Build.props` | MSBuild props enabling analyzers + public-API analyzer for every project. |
