# Agent Integration — Stakeholder Management (Product Manager)

> Companion to the product-operations variant of this methodology. This file focuses on the **PM-as-broker** angle: the PM sitting at the intersection of engineering, design, sales, support and executives, translating across all of them. Read the product-operations `agent-integration.md` for the operational/program-level register, lint script, and CRM sync patterns. Do not duplicate.

## When to use
- A PM has just inherited a product line and the first artifact owed to the new manager is "who do I talk to and how often?". Build the register before the first 1:1.
- An executive has flagged "I keep being surprised by this product". The fix is rarely more updates — it is an explicit upward-comms cadence (monthly written brief, quarterly review, on-demand red-flag channel) tied to that exec's decision rights.
- A feature crosses 3+ functional silos (engineering + design + sales + legal). The PM brokers; the register encodes the brokerage rules so it survives the PM going on vacation.
- Two stakeholders disagree publicly (sales wants feature A, support wants bug-fix B). PM uses the register's `power × interest × attitude` cell to choose the forum (1:1 vs steering vs RFC) before mediating.
- Pre-launch GTM coordination: PM owns the cross-functional matrix where marketing, sales-enablement, support-readiness, infra, and legal must each sign a `Ready` gate.
- Promotion case prep: senior-PM / GPM ladders explicitly grade "executive stakeholder management". The register and decision log are the evidence.

## When NOT to use
- The "stakeholder" is really a customer. Use customer-discovery / Jobs-to-be-Done. A register row for `Acme Corp Procurement` is a category mistake.
- Engineering-only refactor with no business stakeholders. RFC + tech-lead approval is the right tool; a PM register adds zero signal.
- The conflict is actually a strategy disagreement (where are we going?). No comms cadence can paper over a missing strategy. Run a strategy session first; then map stakeholders against the agreed strategy.
- Solo founder. There are no peer stakeholders to broker; you are sales, eng and exec. Skip.
- When the underlying problem is org dysfunction (dual-hatted execs, unclear decision rights). The register exposes the dysfunction but cannot fix it; escalate to the head of product, do not paper over with a longer matrix.

## Where it fails / limitations
- **PM as bottleneck**: PMs who centralize all cross-functional communication through themselves create a single point of failure. The register should *route*, not *funnel* — sometimes eng-lead → sales-lead is the right edge, with the PM informed.
- **Upward-comms inflation**: PMs who escalate every decision upward train executives to ignore them, and train their team to bypass them. Define what *does not* go upward as deliberately as what does. Keep an explicit "I will decide" column on the decision log.
- **Lateral capture**: a friendly head-of-sales becomes the loudest voice in the register and silently steers the roadmap. The grid hides this when sales is one row of many but spends 80% of PM cycles. Track *time spent per stakeholder* monthly; if it does not match power×interest, recalibrate.
- **Executive attitude is volatile and underspecified.** A VP who was a Supporter at the kickoff demo is Neutral by Q2 if metrics dip. Refresh the executive sub-register monthly, not quarterly.
- **Title-based power is a lie at the senior IC level.** A Principal Engineer or Distinguished Architect can have more product power than a director. Power on this register must be measured by *decisions blocked or unblocked in the last quarter*, not the org chart.
- **Skip-level dynamics:** the PM's manager and their manager's manager are stakeholders too, often with conflicting priorities. Generic registers omit the management chain; PM registers must include it.
- **Cross-cultural and remote nuances**: a "high engagement, monthly written" relationship with a US exec works; the same with a Tokyo-based VP may need an in-person quarterly trip. Encoding only the cadence loses this.

## Agentic workflow
The PM-flavored stakeholder pipeline is three loops, with the PM (or a PM-shaped subagent) as the broker node, never as the data terminator. (1) **Translation loop** — every cross-functional artifact (PRD, status update, incident note) must exist in three audience-tailored forms: exec brief (outcomes + risk), eng spec (decisions + constraints), GTM brief (positioning + readiness). The agent generates all three from one source-of-truth doc and the register chooses the route. (2) **Decision-rights loop** — before any meeting, the PM agent reads the register, identifies the named decision-maker (RACI A) for the topic, and refuses to convene unless that person or a delegated proxy is present; otherwise the meeting becomes status theatre. (3) **Upward-comms cadence loop** — the agent drafts the executive brief on a fixed cadence (e.g. first Monday of each month) using a template that forces three sections: *what changed since last brief*, *the one decision I need from you*, *the one risk I am tracking*. Anything more is noise; an exec's attention budget is the constraint, not yours.

