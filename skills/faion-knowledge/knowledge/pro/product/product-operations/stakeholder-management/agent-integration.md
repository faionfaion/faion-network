# Agent Integration — Stakeholder Management

## When to use
- Cross-functional product launch with 5+ named stakeholders (exec sponsor, eng lead, sales, support, key customer) where misalignment has already cost time once. The register + comms matrix become the single source of truth other agents read.
- Re-org or PM handover: the outgoing PM dumps every stakeholder relationship into a register so the incoming PM (or `faion-pm-agent`) can drive engagement without rediscovery.
- Roadmap quarter starts: refresh power/interest grid, decide which stakeholders move from `Inform` to `Partner` for the upcoming bets.
- An SDD feature has a "stakeholder approval" gate (legal, security, head of sales). Codify the gate explicitly so `faion-sdd-executor-agent` blocks merge until the named approver has signed off.
- Building a multi-agent comms pipeline where different agents (status-bot, release-notes-bot, executive-summary-bot) need to pull *audience* from a shared register.

## When NOT to use
- Solo founder pre-revenue with only customers and family as stakeholders. A 6-row register adds ceremony with zero decision impact — keep it as a 5-line note in your project README and move on.
- Internal dev-tools used by < 10 engineers all sitting in the same Slack channel. Async stand-up + RFC comments cover engagement; a register is overhead.
- Crisis/incident mode: when a SEV1 is burning, you need an incident commander and a war room, not a power/interest grid. Run incident-management methodology, restore service, then update the register post-mortem if a new stakeholder surfaced.
- Confusing stakeholder management with project management. If your problem is "we don't know who's doing what work", use `raci-matrix` or WBS, not this.

## Where it fails / limitations
- Register rot: the doc is built once at project kick-off and never updated. By month 3, the named exec sponsor has left the company and the register still drives the weekly update email. Tie register review to the same cadence as roadmap review.
- Power/interest grids hide *attitude*. A high-power stakeholder coded as "Manage Closely" but secretly a Resistor is the silent killer. Always carry an explicit `attitude` column (Supporter / Neutral / Resistor) and color it.
- Communication-plan theatre: an elaborate matrix that nobody actually executes. If the PM isn't running the weekly sync the matrix promises, the matrix is a lie. Reduce cadence to what will actually happen.
- Over-engagement of `Low Power, Low Interest` stakeholders out of politeness. Burns PM cycles and dilutes signal. The whole point of the grid is to deprioritize.
- One-way "stakeholder updates" treated as engagement. A newsletter is information, not engagement; engagement requires bidirectional input loops (decisions, feedback, escalation paths).
- Cross-cultural blind spots: `Power` is more diffuse in matrix orgs and consensus-driven cultures. A simple grid encodes a Western-corporate hierarchy assumption. Annotate, don't auto-trust.

## Agentic workflow
Drive stakeholder management as a 3-loop pipeline. (1) **Discovery loop**: `faion-pm-agent` (or product-manager subagent) interviews the team and outputs a draft `stakeholder-register.md` into `.aidocs/product_docs/`. (2) **Engagement loop**: a status-update agent reads the register, generates audience-tailored updates (executive summary vs. dev daily vs. customer newsletter), and routes via the configured channel adapters. (3) **Drift-detection loop**: weekly cron-driven agent diffs new stakeholder mentions in meeting notes / Slack export against the register and flags additions or attitude shifts for human review. Critical: the register is read by many agents, written by one (or by humans). Treat it like a config file with a clear owner.

