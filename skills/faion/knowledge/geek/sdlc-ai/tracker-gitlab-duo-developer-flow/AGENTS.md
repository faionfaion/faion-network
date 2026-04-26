# GitLab Duo Agent Platform Developer Flow

## Summary

Drive every GitLab issue-to-merge-request transition through the GitLab Duo Agent Platform's named flows: Developer Flow turns an issue into an MR, Code Review Flow runs automated review on the MR, Software Development Flow handles multi-step plan-before-execute changes, and CI/CD Flows handle pipeline migrations and failing-build fixes. Every flow respects the GitLab project's protected-branch rules, CODEOWNERS, and approval-rule policies — the human approver still merges. Triggers are issue labels (`agent:implement`) or scheduled pipelines, never raw API calls. Pre-18.8 GitLab versions are explicitly out of scope because of the locking bug plus feature-flag config issues tracked in GitLab incident #21171.

## Why

GitLab shipped Duo Agent Platform with named flows precisely to keep agent runs visible to project admins, auditors, and protected-branch enforcers — the same surface that already gates human MRs. The mechanism: by tying triggers to label transitions and scheduled pipelines, every agent action is a first-class GitLab event with full audit, project permissions, and protected-branch enforcement. Side webhooks or out-of-platform API drivers bypass that audit and are the documented anti-pattern in GitLab Duo's reference docs. SAST workflows specifically benefit because Duo's flows can be composed (Developer Flow → Code Review Flow with security standard) so false-positive filtering happens once, on the platform, with a single audit trail.

## When To Use

- Self-managed or GitLab.com customers (any tier with Duo) needing GitLab-native agent runs.
- Pipeline-heavy projects where CI/CD Flows (legacy pipeline conversion, fix-failing-build) compose well with Developer Flow.
- SAST-heavy workflows where false-positive filtering is the bottleneck and Code Review Flow can be tuned per security standard.
- On-prem orgs that cannot use Cloud-only platforms (Atlassian Rovo) and need an in-region agent runner.

## When NOT To Use

- Pre-18.8 GitLab versions — locking bug and feature-flag config issues block reliable runs (incident #21171).
- Multi-cloud orgs where the agent must read context outside GitLab's data plane; Duo cannot reach that data.
- Time-critical incident response where Duo's async flow latency is too high for the SLA.
- Single-author solo projects where the flow setup overhead exceeds value.

## Content

| File | What's inside |
|------|---------------|
| `content/01-flows-as-trigger-surface.xml` | Named-flow contract: label triggers, protected-branch inheritance, no side webhooks. |
| `content/02-flow-composition-and-version-floor.xml` | Developer Flow → Code Review Flow composition, the 18.8 version floor, and incident #21171 mitigation. |

## Templates

| File | Purpose |
|------|---------|
| `templates/duo-flows.yaml` | `.gitlab/duo-flows.yaml` config wiring Developer Flow + Code Review Flow with required-human-review and Closes-issue. |

## Related

- https://docs.gitlab.com/user/duo_agent_platform/
- https://about.gitlab.com/gitlab-duo-agent-platform/
- https://www.helpnetsecurity.com/2026/01/16/gitlab-duo-agent-platform-agentic-ai-automation/
