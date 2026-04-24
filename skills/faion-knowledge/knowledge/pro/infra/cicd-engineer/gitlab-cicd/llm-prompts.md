# GitLab CI/CD LLM Prompts

## Pipeline Creation

### Create New Pipeline

```
Create a GitLab CI/CD pipeline for a [LANGUAGE/FRAMEWORK] project with:

Requirements:
- Stages: [build, test, security, deploy]
- Target environment: [Kubernetes/Docker/VM]
- Branch strategy: [main/develop/feature branches]
- Deployment: [staging, production]

Include:
- Proper caching for dependencies
- Test coverage reporting
- Security scanning (SAST, dependency)
- Review apps for merge requests
- Manual production deployment

Output: Complete .gitlab-ci.yml with comments
```

### Optimize Existing Pipeline

```
Optimize this GitLab CI/CD pipeline for speed and efficiency:

Current pipeline:
[PASTE .gitlab-ci.yml]

Focus on:
1. Parallel execution with `needs` keyword
2. Caching strategy improvements
3. Reducing artifact sizes
4. Removing unnecessary jobs
5. Using DAG instead of linear stages

Provide optimized version with explanations for each change.
```

## Troubleshooting

### Debug Pipeline Issues

```
Debug this GitLab CI/CD pipeline issue:

Error message:
[PASTE ERROR]

Current configuration:
[PASTE RELEVANT YAML SECTION]

Runner type: [shared/self-hosted]
GitLab version: [VERSION]

Analyze the issue and provide:
1. Root cause
2. Solution
3. Prevention steps
```

### Fix Caching Issues

```
Fix caching issues in this GitLab pipeline:

Symptoms:
- Cache miss rate: [XX%]
- Build time: [XX minutes]
- Cache key: [CURRENT KEY]

Current cache config:
[PASTE CACHE CONFIG]

Provide:
1. Improved cache key strategy
2. Optimal cache paths
3. Fallback configuration
4. S3/GCS distributed cache setup (if applicable)
```

## Security

### Security Pipeline Review

```
Review this GitLab CI/CD pipeline for security issues:

[PASTE .gitlab-ci.yml]

Check for:
1. Secrets exposure in logs
2. Unprotected variables
3. Missing security scanning
4. Insecure artifact handling
5. Privileged container usage

Output:
- Security issues found
- Severity rating
- Remediation steps
```

### Add Security Scanning

```
Add comprehensive security scanning to this GitLab pipeline:

Current pipeline:
[PASTE .gitlab-ci.yml]

Include:
1. SAST (Static Application Security Testing)
2. DAST (Dynamic Application Security Testing)
3. Dependency scanning
4. Container scanning
5. Secret detection
6. License compliance

Use GitLab templates where appropriate.
```

## Deployment

### Kubernetes Deployment

```
Create a GitLab CI/CD pipeline for Kubernetes deployment:

Requirements:
- Cluster: [EKS/GKE/AKS/self-managed]
- Namespace strategy: [per-env/per-branch]
- Deployment method: [kubectl/Helm/Kustomize]
- Rollback capability: [required/optional]

Include:
- Staging and production environments
- Canary deployment option
- Health checks
- Automatic rollback on failure

Output: Complete pipeline with K8s manifests
```

### Review Apps Setup

```
Add review apps to this GitLab pipeline:

Current setup:
[PASTE .gitlab-ci.yml]

Requirements:
- Create on: merge request open
- Destroy on: merge request close or after [X days]
- URL pattern: [PR_NUMBER].review.example.com
- Resources: [namespace per review/shared namespace]

Include Kubernetes deployment and cleanup.
```

## Migration

### GitHub Actions to GitLab CI

```
Migrate this GitHub Actions workflow to GitLab CI/CD:

[PASTE GITHUB WORKFLOW YAML]

Maintain:
- Same job structure
- Equivalent caching
- Similar trigger conditions
- Artifact handling

Handle GitLab-specific:
- CI/CD variables naming
- Built-in environment variables
- Security templates
```

### Jenkins to GitLab CI

```
Migrate this Jenkins pipeline to GitLab CI/CD:

[PASTE JENKINSFILE]

Map:
- Jenkins stages to GitLab stages
- Jenkins plugins to GitLab features
- Credential management
- Agent/runner configuration

Optimize for GitLab native features.
```

## Auto DevOps

### Enable Auto DevOps

```
Configure Auto DevOps for this project:

Project type: [LANGUAGE/FRAMEWORK]
Deployment target: [Kubernetes cluster]
Custom requirements:
- [List any customizations]

Provide:
1. Required variables
2. Dockerfile modifications (if needed)
3. Helm chart customizations
4. Override file for customizations
```

### Customize Auto DevOps

```
Customize Auto DevOps for these requirements:

Base: Auto DevOps template
Customizations needed:
1. [Customization 1]
2. [Customization 2]
3. [Customization 3]

Current .gitlab-ci.yml:
[PASTE IF EXISTS]

Provide override configuration.
```

## Monitoring

### Pipeline Metrics

```
Add monitoring and metrics to this GitLab pipeline:

Current pipeline:
[PASTE .gitlab-ci.yml]

Track:
- Build duration
- Test coverage trends
- Deployment frequency
- Failure rate
- Lead time for changes

Integration: [Prometheus/Grafana/DataDog]
```

### DORA Metrics Setup

```
Configure DORA metrics tracking for GitLab CI/CD:

Metrics to track:
1. Deployment Frequency
2. Lead Time for Changes
3. Change Failure Rate
4. Time to Restore Service

Provide:
- Pipeline configuration
- GitLab settings
- Dashboard setup
```

## Cost Optimization

### Reduce CI/CD Costs

```
Optimize this GitLab CI/CD pipeline for cost reduction:

Current metrics:
- Monthly CI/CD minutes: [X]
- Average pipeline duration: [X minutes]
- Daily pipeline count: [X]

Current pipeline:
[PASTE .gitlab-ci.yml]

Optimize:
1. Job parallelization
2. Conditional execution
3. Caching efficiency
4. Runner selection
5. Job resource requests
```

## Integration

### External Services Integration

```
Integrate these external services with GitLab CI/CD:

Services:
- [Service 1]: [purpose]
- [Service 2]: [purpose]
- [Service 3]: [purpose]

Current pipeline:
[PASTE .gitlab-ci.yml]

Provide:
1. Integration configuration
2. Variable setup
3. Authentication handling
4. Error handling
```

### Notification Setup

```
Add notifications to this GitLab pipeline:

Current pipeline:
[PASTE .gitlab-ci.yml]

Notify on:
- Pipeline start
- Pipeline success
- Pipeline failure
- Deployment complete

Channels:
- Slack: [webhook URL variable]
- Email: [recipients]
- MS Teams: [webhook URL variable]

Include message templates with relevant information.
```

## Best Practices Check

### Pipeline Review

```
Review this GitLab CI/CD pipeline against best practices:

[PASTE .gitlab-ci.yml]

Check:
1. Stage organization
2. Job naming conventions
3. Caching efficiency
4. Artifact management
5. Security practices
6. Documentation/comments
7. DAG usage
8. Error handling
9. Resource efficiency
10. Maintainability

Rate each area and provide improvement suggestions.
```
