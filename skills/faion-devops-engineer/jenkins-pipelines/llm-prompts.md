# LLM Prompts for Jenkins Pipelines

Prompts for generating Jenkins pipeline configurations.

## Declarative Pipeline Generation

### Basic Pipeline

```
Generate a Jenkins declarative pipeline for a [Node.js/Python/Java/Go] application with:

Project details:
- Language: [language]
- Framework: [framework]
- Test command: [command]
- Build command: [command]

Requirements:
- Stages: checkout, install, test, build, deploy
- Timeout: 30 minutes
- Clean workspace after build
- Parallel unit and integration tests
- Deploy to [staging/production] on main branch

Output: Complete Jenkinsfile with best practices (timestamps, build discarder, concurrent builds disabled).
```

### Kubernetes Agent Pipeline

```
Generate a Jenkins declarative pipeline with Kubernetes pod agent for [project type].

Containers needed:
- [container 1]: [image, purpose]
- [container 2]: [image, purpose]
- [container 3]: [image, purpose]

Stages:
1. [stage 1]: [description, container]
2. [stage 2]: [description, container]
3. [stage 3]: [description, container]

Requirements:
- Resource limits for containers
- Volume mounts if needed
- Proper security context
- Post actions for cleanup

Output: Complete Jenkinsfile with Kubernetes pod YAML definition.
```

### Multi-Environment Pipeline

```
Generate a Jenkins pipeline that deploys to multiple environments:

Environments:
- development: [details]
- staging: [details]
- production: [details]

Deployment rules:
- feature/* branches -> development
- develop branch -> staging
- main branch -> staging, then production (with approval)

Requirements:
- Environment-specific credentials
- Approval gate for production
- Rollback capability
- Notifications per environment

Output: Complete Jenkinsfile with environment-based deployment logic.
```

## Shared Library Generation

### Shared Library Function

```
Generate a Jenkins shared library function in vars/ for [purpose].

Function name: [name]

Parameters:
- [param1]: [type, description, required/optional, default]
- [param2]: [type, description, required/optional, default]
- [param3]: [type, description, required/optional, default]

Behavior:
- [step 1]
- [step 2]
- [step 3]

Error handling:
- [error scenario 1]: [action]
- [error scenario 2]: [action]

Output: Complete Groovy function for vars/[name].groovy with validation and error handling.
```

### Shared Library Class

```
Generate a Jenkins shared library class in src/ for [purpose].

Package: com.[company]
Class name: [ClassName]

Constructor:
- Takes pipeline steps object

Methods:
1. [method1](params): [description, return type]
2. [method2](params): [description, return type]
3. [method3](params): [description, return type]

Requirements:
- Implements Serializable
- Proper credential handling
- Error handling with meaningful messages
- Usage example in comments

Output: Complete Groovy class for src/com/[company]/[ClassName].groovy.
```

## Security Scanning Integration

### Container Security Pipeline

```
Generate a Jenkins pipeline stage for container security scanning.

Scanner: [Trivy/Clair/Snyk/Grype]
Image: ${DOCKER_REGISTRY}/${APP_NAME}:${VERSION}

Requirements:
- Scan for [severity levels]
- Fail build on [conditions]
- Generate report in [format]
- Upload report to [destination]
- Allow exceptions from [file/config]

Output: Complete stage definition with security scanning best practices.
```

### SAST Integration

```
Generate Jenkins pipeline stages for SAST (Static Application Security Testing).

Tools:
- Dependency check: [npm audit/pip-audit/OWASP dependency-check]
- Code analysis: [SonarQube/Semgrep/CodeQL]
- Secret detection: [gitleaks/trufflehog/detect-secrets]

Requirements:
- Run in parallel
- Quality gate thresholds
- Report publishing
- Failure handling

Output: Complete SAST stage with parallel execution and reporting.
```

## Pipeline Migration

### From GitHub Actions to Jenkins

```
Convert this GitHub Actions workflow to Jenkins declarative pipeline:

```yaml
[paste GitHub Actions workflow here]
```

Requirements:
- Maintain all functionality
- Use equivalent Jenkins features
- Add Jenkins-specific best practices
- Handle secrets via Jenkins credentials
- Optimize for Jenkins parallelization

Output: Equivalent Jenkinsfile with comments explaining mappings.
```

### From GitLab CI to Jenkins

```
Convert this GitLab CI pipeline to Jenkins declarative pipeline:

```yaml
[paste GitLab CI pipeline here]
```

Requirements:
- Maintain stage dependencies
- Convert artifacts handling
- Map variables to Jenkins environment
- Handle caching appropriately

Output: Equivalent Jenkinsfile with comments explaining mappings.
```

## Troubleshooting

### Pipeline Debugging

```
My Jenkins pipeline is failing with this error:

```
[paste error message/log]
```

Pipeline context:
- Stage: [stage name]
- Step: [step description]
- Agent: [agent type]

What I've tried:
- [attempt 1]
- [attempt 2]

Provide:
1. Root cause analysis
2. Solution options (ranked by likelihood)
3. Prevention measures
4. Fixed code snippet
```

### Performance Optimization

```
Optimize this Jenkins pipeline for faster execution:

```groovy
[paste current Jenkinsfile]
```

Current build time: [X minutes]
Target build time: [Y minutes]

Constraints:
- [constraint 1]
- [constraint 2]

Provide:
1. Bottleneck analysis
2. Optimization opportunities (with expected impact)
3. Optimized Jenkinsfile
4. Before/after comparison
```

## Blue Ocean Setup

### Pipeline Editor Configuration

```
Help me set up a Blue Ocean pipeline for [project type].

Repository:
- Type: [GitHub/GitLab/Bitbucket]
- URL: [repo URL]
- Branch strategy: [multibranch/single branch]

Pipeline requirements:
- [requirement 1]
- [requirement 2]
- [requirement 3]

Provide:
1. Step-by-step Blue Ocean setup
2. Initial Jenkinsfile for the project
3. Recommended Blue Ocean plugins
4. Common issues and solutions
```

## Template Customization

### Adapt Template for Project

```
I have this Jenkins pipeline template:

```groovy
[paste template]
```

Customize it for my project:
- Language: [language]
- Framework: [framework]
- Registry: [registry URL]
- Deployment target: [K8s/EC2/ECS/etc.]
- Team size: [number]

Additional requirements:
- [requirement 1]
- [requirement 2]

Output: Customized Jenkinsfile with project-specific values and any needed additions.
```
