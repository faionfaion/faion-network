# Agent Integration — RACI Matrix

## When to use
- New project kickoff with multiple roles (PM, dev lead, QA, DevOps, BA, sponsor) and recurring "who decides?" friction.
- Cross-team feature where SDD task ownership is ambiguous (e.g. backend + frontend + data + ops).
- Vendor/contractor engagements: clarify what client owns vs what contractor delivers.
- Audit/compliance projects (SOC2, ISO 27001) where evidence requires named accountable.
- Solopreneur engagements with a designer + developer + VA mix (per README example 2).

## When NOT to use
- One-person solo task with no stakeholders — overhead with zero return.
- Pure agile teams with collective code ownership and one PO — RACI flattens to "PO=A, team=R" everywhere; use DACI for decisions instead.
- Highly emergent work where roles shift weekly — matrix decays faster than it is updated.

## Where it fails / limitations
- Captures responsibility but not skill or capacity — does not stop overload.
- "C" inflation: stakeholders demand to be Consulted, slowing decisions; enforce a Consulted budget per task.
- Static artifact in a Confluence page nobody reads. Pair with task-tracker fields (Jira `assignee`/`reporter` ≠ R/A automatically).
- Cannot replace social negotiation: a manager who refuses an "A" assignment will sandbag the project.
- Multi-A bug: teams compromise on "A1/A2" instead of forcing one accountable; this defeats RACI and hides escalation paths.

## Agentic workflow
A Claude subagent can (1) parse a charter or WBS, (2) propose a draft RACI for each work package, (3) flag rule violations (no A, multiple A, no R, all-I rows), and (4) generate Markdown for PR review. Validation must stay deterministic — keep rule checks in a script, not in the LLM, so the agent surfaces violations rather than rationalising around them. Human-in-loop sign-off is required from the Accountable stakeholder before the matrix is committed.

### Recommended subagents
- `faion-pm-agent` — drafts and validates RACI from charter + WBS.
- `faion-business-analyst` — cross-checks RACI against requirements traceability so every requirement has an A.
- `faion-sdd-executor-agent` — adds R/A fields to SDD task front-matter when generating `TASK_*.md`.

### Prompt pattern
```
Given <charter.md>, <wbs.md>, <stakeholder-register.md>:
1. Build a RACI table (rows = WBS work packages, columns = stakeholder roles).
2. Apply the 4 rules: exactly one A; >=1 R; minimal C; deliberate I.
3. Output table + a violations list. Do NOT auto-resolve violations.
```

```
For each work package without an A: list 2-3 candidate Accountables
with one-sentence justification. Do not pick one — flag for human.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pandoc` | Convert RACI Markdown → DOCX/PDF for sponsor sign-off | https://pandoc.org |
| `mdformat` | Normalise Markdown tables before commit | `pip install mdformat-gfm` |
| `csvkit` | Pivot RACI CSV → role-centric view (`csvsql`) | https://csvkit.readthedocs.io |
| `gh` (GitHub CLI) | Sync R/A to issue assignee/reviewer fields | https://cli.github.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Atlassian Confluence | SaaS | Yes — REST API + page macros | Standard place to host RACI; agents update via `/wiki/rest/api/content` |
| Notion | SaaS | Yes — official API + databases | Native table = filterable RACI; sync from CSV via API |
| Smartsheet | SaaS | Yes — REST + automations | Good when RACI must trigger workflow (notify Accountable) |
| Jira | SaaS | Partial — assignee = R, reporter usable as A; A/C/I needs custom fields | Use ScriptRunner or a custom field set for full RACI |
| Linear | SaaS | Partial — only one assignee; encode A in label | Lightweight; pair with a Notion RACI table |
| RACI Online (raci.online) | SaaS | No public API | Browser-only; not for agents |
| Excel/Google Sheets | SaaS/desktop | Yes — Sheets API | Most common artifact; agents can `gspread` it |

## Templates & scripts
See `templates.md` for the basic RACI grid and `examples.md` for two filled examples. Inline validator (≤50 lines):

```python
# raci_validate.py — checks rule violations in a CSV RACI matrix.
# CSV: first col = task, remaining cols = roles, cells in {R,A,C,I,A/R,""}.
import csv, sys
from collections import Counter

def parse_cell(c):
    return {x.strip().upper() for x in c.replace("/", ",").split(",") if x.strip()}

def main(path):
    rows = list(csv.reader(open(path)))
    header, body = rows[0], rows[1:]
    errors = []
    for row in body:
        task = row[0]
        cells = [parse_cell(c) for c in row[1:]]
        flat = Counter()
        for s in cells:
            for ch in s:
                flat[ch] += 1
        if flat["A"] == 0:
            errors.append((task, "no Accountable"))
        if flat["A"] > 1:
            errors.append((task, f"{flat['A']} Accountables"))
        if flat["R"] == 0:
            errors.append((task, "no Responsible"))
        if flat["C"] > 4:
            errors.append((task, f"{flat['C']} Consulted (>4 = bottleneck)"))
        if not any(s for s in cells):
            errors.append((task, "empty row"))
    for task, msg in errors:
        print(f"[FAIL] {task}: {msg}")
    sys.exit(1 if errors else 0)

if __name__ == "__main__":
    main(sys.argv[1])
```

## Best practices
- One A per task — non-negotiable. If two execs both want it, escalate to sponsor; the matrix surfaces the conflict, doesn't resolve it.
- Keep RACI versioned in the same repo as the SDD docs; PR review forces explicit role changes.
- Walk the RACI in the kickoff meeting cell-by-cell with all roles in the room — silent acknowledgement is not consent.
- Pair with Stakeholder Register (Power × Interest) — Manage-Closely stakeholders are usually A or C.
- Avoid A=R for senior roles: the Accountable should not also be doing the work, or escalation breaks.
- Use "I" generously — informing is cheap; surprise is expensive.

## AI-agent gotchas
- LLMs default to A=R for the project lead because charters use phrases like "PM owns delivery". Force the agent to distinguish "owns outcome" from "does work".
- Agents will assign "C" to every named role to look thorough — set an explicit cap (e.g. ≤3 C per task) in the prompt.
- Updating RACI in long-running projects requires diffing previous matrix; agents should output a unified diff, not a full rewrite, so reviewers can spot role transfers.
- Do not let an agent close a violation by silently changing roles — every change requires a human Accountable signature.
- When deriving RACI from chat transcripts, agents over-weight whoever talks most; cross-check against the formal stakeholder register.

## References
- PMBOK Guide 7th Edition — Team Performance Domain (Project Management Institute, 2021).
- ISO 21502:2020 — Project, programme and portfolio management — Guidance on project management.
- "Making Things Happen" — Scott Berkun (Ch. on roles and accountability).
- Atlassian Confluence RACI templates: https://www.atlassian.com/work-management/project-management/raci-chart
