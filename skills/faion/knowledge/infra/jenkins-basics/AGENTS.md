# Jenkins Basics

## Summary

**One-sentence:** Generates a Declarative Jenkinsfile + JCasC YAML with K8s/Docker agents, zero-executor controller, pinned plugins, withCredentials secrets, and post cleanup.

**One-paragraph:** Jenkins is an open-source automation server with Groovy-based Declarative (recommended) and Scripted pipeline syntax defined in Jenkinsfiles. Use Declarative pipelines for all new pipelines — they support restart-from-stage and syntax validation at load time. Use Shared Libraries to share pipeline code across projects. Use the Kubernetes agent for dynamic build agents — never run builds on the controller node. Manage controller configuration via the JCasC plugin from a YAML file in source control.

**Ефективно для:**

- Brownfield enterprise з існуючою Jenkins-інфраструктурою + plugin-екосистемою.
- On-prem або air-gapped CI з суворими compliance + network isolation вимогами.
- Multibranch / Organization Folder для багатобренчевих репозиторіїв.
- Migration: ad-hoc Jenkins config UI → reproducible JCasC YAML + plugins.txt.
- Dynamic K8s агенти замість long-lived VMs (scale-to-zero, ізольоване середовище build).

## Applies If (ALL must hold)

- Enterprise environments with existing Jenkins infrastructure and established pipelines.
- On-premises deployments with strict network isolation or compliance requirements.
- Pipelines requiring heavy customization via plugins not available in GitLab CI or GitHub Actions.
- Multi-branch projects with complex branching strategies (Organization Folder + Multibranch Pipeline).

## Skip If (ANY kills it)

- New projects on GitHub — GitHub Actions is simpler and has zero infrastructure cost.
- New projects on GitLab — GitLab CI is integrated and eliminates a separate server.
- Small teams or solo projects — Jenkins administration overhead is not justified.
- Projects that need serverless / ephemeral CI — prefer cloud-native CI tools.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Repository tree | filesystem path | git repo |
| Build language + toolchain | name + version | project README / package manifest |
| Deploy target | env name + branch mapping | release plan |
| Secrets inventory | list of credentialsId | Jenkins Credentials store |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[github-actions-basics]] | Comparator surface; decide whether Jenkins is even the right tool. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: declarative-default, zero-controller-executors, jcasc-config, withCredentials-only, options-timeout-buildDiscarder, kubernetes-agent | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for code + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `select-agent-type` | sonnet | Light decision: K8s vs Docker vs label-based. |
| `write-jenkinsfile` | sonnet | Structured Declarative authoring. |
| `lint-jenkinsfile` | haiku | Mechanical pipeline-linter REST call. |

## Templates

| File | Purpose |
|------|---------|
| `templates/Jenkinsfile` | Declarative pipeline skeleton with build/test/deploy + post-actions |
| `templates/kubernetes-agent.groovy` | Kubernetes pod template for dynamic Jenkins agents |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-jenkins-basics.py` | Validate the Jenkinsfile artefact JSON against 02-output-contract schema | CI on each artefact change; pre-commit |

## Related

- [[jenkins-pipeline-patterns]]
- [[github-actions-basics]]
- [[gitlab-cicd]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (project host, infra ownership, build complexity, agent strategy) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the Jenkins methodology to apply.
