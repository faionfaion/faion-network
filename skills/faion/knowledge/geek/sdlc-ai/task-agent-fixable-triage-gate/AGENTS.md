# `agent-fixable` Triage Gate (Humans Pick, Agents Work)

## Summary

Agents that turn issues into pull requests (Devin, Copilot Coding Agent, Codex, Cursor Background) waste tokens spinning on tickets they cannot solve: no acceptance criteria, no reproducible bug, blocked on product decisions, or duplicates of an existing issue. Insert a triage gate as a label — `agent-fixable` (or `copilot`, `devin-pickup`) — applied by a human or by a triage bot AFTER spam/duplicate/scope checks. The coding agent only listens for that label, never for "issue opened". Cognition's published Devin numbers show PR merge rate climbing from 34% to 67% over 2025 once gating was added; the same shape works for any coding agent fleet.

## Why

Without the gate, the agent reads every new issue, attempts ~60% of them, and merges ~10% — burning ~50× the tokens of the gated path. The label is an explicit cognitive contract: a human (or a triage agent constrained to read-only labelling tools) has confirmed the issue meets the agent's solvability bar. The agent treats the label as a precondition, not a hint, and the orchestrator can route by label across a mixed fleet (Devin + Copilot + Codex). The same label conveniently functions as the audit trail: "who decided this was agent-fixable?" is answered by the GitHub event log.

## When To Use

- Issue trackers with > 50 open items where agents would otherwise pick the wrong ones.
- Mixed agent fleets (Devin + Copilot + Codex + Cursor) sharing the same backlog.
- Repos with strict CODEOWNERS where mis-routed agent attempts produce noisy stale PRs.
- Teams adopting their first coding agent — start with a tiny `agent-fixable` allowlist, expand as merge rate stabilizes.

## When NOT To Use

- Tiny backlogs (< 10 open issues) where a human picks each issue manually anyway.
- Tickets needing product discovery, not code — those should carry `needs-spec`, never `agent-fixable`.
- One-off prototypes with no merge rate to optimize.
- Teams that have not yet defined what "fixable by an agent" means — write the criteria first, label after.

## Content

| File | What's inside |
|------|---------------|
| `content/01-label-as-precondition.xml` | The label-only-trigger rule, the agent's listening contract, and the criteria a human checks before applying the label. |
| `content/02-mixed-fleet-routing.xml` | How a single label routes across multiple coding agents and the rule against agents self-applying the label. |

## Templates

| File | Purpose |
|------|---------|
| `templates/agent-pickup.yml` | GitHub Actions workflow that dispatches an agent only on `agent-fixable` label-add. |
| `templates/triage-checklist.md` | Pre-label checklist a human (or read-only triage bot) must satisfy before applying `agent-fixable`. |