### Recommended subagents
- `faion-pm-agent` (referenced in this methodology's frontmatter; spec at `.../product-manager/agents/`) — runs discovery, drafts the PM-flavored register including a `decision-rights` column and a `comms-direction` column (upward / lateral / downward / external).
- `faion-sdd-executor-agent` — for any SDD task touching multiple stakeholders, the executor reads the register's `decision-rights` column and refuses to mark a task `done` until the named approver has logged sign-off; this prevents the classic PM failure of "eng shipped, legal had not approved".
- `faion-business-analyst` (sibling skill) — pairs with the PM to extract *requirements* from each stakeholder; the BA-flavored interview transcripts are the evidence the PM agent cites when classifying interest and attitude.
- `faion-marketing-manager` / `faion-gtm-strategist` — consumes the *external* slice (key customers, partners, analysts) and the *lateral* slice (sales, support, marketing) to drive launch readiness; PM owns the register, marketing/GTM owns execution against it.
- `password-scrubber-agent` — non-negotiable before any register or upward brief lands in a public repo; PM registers contain personal phone numbers, exec emails and sometimes salary-band information embedded in role definitions.

### Prompt pattern
PM register-generation (broker-flavored):
```
You are a PM stakeholder agent. Read PRD at <path>, latest 4 weekly status
notes, the org chart at <path>, and CODEOWNERS. Build a stakeholder register
with these columns:
  name, role, comms_direction (upward|lateral|downward|external),
  decision_rights (Approve|Consult|Inform|None),
  power (cite a recent decision they blocked or unblocked),
  interest (H/M/L), attitude (Supporter|Neutral|Resistor|Unknown),
  cadence (specific: "biweekly 1:1 Wed", not "ad-hoc"),
  channel (1:1, RFC comments, exec brief, sales weekly),
  owner_of_relationship (PM|TPM|EM|head-of-X).
Mark Unknown for any field you cannot ground in cited source. Output to
.aidocs/product/stakeholder-register.md.
```

Upward-comms brief (executive-attention discipline):
```
Read .aidocs/product/stakeholder-register.md and .aidocs/product/decisions.md.
For stakeholders where comms_direction=upward AND decision_rights in
{Approve, Consult}, draft this month's brief. Hard constraints:
  - 1 page maximum
  - 3 sections: "What changed", "One decision I need", "One risk I'm tracking"
  - No status table; status lives in the dashboard, link it
  - Plain English; no internal codenames without a one-line gloss
  - Surface the bad news in section 1, not section 3
Do not send. Output a draft per executive for human review.
```

Conflict-mediation prompt (lateral broker):
```
Stakeholder A wants X. Stakeholder B wants Y. Read the register and the
roadmap. Recommend the right forum to resolve (1:1, written RFC, steering,
escalate to common manager). Cite the power×interest×attitude rationale.
Draft an opening message for the chosen forum that does not pre-decide.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh` (GitHub CLI) | Resolve CODEOWNERS and PR-reviewer history into the *downward* slice of the register | https://cli.github.com |
| `slack-cli` / Slack Web API | Post the three audience-flavored versions of the same update to per-audience channels | https://api.slack.com |
| `notion-cli` / Notion API | Maintain the executive-shareable view of the register; PMs typically already host PRDs in Notion | https://developers.notion.com |
| `clay` / People-data APIs | Enrich exec stakeholders with current title and org changes (catch the silent re-org) | https://www.clay.com |
| `linear-cli` / Linear GraphQL | Pull project subscribers and triage labels into the lateral slice | https://developers.linear.app |
| `pandoc` + LaTeX | Render the monthly exec brief into a board-ready PDF | system package |
| `mailmerge` | Send the per-exec brief from a register CSV (no marketing tooling needed) | `pip install mailmerge` |
| `mdq` / `yq` | Diff register between commits to detect attitude / engagement drift | https://github.com/mikefarah/yq |
| `ngrok` + Slack slash-cmd | Quick `/whoapproves <feature>` lookup against the register from any Slack channel | https://ngrok.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Productboard | SaaS | Yes — REST API | Stakeholder feedback inboxes; pairs naturally with PM register |
| Aha! / Aha! Roadmaps | SaaS | Yes — API | Built-in stakeholder portal and idea-by-stakeholder view; heavy for solo |
| Notion | SaaS | Yes — REST API | Default home for the register if PRDs live there; use a DB with select fields for attitude |
| Coda | SaaS | Yes — REST API | Dynamic stakeholder dashboards with formulas; good for promotion-prep evidence |
| Linear | SaaS | Yes — GraphQL API | Lateral / downward slice (eng); weak for exec |
| Pendo | SaaS | Yes — API | Pulls *user* stakeholder signals (NPS, feature usage) into the register's external slice |
| Gainsight PX | SaaS | Yes — API | CS-side stakeholder telemetry for B2B PMs |
| Lattice / Workday | SaaS | Limited API | Resolve current management chain; needed for the upward-cadence routing |
| Quantive (formerly Gtmhub) | SaaS | Yes — API | OKR ownership maps; cross-reference OKR-owners against register attitudes |
| Glean / Coveo | SaaS | Search API | Index past meeting notes to ground attitude classifications in evidence |
| Otter.ai / Fireflies | SaaS | Yes — API | Auto-transcribe 1:1s; feed transcripts to the PM agent for register updates (review for sensitive language) |
| Slack Workflow Builder | SaaS | Yes — webhooks | Routes the three audience-flavored briefs from a single source doc |
| Plane / OpenProject | OSS | Yes — REST API | Self-hosted register storage if SaaS off-limits |
| Beeminder / Habitica | SaaS | Yes — API | Personal accountability for the PM's own cadence (this is the cadence that actually slips) |

## Templates & scripts
The product-operations variant ships a `stakeholder_lint.py`. Do not duplicate; instead this PM-flavored helper prints the *imbalance* between PM time-spent and stakeholder power×interest, the failure mode unique to PMs.

```python
# pm_attention_diff.py — flag mismatch between PM time and stakeholder weight.
# Inputs:
#   register.md  (PM stakeholder register, table format)
#   calendar.csv (rows: stakeholder_name, minutes_spent_last_30d)
# Usage: python pm_attention_diff.py register.md calendar.csv
import sys, csv, pathlib

reg = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
rows = [r for r in reg.splitlines() if r.startswith("|") and "---" not in r]
hdr = [c.strip().lower() for c in rows[0].strip("|").split("|")]
score = {"high": 3, "medium": 2, "low": 1, "h": 3, "m": 2, "l": 1}
weight = {}
for r in rows[1:]:
    cells = [c.strip() for c in r.strip("|").split("|")]
    if len(cells) < len(hdr): continue
    name = cells[hdr.index("name")].strip()
    p = score.get(cells[hdr.index("power")].lower(), 0)
    i = score.get(cells[hdr.index("interest")].lower(), 0)
    weight[name] = p * i

mins = {}
with open(sys.argv[2]) as fh:
    for row in csv.DictReader(fh):
        mins[row["stakeholder_name"]] = mins.get(row["stakeholder_name"], 0) + int(row["minutes_spent_last_30d"])

total_w = sum(weight.values()) or 1
total_m = sum(mins.values()) or 1
print(f"{'Stakeholder':<28} {'Weight%':>8} {'Time%':>8} {'Delta':>8}")
for name, w in sorted(weight.items(), key=lambda x: -x[1]):
    wp = 100 * w / total_w
    tp = 100 * mins.get(name, 0) / total_m
    delta = tp - wp
    flag = "  OVER" if delta > 15 else "  UNDER" if delta < -15 else ""
    print(f"{name:<28} {wp:>7.1f}% {tp:>7.1f}% {delta:>+7.1f}%{flag}")
```
A `UNDER` on a high-power Resistor is the bug to fix this week.

## Best practices
- Add a `comms_direction` column (upward | lateral | downward | external). The PM-specific failure modes cluster by direction; you cannot diagnose "I'm losing trust upward" without it.
- Add a `decision_rights` column (RACI-style: Approve / Consult / Inform / None). Without this, every stakeholder seems to have veto power; with it, the PM can confidently say "you are Consult on this, not Approve".
- Treat the management chain as first-class stakeholders, including skip-levels. PMs who omit their manager's manager from the register are blindsided by skip-level reviews.
- Run the register *with* the EM and TPM, not as a PM artifact. Joint ownership prevents the PM from grading their own homework on attitudes.
- Keep an exec sub-register on a tighter refresh (monthly), separate from the operational register. Executive attitudes turn faster than feature-team attitudes.
- For each Resistor, write down *what would change their mind* in one sentence and revisit monthly. If the answer is "nothing", they are not a Resistor; they are a constraint — replan.
- The "one decision I need from you" line in every upward brief is the single biggest predictor of useful exec engagement. Force it.
- Pre-mortem the brief: "If this exec ignores my brief, what is the most likely reason?". Usually it is too long, leads with the wrong thing, or asks for a decision that was already made.
- After every major launch, run a stakeholder-retro distinct from the eng-retro: which relationships strengthened, which strained, which need explicit repair. Log decisions for the next cycle.
- Tie the register to your promotion / level expectations; senior-PM / GPM rubrics reward specific evidence of executive influence and cross-functional conflict resolution. The register and decision log are that evidence.

## AI-agent gotchas
- **Hallucinated decision-rights** are the most damaging error. An LLM confidently asserts "Head of Legal must approve" when in fact a delegate does. Always require the agent to cite a policy doc, RACI matrix, or written email when populating `decision_rights`. Lint for unsourced rows.
- **Sycophantic upward briefs**: agents default to softening bad news for high-power readers. Force a structural rule: section 1 must lead with the worst news. Reject drafts that bury risk.
- **Tone-mismatched lateral messages**: an LLM-drafted message to sales reads as eng-snobbery; the same draft to eng reads as sales-fluff. Generate per-audience variants from a structured source, never paraphrase a single draft into multiple audiences.
- **Calendar-scraping privacy**: agents mining 1:1 transcripts to update attitude classifications have a high false-positive rate and cross legal lines in some jurisdictions (EU, CA). Get explicit consent and surface the source quote with every classification change.
- **Auto-escalation traps**: a cron job that flags "exec sentiment dropped" and emails the exec's manager is a fireable offense. All escalations through humans, always.
- **Persona-shifting exec proxies**: when an exec's chief of staff is the actual decision proxy, an agent that addresses the exec by name in a brief routed through the CoS comes across as oblivious. Encode the proxy in the register and have the agent address by role, not name.
- **Multi-agent register drift**: if both `faion-pm-agent` and `faion-business-analyst` write to the register, you will get conflicting attitude classifications. Designate the PM agent as sole writer; BA proposes via a queue file (e.g. `.aidocs/product/register-proposals.md`) the PM agent reviews.
- **Long-context token waste**: never feed the entire register into every prompt. Filter by `comms_direction` or `decision_rights` for the task at hand. A 200-row register dumped into every brief draft costs more than the briefs save.
- **Prompt-injection via meeting notes**: hostile or careless attendees can paste content into shared notes that the agent ingests. Treat ingested transcripts as untrusted input; never let the agent take action (send mail, change register) without human confirmation.
- **Cross-team sentiment models are biased**: tools that score Slack tone tend to over-flag direct cultures (German, Dutch, Israeli) as "Resistor". Calibrate or disable; do not let cultural communication style be encoded as attitude.
- **Promotion-case fabrication**: do not let an agent draft your promotion narrative directly from the register; LLMs invent decisions you never made. Use the decision log + register *to verify*, write the narrative yourself.

## References
- Marty Cagan — *Inspired* (2nd ed., 2017) and *Empowered* (2020) — PM as broker, executive stakeholder management chapters.
- Melissa Perri — *Escaping the Build Trap* (2018) — outcome-vs-output framing for executive comms.
- Lenny Rachitsky — "Managing up as a PM" and "Stakeholder management for PMs" essays (https://www.lennysnewsletter.com).
- Reforge — *Mastering Product Management* program — `Stakeholder Management & Influencing` module materials.
- John Cutler — *The Beautiful Mess* — recurring posts on broker-PM antipatterns and fixes (https://cutlefish.substack.com).
- Mind the Product — annual "ProductTank" recordings on cross-functional alignment.
- Sibling methodologies in this skill: `roadmap-design`, `release-planning`, `competitive-positioning`, `feedback-management`, `blurred-roles-team-evolution`.
- Companion file: `../../../solo/product/product-operations/stakeholder-management/agent-integration.md` (operational/program-level register patterns).
