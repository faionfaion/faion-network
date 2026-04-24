# LLM Prompts for GitHub Actions

Prompts for generating GitHub Actions workflows and configurations.

---

## Generate CI Pipeline

```
Create a GitHub Actions CI workflow for a {{language/framework}} project with:

Project details:
- Language: {{Node.js/Python/Go/Rust}}
- Package manager: {{npm/pnpm/pip/cargo}}
- Test framework: {{jest/pytest/go test}}
- Build output: {{dist/build/.next}}

Requirements:
1. Lint and format checking
2. Unit and integration tests with coverage
3. Build step with artifact upload
4. Matrix testing across {{versions/platforms}}

Follow these best practices:
- Use concurrency groups to cancel duplicate runs
- Set persist-credentials: false on checkout
- Add appropriate timeout-minutes
- Use caching for dependencies
- Set minimal permissions
```

---

## Generate Docker Build Workflow

```
Create a GitHub Actions workflow to build and push Docker images:

Configuration:
- Registry: {{ghcr.io/docker.io/ECR}}
- Platforms: {{linux/amd64,linux/arm64}}
- Trigger: {{push to main, tags v*}}

Features needed:
1. Multi-platform builds with QEMU/Buildx
2. Semantic version tagging
3. GitHub Actions cache for layers
4. SBOM and provenance generation
5. Vulnerability scanning before push

Security requirements:
- Use OIDC for registry auth if supported
- Pin all actions to SHA
- Set minimal GITHUB_TOKEN permissions
```

---

## Generate Deployment Workflow

```
Create a deployment workflow for {{environment type}}:

Infrastructure:
- Cloud provider: {{AWS/GCP/Azure/self-hosted}}
- Deployment target: {{ECS/EKS/Cloud Run/Kubernetes}}
- Environments: {{staging, production}}

Requirements:
1. Use OIDC for cloud authentication (no long-lived secrets)
2. Download build artifact from CI workflow
3. Use GitHub environments with protection rules
4. Add deployment URL to environment
5. Implement rollback capability

Conditions:
- Staging: automatic on main branch push
- Production: manual approval required
```

---

## Generate Reusable Workflow

```
Convert this workflow pattern into a reusable workflow:

Pattern description:
{{Describe the common pattern you want to reuse}}

Inputs needed:
- {{input1}}: {{description}} (required/optional, default: {{value}})
- {{input2}}: {{description}} (required/optional)

Secrets needed:
- {{SECRET_NAME}}: {{description}}

Outputs:
- {{output1}}: {{description}}

Create both:
1. The reusable workflow (.github/workflows/{{name}}-reusable.yml)
2. Example caller workflow showing usage
```

---

## Generate Composite Action

```
Create a composite action for {{purpose}}:

Action should:
1. {{Step 1}}
2. {{Step 2}}
3. {{Step 3}}

Inputs:
- {{input}}: {{description}}

Outputs:
- {{output}}: {{description}}

Requirements:
- Use shell: bash for all run steps
- Include comprehensive description
- Handle errors gracefully
- Support all major runners (ubuntu, macos, windows)
```

---

## Security Audit Prompt

```
Review this GitHub Actions workflow for security issues:

```yaml
{{paste workflow here}}
```

Check for:
1. Unpinned actions (should use SHA)
2. Overly permissive GITHUB_TOKEN permissions
3. Secrets exposure risks
4. Command injection vulnerabilities
5. Missing persist-credentials: false
6. Unsafe use of pull_request_target
7. Missing concurrency controls
8. Hardcoded values that should be secrets

For each issue found, provide:
- Location in workflow
- Risk level (Critical/High/Medium/Low)
- Remediation with corrected code
```

---

## Performance Optimization Prompt

```
Optimize this GitHub Actions workflow for speed and cost:

```yaml
{{paste workflow here}}
```

Analyze and improve:
1. Caching strategy (dependencies, build cache)
2. Job parallelization opportunities
3. Matrix build optimization
4. Unnecessary steps or jobs
5. Runner selection
6. Artifact retention settings

Provide:
- Estimated improvement percentage
- Optimized workflow
- Explanation of changes
```

---

## Convert to Matrix Build

```
Convert this workflow to use matrix strategy:

```yaml
{{paste workflow here}}
```

Matrix dimensions needed:
- {{dimension1}}: [{{values}}]
- {{dimension2}}: [{{values}}]

Include:
- fail-fast: {{true/false}}
- Exclusions for incompatible combinations
- Include for special configurations (e.g., coverage only on one combo)
```

---

## Generate Scheduled Workflow

```
Create a scheduled workflow for {{purpose}}:

Schedule: {{cron expression or description like "daily at 2am UTC"}}

Tasks:
1. {{Task 1}}
2. {{Task 2}}

Also add:
- workflow_dispatch for manual triggering
- Conditional execution based on day/time if needed
- Notification on failure
- Proper timeout settings
```

---

## Generate Release Workflow

```
Create a release workflow with:

Trigger: {{push tag v*, workflow_dispatch, release publish}}

Steps:
1. Build and test
2. Generate changelog from commits
3. Create GitHub release with:
   - Auto-generated release notes
   - Build artifacts attached
   - Semantic versioning

Package publishing (if needed):
- NPM: {{yes/no}}
- PyPI: {{yes/no}}
- Docker: {{yes/no}}
- GitHub Packages: {{yes/no}}
```

---

## Migrate from Other CI

```
Convert this {{Jenkins/GitLab CI/CircleCI/Travis}} configuration to GitHub Actions:

```yaml
{{paste original CI config}}
```

Maintain:
- Same stages/jobs structure
- Environment variables
- Secrets handling
- Caching behavior
- Artifact management

Add GitHub-specific improvements:
- Concurrency controls
- Matrix builds if applicable
- Reusable workflows for common patterns
```

---

## Debug Failing Workflow

```
This GitHub Actions workflow is failing. Help debug it:

Workflow:
```yaml
{{paste workflow}}
```

Error message:
```
{{paste error}}
```

Provide:
1. Root cause analysis
2. Step-by-step fix
3. Prevention measures for future
```

---

## Usage Tips

1. **Be specific** - Include exact versions, package managers, frameworks
2. **Provide context** - Mention existing infrastructure, team size, requirements
3. **Request explanations** - Ask for comments explaining non-obvious parts
4. **Iterate** - Start simple, then add complexity
5. **Validate** - Use actionlint or dry-run before committing

## Sources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax Reference](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
