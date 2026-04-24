# Helm Charts LLM Prompts

Ready-to-use prompts for Helm chart development tasks.

## Chart Creation

### Create New Helm Chart

```
Create a production-ready Helm chart for [APPLICATION_NAME] with:

Application details:
- Type: [web app / API / worker / cronjob]
- Port: [PORT]
- Health endpoints: [/health/live, /health/ready]

Requirements:
1. Chart.yaml with complete metadata
2. values.yaml with:
   - Security context (non-root, read-only, drop capabilities)
   - Resource requests/limits
   - HPA configuration
   - Pod Disruption Budget
   - Network Policy
3. Templates:
   - deployment.yaml with probes
   - service.yaml
   - ingress.yaml (optional)
   - hpa.yaml
   - pdb.yaml
   - networkpolicy.yaml
   - configmap.yaml
   - _helpers.tpl
   - NOTES.txt
4. values.schema.json for validation
5. Environment-specific values files (dev, prod)

Follow Helm best practices 2025-2026.
```

### Add Dependency to Chart

```
Add [DEPENDENCY_NAME] as a dependency to my Helm chart.

Current Chart.yaml:
[PASTE CHART.YAML]

Requirements:
1. Add dependency with condition flag
2. Configure subchart values in values.yaml
3. Pin version appropriately (not wildcard)
4. Add documentation comments
```

## Values Configuration

### Generate values.yaml

```
Generate a comprehensive values.yaml for a [APPLICATION_TYPE] Helm chart.

Include:
1. Global settings (imageRegistry, imagePullSecrets)
2. Image configuration (repository, tag, pullPolicy)
3. ServiceAccount settings
4. Pod and container security contexts
5. Service configuration
6. Ingress with TLS
7. Resources (requests/limits)
8. Autoscaling (HPA)
9. All three probes (liveness, readiness, startup)
10. Environment variables (env, envFrom)
11. ConfigMap data
12. Persistence settings
13. Node selection (nodeSelector, tolerations, affinity)
14. Pod anti-affinity for HA
15. Pod Disruption Budget
16. Network Policy

Add documentation comments for every value.
```

### Create values.schema.json

```
Generate values.schema.json for this values.yaml:

[PASTE VALUES.YAML]

Requirements:
1. Define types for all values
2. Add descriptions
3. Mark required fields
4. Add enum constraints where applicable
5. Add minimum/maximum constraints for numbers
```

## Template Development

### Create _helpers.tpl

```
Create _helpers.tpl template for chart named [CHART_NAME].

Include:
1. name - chart name
2. fullname - fully qualified name
3. chart - chart name and version
4. labels - common labels
5. selectorLabels - selector labels
6. serviceAccountName - service account name
7. image - full image reference
8. configChecksum - checksum for restart on config change
```

### Create Deployment Template

```
Create deployment.yaml template with:

1. Rolling update strategy
2. Config checksum annotation (restart on change)
3. Pod and container security contexts
4. All three probes
5. Resource limits
6. Environment variables from values
7. Volume mounts (if persistence enabled)
8. Pod anti-affinity (configurable soft/hard)
9. Topology spread constraints
10. Termination grace period
```

### Create Network Policy

```
Create networkpolicy.yaml template that:

1. Allows ingress from nginx-ingress namespace
2. Allows ingress from same namespace
3. Allows DNS egress
4. Allows egress to same namespace
5. Supports additional rules from values
```

## Chart Validation

### Review Helm Chart

```
Review this Helm chart for production readiness.

[PASTE CHART STRUCTURE OR FILES]

Check for:
1. Security issues (root user, privileged, missing caps drop)
2. Missing resource limits
3. Missing probes
4. Hardcoded values in templates
5. Missing PDB for HA
6. Missing pod anti-affinity
7. HPA minReplicas < 2
8. Missing network policy
9. Values documentation
10. Schema validation

Provide specific fixes for each issue found.
```

### Fix Helm Lint Errors

```
Fix these helm lint errors:

[PASTE LINT OUTPUT]

Chart files:
[PASTE RELEVANT FILES]
```

## CI/CD Integration

### GitHub Actions for Helm

```
Create GitHub Actions workflow for Helm chart CI/CD.

Requirements:
1. Lint chart on PR
2. Template validation
3. Run helm test
4. Package chart on merge to main
5. Push to OCI registry
6. Create GitHub release

Chart path: [CHART_PATH]
Registry: [REGISTRY_URL]
```

### ArgoCD Application

```
Create ArgoCD Application manifest for Helm chart.

Details:
- Chart: [CHART_NAME]
- Repository: [REPO_URL]
- Target revision: [VERSION]
- Namespace: [NAMESPACE]
- Values files: values.yaml, values-[ENV].yaml

Include:
1. Sync policy (automated, self-heal, prune)
2. Sync options
3. Health checks
```

## Debugging

### Debug Helm Template

```
Debug why this Helm template is not rendering correctly.

Template:
[PASTE TEMPLATE]

Values:
[PASTE VALUES]

Expected output:
[DESCRIBE EXPECTED]

Actual output:
[PASTE ACTUAL OR ERROR]
```

### Troubleshoot Helm Upgrade

```
Troubleshoot this Helm upgrade failure.

Error:
[PASTE ERROR]

Release:
- Name: [RELEASE_NAME]
- Namespace: [NAMESPACE]
- Chart: [CHART_NAME]

Commands tried:
[LIST COMMANDS]

Provide step-by-step resolution.
```

## Migration

### Convert Kustomize to Helm

```
Convert this Kustomize configuration to a Helm chart.

[PASTE KUSTOMIZE FILES]

Requirements:
1. Extract all configurable values
2. Create proper templates with helpers
3. Add values.yaml with defaults
4. Add documentation
```

### Upgrade Chart for Helm 4

```
Upgrade this Helm chart for Helm v4 compatibility.

[PASTE CHART FILES]

Check and update:
1. apiVersion in Chart.yaml
2. Deprecated template functions
3. New features to leverage
4. Best practices changes
```

## Quick Reference

| Task | Key Points |
|------|------------|
| New chart | Security, probes, resources, PDB, HPA |
| Add dependency | Condition flag, pin version, configure in values |
| Values file | Document every value, sensible defaults |
| Schema | Types, descriptions, constraints |
| Helpers | Reusable functions, consistent naming |
| Deployment | Checksum, probes, anti-affinity, graceful shutdown |
| Network policy | Ingress rules, DNS egress, same-namespace |
| Review | Security, reliability, documentation |
