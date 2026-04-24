# Helm Advanced LLM Prompts

Prompt templates for generating Helm advanced patterns with LLMs.

## Library Chart Creation

### Create Library Chart

```
Create a Helm library chart named "{LIBRARY_NAME}" that provides reusable templates for:

Requirements:
- Chart type: library
- Templates needed: {LIST_TEMPLATES}
- Naming convention: {LIBRARY_NAME}.{resource}

Include:
1. Chart.yaml with type: library
2. _helpers.tpl with standard helpers (name, fullname, labels, selectorLabels)
3. _util.tpl with merge utility for template inheritance
4. Template files for each resource type with base definitions
5. Documentation in README.md

The library should follow Bitnami common chart patterns where consuming charts can override specific sections.

Context:
- Target Helm version: 3.x
- Kubernetes version: 1.25+
```

### Extend Library Chart

```
I have a library chart "{LIBRARY_NAME}" that provides base templates.

Create a consuming chart "{CHART_NAME}" that:
1. Adds library as dependency
2. Uses library templates: {LIST_TEMPLATES}
3. Overrides these sections: {OVERRIDE_SECTIONS}

The chart deploys: {APPLICATION_DESCRIPTION}

Provide:
1. Chart.yaml with dependency
2. values.yaml with sensible defaults
3. Template files that use and extend library templates
4. Instructions to run helm dependency update
```

---

## Hook Generation

### Database Migration Hook

```
Create a Helm hook for database migrations with these specifications:

Hook type: pre-install, pre-upgrade
Application: {APP_TYPE} (Django/Rails/Node.js/Go/etc.)
Database: {DB_TYPE} (PostgreSQL/MySQL/MongoDB)
Migration command: {COMMAND}

Requirements:
- Hook weight: -5 (run before main deployment)
- Deletion policy: before-hook-creation, hook-succeeded
- backoffLimit: 3
- ttlSecondsAfterFinished: 300
- Use same image as main deployment
- Read database credentials from existing secret

Include:
1. Job manifest with all annotations
2. Required RBAC if needed
3. values.yaml section for configuration
4. Documentation for the hook
```

### Cleanup Hook

```
Create a pre-delete Helm hook that cleans up external resources:

Resources to clean:
{LIST_RESOURCES}

Requirements:
- Hook weight: 0
- Deletion policy: hook-succeeded, hook-failed
- Use kubectl or custom cleanup script
- Log all cleanup actions
- Handle failures gracefully

Provide:
1. Job manifest with cleanup script
2. ServiceAccount and RBAC if needed
3. ConfigMap for cleanup script (if complex)
4. values.yaml section for configuration
```

### Post-Deploy Notification Hook

```
Create a post-install/post-upgrade hook that sends deployment notifications.

Notification target: {TARGET} (Slack/Teams/Discord/Webhook)
Include in notification:
- Release name
- Namespace
- Version
- Environment
- Deployment timestamp

Requirements:
- Hook weight: 10 (run after everything)
- Deletion policy: hook-succeeded
- backoffLimit: 1
- Use minimal image (curl)

Provide:
1. Job manifest
2. Secret for webhook URL (optional)
3. values.yaml section
```

---

## Test Generation

### Comprehensive Test Suite

```
Create a Helm test suite for chart "{CHART_NAME}" that validates:

1. Service connectivity (HTTP health check)
2. API functionality (specific endpoints)
3. Database connectivity (if applicable)
4. Redis/cache connectivity (if applicable)
5. Authentication (if applicable)

Chart details:
- Service port: {PORT}
- Health endpoint: {HEALTH_PATH}
- API endpoints to test: {ENDPOINTS}
- Database type: {DB_TYPE}
- Cache type: {CACHE_TYPE}

Requirements:
- Each test in separate file under templates/tests/
- Use hook weights for ordering
- Exit 0 on success, non-zero on failure
- Include helpful error messages
- Use appropriate base images

Provide all test Pod manifests and document how to run tests.
```

### API Contract Test

```
Create a Helm test that validates API contract for "{CHART_NAME}".

API specifications:
- Base URL: http://{SERVICE_NAME}:{PORT}
- Endpoints to test:
  {ENDPOINT_LIST_WITH_EXPECTED_RESPONSES}

Requirements:
- Validate HTTP status codes
- Validate response structure (using jq)
- Test with both valid and invalid inputs
- Timeout: 30 seconds per request
- Use curlimages/curl or similar minimal image

Provide:
1. Test Pod manifest
2. Script that performs all validations
3. Clear pass/fail output for each test
```

---

## Umbrella Chart Creation

### Create Umbrella Chart

```
Create a Helm umbrella chart named "{UMBRELLA_NAME}" that composes:

Components:
{LIST_COMPONENTS_WITH_DESCRIPTIONS}

External dependencies:
- PostgreSQL (Bitnami)
- Redis (Bitnami)
- {OTHER_DEPS}

Requirements:
- Global values for shared configuration
- Conditions for optional components
- Environment-specific overrides (dev, staging, prod)
- Proper value scoping for subcharts

Provide:
1. Chart.yaml with all dependencies
2. values.yaml with full configuration
3. values-dev.yaml, values-staging.yaml, values-prod.yaml
4. README.md with deployment instructions
5. NOTES.txt with useful post-install commands
```

