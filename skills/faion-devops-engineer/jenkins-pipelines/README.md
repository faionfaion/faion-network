# Jenkins Pipelines

Advanced Jenkins pipeline patterns for production CI/CD workflows.

## Overview

This module covers declarative pipelines, shared libraries, Blue Ocean, and modern Jenkins practices for 2025-2026.

## Contents

| File | Description |
|------|-------------|
| [checklist.md](checklist.md) | Pre-flight checklist for pipeline implementation |
| [examples.md](examples.md) | Production-grade pipeline examples |
| [templates.md](templates.md) | Reusable pipeline templates |
| [llm-prompts.md](llm-prompts.md) | LLM prompts for pipeline generation |

## Key Concepts

### Declarative vs Scripted

| Aspect | Declarative | Scripted |
|--------|-------------|----------|
| Syntax | Structured, readable | Flexible, Groovy-based |
| Use case | Standard pipelines (default) | Complex logic |
| Maintainability | High | Medium |
| Learning curve | Low | High |

**Recommendation:** Use declarative pipelines by default. Switch to scripted only for complex dynamic logic.

### Shared Libraries

Centralize reusable pipeline code:

```
jenkins-shared-library/
├── vars/                    # Global functions (preferred)
│   ├── buildApp.groovy
│   ├── deployToK8s.groovy
│   └── notifySlack.groovy
├── src/com/example/         # Classes (complex logic)
│   ├── Docker.groovy
│   └── Kubernetes.groovy
└── resources/               # Static files
    └── templates/
```

**Best practice:** Define functions in `vars/` for declarative pipeline compatibility.

### Blue Ocean

Modern UI for Jenkins pipelines:

- Visual pipeline editor
- Stage visualization
- Parallel branch display
- Intuitive log navigation
- Automatic Jenkinsfile creation

**When to use:** Dev-heavy projects, teams new to Jenkins.

## Quick Reference

### Pipeline Structure

```groovy
pipeline {
    agent { ... }
    environment { ... }
    options { ... }
    stages {
        stage('Build') { steps { ... } }
        stage('Test') { steps { ... } }
        stage('Deploy') { steps { ... } }
    }
    post { ... }
}
```

### Essential Options

```groovy
options {
    timeout(time: 30, unit: 'MINUTES')
    timestamps()
    buildDiscarder(logRotator(numToKeepStr: '10'))
    disableConcurrentBuilds()
    ansiColor('xterm')
}
```

### Parallel Execution

```groovy
stage('Test') {
    parallel {
        stage('Unit') { steps { sh 'npm test:unit' } }
        stage('Integration') { steps { sh 'npm test:integration' } }
        stage('E2E') { steps { sh 'npm test:e2e' } }
    }
}
```

## Best Practices (2025-2026)

1. **Declarative first** - Default to declarative syntax
2. **Shared libraries** - Centralize common code
3. **Parallel stages** - Reduce build time
4. **Credentials plugin** - Never hardcode secrets
5. **Timeouts** - Prevent stuck builds
6. **Clean workspace** - Always clean in post section
7. **Blue Ocean** - Modern visualization
8. **Pin library versions** - Stability in shared libraries
9. **Avoid workspace sharing** - Prevent file conflicts
10. **Use plugins** - Prefer plugins over custom shared libraries

## Related

- [jenkins-basics.md](../jenkins-basics.md) - Jenkins fundamentals
- [github-actions.md](../github-actions.md) - Alternative CI/CD
- [gitops.md](../gitops.md) - GitOps practices

## Sources

- [Jenkins Pipeline Documentation](https://www.jenkins.io/doc/book/pipeline/)
- [Shared Libraries](https://www.jenkins.io/doc/book/pipeline/shared-libraries/)
- [Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [Pipeline Best Practices](https://www.jenkins.io/doc/book/pipeline/pipeline-best-practices/)
- [10 Jenkins Best Practices for Scalable CI/CD in 2025](https://dev.to/marketing_team_46cb7140ce/10-jenkins-best-practices-for-scalable-cicd-in-2025-1gp)
- [Jenkins Best Practices for Pipelines, Shared Library & Security](https://cloudinfrastructureservices.co.uk/jenkins-best-practices-for-pipelines-shared-library-security/)
