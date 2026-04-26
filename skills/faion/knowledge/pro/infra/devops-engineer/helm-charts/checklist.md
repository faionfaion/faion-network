# Helm Charts Checklist

Production readiness checklist for Helm charts based on 2025-2026 best practices.

## Chart Structure

- [ ] `Chart.yaml` with complete metadata
- [ ] `values.yaml` with documented defaults
- [ ] `values.schema.json` for input validation
- [ ] `templates/_helpers.tpl` for reusable functions
- [ ] `templates/NOTES.txt` with post-install instructions
- [ ] `templates/tests/` with test pods
- [ ] Chart version follows SemVer 2

## Naming Conventions

- [ ] Chart name: lowercase letters, numbers, hyphens only
- [ ] Chart name starts with a letter
- [ ] No uppercase letters or underscores in chart name
- [ ] No dots in chart name
- [ ] Template names: `{chart}-{resource}.yaml`

## Values Configuration

- [ ] All configurable values in `values.yaml`
- [ ] No hardcoded values in templates
- [ ] Every value commented/documented
- [ ] Sensible defaults (works out-of-box)
- [ ] Boolean flags for optional features
- [ ] Environment-specific values files (`values-{env}.yaml`)
- [ ] Never use one values file for all environments

## Security

- [ ] `securityContext` for pods and containers
- [ ] `runAsNonRoot: true`
- [ ] `readOnlyRootFilesystem: true`
- [ ] `allowPrivilegeEscalation: false`
- [ ] Drop ALL capabilities by default
- [ ] ServiceAccount with minimal permissions
- [ ] No secrets in values files (use External Secrets)
- [ ] NetworkPolicy enabled
- [ ] Image pull policy: `IfNotPresent` or `Always`

## Reliability

- [ ] Resource requests defined
- [ ] Resource limits defined
- [ ] PodDisruptionBudget configured
- [ ] Pod anti-affinity (spread across nodes/zones)
- [ ] HorizontalPodAutoscaler enabled
- [ ] Sensible HPA minimums (not 1)
- [ ] Liveness probe configured
- [ ] Readiness probe configured
- [ ] Startup probe for slow-starting apps

## Dependencies

- [ ] Dependencies declared in `Chart.yaml`
- [ ] `Chart.lock` committed
- [ ] Conditional dependencies (`condition: dep.enabled`)
- [ ] `helm dependency update` before packaging
- [ ] Dependency versions pinned (not `*`)

## Deployment

- [ ] Use `--atomic` flag for upgrades
- [ ] Use `--timeout` flag
- [ ] ConfigMap/Secret checksum annotations (trigger restart)
- [ ] Rolling update strategy configured
- [ ] Grace period for termination

## Testing

- [ ] `helm lint` passes
- [ ] `helm template` renders correctly
- [ ] Test pods in `templates/tests/`
- [ ] `helm test` passes after install
- [ ] Multiple environment configs tested

## CI/CD Integration

- [ ] Chart packaged and pushed to repository
- [ ] OCI registry for chart storage
- [ ] Automated linting in CI
- [ ] Automated testing in CI
- [ ] Version bumping automated

## Documentation

- [ ] `NOTES.txt` shows access instructions
- [ ] README.md in chart root
- [ ] All values documented in values.yaml
- [ ] Upgrade notes for breaking changes
- [ ] artifacthub.io annotations for discoverability

## Common Pitfalls to Avoid

| Pitfall | Solution |
|---------|----------|
| Hardcoded values in templates | Use values.yaml |
| Missing resource limits | Always define requests/limits |
| Forgetting `helm dep update` | Add to CI pipeline |
| Secrets in values files | Use External Secrets Operator |
| Breaking schema changes | Use deprecation paths |
| No atomic upgrades | Always use `--atomic` |
| Single replica HPA min | Set minReplicas >= 2 |
| No PodDisruptionBudget | Add PDB for HA |
| Assuming popular = reliable | Audit charts yourself |
