# Agent Drafts Spec Before Coding

## Summary

When an AI coding agent is assigned a tracker ticket (Linear, Jira, GitHub, GitLab), its first action MUST be a "current state / desired state / proposed plan" comment posted back on the issue, not a code edit. The agent gathers the issue body plus linked context (Notion spec, Slack thread, prior similar issues, code-intel search) and emits a structured spec draft. Implementation only begins after a specialist signals approval — Linear thumbs-up emoji on the agent's comment, Jira `/agent approve` slash command, or an explicit `agent:approved` label transition. First-try-pass on coding (no spec gate) means the agent skipped the discovery step and is fabricating intent.

## Why

April 2026 production data from Linear, Atlassian Rovo, GitHub Copilot Workspace, and GitLab Duo all converge on the same gate: agents that draft a spec comment first land mergeable PRs at materially higher rates than agents that jump to a diff. The mechanism is twofold — (a) the agent is forced to surface its interpretation of "done", which catches misreadings cheaply (a comment is rolled back with a reaction, a wrong PR costs a review cycle); (b) the spec doubles as a permanent audit artefact attached to the ticket, satisfying the same reviewability requirement that branch-protection rules enforce on the diff side. Linear's own engineering team and GitHub's Copilot Workspace both encode this as the first stage of their agent contract.

## When To Use

- Ticket is assigned to an AI coding agent on Linear, Jira, GitHub, or GitLab as the primary owner of the work.
- Issue has any non-trivial scope: feature work, multi-file bug fix, refactor, migration.
- Team has at least one human reviewer who can react with a thumbs-up or run an approval slash command.
- Workflow auto-closes the issue on PR merge (`Fixes #N`, `Closes !N`) — the spec comment becomes the linkable record of intent.

## When NOT To Use

- Trivial tickets pre-flagged `agent:auto-approve` (typo fixes, dependency bumps, log-message tweaks) — gate cost exceeds risk.
- Spike or research tickets where the desired state is itself the deliverable; the agent's job is to discover, not to commit code.
- Hot-path incident response where a postmortem ticket is filed after the fact; spec drafting belongs to the retro, not the fix.
- Single-author solo projects with no second human in the loop — the gate has no approver and the agent stalls.

## Content

| File | What's inside |
|------|---------------|
| `content/01-spec-comment-contract.xml` | The mandatory shape of the agent's first comment: current state, desired state, proposed plan, INVEST decomposition. |
| `content/02-approval-gate-mechanics.xml` | How the human signal is detected per tracker (Linear emoji, Jira slash command, GitHub label) and how the agent blocks until it fires. |

## Templates

| File | Purpose |
|------|---------|
| `templates/spec-comment.md` | Markdown skeleton the agent fills in for the first ticket comment. |
| `templates/approval-gate.yaml` | Per-tracker config mapping the approval signal to the agent's `proceed` event. |
