# Code Decomposition Patterns

## Summary

A catalog of five named decomposition patterns — Extract Service, Extract Component, Extract Module, Extract Configuration, Extract Types — with before/after templates and language-specific layouts for Python/Django, TypeScript/React, and Go. Each pattern has concrete size triggers and acceptance criteria that make application verifiable.

## Why

Fat files (controllers >100 lines, React components >150 lines, settings >150 lines) reduce testability, increase merge conflicts, and obscure responsibility. Named patterns give agents and reviewers a shared vocabulary and precise post-conditions: view files stay thin, services are framework-free, components compose, config splits by environment.

## When To Use

- Controller/view exceeds 100 lines with mixed HTTP handling and business logic → Extract Service.
- React/Vue component exceeds 150 lines with multiple UI concerns → Extract Component.
- Flat directory exceeds 20 files or team ownership is unclear → Extract Module.
- Settings file exceeds 150 lines or mixes environment-specific config → Extract Configuration.
- TypeScript files mix types with logic or types are reused across multiple files → Extract Types.
- New feature scaffolding where the agent must lay out files before writing code.

## When NOT To Use

- Features totalling ≤200 lines — applying a pattern creates more files than logic.
- Framework-mandated single files (e.g., Django `urls.py`) — forced coupling is not a decomposition target.
- Generated code or ORM migrations — structural changes break the generator contract.
- Performance-critical hot loops where indirection has a measured cost.

## Content

| File | What's inside |
|------|---------------|
| `content/01-patterns.xml` | Five named patterns with triggers, benefits, and size invariants. |
| `content/02-language-layouts.xml` | Directory tree templates for Python/Django, TypeScript/React, and Go. |
| `content/03-examples.xml` | Before/after code examples for Extract Service and Extract Component. |
| `content/04-antipatterns.xml` | Leaky services, over-extraction, import-update misses, barrel re-export sprawl. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pattern-guard.sh` | CI script enforcing line-count invariants and detecting circular imports. |
