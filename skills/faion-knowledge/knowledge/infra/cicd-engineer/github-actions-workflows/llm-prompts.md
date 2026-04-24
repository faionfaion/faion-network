# LLM Prompts for GitHub Actions Workflows

Prompts for AI-assisted generation and optimization of GitHub Actions workflows.

## Workflow Generation Prompts

### Generate CI Workflow

```
Generate a GitHub Actions CI workflow for a {LANGUAGE} project with the following requirements:
- Triggers: push to main, pull requests
- Jobs: lint, test, build
- Matrix testing for {VERSIONS}
- Caching for dependencies
- Code coverage upload to Codecov
- Concurrency to cancel redundant runs

Use actions/checkout@v4, actions/setup-{LANGUAGE}@v4, actions/cache@v4.
Pin all third-party actions to SHA commits.
Add appropriate permissions block.
```

### Generate CD Workflow

```
Generate a GitHub Actions CD workflow for deploying to {PLATFORM} with:
- Environments: staging (auto-deploy), production (manual approval)
- Docker image build with multi-platform support (amd64, arm64)
- Push to GitHub Container Registry
- Deployment using {DEPLOYMENT_METHOD}
- Health check and smoke tests
- Slack notifications on failure
- Sentry release creation

Use OIDC for cloud authentication (no long-lived credentials).
Include rollback strategy for failed deployments.
```

### Generate Release Workflow

```
Generate a GitHub Actions release workflow triggered by version tags (v*) that:
- Generates changelog using git-cliff
- Creates GitHub Release with changelog body
- Marks as pre-release for alpha/beta/rc tags
- Publishes package to {REGISTRY}
- Builds and pushes Docker image with version tag
- Supports multi-platform builds

Include proper permissions for contents:write and packages:write.
```

### Generate Matrix Workflow

```
Generate a GitHub Actions workflow with matrix strategy for testing:
- Operating systems: {OS_LIST}
- Language versions: {VERSION_LIST}
- Exclude combinations: {EXCLUSIONS}
- Include special configuration: {INCLUSIONS}

Set fail-fast: false for comprehensive results.
Upload coverage only from one matrix combination.
Use matrix variable in artifact names.
```

## Optimization Prompts

### Optimize Workflow Performance

```
Analyze this GitHub Actions workflow and optimize for performance:

```yaml
{WORKFLOW_CONTENT}
```

Consider:
1. Caching opportunities (dependencies, build artifacts)
2. Parallel job execution
3. Conditional steps to skip unnecessary work
4. Checkout depth optimization
5. Matrix strategy improvements
6. Concurrency settings

Provide the optimized workflow with comments explaining changes.
```

### Add Caching

```
Add caching to this GitHub Actions workflow for {PACKAGE_MANAGER}:

```yaml
{WORKFLOW_CONTENT}
```

Use actions/cache@v4 with appropriate:
- Cache paths for {PACKAGE_MANAGER}
- Key pattern including OS and lockfile hash
- Restore keys for partial matches
- Cache hit detection for conditional steps
```

### Convert to Reusable Workflow

```
Convert this GitHub Actions workflow into a reusable workflow:

```yaml
{WORKFLOW_CONTENT}
```

Create:
1. Reusable workflow with workflow_call trigger
2. Inputs for all configurable values
3. Secrets section for sensitive values
4. Outputs for downstream workflows
5. Example caller workflow

Follow best practices for reusable workflow design.
```

## Security Prompts

### Security Audit

```
Audit this GitHub Actions workflow for security issues:

```yaml
{WORKFLOW_CONTENT}
```

Check for:
1. Actions pinned to SHA vs tags
2. GITHUB_TOKEN permission scope
3. Secrets exposure in logs
4. Third-party action trust
5. Script injection vulnerabilities
6. Environment protection rules
7. OIDC usage for cloud auth

Provide remediation for each issue found.
```

### Add OIDC Authentication

```
Convert this workflow from using long-lived credentials to OIDC authentication for {CLOUD_PROVIDER}:

```yaml
{WORKFLOW_CONTENT}
```

Include:
1. Required permissions (id-token: write)
2. OIDC configuration for {CLOUD_PROVIDER}
3. Trust policy requirements (for reference)
4. Error handling for OIDC failures
```

### Pin Actions to SHA

```
Update all action references in this workflow to use SHA commits instead of tags:

```yaml
{WORKFLOW_CONTENT}
```

For each action:
1. Find the current latest release SHA
2. Add comment with version number
3. Preserve the rest of the configuration

Format: uses: owner/action@{SHA} # v{VERSION}
```

## Debugging Prompts

### Debug Failing Workflow

