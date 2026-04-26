# Jenkins Pipelines

## Summary

Declarative Jenkins pipelines for production CI/CD: parallel stages, Kubernetes pod agents, shared libraries, and multi-environment deployment with manual approval gates. Default to declarative syntax; use scripted only for dynamic logic (e.g., detecting changed services in a monorepo).

## Why

Declarative pipelines are readable, maintainable, and support all built-in features (parallel, matrix, input) without Groovy complexity. Shared libraries in `vars/` centralize build/deploy/notify logic, eliminating copy-paste across Jenkinsfiles. Parallel test stages and Kubernetes agents dramatically reduce build times.

## When To Use

- CI/CD pipelines on an existing Jenkins installation
- Multi-environment deployments requiring human approval gates before production
- Monorepo builds that need to detect changed services and build only those
- Containerized builds requiring isolated, disposable Kubernetes pod agents

## When NOT To Use

- New projects without existing Jenkins investment — prefer GitHub Actions or GitLab CI
- Simple single-step builds — overhead of Jenkins setup is not justified
- When you need native OIDC cloud auth without plugins — Jenkins requires plugins for this
- GitOps-first workflows — ArgoCD/Flux are better fits than Jenkins for K8s GitOps

## Content

| File | What's inside |
|------|---------------|
| `content/01-pipeline-structure.xml` | Declarative syntax, options block, parallel stages, when conditions, post actions |
| `content/02-shared-libraries.xml` | Library structure (vars/ vs src/), versioning, buildApp/deployToK8s/notifySlack patterns |
| `content/03-examples.xml` | Production pipeline with K8s agent, multibranch, matrix build, canary deployment |

## Templates

| File | Purpose |
|------|---------|
| `templates/Jenkinsfile.groovy` | Basic declarative Jenkinsfile template with all recommended options |
| `templates/Jenkinsfile-k8s.groovy` | Kubernetes pod agent template with node/docker/kubectl containers |
| `templates/buildApp.groovy` | Shared library: build and push Docker image |
| `templates/deployToK8s.groovy` | Shared library: kubectl set image + rollout status |
| `templates/notifySlack.groovy` | Shared library: Slack notification with color by status |
| `templates/prompt-generate-pipeline.txt` | LLM prompt for generating a declarative pipeline |
