# CodeQL + Copilot Autofix as the PR-time SAST Gate

## Summary

Every GitHub repository enables Code Scanning with CodeQL on `push` and `pull_request`. PRs that introduce a new CodeQL alert MUST be blocked from merge by a required check. Copilot Autofix runs automatically on alerts and posts an AI-generated patch as a PR suggestion that a human accepts, edits, or rejects — never auto-merge. For ecosystems CodeQL does not cover (Bash, Dockerfile, Terraform/HCL, PHP), enable AI-powered detections in the same Code Scanning pipeline so the gate is uniform across the stack.

## Why

CodeQL is a semantic dataflow engine, not a regex scanner: it follows tainted user input through control flow and catches injection, SSRF, deserialization and auth-bypass classes that pattern matchers miss. Copilot Autofix (GA 2024, expanded with hybrid AI detections in 2026) covers more than 90% of alert types in JavaScript, TypeScript, Java and Python and resolves over two-thirds of findings with little or no editing — GitHub's own measurements report median time-to-fix dropping from 1.5 hours manual to about 28 minutes when Autofix is enabled. The PR-time gate beats nightly scans because the diff is fresh, the author is paged, and the suggestion lands inside the review the human is already doing.

## When To Use

- Any GitHub-hosted repository with executable code (public OSS gets it free; private repos need GitHub Advanced Security or Copilot Enterprise).
- Any repo with HTTP, auth, deserialization, SQL/NoSQL, or template rendering surface.
- Polyglot repos where shell, Dockerfile, Terraform or PHP also need SAST coverage via the AI detections lane.
- Agent-driven feature work — agents read SARIF via `gh api` and treat new alerts as merge blockers.

## When NOT To Use

- Repositories not hosted on GitHub — use Semgrep or SonarQube instead; the Autofix loop is GitHub-specific.
- Pure documentation, asset, or notebook repositories with no executable surface — overhead exceeds value.
- Throwaway experimental branches that will never be merged — do not waste minutes on Code Scanning runs there.
- Mass-renaming refactors that legitimately churn thousands of lines — schedule a one-shot baseline reset, not per-PR Autofix.

## Content

| File | What's inside |
|------|---------------|
| `content/01-pr-blocking-gate.xml` | The "required check + new-alert-blocks-merge" rule and the SARIF-as-source-of-truth contract. |
| `content/02-autofix-suggestion-loop.xml` | How Copilot Autofix surfaces patches as suggestions and how an agent verifies, edits or rejects them. |

## Templates

| File | Purpose |
|------|---------|
| `templates/codeql-workflow.yml` | Minimal GitHub Actions workflow enabling CodeQL on push and PR with autobuild and SARIF upload. |
| `templates/branch-protection.json` | Required-status-check JSON snippet for the `gh api` call that wires CodeQL into branch protection. |
