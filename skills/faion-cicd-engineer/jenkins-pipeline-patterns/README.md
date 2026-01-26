# Jenkins Pipeline Patterns

## Overview

Advanced Jenkins pipeline patterns including production-grade declarative pipelines, shared libraries, scripted pipelines, and reusable components. This guide covers best practices for 2025-2026.

**Related:** [jenkins-basics.md](../jenkins-basics.md)

## Key Concepts

| Concept | Description |
|---------|-------------|
| Declarative Pipeline | Structured syntax, easier to read, enforces best practices |
| Scripted Pipeline | Flexible Groovy-based, for complex logic |
| Shared Libraries | Reusable code across pipelines |
| Parallel Stages | Run independent tasks simultaneously |
| Matrix Builds | Cartesian product of axis values |
| Sequential Stages | Multiple stages in parallel branches |

## Declarative vs Scripted

| Aspect | Declarative | Scripted |
|--------|-------------|----------|
| Syntax | Structured, predefined | Free-form Groovy |
| Learning curve | Lower | Higher |
| Flexibility | Limited | Full Groovy power |
| Error handling | Built-in `post` section | Manual try-catch |
| Best for | Standard CI/CD, team maintainability | Complex conditional logic |
| Validation | Syntax validation before run | Runtime errors only |

**Recommendation:** Use Declarative for most pipelines. Use Scripted only when Declarative cannot express the required logic.

## Shared Libraries

### Benefits

1. **DRY Principle** - Centralize common pipeline code
2. **Consistency** - Enforce standards across teams
3. **Maintainability** - Single point of updates
4. **Testing** - Unit test pipeline logic separately
5. **Versioning** - Pin to specific versions for stability

### Directory Structure

```
jenkins-shared-library/
├── vars/                    # Global variables/functions
│   ├── buildApp.groovy
│   ├── deployToK8s.groovy
│   ├── notifySlack.groovy
│   └── runTests.groovy
├── src/                     # Groovy classes
│   └── com/
│       └── example/
│           ├── Docker.groovy
│           └── Kubernetes.groovy
├── resources/               # Non-Groovy files
│   └── templates/
│       └── deployment.yaml
└── test/                    # Unit tests
    └── groovy/
        └── com/example/
            └── DockerTest.groovy
```

### Best Practices

| Practice | Reason |
|----------|--------|
| Use dedicated repository | Separation of concerns |
| Implement `Serializable` | Avoid CPS transformation issues |
| Never override built-in steps | API changes can break pipelines |
| Keep libraries small | Reduce checkout time and memory |
| Version with tags | Stability in production |
| Write unit tests | Catch bugs early |

## Parallel Stages

### Use Cases

- Cross-platform builds (Linux, Windows, macOS)
- Multi-environment testing (Chrome, Firefox, Safari)
- Independent tasks (lint, test, scan)
- Matrix builds (multiple versions)

### Pitfalls and Solutions

| Pitfall | Solution |
|---------|----------|
| Resource exhaustion | Use agent labels, limit parallelism |
| Shared resource conflicts | Use `lock` step or separate resources |
| Common workspace races | Use `dir()` or unique workspaces |
| Unclear failure attribution | Use `failFast: true` carefully |

## Pipeline Options

| Option | Purpose |
|--------|---------|
| `timeout` | Prevent stuck builds |
| `timestamps` | Add timestamps to console output |
| `buildDiscarder` | Limit build history |
| `disableConcurrentBuilds` | Prevent parallel executions |
| `ansiColor` | Enable colored output |
| `skipDefaultCheckout` | Manual checkout control |
| `preserveStashes` | Keep stashes after build |

## Files in This Folder

| File | Content |
|------|---------|
| [README.md](README.md) | This overview |
| [checklist.md](checklist.md) | Pre-production checklist |
| [examples.md](examples.md) | Working code examples |
| [templates.md](templates.md) | Copy-paste templates |
| [llm-prompts.md](llm-prompts.md) | AI-assisted generation prompts |

## Sources

- [Jenkins Shared Libraries](https://www.jenkins.io/doc/book/pipeline/shared-libraries/)
- [Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [Pipeline Best Practices](https://www.jenkins.io/doc/book/pipeline/pipeline-best-practices/)
- [Parallel Stages](https://www.jenkins.io/blog/2017/09/25/declarative-1/)
- [Sequential Stages](https://www.jenkins.io/blog/2018/07/02/whats-new-declarative-piepline-13x-sequential-stages/)
- [DevOpsCube Tutorial](https://devopscube.com/jenkins-shared-library-tutorial/)
- [Best Practices for Shared Libraries](https://bmuschko.com/blog/jenkins-shared-libraries/)
