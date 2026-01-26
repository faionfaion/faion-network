# Jenkins Pipeline Checklist

## Pre-Production Checklist

### Pipeline Structure

- [ ] Using Declarative syntax (unless complex logic requires Scripted)
- [ ] Pipeline validated with `declarative-linter`
- [ ] All stages have meaningful names
- [ ] Stages grouped logically (build, test, deploy)

### Security

- [ ] No hardcoded credentials in Jenkinsfile
- [ ] Credentials stored in Jenkins Credentials store
- [ ] Using `withCredentials` for secret access
- [ ] Secrets masked in console output
- [ ] Container images scanned for vulnerabilities
- [ ] SAST/DAST scanning integrated

### Error Handling

- [ ] `timeout` set for pipeline and long-running stages
- [ ] `post` section handles success, failure, always
- [ ] Notifications configured (Slack, email)
- [ ] `cleanWs()` in post.always to clean workspace
- [ ] Retry logic for flaky operations (network, external services)

### Performance

- [ ] Parallel stages for independent tasks
- [ ] Build artifacts cached where possible
- [ ] Docker layer caching enabled
- [ ] Shared library loaded efficiently (specific version)
- [ ] Agent resources appropriate for workload

### Maintainability

- [ ] Common code extracted to shared library
- [ ] Environment variables defined in `environment` block
- [ ] Parameters documented with descriptions
- [ ] Pipeline documented (README or inline comments)
- [ ] Version control for Jenkinsfile

### Kubernetes Agents (if applicable)

- [ ] Pod template defined with required containers
- [ ] Resource limits set (CPU, memory)
- [ ] Service account with minimal permissions
- [ ] Node affinity configured if needed
- [ ] Pod template cached for reuse

---

## Shared Library Checklist

### Structure

- [ ] Dedicated Git repository
- [ ] Standard directory structure (vars/, src/, resources/)
- [ ] Unit tests in test/ directory
- [ ] README with usage examples

### Code Quality

- [ ] All classes implement `Serializable`
- [ ] No override of built-in Pipeline steps
- [ ] Consistent error handling
- [ ] Input validation for all functions
- [ ] Default values for optional parameters

### Configuration

- [ ] Library configured in Jenkins (Manage Jenkins > Configure System)
- [ ] Version pinned in `@Library` annotation
- [ ] Implicit loading disabled (explicit `@Library` required)

### Documentation

- [ ] Each `vars/*.groovy` file documented
- [ ] Parameter descriptions in code
- [ ] Usage examples provided
- [ ] Changelog maintained

---

## Parallel Stages Checklist

- [ ] Independent tasks identified
- [ ] `failFast` behavior defined
- [ ] Resource limits considered
- [ ] Shared resource conflicts resolved
- [ ] Each parallel branch has clear naming
- [ ] Test results aggregated from all branches

---

## Deployment Stage Checklist

### Pre-Deployment

- [ ] Environment-specific configuration externalized
- [ ] Rollback strategy defined
- [ ] Health checks configured
- [ ] Smoke tests ready to run

### Deployment

- [ ] Deployment approval for production (`input` step)
- [ ] Submitter restricted to authorized users
- [ ] Deployment timeout configured
- [ ] Rollout status verified (`kubectl rollout status`)

### Post-Deployment

- [ ] Smoke tests executed
- [ ] Monitoring alerts active
- [ ] Deployment notification sent
- [ ] Audit log updated

---

## Review Questions

### Before Merge

1. Does this pipeline follow the team's standards?
2. Are all credentials handled securely?
3. Will this pipeline scale with increased load?
4. Is the failure path well-defined?
5. Can a new team member understand this pipeline?

### Before Production

1. Has this pipeline been tested in staging?
2. Are all approval gates in place?
3. Is monitoring configured for pipeline metrics?
4. Is there a rollback procedure?
5. Are all stakeholders notified of the deployment?
