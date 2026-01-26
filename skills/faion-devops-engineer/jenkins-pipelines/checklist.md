# Jenkins Pipeline Checklist

Pre-flight checklist for implementing Jenkins pipelines.

## Pipeline Setup

### Initial Configuration

- [ ] Jenkins version 2.400+ installed
- [ ] Required plugins installed:
  - [ ] Pipeline
  - [ ] Blue Ocean
  - [ ] Git
  - [ ] Credentials Binding
  - [ ] Docker Pipeline (if using Docker)
  - [ ] Kubernetes (if using K8s agents)
- [ ] Shared library configured (if using)
- [ ] Credentials configured in Jenkins

### Jenkinsfile

- [ ] Declarative syntax used (unless complex logic required)
- [ ] `agent` block defined
- [ ] `environment` block for variables
- [ ] `options` block with:
  - [ ] `timeout()` set
  - [ ] `timestamps()` enabled
  - [ ] `buildDiscarder()` configured
  - [ ] `disableConcurrentBuilds()` if needed
- [ ] `stages` block with logical stages
- [ ] `post` block with cleanup

## Security

### Credentials

- [ ] No hardcoded secrets
- [ ] Credentials plugin used
- [ ] Credentials scoped appropriately
- [ ] Service accounts with minimal permissions
- [ ] Secrets rotated regularly

### Access Control

- [ ] Role-based access configured
- [ ] Input approvers defined for production
- [ ] Audit logging enabled

### Container Security

- [ ] Base images from trusted sources
- [ ] Container scanning enabled (Trivy, etc.)
- [ ] Non-root containers preferred
- [ ] Resource limits set

## Performance

### Build Optimization

- [ ] Parallel stages for independent tasks
- [ ] Workspace cleanup after builds
- [ ] Artifact caching configured
- [ ] Build agents sized appropriately
- [ ] Build history limited

### Resource Management

- [ ] Agent pods/containers cleaned up
- [ ] Docker images pruned regularly
- [ ] Disk space monitored
- [ ] Memory limits set

## Quality

### Testing

- [ ] Unit tests in pipeline
- [ ] Integration tests in pipeline
- [ ] Test results published (JUnit, etc.)
- [ ] Coverage reports published
- [ ] Quality gates defined

### Code Quality

- [ ] Linting/formatting checks
- [ ] SAST scanning (npm audit, etc.)
- [ ] Dependency vulnerability scanning
- [ ] Code review required

## Deployment

### Staging

- [ ] Staging deployment automated
- [ ] Smoke tests after deployment
- [ ] Rollback strategy defined

### Production

- [ ] Manual approval gate
- [ ] Deployment window defined
- [ ] Rollout status verification
- [ ] Rollback tested

### Monitoring

- [ ] Build notifications configured
- [ ] Failure alerts (Slack, email)
- [ ] Metrics collection enabled
- [ ] Log aggregation configured

## Shared Libraries

### Structure

- [ ] `vars/` for global functions
- [ ] `src/` for complex classes
- [ ] `resources/` for templates
- [ ] Unit tests for library code
- [ ] Documentation in README

### Versioning

- [ ] Library versioned in Git
- [ ] Semantic versioning used
- [ ] Changelog maintained
- [ ] Breaking changes documented

### Usage

- [ ] Library pinned to specific version
- [ ] Fallback for library failures
- [ ] Library updates tested

## Blue Ocean

- [ ] Blue Ocean plugin installed
- [ ] Pipeline visualization works
- [ ] Parallel branches display correctly
- [ ] Logs accessible and readable
- [ ] Pipeline editor functional

## Post-Implementation

### Documentation

- [ ] Pipeline documented
- [ ] Runbooks created
- [ ] Troubleshooting guide available
- [ ] Team trained

### Maintenance

- [ ] Plugin updates scheduled
- [ ] Regular pipeline reviews
- [ ] Performance monitoring
- [ ] Security audits scheduled

## Quick Validation

```groovy
// Minimal pipeline to test setup
pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
                echo 'Pipeline working!'
            }
        }
    }
}
```

Run this minimal pipeline first to validate Jenkins configuration.
