---
slug: fitness-functions-as-code
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
content_id: "a4033100917076ae"
summary: "Encode architecture rules (layering, dependency direction, package boundaries, performance budgets, license constraints) as runnable tests in the SDLC: ArchUnit / dependency-cruiser / ts-arch run on every PR so quarterly review and drift detection have hard signals instead of opinion."
tags: [geek, sdlc-ai, architecture, fitness-functions, archunit, dependency-cruiser, drift]
---
# Fitness Functions as Code

## Summary

The geek/sdlc-ai group's quarterly architecture review and drift detection both fail without machine-readable architecture rules: code reviewers cannot remember layering and dependency-direction invariants across a quarter, and AI agents have no signal to flag a violation in a generated PR. This methodology encodes those invariants as runnable tests — ArchUnit for JVM, ts-arch / dependency-cruiser for TypeScript, import-linter for Python, depgraph for Go, plus performance-budget assertions and license/SPDX checks — committed to the repo and executed on every PR. Quarterly review becomes a diff of green-bar invariants over time, not an archaeology dig.

## Applies If

- The system has more than one layered module or package boundary that an AI-generated PR could accidentally cross.
- Architecture decisions (allowed dependencies, hot-path budgets, license allow-list) are written down somewhere and could in principle be expressed as predicates.
- CI runs on every PR and can be extended with a new test stage.
- The team is doing quarterly architecture review or formal drift detection as a process.

## Skip If

- The codebase is a single flat package with no layering — there are no architectural invariants to encode.
- Architecture is purely verbal and not yet written anywhere — encode it as prose first, then return.
- The PR throughput is low enough that human reviewers comfortably cover the same checks (very small teams, very slow change rate).

## Content

| File | Depth | What's inside |
|------|-------|---------------|
| `content/01-core-rules.xml` | essential | Five testable rules covering test-as-code framework choice, layering predicates, performance budgets, license invariants, and the quarterly-review feedback loop |

## Related

- parent skill: `geek/sdlc-ai/`
- triggering activity: `Architecture-as-code repository — continuous maintenance with monthly review`, `Quarterly architecture review cycle`
- neighbouring: `geek/sdlc-ai/kb-adr-decay-detector-agent`, `geek/sdlc-ai/lang-csharp-roslyn-analyzer-errors`, `geek/sdlc-ai/test-property-based-llm-invariants`
