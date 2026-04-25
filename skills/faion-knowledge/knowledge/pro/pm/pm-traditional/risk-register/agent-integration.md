# Agent Integration — Risk Register

## When to use
- Multi-month delivery requiring a single source of truth for risks across teams.
- Audited / regulated programs needing a register with IDs, owners, and decision history.
- Programs with quantitative contingency reserves that must be defended to finance.
- Cross-vendor / cross-org work where risks span ownership boundaries.

## When NOT to use
- Solo / hobby projects (a `RISKS.md` checklist is enough).
- Pure-Scrum teams running impediment + retro loops with adequate coverage.
- Spike / discovery work where most "risks" are research questions.

## Where it fails / limitations
- Stale registers — without weekly review, scores drift from reality fast.
- Probability/impact buckets compress information (Medium-Medium swamp).
- Score = P × I treats risks as independent; correlated risks (vendor delays cluster) are under-weighted.
- "All accept" anti-pattern: every row marked Accept with no contingency funded.
- Opportunities are systematically under-tracked — registers become threat-only.

## Agentic workflow
A subagent owns the register's mechanical lifecycle: ingest meeting notes / status reports / change events to surface candidate risks, normalize entries (ID, category, P, I, score, strategy), produce a weekly diff (new / changed / closed / stale), and push updates to the tracker. Humans own probability/impact judgement, response approval, and contingency funding. This methodology is the artefact; pair with `risk-management` (process) for a complete loop.

### Recommended subagents
- `faion-pm-agent` — owns register, drafts entries, runs weekly diffs.
- `faion-brainstorm` (skill) — diverge round at kickoff and phase gates to seed the register.
- `faion-business-analyst` — strong on category coverage (technical/external/organizational/PM).
- `faion-improver` — reviews closed risks → lessons-learned input.

### Prompt pattern
```
You are a risk-register curator. Inputs: charter, current register, last
14 days of status reports + meeting notes.
Output JSON with three lists: NEW (proposed entries), CHANGED (id +
field deltas), STALE (id, last_update_date). For every entry include
rationale citing source. Do NOT mutate; emit proposals only.
```

```
Score this risk on the 5x5 P/I matrix. Output P, I, score, priority, plus
one-sentence rationale per axis citing project artefacts. If confidence
is low, set needs_review=true and explain.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `riskman` (npm) | Markdown-driven register with CLI scoring | https://www.npmjs.com/package/riskman |
| `risk-cli` (Python) | Monte Carlo on EMV inputs | `pipx install risk-cli` |
| `jira-cli` | Risks as `Risk` issue type with custom fields | https://github.com/ankitpokhrel/jira-cli |
| `gh` | Risks as issues with `risk` + priority labels | https://cli.github.com |
| `csvkit` / `dsq` | Query CSV registers (`dsq risks.csv 'select ...'`) | https://github.com/multiprocessio/dsq |
| `pandoc` | Render to PDF for steering committee | https://pandoc.org |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Jira RMsis / Risk Management for Jira | SaaS plugin | Yes — REST API | First-class risk type, P×I custom fields, register reports. |
| Smartsheet RAID log | SaaS | Yes — REST API | Strong for PMOs and contractors. |
| Monday.com risk template | SaaS | Yes — GraphQL | Easy adoption, weak quantitative tooling. |
| ServiceNow GRC | Enterprise SaaS | Yes — REST API | Heavyweight; for regulated programs. |
| Notion risk DB | SaaS | Yes — REST API | Best for solo / SDD repos; agent fully drives. |
| Active Risk Manager (Sword) | Enterprise | Yes — SOAP/REST | Defense / megaproject context. |
| Resolver | Enterprise SaaS | Yes — REST API | GRC-heavy organizations. |

## Templates & scripts
See `templates.md` for register layout and individual risk card. Helper to flag stale and high-score risks:

```python
# risk_audit.py — stale or high-priority risks in a CSV register.
import csv, datetime, sys
today = datetime.date.today()
with open(sys.argv[1]) as f:
    for r in csv.DictReader(f):
        score = int(r.get("score") or 0)
        upd = r.get("last_update")
        try:
            d = datetime.date.fromisoformat(upd)
        except Exception:
            d = today
        stale_days = (today - d).days
        flags = []
        if score >= 15: flags.append("HIGH")
        if stale_days > 14 and r.get("status","").lower()=="open":
            flags.append(f"STALE_{stale_days}d")
        if not r.get("owner"): flags.append("NO_OWNER")
        if flags: print(r["id"], ",".join(flags))
```

## Best practices
- Pair every risk with a measurable trigger; without a trigger you cannot detect activation.
- Mandate explicit owner per row — "team" is not an owner.
- Keep the top-5 risks on every status report; long-tail goes in appendix.
- Roll EMVs into a single contingency request; finance funds aggregates, not rows.
- Color-code opportunities and threats; review parity at every weekly meeting.
- Close risks explicitly with outcome (materialized / passed / merged-into-RX); never delete.
- For SDD repos: store the register as Markdown + table for diff-friendly history.

## AI-agent gotchas
- LLMs cluster scores at Medium-Medium; require per-axis rationale to spread distribution.
- Auto-generated risks are often generic ("vendor delay"); seed with project-specific artefacts (charter, ADRs, vendor SOWs).
- Agents will assign owners speculatively — leave blank by default and flag for human assignment.
- Do not allow autonomous closure; closure has audit consequences and impacts contingency calculations.
- Token budget: send only top-N + changed rows, not the full register, on each turn.
- Human-in-loop checkpoints: (1) calibration round at kickoff, (2) approval of NEW high-score entries, (3) weekly diff review, (4) any contingency-impacting change.

## References
- PMI, *PMBOK Guide* 7th ed., Uncertainty Performance Domain.
- PMI, *Practice Standard for Project Risk Management*.
- ISO 31000:2018 — Risk management guidelines.
- D. Hubbard, *The Failure of Risk Management* (2009) — critique of P×I matrices.
- D. Vose, *Risk Analysis: A Quantitative Guide* (3rd ed.) — Monte Carlo for EMV.
