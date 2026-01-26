---
id: jenkins-basics
name: "Jenkins Basics"
domain: OPS
skill: faion-devops-engineer
category: "devops"
version: "2.0"
updated: "2026-01"
---

# Jenkins Basics

## Overview

Jenkins is an open-source automation server for building CI/CD pipelines. It uses Groovy-based Declarative or Scripted Pipeline syntax defined in Jenkinsfiles, supporting complex workflows, distributed builds, and extensive plugin ecosystem.

## When to Use

| Scenario | Recommendation |
|----------|----------------|
| Enterprise environments with existing Jenkins infrastructure | Recommended |
| Complex build requirements needing extensive customization | Recommended |
| On-premises deployments with strict security requirements | Recommended |
| Multi-branch projects with complex branching strategies | Recommended |
| Pipelines requiring custom plugins or integrations | Recommended |
| Simple projects, small teams | Consider GitHub Actions/GitLab CI instead |

## Key Concepts

| Concept | Description |
|---------|-------------|
| Pipeline | Automated workflow defined in Jenkinsfile |
| Stage | Logical division of pipeline (Build, Test, Deploy) |
| Step | Single task within a stage |
| Agent | Executor running pipeline (controller, node, docker, kubernetes) |
| Declarative | Structured pipeline syntax with predefined sections |
| Scripted | Flexible Groovy-based pipeline syntax |
| Shared Library | Reusable pipeline code across projects |
| Blue Ocean | Modern pipeline visualization UI |
| Multibranch Pipeline | Auto-discovery of branches and PRs |
| Organization Folder | Auto-discovery of repositories |

## Pipeline Types Comparison

| Feature | Declarative | Scripted |
|---------|-------------|----------|
| Syntax | Structured, predefined | Flexible Groovy |
| Error handling | Built-in post sections | try-catch blocks |
| Readability | Easier for beginners | More complex |
| Flexibility | Limited | Full Groovy power |
| Validation | Syntax validation at load | Runtime only |
| Restart from stage | Supported | Not supported |
| Recommended for | Most use cases | Complex logic only |

## Agent Types

| Agent Type | Use Case | Example |
|------------|----------|---------|
| `any` | Run on any available agent | `agent any` |
| `none` | No global agent, specify per stage | `agent none` |
| `label` | Run on agent with specific label | `agent { label 'linux' }` |
| `docker` | Run inside Docker container | `agent { docker 'node:20' }` |
| `dockerfile` | Build and run from Dockerfile | `agent { dockerfile true }` |
| `kubernetes` | Run as Kubernetes pod | `agent { kubernetes { ... } }` |

## Essential Plugins (2025-2026)

| Plugin | Purpose |
|--------|---------|
| Pipeline | Core pipeline functionality |
| Blue Ocean | Modern UI for pipeline visualization |
| Kubernetes | Dynamic agents in K8s clusters |
| Docker Pipeline | Docker integration in pipelines |
| Git | Git SCM integration |
| GitHub Branch Source | GitHub multi-branch support |
| Credentials Binding | Secure credential access |
| Throttle Concurrent Builds | Limit concurrent jobs |
| Pipeline Utility Steps | File operations, JSON/YAML parsing |
| Slack Notification | Slack integration |
| Prometheus Metrics | Metrics export for monitoring |
| Configuration as Code (JCasC) | Jenkins configuration in YAML |
| OWASP Dependency-Check | Security vulnerability scanning |
| SonarQube Scanner | Code quality analysis |

## Folder Structure

```
jenkins-basics/
├── README.md           # This file - overview and concepts
├── checklist.md        # Implementation checklist
├── examples.md         # Code examples and patterns
├── templates.md        # Ready-to-use templates
└── llm-prompts.md      # Prompts for AI-assisted development
```

## Related Resources

- [checklist.md](checklist.md) - Implementation checklist
- [examples.md](examples.md) - Code examples
- [templates.md](templates.md) - Ready-to-use templates
- [llm-prompts.md](llm-prompts.md) - AI prompts

## Sources

- [Jenkins Pipeline Documentation](https://www.jenkins.io/doc/book/pipeline/)
- [Pipeline Best Practices](https://www.jenkins.io/doc/book/pipeline/pipeline-best-practices/)
- [Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [Using a Jenkinsfile](https://www.jenkins.io/doc/book/pipeline/jenkinsfile/)
- [Shared Libraries](https://www.jenkins.io/doc/book/pipeline/shared-libraries/)
- [Blue Ocean](https://www.jenkins.io/doc/book/blueocean/)
- [Jenkins Best Practices](https://www.jenkins.io/doc/book/using/best-practices/)
- [CloudBees Best Practices for Jenkins Pipeline](https://www.cloudbees.com/blog/best-practices-for-jenkins-pipeline)
- [BrowserStack Jenkins Best Practices 2025](https://www.browserstack.com/guide/jenkins-best-practices-every-developer-must-know)
- [LambdaTest Jenkins Best Practices](https://www.lambdatest.com/blog/jenkins-best-practices/)
