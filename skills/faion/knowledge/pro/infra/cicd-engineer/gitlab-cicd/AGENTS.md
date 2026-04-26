# GitLab CI/CD

## Summary

GitLab CI/CD is an integrated DevSecOps platform using `.gitlab-ci.yml` to define pipelines with stages, jobs, rules, and environments. Use DAG with the `needs` keyword to replace sequential stages and achieve parallelism. Never store secrets in `.gitlab-ci.yml` — use protected, masked CI/CD variables. GitLab 18 (2025) adds immutable artifact tags and structured pipeline inputs.

## Why

GitLab CI/CD provides a single platform for source control, pipelines, container registry, environments, DORA metrics, and security scanning — eliminating the integration overhead of separate tools. The `needs` keyword unlocks DAG-based pipelines that run 2–5x faster than sequential stages by parallelizing independent jobs.

## When To Use

- Projects hosted on GitLab (cloud or self-hosted)
- Teams needing integrated DevSecOps: SAST, DAST, dependency scanning, secret detection
- Multi-environment deployments with review apps per merge request
- Monorepo projects with change-based job filtering (`rules: changes`)
- Organizations tracking DORA metrics natively

## When NOT To Use

- Repositories hosted on GitHub — use GitHub Actions instead
- Simple single-developer projects — overhead of `.gitlab-ci.yml` is not justified; use a Makefile
- Projects requiring Jenkins-level plugin customization not available in GitLab

## Content

| File | What's inside |
|------|---------------|
| `content/01-pipeline-rules.xml` | DAG vs sequential stages, workflow rules, job templates with `extends`, caching strategy rules |
| `content/02-security.xml` | Protected variables, SAST/DAST template inclusion, container scanning, secret detection patterns |
| `content/03-environments.xml` | Review apps lifecycle, auto-stop, canary deployment, manual approval gate patterns |
| `content/04-examples.xml` | Node.js pipeline, Docker build + Trivy scan, Kubernetes deployment, monorepo with change detection |

## Templates

| File | Purpose |
|------|---------|
| `templates/nodejs-pipeline.yml` | Standard Node.js pipeline with install/lint/test/build/deploy stages and DAG |
| `templates/docker-build.yml` | Docker build with BuildKit cache, Trivy scan, and registry push |
| `templates/review-app.yml` | Review app deploy/stop lifecycle with auto_stop_in and namespace cleanup |
| `templates/security-scan.yml` | GitLab security template includes: SAST, dependency, container, secret detection |