### Recommended subagents
- `faion-pm-agent` (referenced in this methodology's frontmatter) — runs Step 1–2 of the framework: identify, analyze, draft engagement plan. Outputs to `.aidocs/product_docs/stakeholder-register.md`.
- `faion-sdd-executor-agent` — wraps stakeholder-related SDD tasks ("F-053: Get legal sign-off on data-export feature"); enforces that the named stakeholder from the register is captured as task approver and blocks `done` transition until sign-off is logged.
- `password-scrubber-agent` — run before committing any register or comms-plan artifact: registers contain personal contact details, internal email addresses, sometimes phone numbers. Strip or hash before the file lands in a public repo.
- `faion-marketing-manager` (sibling skill) — consumes the register's *external* segment (customers, advisors, partners) to drive newsletter and announcement sequencing. Don't duplicate customer lists — link.

### Prompt pattern
Discovery prompt (sub-agent input):
```
Input: project brief at .aidocs/product_docs/project-brief.md +
       team-list at .aidocs/team.md
Task: Build stakeholder register. For each candidate stakeholder, populate
columns: name, role, interest (H/M/L), power (H/M/L), attitude
(Supporter/Neutral/Resistor — mark Unknown if you cannot infer), engagement
level (Partner/Involved/Informed/Monitor), owner. Cite the source line for
every Power and Attitude classification (no inference without source). Mark
any stakeholder with attitude=Unknown for human follow-up. Output as a single
markdown table to .aidocs/product_docs/stakeholder-register.md.
```

Engagement plan prompt:
```
Read .aidocs/product_docs/stakeholder-register.md. For each stakeholder where
engagement >= Informed, generate a one-line message draft for this week's
update, tailored to their (power, interest, attitude) cell. Resistors get a
separate "concern + mitigation" message. Do not send; output to a draft file
for human review.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh` (GitHub CLI) | Map code-owners + PR reviewers to register; `gh api` to pull team membership | https://cli.github.com |
| `slack-cli` / Slack API | Bulk-push tailored updates to channels per audience segment | https://api.slack.com |
| `notion-cli` / Notion API | Sync register to a Notion DB shared with non-eng stakeholders | https://developers.notion.com |
| `linear-cli` / Linear API | Pull issue stakeholders, sync into register | https://developers.linear.app |
| `confluence` REST | Publish exec-summary updates to a stakeholder-visible space | https://developer.atlassian.com/cloud/confluence |
| `jira-cli` | Pull approvers and watchers per ticket, reconcile with register | https://developer.atlassian.com/cloud/jira |
| `pandoc` | Render register markdown into board-ready PDF / DOCX | system package |
| `yq` | Diff register YAML between commits to detect attitude/engagement shifts | https://github.com/mikefarah/yq |
| `mailmerge` (Python) | Send tailored email updates from a register CSV | `pip install mailmerge` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Notion | SaaS | Yes — REST API for DBs | Best for shared register with non-eng access; tag attitudes via select fields |
| Confluence | SaaS | Yes — REST API | Enterprise default; pair with Jira approver field |
| Linear | SaaS | Yes — GraphQL API | Pull project stakeholders into register; weak for non-eng audience |
| Jira | SaaS | Yes — REST API | Approver/watcher lists feed register; over-eng for solo |
| Productboard | SaaS | Yes — API | Native concept of stakeholder feedback loops; useful for `Inform` segment |
| Aha! | SaaS | Yes — API | Roadmap + stakeholder portal in one |
| Stakeholder Circle | SaaS | Limited API | Specialty tool; useful only for very large programs |
| Trello | SaaS | Yes — REST API | Lightweight register for small teams |
| Slack | SaaS | Yes — Web API + Bots | Engagement channel, not register storage |
| Discord | SaaS | Yes — REST + bots | External-customer segment for indie products |
| Mailchimp / Buttondown | SaaS | Yes — API | `Inform` tier newsletter automation |
| Loomio | OSS / SaaS | Yes — API (limited) | Decision-record + stakeholder-vote audit trail |
| Mural / Miro | SaaS | Limited API | Power/interest grid as a live workshop artifact |
| OpenProject | OSS | Yes — REST API | Self-hosted alternative for register + comms log |

## Templates & scripts
See `templates.md` (currently empty — the README's "Stakeholder Register", "Communication Plan", and "Stakeholder Meeting" templates are the canonical shapes). For an agent-callable register lint that catches the most common rot patterns, the script below runs as a pre-commit or weekly cron.

```python
# stakeholder_lint.py — lint a stakeholder register for known rot patterns.
# Usage: python stakeholder_lint.py .aidocs/product_docs/stakeholder-register.md
import sys, re, pathlib, datetime, collections

src = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
rows = [r.strip() for r in src.splitlines() if r.startswith("|") and "---" not in r]
header = [c.strip().lower() for c in rows[0].strip("|").split("|")]
required = {"name", "role", "interest", "power", "attitude", "engagement", "owner"}
missing_cols = required - set(header)
if missing_cols:
    print(f"FAIL: missing columns: {sorted(missing_cols)}"); sys.exit(1)

idx = {c: header.index(c) for c in required}
issues = collections.Counter()
for r in rows[1:]:
    cells = [c.strip() for c in r.strip("|").split("|")]
    if len(cells) < len(header):
        continue
    if cells[idx["attitude"]].lower() in ("", "unknown", "tbd"):
        issues["attitude_unknown"] += 1
    if cells[idx["owner"]].lower() in ("", "tbd", "?"):
        issues["no_owner"] += 1
    if cells[idx["power"]].lower() == "high" and \
       cells[idx["engagement"]].lower() in ("monitor", "informed"):
        issues["high_power_under_engaged"] += 1
    if cells[idx["interest"]].lower() == "low" and \
       cells[idx["power"]].lower() == "low" and \
       cells[idx["engagement"]].lower() == "partner":
        issues["over_engaged_low_low"] += 1

if issues:
    print(f"WARN ({datetime.date.today()}): {dict(issues)}")
    sys.exit(2 if "high_power_under_engaged" in issues else 0)
print("OK: register lint passed")
```

## Best practices
- Carry an explicit `attitude` column. Power/interest grids without attitude are 2D maps of a 3D problem; resistors hidden in the `Manage Closely` quadrant kill projects.
- One owner per stakeholder relationship. "Whole team manages this exec" means nobody does. The owner column is non-optional.
- Every stakeholder has a *named* engagement cadence (weekly 1:1, biweekly email, monthly review). "Ad-hoc" is code for "nothing happens".
- Pair the register with a decision log. Engagement that doesn't produce decisions is theatre. Each `Partner`-tier stakeholder should appear in the decision log monthly or be downgraded.
- Negative space matters: maintain a "former stakeholders" archive, not just a current list. When someone moves on, don't delete — record exit + reason. Future PMs need that context.
- Tie escalation paths to real names + backups. "Escalate to Director" with no name is unactionable at 11pm.
- For external/customer stakeholders, separate the register from any marketing CRM. Treat the register as program-management metadata; let the CRM hold the relationship history. Cross-link by ID, don't duplicate.
- Refresh quarterly with the team in a 30-min meeting; do not let the PM update unilaterally. Other people see attitudes the PM misses.
- Pair this methodology with `raci-matrix` (responsibility) and `roadmap-design` (timing). The trio answers Who / What-they-do / When.

## AI-agent gotchas
- LLM-generated stakeholder analyses hallucinate stakeholders that "should" exist for a given project type ("Compliance Officer", "Data Privacy Lead"). Always require the model to cite an actual source — meeting notes, org chart, repo CODEOWNERS — before adding a row.
- Models drift toward sycophancy when classifying *attitude*. Asked "is this exec a supporter?" they default to Yes. Force the model to mark Unknown unless evidence cited; lint for it (script above).
- Power/interest classifications based purely on title are wrong in matrix orgs; an LLM with no org-context will infer from title alone. Feed it actual org-chart text or interview snippets.
- PII leakage: registers contain emails, phone numbers, sometimes salary info ("VP-level"). Never let an agent push a register to a public-readable location without scrubbing. Use `password-scrubber-agent` or equivalent.
- Auto-generated stakeholder updates can be passive-aggressive without intent — language-model paraphrases of "delayed" read as accusatory in some cultures. Have a human review tone for any message going to a Resistor or to high-context cultures.
- Don't let an agent autonomously change a stakeholder's `engagement` level. Changing someone from `Partner` to `Informed` is a relationship downgrade with political consequences. Agent suggests, human approves.
- Multi-agent pipelines duplicating contact lists (CRM + register + newsletter) drift fast. Pick one source of truth (the register) and have other systems read from it via API; never copy.
- Cron-driven "weekly stakeholder sentiment scan" of Slack messages is high-risk: a mis-classified Resistor signal can trigger an unnecessary escalation. Always queue findings for human review, never auto-escalate.
- Agents writing meeting minutes can mis-attribute decisions to the wrong stakeholder when multiple people speak. Cross-check minutes against the register's `Owner` column before storing as a decision record.
- Long-context dumps of the register into every agent prompt waste tokens and leak data. Pass only the relevant slice (one quadrant, or one engagement tier) to each agent.

## References
- Mitchell, R. K., Agle, B. R., & Wood, D. J. — "Toward a Theory of Stakeholder Identification and Salience" (Academy of Management Review, 1997)
- Freeman, R. E. — *Strategic Management: A Stakeholder Approach* (1984; reissued Cambridge, 2010)
- PMI — *Pulse of the Profession: Stakeholder Engagement* (https://www.pmi.org/learning/library)
- Bourne, L. — *Stakeholder Relationship Management* (Gower, 2009) — origin of the Stakeholder Circle method
- Atlassian — "Stakeholder analysis: a guide" (https://www.atlassian.com/work-management/project-management/stakeholder-analysis)
- Sibling methodologies: `stakeholder-engagement` (pro/pm/project-manager), `raci-matrix` (pro/pm), `roadmap-design` (pro/product), `business-analysis-planning` (pro/ba), `gtm-strategy` (pro/marketing)
