# Helm Advanced Checklist

## Library Chart Setup

- [ ] Create chart scaffold: `helm create mylibchart`
- [ ] Remove template YAML files (keep `_*.tpl`)
- [ ] Remove `values.yaml`
- [ ] Set `type: library` in Chart.yaml
- [ ] Define named templates with `define`
- [ ] Implement merge utility for overrides
- [ ] Test with `helm lint`
- [ ] Document expected override patterns

## Hooks Implementation

### Pre-Install Hook

- [ ] Create Job manifest in `templates/`
- [ ] Add annotation: `"helm.sh/hook": pre-install`
- [ ] Set hook weight: `"helm.sh/hook-weight": "0"`
- [ ] Define deletion policy: `"helm.sh/hook-delete-policy": before-hook-creation`
- [ ] Set appropriate `backoffLimit`
- [ ] Configure `ttlSecondsAfterFinished` for cleanup
- [ ] Test with `helm install --dry-run`

### Post-Install Hook

- [ ] Add annotation: `"helm.sh/hook": post-install`
- [ ] Consider using `hook-succeeded` deletion policy
- [ ] Verify hook executes after main resources
- [ ] Test with actual installation

### Database Migration Hook

- [ ] Use `pre-upgrade` for migrations
- [ ] Set negative weight to run first: `"helm.sh/hook-weight": "-5"`
- [ ] Handle migration failures gracefully
- [ ] Consider idempotent migrations
- [ ] Test rollback behavior

### Cleanup Hook

- [ ] Use `pre-delete` or `post-delete`
- [ ] Set `"helm.sh/hook-delete-policy": hook-succeeded`
- [ ] Handle external resource cleanup
- [ ] Log cleanup actions

## Chart Tests

### Test Pod Setup

- [ ] Create `templates/tests/` directory
- [ ] Add annotation: `"helm.sh/hook": test`
- [ ] Set `restartPolicy: Never`
- [ ] Use minimal base image (busybox, alpine)
- [ ] Exit 0 on success, non-zero on failure

### Test Coverage

- [ ] Service connectivity test
- [ ] Health endpoint validation
- [ ] Configuration injection verification
- [ ] Authentication test (if applicable)
- [ ] Database connectivity (if applicable)

### Test Execution

- [ ] Wait for deployment ready before testing
- [ ] Run: `helm test <release>`
- [ ] Review test pod logs on failure
- [ ] Add `tests/` to `.helmignore`

## Umbrella Chart Setup

### Structure

- [ ] Create parent chart: `helm create umbrella`
- [ ] Add subcharts to `charts/` directory
- [ ] Define dependencies in Chart.yaml
- [ ] Configure global values
- [ ] Set subchart-specific values with proper scoping

### Dependencies

- [ ] Add each subchart to dependencies
- [ ] Specify version constraints
- [ ] Add conditions for optional subcharts
- [ ] Run `helm dependency update`
- [ ] Verify `Chart.lock` generated

### Value Inheritance

- [ ] Define `global:` section for shared values
- [ ] Scope subchart values under their name
- [ ] Test value precedence
- [ ] Document value structure

### Versioning

- [ ] Decide versioning strategy (1-1 or independent)
- [ ] Document version bump criteria
- [ ] Keep dependencies updated
- [ ] Test upgrades between versions

## Template Helpers

### Standard Helpers

- [ ] `<chart>.name` - truncated chart name
- [ ] `<chart>.fullname` - qualified release name
- [ ] `<chart>.chart` - chart name and version
- [ ] `<chart>.labels` - common labels
- [ ] `<chart>.selectorLabels` - selector labels
- [ ] `<chart>.serviceAccountName` - SA name logic

### Advanced Helpers

- [ ] Image name construction with registry
- [ ] Resource requirement merging
- [ ] Conditional annotation generation
- [ ] Environment variable formatting

## Quality Gates

### Before Publishing

- [ ] `helm lint ./chart` passes
- [ ] `helm template` renders correctly
- [ ] All required values documented
- [ ] NOTES.txt provides useful output
- [ ] README.md complete
- [ ] Tests pass in CI

### Security Checks

- [ ] No hardcoded secrets
- [ ] SecurityContext defined
- [ ] RunAsNonRoot when possible
- [ ] ReadOnlyRootFilesystem considered
- [ ] Resource limits set

### Compatibility

- [ ] Tested with target K8s versions
- [ ] API versions correct for K8s target
- [ ] Helm version requirements documented
- [ ] Subchart version compatibility verified

## CI/CD Integration

- [ ] Lint in PR pipeline
- [ ] Template validation
- [ ] Run helm tests post-deploy
- [ ] Automated version bumping
- [ ] Chart publishing to repository
- [ ] Integration tests with real cluster
