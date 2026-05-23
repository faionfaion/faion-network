# Jenkins Pipeline Patterns

## Summary

**One-sentence:** Generates production-grade Declarative Jenkinsfiles + version-pinned Shared Libraries + isolated parallel stages + K8s pod templates for brownfield orgs.

**One-paragraph:** Advanced Jenkins pipeline patterns for production-grade Declarative pipelines, Shared Libraries, scripted escapes, and reusable components across an organization. Covers Declarative-by-default with Scripted only inside `script { }`, Shared Library directory structure + CPS serialization rules, parallel stages with workspace isolation + lock(), Kubernetes pod templates with explicit resource requests/limits, and full pipeline options for timeout + buildDiscarder + concurrent-builds policy. Aimed at brownfield orgs with 50+ pipelines where standardisation matters more than raw speed.

**Ефективно для:**

- 50+ pipelines в одній організації, потребують shared library з єдиним стандартом.
- CPS-сериалізація: уникнути `NotSerializableException` на годинах робіт через `@NonCPS`.
- Parallel matrix builds (cross-OS / cross-JDK / cross-Node) з resource-aware агентами.
- Kubernetes pod templates з explicit requests/limits та dedicated service accounts.
- Migration: монолітні Jenkinsfile → модулярні `vars/`-функції з pinned `@Library('lib@v1.2.3')`.

## Applies If (ALL must hold)

- Brownfield organization running a Jenkins controller (LTS) with no migration off Jenkins on the roadmap.
- You need a Groovy Shared Library to enforce conventions across 50+ pipelines.
- Matrix or fan-out builds across multiple OS / JDK / Node axes.
- Heavy on-prem / air-gapped scenarios with Vault or Artifactory integration.
- Existing investment in Jenkinsfile + plugin ecosystem + team Groovy familiarity.

## Skip If (ANY kills it)

- Greenfield repo on GitHub or GitLab — use native CI; Jenkins adds operator burden with no upside.
- Solo dev or small team — controller maintenance outweighs benefits.
- Workloads that fit cleanly into GitHub Actions reusable workflows or composite actions.
- Ephemeral / serverless CI requirements — Jenkins is stateful and assumes a long-lived controller.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Existing Jenkinsfile or pipeline spec | Groovy / Markdown | repo / team |
| Shared Library repo URL | git URL | platform team |
| Library version tag | semver tag | release manager |
| Agent strategy | label / docker / kubernetes | infra |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[jenkins-basics]] | Declarative + JCasC + zero-controller-executors fundamentals. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: declarative-with-script-escape, shared-lib-dedicated-repo, library-version-pinned, parallel-workspace-isolation, pod-resources-required, options-required | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema for code + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `select-pattern` | sonnet | Decision among shared-lib / parallel / matrix variants. |
| `write-shared-lib-var` | opus | CPS serialization + Groovy idiom judgement. |
| `lint-cps-issues` | haiku | Mechanical regex audit for `Pattern.compile`, `each {}`, `@NonCPS`. |

## Templates

| File | Purpose |
|------|---------|
| `templates/Jenkinsfile.declarative` | Declarative pipeline with parallel stages + options + post handlers |
| `templates/shared-library-var.groovy` | `vars/buildApp.groovy` skeleton enforcing CPS-safe patterns |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-jenkins-pipeline-patterns.py` | Validate the pipeline-pattern artefact JSON against 02-output-contract schema | CI on each artefact change; pre-commit |

## Related

- [[jenkins-basics]]
- [[github-actions-basics]]
- [[gitlab-cicd]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (pipeline count, library presence, parallelism need, agent type) to a concrete pattern variant, each leaf referencing a rule from `01-core-rules.xml`.
