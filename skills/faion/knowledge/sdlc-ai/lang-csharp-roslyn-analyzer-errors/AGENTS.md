# C# Roslyn Analyzers as Compile Errors + Public API Lock

## Summary

**One-sentence:** Escalate Roslyn analyzer warnings (nullable refs, ConfigureAwait, async-void, CancellationToken) to errors and lock the public API via Microsoft.CodeAnalysis.PublicApiAnalyzers — both gates on every PR for .NET repos.

**One-paragraph:** C# Roslyn Analyzers as Compile Errors + Public API Lock produces a config artefact for the sdlc-ai domain. It pins observable preconditions, scores candidate decisions against ≥5 testable rules, fails fast on disqualifiers, and emits a schema-validated output. The methodology routes between apply and skip-this-methodology via an explicit decision tree so downstream agents never run it on an unsuitable input.

**Ефективно для:**

- Any .NET repo where AI agents are allowed to author code.
- Libraries / NuGet packages where accidental public API drift breaks consumers.
- Async-heavy services with prior production deadlocks or missing CancellationToken.
- Codebase migrating to nullable reference types.

## Applies If (ALL must hold)

- .NET 6+ / SDK-style csproj available.
- Repo can adopt TreatWarningsAsErrors=true in Release.
- CI pipeline can run dotnet build with strict analyzer config.
- Team accepts public-API additions go through PublicAPI.Unshipped.txt edits.

## Skip If (ANY kills it)

- Legacy .NET Framework < 4.7.2 — analyzer support patchy.
- Code generators dominate (e.g. ServiceModel) — false-positive flood.
- Repo is throwaway / spike — gate cost outweighs value.
- Team refuses TreatWarningsAsErrors — partial adoption is worse than none.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| .editorconfig | top-level file | repo lead |
| Directory.Build.props | central MSBuild props | platform |
| CI build step | dotnet build Release | ci-eng |
| PublicAPI baseline | ShippedAPI.txt for each lib | lib owner |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[lint-precommit-floor]] | Hook framework carries the local build check |

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
| `analyzer_id_pick` | sonnet | Choose which IDs to escalate. |
| `public_api_baseline` | haiku | Generate ShippedAPI.txt baselines. |
| `ci_gate_wire_up` | sonnet | Integrate dotnet build into CI. |

## Templates

| File | Purpose |
|------|---------|
| `templates/editorconfig.editorconfig` | Top-level .editorconfig with analyzer escalations. |
| `templates/Directory.Build.props` | Central MSBuild config. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-lang-csharp-roslyn-analyzer-errors.py` | Validate the analyzer-config artefact. | pre-merge of analyzer config |

## Related

- [[lint-precommit-floor]]
- [[mr-codemod-refactor-agent]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (precondition flag, repo metric, capability flag) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on a rule that triggers the procedure or on `skip-this-methodology`.
