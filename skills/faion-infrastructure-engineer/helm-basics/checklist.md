# Helm Basics Checklist

## Chart Development Checklist

### Structure

- [ ] Chart.yaml has all required fields (apiVersion, name, version)
- [ ] Chart.yaml has meaningful description and keywords
- [ ] appVersion reflects actual application version
- [ ] values.yaml has sensible defaults (works out-of-box)
- [ ] values.schema.json validates all required inputs
- [ ] NOTES.txt provides clear post-install instructions
- [ ] _helpers.tpl defines reusable template functions
- [ ] One template file per Kubernetes resource type
- [ ] tests/ folder contains connection tests

### Naming Conventions

- [ ] Template files use `.yaml` extension (not `.yml`)
- [ ] Helper files use `.tpl` extension
- [ ] File names use dashed notation (`my-configmap.yaml`)
- [ ] Defined templates are namespaced (`{{ define "mychart.fullname" }}`)
- [ ] Resource names include release name to avoid collisions

### Values Organization

- [ ] Related values grouped together
- [ ] Descriptive, consistent naming
- [ ] All values documented with comments
- [ ] Environment-specific files separated (`values-dev.yaml`, `values-prod.yaml`)
- [ ] Secrets NOT stored in values files
- [ ] Default values work for development environment

### Templates Quality

- [ ] Two-space indentation (no tabs)
- [ ] Whitespace after `{{` and before `}}`
- [ ] Minimal whitespace in generated output (`{{-` and `-}}`)
- [ ] Template comments for logic (`{{- /* comment */ -}}`)
- [ ] YAML comments for debugging help
- [ ] Conditional logic limited to optional features
- [ ] No hardcoded values in templates

---

## Pre-Deployment Checklist

### Validation

- [ ] `helm lint ./mychart` passes without errors
- [ ] `helm template myrelease ./mychart` generates valid YAML
- [ ] `helm install --dry-run --debug` succeeds
- [ ] JSON Schema validates all provided values

### Security

- [ ] No secrets in values.yaml or environment files
- [ ] Secrets reference Kubernetes Secrets or external managers
- [ ] podSecurityContext configured (runAsNonRoot, fsGroup)
- [ ] securityContext configured (allowPrivilegeEscalation: false)
- [ ] readOnlyRootFilesystem enabled where possible
- [ ] NetworkPolicy defined if required
- [ ] ServiceAccount with minimal permissions

### Resources

- [ ] Resource requests defined for all containers
- [ ] Resource limits defined for all containers
- [ ] HPA configured if autoscaling needed
- [ ] PodDisruptionBudget defined for high availability

### Probes

- [ ] livenessProbe configured with appropriate thresholds
- [ ] readinessProbe configured with appropriate thresholds
- [ ] startupProbe configured for slow-starting applications
- [ ] Probe paths exist and return expected responses

### Dependencies

- [ ] All dependencies listed in Chart.yaml
- [ ] `helm dependency update` executed
- [ ] Dependency conditions documented
- [ ] Subchart configurations tested

---

## Release Management Checklist

### Before Upgrade

- [ ] Review helm history for current state
- [ ] Backup critical data if needed
- [ ] Test upgrade in staging environment first
- [ ] Review CHANGELOG for breaking changes
- [ ] Verify rollback plan

### During Upgrade

- [ ] Use `--atomic` flag for automatic rollback
- [ ] Set appropriate `--timeout`
- [ ] Use correct namespace
- [ ] Apply correct values file for environment

### After Upgrade

- [ ] Verify all pods running and ready
- [ ] Check application health endpoints
- [ ] Verify service endpoints
- [ ] Review pod logs for errors
- [ ] Test critical functionality

### Rollback Procedure

- [ ] Identify target revision (`helm history`)
- [ ] Execute rollback (`helm rollback myrelease <revision>`)
- [ ] Verify rollback success
- [ ] Document incident

---

## Versioning Checklist

### Chart Version (version field)

- [ ] Increment patch for bug fixes
- [ ] Increment minor for new features (backward compatible)
- [ ] Increment major for breaking changes
- [ ] Update Chart.lock after version change

### App Version (appVersion field)

- [ ] Matches actual application version
- [ ] Updated when application image changes
- [ ] Follows application's versioning scheme

### Breaking Changes

- [ ] Documented in CHANGELOG
- [ ] Migration path provided
- [ ] Deprecation warnings in values.yaml
- [ ] Major version incremented

---

## Repository Publishing Checklist

### Before Publishing

- [ ] All tests pass
- [ ] Documentation complete
- [ ] CHANGELOG updated
- [ ] Version bumped appropriately
- [ ] Chart packaged successfully

### Publishing

- [ ] Chart pushed to repository/registry
- [ ] Repository index updated
- [ ] Artifact Hub annotations present (if applicable)
- [ ] Release notes published

---

## Quick Validation Commands

```bash
# Full validation sequence
helm lint ./mychart && \
helm template test ./mychart -f values.yaml && \
helm install test ./mychart --dry-run --debug

# Check rendered output
helm template myrelease ./mychart -f values-prod.yaml | kubectl apply --dry-run=client -f -

# Validate against live cluster
helm install myrelease ./mychart --namespace test --create-namespace --dry-run --debug
```
