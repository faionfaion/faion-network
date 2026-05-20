---
slug: jenkins-pipeline-patterns
tier: pro
group: infra
domain: cicd-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Advanced Jenkins pipeline patterns for production-grade declarative pipelines, shared libraries, scripted pipelines, and reusable components throughout organizations.
content_id: "6ce6b4e84a490913"
tags: [jenkins, pipeline, cicd, groovy, shared-libraries]
---
# Jenkins Pipeline Patterns

## Summary

**One-sentence:** Advanced Jenkins pipeline patterns for production-grade declarative pipelines, shared libraries, scripted pipelines, and reusable components throughout organizations.

**One-paragraph:** Advanced Jenkins pipeline patterns for production-grade declarative pipelines, shared libraries, scripted pipelines, and reusable components throughout organizations. This guide covers best practices for 2025-2026, including proper separation between declarative (structured, team-maintainable) and scripted (complex, flexible Groovy) approaches, shared library directory structure and Groovy serialization rules for CPS safety, parallel stages with resource management and workspace isolation, Kubernetes pod templates for dynamic provisioning, and agentic workflow for autonomous pipeline authoring with validation checkpoints.

## Applies If (ALL must hold)

- Brownfield organization running Jenkins controller (LTS) where migration to GitHub Actions or GitLab CI is not on the roadmap.
- You need a Groovy shared library to enforce conventions across 50+ pipelines (build/test/deploy/notify steps).
- Matrix or fan-out builds across multiple JDK, Node, or OS axes that GitHub Actions matrices cannot express cheaply.
- Heavy on-prem, air-gapped scenarios with self-hosted agents and tight Vault or Artifactory integration.
- Existing investment in Jenkinsfile, plugin ecosystem (Blue Ocean, Configuration as Code, Job DSL), and team familiarity with Groovy.

## Skip If (ANY kills it)

- Greenfield repo on GitHub or GitLab — use native CI; Jenkins adds operator burden with no upside. GitHub Actions is simpler to set up and requires no infrastructure.
- Solo dev or small team — Jenkins controller maintenance (plugin upgrades, JVM tuning, agent provisioning) outweighs benefits. GitHub Actions is serverless.
- Workloads that fit cleanly into GitHub Actions reusable workflows or composite actions. Most modern pipelines do.
- Ephemeral or serverless CI requirements — Jenkins is stateful and assumes long-lived controllers. Lambda-based CI is incompatible with Jenkins architecture.

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

- parent skill: `pro/infra/cicd-engineer/`
