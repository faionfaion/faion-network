# LLM Prompts for Jenkins Pipelines

AI-assisted prompts for generating and improving Jenkins pipelines.

---

## Pipeline Generation Prompts

### Basic Pipeline Generation

```
Generate a Jenkins Declarative Pipeline for a [LANGUAGE] application with:
- Build stage using [BUILD_TOOL]
- Test stage with JUnit report publishing
- Docker build and push to [REGISTRY]
- Deployment to [ENVIRONMENT] using kubectl
- Slack notifications on success/failure
- Timeout of 30 minutes
- Workspace cleanup

Requirements:
- Use credentials plugin for secrets
- Add timestamps to output
- Keep last 10 builds
```

### Shared Library Generation

```
Create a Jenkins Shared Library function called [FUNCTION_NAME] that:
- Accepts parameters: [LIST_PARAMETERS]
- Validates required parameters
- Implements [FUNCTIONALITY]
- Handles errors gracefully
- Returns [RETURN_VALUE]

Follow these conventions:
- Place in vars/ directory
- Implement java.io.Serializable if using classes
- Include usage example in comments
- Support optional parameters with defaults
```

### Kubernetes Agent Generation

```
Generate a Jenkins Kubernetes Pod template with:
- Container 1: [IMAGE1] for [PURPOSE1]
- Container 2: [IMAGE2] for [PURPOSE2]
- Resource limits: [CPU/MEMORY]
- Volume mounts for [VOLUMES]
- Service account: [SERVICE_ACCOUNT]

Include:
- Proper security context
- Resource requests and limits
- Appropriate labels
```

---

## Pipeline Review Prompts

### Security Review

```
Review this Jenkins Pipeline for security issues:

[PASTE_PIPELINE]

Check for:
1. Hardcoded credentials or secrets
2. Unsafe script approvals needed
3. Missing credential masking
4. Privileged container usage
5. Unsafe shell commands
6. Missing input validation
7. Exposed sensitive environment variables

Provide specific recommendations for each issue found.
```

### Performance Review

```
Analyze this Jenkins Pipeline for performance optimization:

[PASTE_PIPELINE]

Evaluate:
1. Opportunities for parallel execution
2. Unnecessary sequential stages
3. Inefficient artifact handling
4. Missing caching opportunities
5. Agent allocation efficiency
6. Workspace management
7. Resource utilization

Provide specific improvements with code examples.
```

### Best Practices Review

```
Review this Jenkins Pipeline against best practices:

[PASTE_PIPELINE]

Check compliance with:
1. Declarative syntax usage
2. Error handling patterns
3. Timeout configuration
4. Build history management
5. Notification setup
6. Credential management
7. Documentation

Rate each area and provide improvement suggestions.
```

---

## Conversion Prompts

### Scripted to Declarative

```
Convert this Scripted Pipeline to Declarative syntax:

[PASTE_SCRIPTED_PIPELINE]

Requirements:
- Maintain all functionality
- Use appropriate Declarative blocks
- Handle complex logic with script blocks only when necessary
- Add proper post conditions
- Include environment and options blocks
```

### Jenkins to GitHub Actions

```
Convert this Jenkins Pipeline to GitHub Actions workflow:

[PASTE_JENKINS_PIPELINE]

Map Jenkins concepts to GitHub Actions:
- stages -> jobs/steps
- parallel -> matrix or parallel jobs
- agent -> runs-on
- environment -> env
- credentials -> secrets
- post -> if: always()/failure()/success()
```

### Extract Shared Library

```
Analyze this Jenkins Pipeline and identify code that should be extracted to a Shared Library:

[PASTE_PIPELINE]

Identify:
1. Repeated patterns across stages
2. Complex logic that could be encapsulated
3. Configuration that should be parameterized
4. Functions that could be reused

Generate the Shared Library structure with:
- vars/ functions for simple operations
- src/ classes for complex logic
- Usage examples for each
```

---

## Troubleshooting Prompts

