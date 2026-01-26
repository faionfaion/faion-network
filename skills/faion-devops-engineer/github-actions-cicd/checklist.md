# GitHub Actions Checklist

## Security Checklist

### Action Pinning

- [ ] Pin all third-party actions to full SHA (not tags)
- [ ] Never use `@main` or `@master` for production
- [ ] Use Dependabot to keep actions updated
- [ ] Audit actions before adding to workflows

```yaml
# Bad - mutable tag
uses: actions/checkout@v4

# Good - immutable SHA
uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11 # v4.1.1
```

### Secrets Management

- [ ] Use GitHub Secrets, never hardcode credentials
- [ ] Use OIDC for cloud provider authentication (AWS, GCP, Azure)
- [ ] Access secrets individually, never use `${{ toJson(secrets) }}`
- [ ] Rotate secrets regularly
- [ ] Grant least privilege to secrets
- [ ] Mask sensitive outputs with `::add-mask::`

### GITHUB_TOKEN Permissions

- [ ] Set default permission to `read` for contents
- [ ] Explicitly declare required permissions per job
- [ ] Use minimum necessary permissions
- [ ] Review permission escalation in PRs

```yaml
permissions:
  contents: read
  packages: write
  # Explicit > implicit
```

### Checkout Security

- [ ] Set `persist-credentials: false` unless needed
- [ ] Use `fetch-depth: 1` for faster clones (unless history needed)
- [ ] Avoid checking out untrusted PR code in privileged context

```yaml
- uses: actions/checkout@v4
  with:
    persist-credentials: false
    fetch-depth: 1
```

### Fork Security

- [ ] Limit secrets exposure to forks
- [ ] Use `pull_request_target` carefully (security risk)
- [ ] Review fork PRs before running privileged workflows
- [ ] Consider `environment` protection for fork PRs

### Input Validation

- [ ] Validate all workflow inputs
- [ ] Sanitize user-provided data
- [ ] Avoid command injection in `run:` steps
- [ ] Use `${{ inputs.* }}` safely in shell commands

```yaml
# Bad - injection risk
run: echo "${{ github.event.pull_request.title }}"

# Good - use environment variable
env:
  PR_TITLE: ${{ github.event.pull_request.title }}
run: echo "$PR_TITLE"
```

---

## Performance Checklist

### Caching

- [ ] Cache package manager dependencies (npm, pip, cargo)
- [ ] Use hash-based cache keys
- [ ] Include restore-keys for fallback
- [ ] Monitor cache hit rates in logs
- [ ] Don't cache large, frequently changing files

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-npm-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-npm-
```

### Concurrency

- [ ] Use concurrency groups to prevent duplicate runs
- [ ] Enable `cancel-in-progress` for PRs
- [ ] Separate concurrency groups per branch/PR

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: ${{ github.event_name == 'pull_request' }}
```

### Job Dependencies

- [ ] Use `needs:` to create job dependencies
- [ ] Parallelize independent jobs
- [ ] Fail fast when appropriate
- [ ] Use matrix for multi-version testing

### Runners

- [ ] Use `ubuntu-latest` for most jobs (faster)
- [ ] Consider self-hosted runners for heavy builds
- [ ] Use larger runners for memory-intensive tasks
- [ ] Match runner OS to deployment target

### Timeouts

- [ ] Set `timeout-minutes` on all jobs
- [ ] Use step-level timeouts for potentially hanging steps
- [ ] Default timeout is 360 minutes (6 hours) - too long

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    timeout-minutes: 15
```

---

## Workflow Structure Checklist

### Organization

- [ ] Use descriptive workflow and job names
- [ ] Group related steps logically
- [ ] Extract common steps to composite actions
- [ ] Use reusable workflows for shared patterns
- [ ] Add `workflow_dispatch` for manual triggering

### Documentation

- [ ] Add workflow description in comments
- [ ] Document required secrets in README
- [ ] Explain non-obvious conditions
- [ ] Use meaningful step names

### Error Handling

- [ ] Use `continue-on-error` sparingly and intentionally
- [ ] Upload logs/artifacts on failure
- [ ] Send notifications on critical failures
- [ ] Use `if: failure()` for cleanup steps

```yaml
- name: Upload logs on failure
  if: failure()
  uses: actions/upload-artifact@v4
  with:
    name: failure-logs
    path: logs/
```

### Outputs and Artifacts

- [ ] Use outputs for data between jobs
- [ ] Use artifacts for files between jobs
- [ ] Set appropriate retention days
- [ ] Use `cache` for dependencies, `artifacts` for results

---

## Reusable Workflows Checklist

- [ ] Define clear inputs and outputs
- [ ] Document all parameters
- [ ] Use `workflow_call` trigger
- [ ] Pass secrets explicitly with `secrets: inherit` or named
- [ ] Limit nesting (max 10 levels, 50 total workflows)

```yaml
on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
    secrets:
      DEPLOY_KEY:
        required: true
```

---

## Composite Actions Checklist

- [ ] Create `action.yml` in `.github/actions/` folder
- [ ] Define clear inputs and outputs
- [ ] Use `shell: bash` explicitly in steps
- [ ] Document usage in action description
- [ ] Version with tags if shared across repos

---

## Pre-Deployment Checklist

- [ ] All security items checked
- [ ] Caching configured properly
- [ ] Timeouts set
- [ ] Concurrency configured
- [ ] Secrets documented
- [ ] Test workflow on feature branch first
- [ ] Review with team before merging

---

## Tools for Security Auditing

| Tool | Purpose |
|------|---------|
| [zizmor](https://github.com/woodruffw/zizmor) | Static analysis for GitHub Actions |
| [allstar](https://github.com/ossf/allstar) | Security policy enforcement |
| [actionlint](https://github.com/rhysd/actionlint) | Workflow syntax linter |
| Dependabot | Keep actions updated |

## Sources

- [GitHub Actions Security Best Practices - StepSecurity](https://www.stepsecurity.io/blog/github-actions-security-best-practices)
- [GitHub Actions Security Cheat Sheet - GitGuardian](https://blog.gitguardian.com/github-actions-security-cheat-sheet/)
- [Salesforce Security Best Practices](https://engineering.salesforce.com/github-actions-security-best-practices-b8f9df5c75f5/)
- [Hardening GitHub Actions - Wiz](https://www.wiz.io/blog/github-actions-security-guide)
