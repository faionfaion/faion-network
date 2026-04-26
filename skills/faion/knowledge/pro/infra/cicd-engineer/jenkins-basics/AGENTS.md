# Jenkins Basics

## Summary

Jenkins is an open-source automation server with Groovy-based Declarative (recommended) and Scripted pipeline syntax defined in Jenkinsfiles. Use Declarative pipelines for all new pipelines — they support restart-from-stage and syntax validation at load time. Use Shared Libraries to share pipeline code across projects. Use the Kubernetes agent for dynamic build agents — never run builds on the controller node.

## Why

Jenkins excels in enterprise environments with complex, multi-step builds, legacy integrations, or strict on-premises security requirements. Its plugin ecosystem (1800+ plugins) covers virtually every integration need. Configuration as Code (JCasC) plugin enables reproducible Jenkins setups — critical for disaster recovery and multi-instance rollouts.

## When To Use

- Enterprise environments with existing Jenkins infrastructure and established pipelines
- On-premises deployments with strict network isolation or compliance requirements
- Pipelines requiring heavy customization via plugins not available in GitLab CI or GitHub Actions
- Multi-branch projects with complex branching strategies (Organization Folder + Multibranch Pipeline)

## When NOT To Use

- New projects on GitHub — GitHub Actions is simpler and has zero infrastructure cost
- New projects on GitLab — GitLab CI is integrated and eliminates a separate server
- Small teams or solo projects — Jenkins administration overhead is not justified
- Projects that need serverless/ephemeral CI — prefer cloud-native CI tools

## Content

| File | What's inside |
|------|---------------|
| `content/01-concepts.xml` | Pipeline types comparison, agent types, plugin selection rules, JCasC requirement |
| `content/02-pipeline-rules.xml` | Declarative syntax rules, Shared Library structure, parallel stage patterns, credentials binding |
| `content/03-examples.xml` | Declarative pipeline skeleton, Kubernetes agent example, Shared Library call, parallel test execution |

## Templates

| File | Purpose |
|------|---------|
| `templates/Jenkinsfile` | Declarative pipeline template with build/test/deploy stages and post-actions |
| `templates/kubernetes-agent.groovy` | Kubernetes pod template for dynamic Jenkins agents |
