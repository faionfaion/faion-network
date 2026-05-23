# Shadow Handover Session Runbook

## Summary

**One-sentence:** A runbook for live shadow-handover sessions where the receiver executes real work while the outgoing engineer watches silently, with predefined task list, structured checkpoints, written gap log, and a sign-off gate that forces verified transfer instead of demo theatre.

**One-paragraph:** The offshore-to-onshore rotation pattern dominates outsourced delivery but the failure mode is consistent: outgoing engineer demos confidently, receiver nods, receiver cannot reproduce post-rotation. This runbook forces the inversion — receiver drives the keyboard for a pre-agreed task list, outgoing engineer answers only on explicit question, every question is logged into a written gap log with answer + permanent-doc link, and the session ends with a signed two-party gate naming what the receiver drove unaided, what needs a second session, and any single-point-of-failure facts still undocumented. No silent task-skipping.

**Ефективно для:**

- Pre-handover documentation pack converting demo into verified transfer.
- Cross-team / cross-vendor rotation where receiver inherits live ops.
- Catching tribal-knowledge gaps before the outgoing engineer rotates out.
- Quarterly review: gap log entries that lack doc links become deferred work.

## Applies If (ALL must hold)

- Engagement transfers operational ownership of a system from one engineer / team to another.
- Outgoing engineer available + willing for ≥ 1 session.
- Real executable tasks exist (not just docs reading).
- Tier == pro or higher.

## Skip If (ANY kills it)

- Outgoing engineer already gone — use forensic-handover artefacts.
- System greenfield with receiver having built half of it.
- Transfer is purely documentation — use a doc-walkthrough pattern.
- No predefined task list available.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Task list (pre-agreed, executable) | Markdown / YAML | outgoing + receiver |
| System access (creds, VPN, SSH) | secrets vault | platform |
| Gap log doc | shared editable doc | receiver |
| Sign-off template | Markdown | this methodology |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[wbs-creation]] | Task list maps onto WBS leaves the system implements. |
| [[proposal-red-team-checklist]] | Handover risks feed proposal red-team pause-points. |
| [[remote-1-1-async-fallback]] | Async fallback if synchronous shadow not possible. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: receiver-drives, silent-watch default, written gap log, sign-off gate, no-skipped-tasks | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for `HandoverSessionRecord` + forbidden patterns | ~800 |
| `content/03-failure-modes.xml` | essential | 6 modes: demo theatre, spontaneous corrections, skipped tasks, missing doc links, unsigned gate, single-point-of-failure leakage | ~900 |
| `content/04-procedure.xml` | medium | 5-step: agree task list → run session → log gaps → sign-off → defer-or-document | ~600 |
| `content/06-decision-tree.xml` | essential | Tree: outgoing available? task list ready? gap log complete? sign-off captured? → run / defer / forensic-fallback | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `task-list-prep` | sonnet | Selection of representative ops tasks. |
| `gap-log-synthesis` | sonnet | Converting verbal Q/A into doc-linked rows. |
| `sign-off-drafter` | haiku | Mechanical fill of sign-off template. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | HandoverSessionRecord skeleton with task list + gap log + sign-off blocks |
| `templates/header.yaml` | Frontmatter schema |
| `templates/_smoke-test.json` | Minimum viable filled `HandoverSessionRecord` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-shadow-handover-session-runbook.py` | Validate: receiver_drove_count, gap_log.doc_link per row, two-party signature, no_skipped_tasks | Pre-merge |
| `scripts/staleness-check.py` | Flag records whose `last_reviewed` > 90 days | Weekly cron |

## Related

- [[wbs-creation]]
- [[proposal-red-team-checklist]]
- [[remote-1-1-async-fallback]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (outgoing-availability, task-list readiness, gap-log completeness, sign-off captured) to run-session / defer / forensic-fallback. Every leaf references a rule from `01-core-rules.xml`.
