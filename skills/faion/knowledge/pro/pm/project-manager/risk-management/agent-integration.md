# Agent Integration — Risk Management

## When to use
- Project initiation: build initial risk register before charter sign-off.
- Stage-gate reviews: refresh probability/impact and trigger statuses.
- Pre-launch (T-2 weeks): focused launch-risk pass with rollback plans.
- After incidents: feed lessons back as new risks for similar projects.
- High-uncertainty domains (new tech, new vendor, regulatory change) — treat continuously, not as a one-off artefact.

## When NOT to use
- Trivial internal task (1 person, <1 week, no external dependency) — overhead exceeds value.
- Pure agile teams with strong incremental delivery already de-risk via short cycles; a heavy register adds bureaucracy. Use a "top 5 risks" sticky list instead.
- Crisis already in progress — you do incident response, not risk management. Add lessons later.

## Where it fails / limitations
- Probability × Impact scores are subjective; team optimism systematically under-rates probability of own work failing.
- Black-swan / unknown-unknown risks are by definition not in the register; rely on resilience design, not prediction.
- "Accept" is the most-abused response: it lets teams skip planning while pretending to manage the risk.
- Registers go stale within weeks if not actively reviewed; a 6-month-old register is worse than none (false confidence).
- EMV math implies precision the inputs don't have; use it for relative ranking only.

## Agentic workflow
A subagent can scaffold the initial register from charter, scope, WBS, similar past projects' lessons, and a prompt list of risk categories. Use a 2-pass model: first pass enumerates, second pass deduplicates and rates. Keep numerical scoring deterministic via a script — let the LLM produce candidates, the script computes Score and EMV. Human-in-loop required for risk responses (Avoid/Transfer/Mitigate/Accept) because they imply budget and decisions. Schedule weekly automated re-scan of register vs new comms logs to surface drift.

### Recommended subagents
- `faion-pm-agent` — drafts register, runs weekly review.
- `faion-business-analyst` — derives requirement-driven risks (assumptions made → risks).
- `faion-improver` — pulls lessons-learned from done projects and seeds new risks.
- `faion-sdd-executor-agent` — links risks to specific SDD tasks via `risk_id` field.

### Prompt pattern
```
Input: charter.md, wbs.md, prior_lessons.md, vendor_list.md
Output: risks.yaml (id, title, category{technical|external|org|project},
probability{L,M,H}, impact{L,M,H}, type{threat|opportunity},
trigger, owner_role, response_strategy, response_plan, status).
Rules: each risk has a quoted source from input. No invented vendors.
```

```
Weekly audit: compare current register against last 7 days of <status_reports>.
Flag: closed risks still listed; new issues mentioned twice but not in register;
stale risks (no update in 30 days).
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `yq` | Filter risks by score, owner | https://github.com/mikefarah/yq |
| `jq` | Process JSON exports from Jira/Risk modules | https://stedolan.github.io/jq |
| `python -m statistics` / `numpy` | Monte Carlo for schedule risk (PERT) | stdlib + numpy |
| `pandoc` | Render register to DOCX for steering committee | https://pandoc.org |
| `Quantified-self` (`@risk`, `crystal-ball` Excel add-ons) | Quantitative risk; not agent-friendly | commercial |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Jira (Risk Register plugin) | SaaS | Yes — REST API | Use a Risk issue type with custom P/I fields |
| Atlassian Confluence | SaaS | Yes — REST API | Common register host |
| Smartsheet | SaaS | Yes — REST + automations | Triggers when status changes |
| Riskonnect | SaaS | Yes — API | Enterprise risk; heavy |
| ServiceNow GRC | SaaS | Yes — Table API | For regulated industries |
| LogicManager | SaaS | Yes — API | Mid-market GRC |
| OpenRisk (FAIR) | OSS | Yes — Python lib `pyfair` | Quantitative risk in $ terms (FAIR model) |
| Notion / Airtable | SaaS | Yes — REST API | Lightweight registers for solo/small projects |

## Templates & scripts
See `templates.md` for register and response-plan formats. Inline scorer (≤50 lines):

```python
# risk_score.py — compute Score and EMV from a risks.yaml file
import yaml, sys
SCORES = {("L","L"):"low",("L","M"):"low",("L","H"):"med",
          ("M","L"):"low",("M","M"):"med",("M","H"):"high",
          ("H","L"):"med",("H","M"):"high",("H","H"):"crit"}
P_NUM = {"L":0.10,"M":0.30,"H":0.60}

def score(risks):
    out = []
    for r in risks:
        s = SCORES[(r["probability"], r["impact"])]
        emv = None
        if "impact_usd" in r:
            emv = round(P_NUM[r["probability"]] * r["impact_usd"])
        out.append({**r, "score": s, "emv_usd": emv})
    return out

if __name__ == "__main__":
    data = yaml.safe_load(open(sys.argv[1]))
    for r in sorted(score(data), key=lambda x: -(x["emv_usd"] or 0)):
        print(f"{r['id']:<6} {r['score']:<5} EMV={r['emv_usd']!s:<8} {r['title']}")
```

## Best practices
- Track opportunities, not just threats — Exploit/Enhance/Share/Accept symmetric to threat strategies.
- Every risk has an Owner who is a person, not a role like "the team".
- Define explicit Triggers (observable signals) so risks become actionable, not abstract.
- Reserve contingency = sum(EMV) of accepted risks; management reserve sits on top for unknown-unknowns.
- Convert a risk that materialises into an Issue and remove it from the register (don't double-track).
- Risk reviews are short (15 min) but frequent (weekly) — not 2-hour quarterly drills.
- Pair with Change Control: any change request triggers a risk re-rating pass.

## AI-agent gotchas
- LLMs invent generic risks ("scope creep", "team turnover") without grounding; force quoted evidence from inputs.
- Probability ratings cluster around "Medium" — too safe; require justification ("M because vendor missed last 2 SLAs in Q1").
- Numerical EMV implies false precision; always print confidence interval or skip the dollars in agent output.
- Agent may merge distinct risks into one (loses owner clarity) or split one risk into many (inflates register). Constrain via target count: "produce 8-15 risks for a 6-month project".
- Auto-closing risks based on no-mention-in-status-reports is wrong — the absence of mention is not evidence of resolution. Require explicit "closed by" field.
- Do not let an agent tag a risk as "Accept" without a budget/contingency line item — accepting without provisioning is just hoping.

## References
- PMBOK Guide 7th Edition — Uncertainty Performance Domain.
- ISO 31000:2018 — Risk management guidelines.
- "Identifying and Managing Project Risk" — Tom Kendrick.
- FAIR (Factor Analysis of Information Risk) — https://www.fairinstitute.org
- "Black Swan" — Nassim Taleb (on tail-risk and the limits of prediction).
