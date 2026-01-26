# Helm Basics LLM Prompts

AI-ready prompts for Helm chart development tasks.

---

## Chart Creation

### Create New Helm Chart

```
Create a Helm chart for a [APPLICATION_TYPE] application with:

Application details:
- Name: [APP_NAME]
- Container image: [IMAGE_REPO]:[TAG]
- Container port: [PORT]
- Health endpoints: /health/live, /health/ready

Requirements:
- Production-ready security contexts
- Resource limits and requests
- HPA with CPU/memory scaling
- Ingress with TLS
- ConfigMap for environment variables
- PodDisruptionBudget
- NetworkPolicy

Include:
1. Chart.yaml with proper metadata
2. values.yaml with documented defaults
3. _helpers.tpl with standard functions
4. All necessary template files
5. NOTES.txt with access instructions
6. Test pod for connection verification

Follow Helm best practices:
- Semantic versioning
- Namespaced template definitions
- Checksum annotations for ConfigMap changes
- Optional features via conditions
```

### Convert Kubernetes Manifests to Helm Chart

```
Convert these Kubernetes manifests to a Helm chart:

[PASTE MANIFESTS HERE]

Requirements:
1. Extract hardcoded values to values.yaml
2. Create _helpers.tpl with name/label functions
3. Add standard Kubernetes labels
4. Make resources configurable (replicas, resources, etc.)
5. Add conditions for optional resources
6. Include NOTES.txt

Follow best practices:
- Group related values logically
- Document all values with comments
- Use consistent naming conventions
- Add resource limits if missing
```

---

## Values Configuration

### Design values.yaml Structure

```
Design a values.yaml structure for a [APPLICATION_TYPE] with:

Components:
- [LIST COMPONENTS]

Environments:
- Development
- Staging
- Production

Requirements:
1. Logical grouping of related values
2. Sensible defaults for development
3. Comments explaining each value
4. Support for:
   - Multiple replicas
   - Resource limits
   - Ingress with TLS
   - Autoscaling
   - External secrets reference
   - Database connections
   - Feature flags

Output:
- Complete values.yaml with comments
- values-dev.yaml overrides
- values-prod.yaml overrides
```

### Create values.schema.json

```
Create a values.schema.json for this values.yaml:

[PASTE VALUES.YAML]

Requirements:
1. Define types for all values
2. Mark required fields
3. Add validation constraints:
   - Minimum/maximum for numbers
   - Enum for predefined options
   - Pattern for strings where applicable
4. Include descriptions from comments
5. Set appropriate defaults
```

---

## Template Development

### Create Template with Best Practices

```
Create a Helm template for [RESOURCE_TYPE] with:

Purpose: [DESCRIBE PURPOSE]

Features needed:
- [LIST FEATURES]

Requirements:
1. Use helper functions for names and labels
2. Two-space indentation
3. Proper whitespace management ({{- and -}})
4. Conditional sections for optional features
5. toYaml for complex nested values
6. Quote strings appropriately
7. Include both YAML and template comments

The template should handle:
- Missing optional values gracefully
- Empty arrays/maps
- Boolean conditions
```

### Create _helpers.tpl Functions

```
Create _helpers.tpl template helpers for chart "[CHART_NAME]" with:

Required functions:
1. name - Chart name with override support
2. fullname - Release-qualified name
3. chart - Chart name and version
4. labels - Common labels
5. selectorLabels - Pod selector labels
6. serviceAccountName - SA name with creation check
7. image - Full image name with tag

Additional functions:
- [LIST ANY CUSTOM HELPERS NEEDED]

Follow conventions:
- Namespace all definitions with chart name
- Truncate to 63 chars for K8s limits
- Handle edge cases (overrides, contains checks)
```

---

## Debugging and Troubleshooting

### Debug Helm Template Issues

```
Debug this Helm template error:

Command: [HELM COMMAND]
Error: [ERROR MESSAGE]

Template:
[PASTE TEMPLATE]

Values:
[PASTE RELEVANT VALUES]

Analyze:
1. What is causing the error?
2. How to fix it?
3. What best practices were violated?
4. Provide corrected template
```

### Review Helm Chart for Issues

```
Review this Helm chart for issues:

Chart.yaml:
[PASTE CHART.YAML]

values.yaml:
[PASTE VALUES.YAML]

templates/deployment.yaml:
[PASTE DEPLOYMENT]

Check for:
1. Security issues
2. Missing best practices
3. Potential runtime problems
4. Template bugs
5. Values that should be configurable
6. Missing resources (probes, limits, etc.)

Provide:
- List of issues with severity
- Recommended fixes
- Improved code where needed
```

---

## Release Management

### Create Release Strategy