### Error Analysis

```
Analyze this Jenkins Pipeline error and provide solutions:

Pipeline:
[PASTE_PIPELINE]

Error:
[PASTE_ERROR_MESSAGE]

Provide:
1. Root cause analysis
2. Multiple solution approaches
3. Code fixes
4. Prevention strategies
```

### Performance Debugging

```
This Jenkins Pipeline is slow. Analyze and optimize:

Pipeline:
[PASTE_PIPELINE]

Current metrics:
- Total duration: [TIME]
- Longest stage: [STAGE] at [TIME]
- Agent wait time: [TIME]

Identify:
1. Bottlenecks
2. Optimization opportunities
3. Parallelization possibilities
4. Caching improvements
```

---

## Enhancement Prompts

### Add Security Scanning

```
Enhance this pipeline with security scanning:

[PASTE_PIPELINE]

Add:
1. SAST scanning with [TOOL: SonarQube/Snyk/etc]
2. Dependency vulnerability scanning
3. Container image scanning with Trivy
4. Secret detection
5. Quality gates that fail build on critical issues

Integrate results with:
- Pipeline status
- PR comments (if applicable)
- Security dashboard
```

### Add Observability

```
Add observability to this Jenkins Pipeline:

[PASTE_PIPELINE]

Implement:
1. Build metrics collection (duration, status, stages)
2. Prometheus metrics endpoint
3. Custom metrics for [SPECIFIC_METRICS]
4. Integration with Grafana dashboard
5. Alert rules for failed builds

Include example queries and dashboard JSON.
```

### Add Multi-Environment Support

```
Extend this pipeline for multi-environment deployment:

[PASTE_PIPELINE]

Environments: dev, staging, production

Requirements:
1. Environment-specific configuration
2. Approval gates for production
3. Automatic dev deployment on PR merge
4. Manual staging/production triggers
5. Environment-specific secrets
6. Rollback capability
```

---

## Documentation Prompts

### Generate Pipeline Documentation

```
Generate documentation for this Jenkins Pipeline:

[PASTE_PIPELINE]

Include:
1. Overview and purpose
2. Prerequisites
3. Parameters description
4. Stages explanation
5. Environment variables
6. Required credentials
7. Troubleshooting guide
8. Example usage

Format as Markdown with code examples.
```

### Generate Shared Library Documentation

```
Generate documentation for this Jenkins Shared Library:

[PASTE_LIBRARY_CODE]

Include:
1. Library overview
2. Installation instructions
3. Each function with:
   - Description
   - Parameters (required/optional)
   - Return value
   - Example usage
4. Configuration options
5. Troubleshooting
```

---

## Advanced Prompts

### Matrix Build Generation

```
Generate a Jenkins Matrix build for:

Application: [APP_NAME]
Platforms: [linux, windows, macos]
Versions: [LIST_VERSIONS]
Exclusions: [EXCLUSION_RULES]

Requirements:
1. Build on each platform/version combination
2. Aggregate test results
3. Fail fast on critical issues
4. Parallel execution where possible
5. Resource-efficient agent allocation
```

### Blue-Green Deployment Pipeline

```
Generate a Jenkins Pipeline for blue-green deployment:

Application: [APP_NAME]
Infrastructure: Kubernetes
Load Balancer: [NGINX/Istio/etc]

Requirements:
1. Deploy to inactive environment (green)
2. Run smoke tests
3. Switch traffic
4. Monitor for errors
5. Automatic rollback on failure
6. Cleanup old environment
```

### Canary Deployment Pipeline

```
Generate a Jenkins Pipeline for canary deployment:

Application: [APP_NAME]
Infrastructure: Kubernetes with Istio
Metrics: Prometheus

Requirements:
1. Deploy canary with 10% traffic
2. Monitor error rate and latency
3. Progressive traffic increase (10% -> 25% -> 50% -> 100%)
4. Automatic rollback if SLO breached
5. Configurable thresholds
6. Integration with alerting
```
