# GitHub Copilot Workspace Four-Gate Pipeline

## Summary

Drive every GitHub-hosted ticket-to-PR through Copilot Workspace's four explicit gates: (1) AI generates a current-state plus desired-state spec from the issue, (2) AI generates a file-level plan, (3) AI generates the diff, (4) AI opens the PR. The human can edit at every stage, and skipping any gate is a hard refusal — agents that go straight from issue to diff are configured to abort. Every Workspace PR includes an auto-attached comment with a read-only Workspace snapshot link so reviewers can see the spec and plan that produced the diff, not just the diff itself.

## Why

GitHub published the four-gate flow as the canonical pattern for agentic PRs and reported a roughly 30% "agentic PR fail-rate" in April 2026 when teams skipped the spec/plan gates. The mechanism is reviewability: the snapshot link gives the reviewer the agent's chain-of-thought as artefacts they can read and react to, not as logs they have to dig out. Empirically the spec gate catches misread requirements before any code is written (cheapest fix), and the plan gate catches wrong-file changes before the diff exists (next-cheapest). Both gates are gone if the agent runs end-to-end without surfacing intermediate artefacts.

## When To Use

- GitHub-hosted single-repo issues with well-scoped acceptance criteria.
- Bug fixes and small-to-medium features where reviewers want to see the agent's reasoning, not just the patch.
- Greenfield bootstrap tickets where the spec gate is the only chance to align on direction before scaffolding lands.
- Teams that already enforce branch protection requiring `Closes #N` in PR body — the four-gate flow guarantees the link.

## When NOT To Use

- Multi-repo changes — Workspace is single-repo per session and the four-gate flow does not span repos.
- SLA-critical paths where the documented ~30% agentic PR fail-rate is unacceptable; route those through human-led changes.
- Teams that prefer the autonomous Copilot coding-agent flow (assign Copilot directly, no Workspace UI) — different contract.
- Trivial typo fixes pre-flagged auto-merge; gate cost exceeds the risk and slows trivial flow.

## Content

| File | What's inside |
|------|---------------|
| `content/01-four-gate-contract.xml` | The four mandatory gates (spec, plan, diff, PR), the per-gate edit point, and the "no gate skip" hard refusal. |
| `content/02-snapshot-and-link.xml` | Workspace snapshot link auto-attached to PR + `Closes #N` enforcement. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pr-template.md` | PR body template with `Closes #N` line and the Workspace snapshot link slot. |

## Related

- https://githubnext.com/projects/copilot-workspace
- https://github.com/features/copilot/whats-new
- https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/make-changes-to-an-existing-pr
