# GitLab CI/CD LLM Prompts

AI-assisted prompts for generating and optimizing GitLab CI/CD pipelines.

## Pipeline Generation

### Generate Complete Pipeline

```
Create a GitLab CI/CD pipeline for a [LANGUAGE/FRAMEWORK] project with:

Project details:
- Language: [Node.js/Python/Go/Java/etc.]
- Framework: [Next.js/Django/FastAPI/Spring/etc.]
- Testing: [Jest/Pytest/Go test/JUnit]
- Container: [Docker/Podman/Buildah]
- Deploy target: [Kubernetes/AWS/GCP/Heroku/VPS]

Requirements:
1. Build stage with caching
2. Unit and integration tests with coverage
3. Security scanning (SAST, dependencies)
4. Staging deployment on main branch
5. Production deployment on tags (manual)
6. Review apps for merge requests

Use GitLab CI/CD best practices:
- Use `rules:` instead of `only/except`
- Use `needs:` for DAG parallelization
- Cache dependencies, artifact build outputs
- Include security scanning templates
- Set appropriate `expire_in` for artifacts
```

### Optimize Existing Pipeline

```
Optimize this GitLab CI/CD pipeline for faster execution:

[PASTE EXISTING .gitlab-ci.yml]

Focus on:
1. Identify jobs that can run in parallel using `needs:`
2. Improve caching strategy (key, paths, policy)
3. Reduce artifact sizes
4. Remove redundant steps
5. Add `interruptible: true` where appropriate
6. Suggest rule improvements

Return the optimized pipeline with comments explaining changes.
```

## Specific Pipeline Types

### Monorepo Pipeline

```
Create a GitLab CI/CD pipeline for a monorepo with these services:

Services:
- /services/api - Node.js REST API
- /services/web - Next.js frontend
- /services/worker - Python background worker
- /packages/shared - Shared TypeScript library

Requirements:
1. Only build/test changed services
2. Shared package changes trigger dependent services
3. Independent deployments per service
4. Parent-child pipeline structure
5. Service-specific caching
6. Matrix testing for shared package

Use `changes:` rules for conditional execution.
```

### Auto DevOps Integration

```
Configure GitLab Auto DevOps for a [LANGUAGE] project:

Project details:
- Kubernetes cluster: [EKS/GKE/self-managed]
- Domain: [example.com]
- Database: [PostgreSQL/MySQL/none]
- Staging: [enabled/disabled]
- Canary deployments: [enabled/disabled]

Provide:
1. Auto DevOps configuration variables
2. Buildpack customizations if needed
3. Override jobs for custom behavior
4. Environment-specific values files
5. Monitoring and alerting setup
```

### Security-Focused Pipeline

```
Create a security-hardened GitLab CI/CD pipeline with:

Security requirements:
1. SAST (Static Application Security Testing)
2. DAST (Dynamic Application Security Testing)
3. Dependency scanning
4. Container scanning
5. Secret detection
6. License compliance
7. Trivy vulnerability scanning

Additional:
- Block pipeline on HIGH/CRITICAL vulnerabilities
- Generate security reports for merge requests
- Integrate with GitLab Security Dashboard
- Set up security policies
```

## Troubleshooting Prompts

### Debug Pipeline Failures

```
Help debug this GitLab CI/CD pipeline failure:

Error message:
[PASTE ERROR]

Job configuration:
[PASTE JOB YAML]

Questions:
1. What is the root cause of this error?
2. How can I fix it?
3. Are there any best practices I'm violating?
4. How can I prevent this in the future?
```

### Cache Issues

```
My GitLab CI/CD cache isn't working as expected:

Current cache configuration:
[PASTE CACHE CONFIG]

Symptoms:
- [Describe what's happening]

Help me:
1. Identify why cache isn't being used
2. Fix the cache key strategy
3. Ensure proper cache sharing between jobs
4. Add cache debugging steps
```

### Slow Pipeline Analysis

```
Analyze this slow GitLab CI/CD pipeline and suggest improvements:

Pipeline duration: [X minutes]
Slowest jobs:
- [job1]: [duration]
- [job2]: [duration]

Current configuration:
[PASTE .gitlab-ci.yml]

Identify:
1. Bottlenecks in the pipeline
2. Jobs that should run in parallel
3. Unnecessary dependencies
4. Cache/artifact optimizations
5. Resource allocation issues
```