```
Create a Helm release strategy for:

Application: [APP_NAME]
Environments: [dev, staging, prod]
CI/CD: [GitHub Actions / GitLab CI / ArgoCD / Flux]

Requirements:
1. Values file organization
2. Release naming conventions
3. Namespace strategy
4. Upgrade process with --atomic
5. Rollback procedures
6. Testing strategy

Output:
- Directory structure
- CI/CD configuration
- Release commands for each environment
- Rollback commands
```

### Migrate Helm 2 to Helm 3

```
Migrate this Helm 2 chart to Helm 3:

[PASTE CHART FILES]

Changes needed:
1. Update apiVersion to v2
2. Remove Tiller references
3. Update deprecated APIs
4. Fix any template syntax changes
5. Update hooks if needed

Provide:
- Updated Chart.yaml
- Updated templates
- Migration steps
- Testing commands
```

---

## Dependencies

### Configure Chart Dependencies

```
Configure Helm dependencies for [CHART_NAME]:

Dependencies needed:
- [DEPENDENCY 1]: [VERSION]
- [DEPENDENCY 2]: [VERSION]

Requirements:
1. Add to Chart.yaml
2. Configure conditions for enabling/disabling
3. Set up values for each dependency
4. Handle shared configurations

Output:
- Updated Chart.yaml
- Updated values.yaml with dependency configs
- Commands to update dependencies
```

### Create Library Chart

```
Create a library chart for shared templates:

Shared across charts: [LIST CHARTS]

Common elements:
- [LIST COMMON TEMPLATES]

Requirements:
1. Chart.yaml with type: library
2. Reusable template functions
3. Documentation for usage
4. Version strategy

Show:
- Library chart structure
- How to include in application charts
- Example usage in templates
```

---

## GitOps Integration

### ArgoCD Application for Helm

```
Create ArgoCD Application for Helm chart:

Chart: [CHART_NAME]
Repository: [REPO_URL]
Environments: [dev, staging, prod]

Requirements:
1. ApplicationSet for multiple environments
2. Values file per environment
3. Auto-sync with pruning
4. Health checks
5. Sync waves if needed

Output:
- ArgoCD Application manifests
- Repository structure
- Values organization
```

### Flux HelmRelease

```
Create Flux HelmRelease for:

Chart: [CHART_NAME] from [REPOSITORY]
Namespace: [NAMESPACE]
Values from: [ConfigMap / Secret / inline]

Requirements:
1. HelmRepository source
2. HelmRelease with version constraint
3. Values override strategy
4. Remediation on failure

Output:
- HelmRepository manifest
- HelmRelease manifest
- Kustomization if needed
```

---

## Security

### Secure Helm Chart

```
Secure this Helm chart:

[PASTE CHART FILES]

Apply security best practices:
1. Pod security contexts
2. Container security contexts
3. Network policies
4. Service account with minimal permissions
5. Secret management (external secrets)
6. Read-only root filesystem
7. Non-root user
8. Dropped capabilities

Output:
- Updated templates
- Security-focused values
- RBAC templates if needed
```

### External Secrets Integration

```
Add External Secrets Operator integration to chart:

Secret provider: [AWS Secrets Manager / Vault / etc.]
Secrets needed:
- [SECRET_1]: [PATH]
- [SECRET_2]: [PATH]

Requirements:
1. ExternalSecret template
2. Values for configuration
3. Conditional creation
4. Documentation

Output:
- ExternalSecret template
- Updated values.yaml
- Usage instructions
```

---

## Testing

### Create Helm Test Suite

```
Create comprehensive tests for chart [CHART_NAME]:

Test types needed:
1. Connection test (basic)
2. API health check
3. Database connectivity
4. Feature verification

Requirements:
- helm.sh/hook: test annotations
- Cleanup policies
- Meaningful test names
- Clear pass/fail criteria

Output:
- Test pod templates
- Testing instructions
- CI integration example
```

### Validate Chart with ct (chart-testing)

```
Create chart-testing configuration for [CHART_NAME]:

Requirements:
1. ct.yaml configuration
2. Test values for different scenarios
3. CI workflow integration
4. Lint and install tests

Output:
- ct.yaml
- Test values files
- GitHub Actions / GitLab CI workflow
```

---

## Documentation

### Generate Chart Documentation

```
Generate documentation for this Helm chart:

[PASTE CHART.YAML AND VALUES.YAML]

Include:
1. README.md with:
   - Description
   - Prerequisites
   - Installation commands
   - Configuration table (all values)
   - Examples
   - Upgrading notes
2. CHANGELOG.md structure
3. CONTRIBUTING.md if applicable

Format:
- Markdown tables for values
- Code blocks for examples
- Clear headings
```