### Migrate to Umbrella Pattern

```
I have multiple Helm charts that deploy related components:
{LIST_EXISTING_CHARTS}

Help me refactor into an umbrella chart pattern:

Requirements:
- Maintain backward compatibility
- Extract common templates to library chart
- Create umbrella for composed deployment
- Keep ability to deploy components individually
- Version strategy: {1-1 or independent}

Provide:
1. Refactoring plan (step by step)
2. Library chart structure
3. Umbrella chart structure
4. Migration guide for existing deployments
```

---

## Template Helper Generation

### Custom Helpers

```
Create custom Helm template helpers for "{CHART_NAME}" that provide:

Required helpers:
{LIST_HELPER_FUNCTIONS_WITH_DESCRIPTIONS}

Example helper needs:
- {HELPER_1}: {DESCRIPTION_AND_INPUTS}
- {HELPER_2}: {DESCRIPTION_AND_INPUTS}

Requirements:
- Follow Helm naming conventions
- Include documentation comments
- Handle edge cases (empty values, missing keys)
- Use default values where appropriate

Provide _helpers.tpl with all requested functions and usage examples.
```

### Global Configuration Helper

```
Create Helm helpers for managing global configuration across an umbrella chart.

Global config includes:
- Image registry and pull secrets
- Environment variables
- Resource defaults
- Security context defaults
- Affinity/tolerations defaults

Requirements:
- Helpers should work in both parent and subcharts
- Allow overrides at subchart level
- Merge logic for complex structures

Provide:
1. _globals.tpl with all helpers
2. Example usage in deployment template
3. values.yaml structure that supports this
```

---

## Debugging and Validation

### Debug Template Issues

```
I'm getting this error when rendering my Helm chart:
{ERROR_MESSAGE}

Relevant template section:
```
{TEMPLATE_CODE}
```

Values used:
```yaml
{VALUES_YAML}
```

Help me:
1. Identify the cause of the error
2. Fix the template
3. Explain what went wrong
4. Suggest best practices to avoid this
```

### Validate Chart Structure

```
Review this Helm chart structure and identify issues:

Chart.yaml:
```yaml
{CHART_YAML}
```

values.yaml:
```yaml
{VALUES_YAML}
```

Key template (deployment.yaml):
```yaml
{DEPLOYMENT_TEMPLATE}
```

Check for:
1. Best practice violations
2. Security issues
3. Maintainability concerns
4. Missing common patterns
5. Potential runtime issues

Provide:
1. List of issues found
2. Recommended fixes for each
3. General improvement suggestions
```

---

## CI/CD Integration

### GitHub Actions for Helm

```
Create a GitHub Actions workflow for Helm chart CI/CD:

Repository structure:
- charts/{CHART_NAME}/

Requirements:
- Lint charts on PR
- Template validation
- Run helm test on merge to main
- Package and publish to {REGISTRY_TYPE}
- Semantic versioning based on commits

Provide:
1. .github/workflows/helm-ci.yaml
2. .github/workflows/helm-release.yaml
3. Required secrets documentation
4. Chart README updates
```

### ArgoCD Application

```
Create ArgoCD Application manifests for deploying "{CHART_NAME}":

Environments:
- dev (auto-sync)
- staging (manual sync)
- prod (manual sync with approval)

Requirements:
- Use Helm chart from {REPOSITORY}
- Environment-specific values files
- Health checks configured
- Sync waves for dependencies
- Notifications on sync status

Provide:
1. Application manifest per environment
2. AppProject with appropriate permissions
3. Values files per environment
4. Documentation for rollback procedures
```

---

## Migration Scenarios

### Migrate from Kustomize to Helm

```
Help me migrate this Kustomize deployment to Helm:

Current Kustomize structure:
{KUSTOMIZE_STRUCTURE}

Key manifests:
{MANIFEST_EXAMPLES}

Requirements:
- Preserve all existing functionality
- Make configurable: {LIST_CONFIG_POINTS}
- Add standard Helm patterns (helpers, NOTES.txt)
- Support multiple environments

Provide:
1. Complete Helm chart structure
2. Mapping of Kustomize overlays to values files
3. Migration checklist
4. Testing plan
```

### Upgrade Helm Chart to v3 Patterns

```
I have a Helm chart created for Helm 2. Help me modernize it:

Current Chart.yaml:
```yaml
{CURRENT_CHART_YAML}
```

Current patterns used:
{LIST_PATTERNS}

Requirements:
- Update to apiVersion: v2
- Remove deprecated patterns
- Add library chart dependencies if beneficial
- Implement hooks where appropriate
- Add comprehensive tests

Provide:
1. Updated Chart.yaml
2. List of changes needed
3. Updated templates with modern patterns
4. Test manifests
```
