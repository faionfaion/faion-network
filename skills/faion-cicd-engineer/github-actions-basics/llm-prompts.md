# LLM Prompts for GitHub Actions

## Workflow Generation

### Create CI Pipeline

```
Create a GitHub Actions CI workflow for a {LANGUAGE} project with:
- Linting
- Unit tests with coverage
- Build step
- Artifact upload

Requirements:
- Use concurrency groups to cancel outdated runs
- Enable workflow_dispatch for manual triggering
- Cache dependencies
- Set appropriate timeouts
- Pin actions to specific versions (not @main or @v1)
- Use minimal GITHUB_TOKEN permissions

Output: Complete .github/workflows/ci.yml
```

### Create CD Pipeline

```
Create a GitHub Actions CD workflow that deploys to {CLOUD_PROVIDER} with:
- Environment protection rules
- OIDC authentication (no long-lived secrets)
- Deployment approval gates
- Rollback capability
- Slack/Teams notifications

Target environments: staging, production
Deployment method: {DEPLOYMENT_METHOD}

Output: Complete .github/workflows/cd.yml
```

### Create Docker Workflow

```
Create a GitHub Actions workflow for Docker image builds:
- Multi-platform support (amd64, arm64)
- Push to GitHub Container Registry
- Semantic versioning tags
- Build cache optimization
- SBOM and provenance attestation

Trigger: Push to main branch and tags

Output: Complete .github/workflows/docker.yml
```

## Workflow Analysis

### Review Workflow Security

```
Review this GitHub Actions workflow for security issues:

{PASTE_WORKFLOW_YAML}

Check for:
1. Unpinned actions (should use SHA, not @main or @v1)
2. GITHUB_TOKEN permissions (should be minimal)
3. Hardcoded secrets
4. Command injection vulnerabilities
5. Third-party action risks
6. Missing concurrency controls

Output: Security findings with severity and remediation steps
```

### Optimize Workflow Performance

```
Analyze this GitHub Actions workflow for performance improvements:

{PASTE_WORKFLOW_YAML}

Check for:
1. Missing dependency caching
2. Unnecessary sequential jobs (could be parallel)
3. Missing fail-fast strategy in matrices
4. Inefficient artifact handling
5. Missing job timeouts
6. Redundant steps

Output: Performance recommendations with expected impact
```

### Debug Workflow Failure

```
This GitHub Actions workflow is failing with the following error:

Workflow: {PASTE_WORKFLOW_YAML}

Error output:
{PASTE_ERROR_LOG}

Context:
- Repository: {REPO_URL}
- Branch: {BRANCH}
- Recent changes: {CHANGES_DESCRIPTION}

Analyze the error and provide:
1. Root cause
2. Step-by-step fix
3. Prevention measures
```

## Specific Tasks

### Convert Pipeline

```
Convert this {SOURCE_CI_SYSTEM} pipeline to GitHub Actions:

{PASTE_SOURCE_PIPELINE}

Requirements:
- Preserve all functionality
- Use GitHub Actions best practices
- Add caching where appropriate
- Use native GitHub features (environments, secrets)

Output: Complete .github/workflows/*.yml files
```

### Add Matrix Build

```
Add matrix testing to this workflow:

{PASTE_WORKFLOW_YAML}

Matrix dimensions:
- Operating systems: {OS_LIST}
- Language versions: {VERSION_LIST}

Requirements:
- Use fail-fast: false
- Add exclusions for known incompatible combinations
- Enable coverage on one combination only

Output: Updated workflow with matrix strategy
```

### Create Reusable Workflow

```
Extract reusable workflow from these workflows:

Workflow 1: {PASTE_WORKFLOW_1}
Workflow 2: {PASTE_WORKFLOW_2}

Identify common patterns and create:
1. Reusable workflow (.github/workflows/reusable-*.yml)
2. Updated caller workflows

Requirements:
- Proper input/secret definitions
- Output passing between jobs
- Environment support
```

### Add Security Scanning

```
Add security scanning to this CI workflow:

{PASTE_WORKFLOW_YAML}

Include:
1. Dependency vulnerability scanning (Trivy/Snyk)
2. Static code analysis (CodeQL/Semgrep)
3. Secret detection (GitLeaks/TruffleHog)
4. Container scanning (if Docker)

Requirements:
- Run in parallel with existing jobs
- Fail on critical/high vulnerabilities
- Upload results to GitHub Security tab

Output: Updated workflow with security jobs
```

### Create Composite Action

```
Create a composite action that encapsulates:

{DESCRIBE_COMMON_STEPS}

Requirements:
- Accept configurable inputs
- Provide useful outputs
- Include proper documentation
- Handle errors gracefully

Output: .github/actions/{ACTION_NAME}/action.yml
```

## Maintenance

### Update Action Versions

```
Update all actions in this workflow to latest secure versions:

{PASTE_WORKFLOW_YAML}

Requirements:
- Pin to full commit SHA
- Include version comment (e.g., # v4.1.1)
- Verify compatibility
- List breaking changes

Output: Updated workflow with version comments
```

### Add Observability

```
Add observability to this workflow:

{PASTE_WORKFLOW_YAML}

Include:
1. Job summary with key metrics
2. Annotations for warnings/errors
3. Build time tracking
4. Custom metrics output

Output: Updated workflow with observability steps
```

## Prompt Patterns

### System Context

```
You are a GitHub Actions expert. Follow these guidelines:
- Always pin actions to full commit SHA
- Use minimal GITHUB_TOKEN permissions
- Enable concurrency controls
- Cache dependencies appropriately
- Set job timeouts
- Never hardcode secrets
- Prefer OIDC for cloud authentication
```

### Output Format

```
Respond with:
1. Complete YAML workflow (code block)
2. Brief explanation of key decisions
3. Security considerations
4. Required secrets/variables to configure
```

### Iteration Pattern

```
I need to iterate on a GitHub Actions workflow.

Current workflow:
{PASTE_CURRENT_YAML}

Change requested:
{DESCRIBE_CHANGE}

Constraints:
{ANY_CONSTRAINTS}

Output: Updated workflow with changes highlighted
```

---

*LLM prompts for GitHub Actions tasks*