```
This GitHub Actions workflow is failing with the error:

```
{ERROR_MESSAGE}
```

Workflow:
```yaml
{WORKFLOW_CONTENT}
```

Diagnose the issue and provide:
1. Root cause analysis
2. Fix for the issue
3. Prevention strategies
4. Debug logging additions if needed
```

### Add Error Handling

```
Add comprehensive error handling to this workflow:

```yaml
{WORKFLOW_CONTENT}
```

Include:
1. Appropriate if: conditions
2. continue-on-error where needed
3. Failure notifications
4. Job status outputs
5. Retry logic for flaky steps
6. Timeout configurations
```

## Advanced Patterns

### Generate Monorepo Workflow

```
Generate a GitHub Actions workflow for a monorepo with:
- Packages: {PACKAGE_LIST}
- Package manager: {PACKAGE_MANAGER}

Implement:
1. Path filtering to detect changes
2. Conditional jobs per package
3. Shared dependencies caching
4. Parallel builds for changed packages
5. Workspace-aware commands
```

### Generate Canary Deployment

```
Generate a canary deployment workflow for Kubernetes that:
1. Deploys canary with {CANARY_PERCENTAGE}% traffic
2. Monitors for {MONITORING_DURATION}
3. Checks metrics from {MONITORING_TOOL}
4. Promotes to full deployment if healthy
5. Rolls back if metrics degrade
6. Sends notifications at each stage

Include proper error handling and manual override capability.
```

### Generate Blue-Green Deployment

```
Generate a blue-green deployment workflow that:
1. Deploys to inactive environment
2. Runs comprehensive tests
3. Switches traffic (update load balancer)
4. Keeps old environment for quick rollback
5. Cleans up after validation period

Use {INFRASTRUCTURE_TOOL} for environment management.
```

## Template Customization

### Customize for Tech Stack

```
Customize this workflow template for a {TECH_STACK} project:

Template:
```yaml
{TEMPLATE_CONTENT}
```

Tech stack details:
- Framework: {FRAMEWORK}
- Database: {DATABASE}
- Testing: {TESTING_FRAMEWORK}
- Deployment target: {DEPLOYMENT_TARGET}

Adjust:
- Setup actions for the language/framework
- Test commands and coverage tools
- Build commands and artifacts
- Deployment steps
```

### Add Environment-Specific Config

```
Extend this workflow to support multiple environments with different configurations:

```yaml
{WORKFLOW_CONTENT}
```

Environments:
- development: {DEV_CONFIG}
- staging: {STAGING_CONFIG}
- production: {PROD_CONFIG}

Use:
- GitHub Environments for secrets/variables
- Environment protection rules
- Deployment approval for production
- Environment-specific URLs
```

## Documentation Prompts

### Document Workflow

```
Generate documentation for this GitHub Actions workflow:

```yaml
{WORKFLOW_CONTENT}
```

Include:
1. Purpose and overview
2. Trigger conditions
3. Job descriptions
4. Required secrets
5. Required variables
6. Manual trigger inputs
7. Success/failure behavior
8. Troubleshooting guide
```

### Generate Workflow Diagram

```
Create a Mermaid diagram showing the job dependencies and flow for this workflow:

```yaml
{WORKFLOW_CONTENT}
```

Include:
- Job names and descriptions
- Dependencies (needs)
- Conditional execution (if)
- Environment deployments
- Artifacts flow
```

## Prompt Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `{LANGUAGE}` | Programming language | node, python, go |
| `{VERSIONS}` | Version matrix | [18, 20, 22] |
| `{PLATFORM}` | Deployment platform | AWS EKS, Vercel, Netlify |
| `{DEPLOYMENT_METHOD}` | How to deploy | kubectl, Terraform, SSH |
| `{REGISTRY}` | Package registry | npm, PyPI, Docker Hub |
| `{PACKAGE_MANAGER}` | Package manager | npm, pip, go mod |
| `{CLOUD_PROVIDER}` | Cloud provider | AWS, GCP, Azure |
| `{OS_LIST}` | Operating systems | ubuntu-latest, windows-latest |
| `{VERSION_LIST}` | Language versions | ['3.10', '3.11', '3.12'] |
| `{TECH_STACK}` | Full tech stack | Next.js + Prisma + PostgreSQL |
| `{FRAMEWORK}` | Framework name | Django, FastAPI, Express |
| `{TESTING_FRAMEWORK}` | Test framework | pytest, jest, go test |
| `{WORKFLOW_CONTENT}` | Existing workflow YAML | Full workflow file content |
| `{ERROR_MESSAGE}` | Error from failed run | Full error output |
