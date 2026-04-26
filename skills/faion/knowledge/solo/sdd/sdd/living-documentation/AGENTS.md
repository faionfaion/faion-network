# Living Documentation

## Summary

Living Documentation (Docs-as-Code) treats documentation as a versioned artifact co-located with source code, auto-generated from code where possible, validated in CI, and never manually edited in the auto-generated sections. ADRs and design rationale remain hand-authored. API reference, changelogs, and link validity are automated. Every auto-generated section is tagged `<!-- AUTO-GENERATED -->` so agents and humans know not to overwrite it manually.

## Why

Static wikis become graveyards within months. Docs that live outside version control drift from the code they describe. Broken links and stale examples erode trust. The Docs-as-Code model applies the same review, CI, and versioning discipline to documentation that code already has — documentation failures block deploys the same as test failures.

## When To Use

- Setting up a new project's documentation pipeline: generator, CI pipeline, auto-generated API reference
- When documentation has drifted from code: regenerate API reference from OpenAPI spec
- When onboarding a new agent: living docs (especially llms.txt and structured README) reduce hallucination
- When deploying a developer portal that surfaces service ownership and runbooks

## When NOT To Use

- Internal ADRs and design rationale — must remain manually authored; auto-generated "why" is always wrong
- User-facing marketing copy — optimized for accuracy, not persuasion
- Projects to be archived within 3 months — infrastructure investment exceeds value
- Teams without code review discipline — Docs-as-Code requires the same PR review rigor as code PRs

## Content

| File | What's inside |
|------|---------------|
| `content/01-principles.xml` | Core Docs-as-Code rules: co-location, CI integration, auto-generation boundaries |
| `content/02-toolchain.xml` | Generator selection, linting tools (Vale, Spectral, linkinator), CI pipeline steps |

## Templates

| File | Purpose |
|------|---------|
| `templates/docs-ci.yaml` | GitHub Actions workflow: lint, link check, API spec validate, build, deploy |
| `templates/mkdocs.yml` | MkDocs Material theme configuration for technical docs |
