# LLM Prompts for Jenkins Pipeline Development

## Pipeline Generation

### Basic Pipeline

```
Create a Jenkins Declarative Pipeline for a [Node.js/Python/Java/Go] application with the following requirements:
- Build tool: [npm/pip/maven/gradle]
- Test framework: [jest/pytest/junit]
- Deployment target: [Kubernetes/AWS/Docker Hub]
- Branches: main (production), develop (staging), feature/* (preview)

Requirements:
1. Use Declarative syntax
2. Set appropriate timeouts
3. Clean workspace after build
4. Use parallel stages where possible
5. Include proper error handling
```

### Kubernetes Agent Pipeline

```
Create a Jenkins Pipeline using Kubernetes agents with:
- Pod template with containers: [list containers needed]
- Build tool: [npm/maven/gradle]
- Docker build capability
- Helm deployment

Include:
1. Pod YAML specification
2. Container-specific steps
3. Credential handling for registry and kubeconfig
4. Deployment verification
```

### Multibranch Pipeline

```
Create a Jenkins Multibranch Pipeline configuration for:
- Repository: GitHub/GitLab/Bitbucket
- Branch patterns: main, develop, feature/*, release/*
- PR detection: enabled

Each branch type should:
- main: deploy to production with approval
- develop: auto-deploy to staging
- feature/*: run tests only
- release/*: deploy to UAT

Include branch-specific when conditions and input steps.
```

## Shared Library Development

### Create Shared Library Function

```
Create a Jenkins Shared Library function for [describe purpose]:

Function requirements:
- Name: [functionName]
- Parameters: [list parameters]
- Steps: [describe what it should do]

Include:
1. Proper parameter validation
2. Error handling
3. Documentation comments
4. Example usage
```

### Standardized Pipeline Library

```
Create a Jenkins Shared Library that provides a standardized pipeline for [application type] with:

Configurable options:
- Docker image
- Build commands
- Test commands
- Deploy targets
- Notification channels

Include:
1. vars/standardPipeline.groovy
2. Default values for all options
3. Post-build notifications
4. Workspace cleanup
```

## Troubleshooting

### Debug Pipeline Issues

```
My Jenkins Pipeline is failing with the following error:

[paste error message]

Pipeline context:
- Stage: [stage name]
- Agent: [agent type]
- Step: [step that failed]

Please:
1. Explain what the error means
2. Identify the root cause
3. Provide a fix
4. Suggest preventive measures
```

### Optimize Pipeline Performance

```
Analyze this Jenkins Pipeline and suggest optimizations:

[paste Jenkinsfile]

Focus on:
1. Parallel execution opportunities
2. Caching strategies
3. Agent selection
4. Unnecessary steps
5. Build time reduction
```

### Security Review

```
Review this Jenkins Pipeline for security issues:

[paste Jenkinsfile]

Check for:
1. Credential handling
2. Script approval risks
3. Agent security
4. Input validation
5. Secret exposure in logs
```

## Migration

### Convert from Scripted to Declarative

```
Convert this Scripted Pipeline to Declarative syntax:

[paste scripted pipeline]

Requirements:
1. Preserve all functionality
2. Use proper post sections instead of try-catch
3. Add options (timeout, timestamps)
4. Add proper when conditions
```

### Migrate from Other CI Systems

```
Convert this [GitHub Actions/GitLab CI/CircleCI] workflow to Jenkins Pipeline:

[paste workflow file]

Considerations:
1. Map jobs to stages
2. Convert environment variables
3. Handle secrets/credentials
4. Adapt caching strategy
5. Convert matrix builds if present
```

## Integration

### Add Code Quality Integration

```
Add SonarQube integration to this Jenkins Pipeline:

[paste Jenkinsfile]

Requirements:
1. Run SonarQube analysis
2. Wait for quality gate
3. Fail build if quality gate fails
4. Configure project key and server URL as parameters
```

### Add Security Scanning

```
Add security scanning to this Jenkins Pipeline:

[paste Jenkinsfile]

Include:
1. OWASP Dependency-Check for vulnerabilities
2. Trivy for container scanning
3. SAST with [SonarQube/Checkmarx/Snyk]
4. Fail on critical vulnerabilities
5. Archive reports
```

### Add Notifications

```
Add notification integration to this Jenkins Pipeline:

[paste Jenkinsfile]

Notification channels:
- Slack: #builds channel
- Email: team@example.com
- Microsoft Teams: webhook URL

Notify on:
- Build start
- Build success
- Build failure
- Deployment completion
```

## Infrastructure

### Jenkins Configuration as Code

```
Create a Jenkins Configuration as Code (JCasC) file for:

Jenkins setup:
- Security: [LDAP/local users/OAuth]
- Agents: [list of agents with labels]
- Plugins: [list required plugins]
- Global libraries: [list libraries]
- Credentials: [types needed]

Include all necessary YAML configuration.
```

### Docker-based Jenkins Setup

```
Create a Docker Compose setup for Jenkins with:
- Jenkins controller
- Docker-in-Docker agent
- Persistent volumes
- Custom plugins pre-installed

Include:
1. docker-compose.yml
2. Dockerfile for custom Jenkins image
3. plugins.txt for plugin installation
4. Initial JCasC configuration
```

## Best Practices Review

### Review Pipeline Against Best Practices

```
Review this Jenkins Pipeline against best practices:

[paste Jenkinsfile]

Check against:
1. Declarative vs Scripted usage
2. Agent configuration
3. Timeout and build discarder settings
4. Credential handling
5. Parallel execution
6. Post-build cleanup
7. Error handling
8. Code organization

Provide specific recommendations with code examples.
```

### Create Pipeline from Scratch

```
I need to create a Jenkins Pipeline for a new project:

Project details:
- Type: [web app/API/library/microservice]
- Language: [Node.js/Python/Java/Go]
- Repository: [GitHub/GitLab/Bitbucket]
- Deployment: [Kubernetes/AWS/Docker/VM]
- Team size: [small/medium/large]

Create a production-ready Pipeline following all best practices from Jenkins documentation and CloudBees recommendations.
```
