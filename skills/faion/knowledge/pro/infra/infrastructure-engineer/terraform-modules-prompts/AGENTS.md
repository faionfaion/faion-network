---
slug: terraform-modules-prompts
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A complete set of prompt templates for AI-assisted Terraform module development.
content_id: "b01288160fcf6ed6"
tags: [terraform, modules, prompts, llm, iac]
---
# Terraform Module LLM Prompt Library

## Summary

**One-sentence:** A complete set of prompt templates for AI-assisted Terraform module development.

**One-paragraph:** A complete set of prompt templates for AI-assisted Terraform module development. Covers the full module lifecycle: generation, review (security, best practices, performance), refactoring, testing, documentation, troubleshooting, migration, composition design, and cost optimization. Each prompt follows the fill-in-the-blank pattern with clear sections for context injection.

## Applies If (ALL must hold)

- Generating a new Terraform module for a resource type you have not written before.
- Reviewing an existing module for security, best practices, or performance issues.
- Refactoring a large or poorly structured module.
- Generating terraform test or Terratest test files for an existing module.
- Troubleshooting a Terraform error message or state issue.
- Migrating from inline resources to a module, or between module versions.
- Designing a module architecture for a new infrastructure component.
- Analyzing cost implications of a module's default configuration.

## Skip If (ANY kills it)

- When you already know the exact module code — writing it directly is faster than prompt-engineering for known patterns.
- For highly organization-specific compliance requirements — prompts produce generic best practices; layer your org-specific rules on top.

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

- parent skill: `pro/infra/infrastructure-engineer/`