## Migration Prompts

### GitHub Actions to GitLab CI

```
Convert this GitHub Actions workflow to GitLab CI/CD:

[PASTE .github/workflows/ci.yml]

Requirements:
1. Maintain same functionality
2. Use GitLab-native features where better
3. Convert secrets to GitLab variables
4. Use GitLab container registry
5. Set up environments properly

Explain key differences and GitLab advantages.
```

### Jenkins to GitLab CI

```
Migrate this Jenkinsfile to GitLab CI/CD:

[PASTE Jenkinsfile]

Convert:
1. Stages to GitLab stages
2. Parallel blocks to parallel jobs
3. Agent specifications to images/runners
4. Post actions to after_script
5. Environment variables to GitLab variables
6. Credentials to protected variables
```

## Advanced Patterns

### Dynamic Pipeline Generation

```
Create a GitLab CI/CD pipeline that dynamically generates child pipelines:

Use case:
- [Describe the dynamic aspect]

Requirements:
1. Parent pipeline detects what to build
2. Generate child pipeline YAML dynamically
3. Trigger child pipeline with generated config
4. Pass variables between parent and child
5. Handle failures appropriately
```

### Multi-Project Pipeline

```
Set up a multi-project GitLab CI/CD pipeline:

Projects:
- Project A: [description, triggers]
- Project B: [description, triggers]
- Project C: [description, triggers]

Requirements:
1. Project A triggers Project B on success
2. Pass variables between projects
3. Wait for downstream completion
4. Handle deployment dependencies
5. Implement rollback strategy
```

### Matrix Testing

```
Create a GitLab CI/CD matrix testing job:

Test matrix:
- [Dimension 1]: [values]
- [Dimension 2]: [values]
- [Dimension 3]: [values]

Requirements:
1. Use parallel:matrix for job generation
2. Allow specific combinations to fail
3. Aggregate results from all jobs
4. Optimize for minimum total duration
```

## Review Prompts

### Pipeline Code Review

```
Review this GitLab CI/CD pipeline for issues and improvements:

[PASTE .gitlab-ci.yml]

Check for:
1. Security issues (exposed secrets, missing scans)
2. Performance problems (missing cache, large artifacts)
3. Reliability issues (no retry, missing timeouts)
4. Best practice violations
5. Maintainability concerns
6. Missing environments/rules

Provide specific fixes with code examples.
```

### Pre-Deployment Checklist

```
Generate a pre-deployment checklist for this GitLab pipeline:

[PASTE .gitlab-ci.yml]

Include checks for:
1. All required stages present
2. Security scanning configured
3. Proper environment setup
4. Rollback capabilities
5. Monitoring integration
6. Notification setup
7. Manual approval gates
```

## Documentation Prompts

### Generate Pipeline Documentation

```
Generate documentation for this GitLab CI/CD pipeline:

[PASTE .gitlab-ci.yml]

Include:
1. Pipeline overview diagram (mermaid)
2. Stage descriptions
3. Job descriptions with inputs/outputs
4. Required variables (with descriptions)
5. Environment URLs
6. Troubleshooting guide
7. How to extend the pipeline
```

### Runbook Generation

```
Create a runbook for operating this GitLab CI/CD pipeline:

[PASTE .gitlab-ci.yml]

Include:
1. Common failure scenarios and fixes
2. Manual intervention procedures
3. Rollback steps
4. Emergency procedures
5. Monitoring and alerting
6. Escalation paths
```

## Sources

- [GitLab CI/CD Documentation](https://docs.gitlab.com/ee/ci/)
- [GitLab CI: 10+ Best Practices](https://dev.to/zenika/gitlab-ci-10-best-practices-to-avoid-widespread-anti-patterns-2mb5)
- [How to Write a GitLab CI/CD Pipeline From Scratch (2026 Edition)](https://thelinuxcode.com/how-to-write-a-gitlab-cicd-pipeline-from-scratch-2026-edition/)
