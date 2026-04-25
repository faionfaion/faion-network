# Agent Integration — RACI Matrix

## When to use
- Multi-role projects where ownership of decisions, deliverables, and approvals is unclear (>3 roles, >10 deliverables).
- Solopreneur engagements with contractors/VAs/agencies where one human plus several outsourced parties need a single accountable owner per task.
- Onboarding a new hire or contractor — encode "who owns what" in one table they can read in 5 minutes.
- Pre-mortem / kickoff for cross-functional features (PM + Eng + Design + QA + DevOps) before sprint zero.
- Incident response retros where "no one owned X" was a root cause — bake the new RACI into the runbook.

## When NOT to use
- Solo work with no external collaborators — overhead with zero return.
- Self-organizing Scrum team where the Definition of Done plus collective code ownership already covers accountability; a RACI here can undermine team agency.
- Hyper-dynamic discovery work where tasks change weekly — the matrix goes stale faster than you maintain it.
- Highly autonomous senior teams operating under "DACI" / "Advice Process" / "RAPID" — those frameworks are better fits than RACI for decision rights.

## Where it fails / limitations
- Captures who, not when — pair with a timeline/Gantt or sprint plan.
- Encourages role inflation: people demand "C" status to feel included, slowing decisions. Push back hard.
- Two-dimensional view hides cross-task dependencies. Augment with a dependency graph.
- "A also = R" fudge silently re-creates the "no clear owner" problem the matrix was supposed to fix.
- Teams maintain it once at kickoff and never revisit; it becomes wallpaper.

## Agentic workflow
A Claude subagent can ingest a project charter or epic and emit a draft RACI matrix as a Markdown table; a reviewer agent then checks the rules (exactly one A per row, ≥1 R per row, no empty rows) and flags violations. For ongoing projects, a third agent diffs the new RACI against the previous version and posts the delta to Slack/Issue tracker. Keep the human PM as the Accountable role for the matrix itself — do not let the agent be the final approver.

### Recommended subagents
- `raci-drafter` — reads charter/spec, lists tasks × roles, fills R/A/C/I per cell, returns Markdown table.
- `raci-validator` — enforces rules: exactly one A, ≥1 R, no all-I rows, ≤3 C per row; returns violations list.
- `raci-diff` — compares two RACI matrices (Markdown or YAML), outputs added/removed/changed cells.
- `faion-sdd-executor-agent` — already in repo; can be prompted to attach a RACI section to design.md as part of feature SDD.

### Prompt pattern
```
You are raci-drafter. Inputs: <project charter>. Tasks list: <list>. Roles list: <list>.
Output a Markdown RACI matrix. Rules: exactly one A per row, at least one R per row,
minimize C, be generous with I. Do not invent tasks or roles. Return only the table.
```

```
You are raci-validator. Input: a Markdown RACI table. Output a JSON list of violations
with {row, rule, suggestion}. Rules: A_unique, R_present, C_max_3, no_empty_row.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pandas` + Markdown | Lint RACI rules in CI; pandas reads the table, asserts row constraints | `pip install pandas` |
| `mermaid-cli` (`mmdc`) | Render RACI as a colored heatmap from CSV | `npm i -g @mermaid-js/mermaid-cli` |
| `yq` | Edit RACI stored as YAML in a repo without losing comments | https://github.com/mikefarah/yq |
| `gh` CLI | Create GitHub issues/labels from RACI rows ("A: @alice" → assignee) | https://cli.github.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Notion | SaaS | Yes — REST API | Database with R/A/C/I select properties; agent can CRUD via official API. |
| Confluence | SaaS | Partial — REST API verbose | Store RACI as table macro; updates need page version bumps. |
| Coda | SaaS | Yes — REST API | Tables with formulas validate "exactly one A" automatically. |
| Smartsheet | SaaS | Yes — REST API | Native RACI templates; cellLink to project plan. |
| Lucidchart / Miro | SaaS | Limited API | Useful for whiteboard kickoff, painful to maintain via agent. |
| Jira (custom field) | SaaS | Yes — REST API | Add R/A/C/I custom fields per role on each issue; query via JQL. |
| GitHub Projects v2 | SaaS | Yes — GraphQL | Single-select fields per role; CODEOWNERS handles A for code paths. |

## Templates & scripts
See `templates.md` for the canonical Markdown RACI block. Inline validator (drop in `scripts/raci_lint.py`):

```python
#!/usr/bin/env python3
"""Lint a Markdown RACI table on stdin. Exit 1 on violations."""
import re, sys

text = sys.stdin.read()
rows = [l for l in text.splitlines() if l.startswith("|") and "---" not in l]
header = [c.strip() for c in rows[0].strip("|").split("|")]
roles = header[1:]
violations = []
for row in rows[1:]:
    cells = [c.strip() for c in row.strip("|").split("|")]
    task, vals = cells[0], cells[1:]
    a = sum("A" in v for v in vals)
    r = sum("R" in v for v in vals)
    c = sum(v == "C" for v in vals)
    if a != 1: violations.append(f"{task}: A_count={a}")
    if r < 1:  violations.append(f"{task}: no R")
    if c > 3:  violations.append(f"{task}: too many C ({c})")
for v in violations: print(v)
sys.exit(1 if violations else 0)
```

## Best practices
- One A per row is the only rule that matters; everything else is style. Enforce it in CI.
- Name roles, not people. People rotate; roles stick. Map role→person in a separate table.
- Extend with "S" (Support) and "V" (Verify) only if you actually use them — otherwise it's noise.
- Tag RACI changes in version control with the commit that introduced them; lets you do `git blame` on accountability.
- Pair RACI with an escalation path: "If A is unavailable >24h, escalation owner is X."
- For agent-driven projects, declare which rows the agent is "R" on and which require human "A" sign-off.

## AI-agent gotchas
- Agents tend to assign themselves "A" — explicitly forbid this in the system prompt and validate.
- LLMs hallucinate plausible-but-wrong stakeholder names. Pass roles list as input; reject any role not on the list.
- Token cost scales with tasks × roles; for >50 tasks, chunk by phase and stitch matrices afterward.
- Markdown table parsing is brittle — prefer YAML when an agent mutates RACI iteratively, render Markdown only for humans.
- Watch for "all-I" rows (everyone informed, no one acting) — agents produce these when the underlying task is too vague.

## References
- PMI PMBOK Guide, 7th edition — Stakeholder Performance Domain
- https://www.atlassian.com/work-management/project-management/raci-chart
- https://www.prosci.com/methodology/adkar — Change-management adjacency
- "Making the Matrix Work" (Kevan Hall) — RACI failure modes in matrix orgs
