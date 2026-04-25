# Agent Integration — Contractor Basics

## When to use
- Solo founder maxed on time and ready to delegate first paid work to a contractor.
- Need to draft a job posting, build a paid-test-task brief, or rank applicants from Upwork/Fiverr/LinkedIn.
- Re-evaluating which tasks are core vs delegate-worthy after a workload spike.
- Computing ROI of delegation vs DIY before committing budget.
- Pre-flight before engaging a contractor: red/green flag screening of a candidate dossier.

## When NOT to use
- Hiring W-2 employees — misclassification risk; use HR-recruiter knowledge instead.
- Running an existing contractor relationship — use `ops-contractor-management` for onboarding, feedback, evaluation.
- Procurement of vendor SaaS or agencies on retainer — different commercial structure (MSA + SOW).
- Hiring inside regulated roles (legal, medical, financial advice) — needs licensed-professional checks beyond this scope.
- Markets where independent contractor classification is legally constrained (CA AB5, EU dependent-contractor tests) — escalate to legal counsel first.

## Where it fails / limitations
- US-centric tax/classification framing (IRS 20-factor test, EIN, W-9). Outside US, agent must localize.
- Hourly rate tables in source README are illustrative only — agent must verify current market rates by region/skill before using them in a brief.
- No guidance on equity-as-comp or revenue share — purely cash-rate model.
- Doesn't cover team-of-contractors coordination — single-contractor framing only.
- Quality screening relies on portfolio assessment; LLM cannot reliably judge visual design quality without a human reviewer in the loop.

## Agentic workflow
Use a single-agent loop for sourcing and shortlisting: scrape job posts, parse applicant data, draft outreach messages. Hand off to a human-in-loop checkpoint before any paid commitment (test task, contract sign, first invoice). Pair with `ops-contractor-management` for the post-hire phase and `ops-legal-basics` for contractor-agreement boilerplate. The agent's job is reducing screening overhead, not picking the contractor.

### Recommended subagents
- `faion-growth-agent` (per source README) — drafts job posts, shortlists candidates, runs ROI math.
- `faion-content-agent` — when the role being hired is content/writing, generates the paid-test-task brief and grades sample work.
- `faion-researcher` — sourcing-channel comparison, current market-rate verification via WebSearch.
- General-purpose Claude subagent — Hagedorn-style "evaluator" pass over candidate dossiers using a structured rubric.

### Prompt pattern
```
You are reviewing 12 Upwork applications for <role>. For each: extract years of experience,
3 most relevant portfolio links, communication quality (1-5), red flags, green flags.
Output JSON array sorted by fit-score. Do NOT recommend a hire — surface a top-3 for human review.
```

```
Compute delegation ROI: my hourly value=$X, task takes me Y hrs/week, contractor rate=$Z/hr,
contractor takes K hrs to do same task. Return weekly savings, annual savings, payback if onboarding takes M hrs.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh` | Pull contractor work product from PRs they own; review diffs | `brew install gh` / cli.github.com |
| `op` | Pull contractor credentials from 1Password vault for tool provisioning | developer.1password.com/docs/cli |
| `wise-cli` (community) | Programmatic Wise transfers for cross-border contractor pay | unofficial wrappers on PyPI; or use Wise REST API directly |
| `stripe` | Create Stripe Connect Express accounts for contractor payouts | `brew install stripe/stripe-cli/stripe` |
| `jq` | Parse Upwork/Toptal API responses, candidate exports | `apt install jq` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Upwork | SaaS | Partial | Public REST API exists but heavily rate-limited; scraping ToS-restricted. Use exported CSVs. |
| Toptal | SaaS | No | No public API; pre-vetted talent — agent's role is brief-writing, not screening. |
| Deel | SaaS | Yes | REST API for contractor onboarding, contracts, payments, compliance docs. Strong agent fit. |
| Remote.com | SaaS | Yes | API for contractor agreements + global payments. Similar to Deel. |
| Bonsai | SaaS | Yes | API for proposals, contracts, invoices — solo-friendly. |
| Wise | SaaS | Yes | REST API for batched contractor payouts (USD→local). |
| Stripe Connect | SaaS | Yes | Programmatic onboarding + payout for US-based contractors. |
| HelloSign / Dropbox Sign | SaaS | Yes | API to send contractor agreements for e-signature. |
| DocuSign | SaaS | Yes | Mature API, more enterprise-leaning. |
| LinkedIn Recruiter | SaaS | No | No agent-grade API for solopreneur tier. |

## Templates & scripts
See `templates.md` for job-post boilerplate and ROI worksheet. Inline helper for delegation triage:

```python
# Delegation ROI calculator
def delegation_roi(my_rate, task_hours_per_week, contractor_rate, contractor_hours):
    my_cost = my_rate * task_hours_per_week
    contractor_cost = contractor_rate * contractor_hours
    weekly_save = my_cost - contractor_cost
    return {
        "weekly_save": weekly_save,
        "annual_save": weekly_save * 50,
        "delegate": weekly_save > 0 and contractor_rate < my_rate * 0.6,
    }

# Example: my_rate=$100, task=5h, contractor=$30/hr, takes 4h
print(delegation_roi(100, 5, 30, 4))
# {'weekly_save': 380, 'annual_save': 19000, 'delegate': True}
```

## Best practices
- Always run a paid test task before committing to ongoing engagement; budget the test as marketing spend, not as work owed.
- Tie the test task to a real deliverable you can ship — never throwaway work; respect contractor's time.
- Force a 24-hour cool-down between shortlist and hire decision; LLM-driven shortlists optimize for surface signal.
- Document the role's quality bar with 2-3 examples of "good" and "bad" output before posting — this is the hardest artifact to produce and the highest-leverage one.
- Use platforms with escrow (Upwork) for first engagement with a new contractor; switch to direct payment (Wise/Stripe) only after 2-3 successful cycles.
- Set explicit timezone overlap requirements in the job post — vague "async friendly" attracts mismatch.
- Never ask for unpaid sample work; this filters out the contractors you actually want.

## AI-agent gotchas
- LLM-generated job posts default to vague "rockstar/ninja" copy — agent must extract specific deliverables from the human first or the post won't filter applicants.
- Agents will hallucinate market rates; always WebSearch current rates by `<role> <region> hourly rate 2025` before publishing a budget range.
- When summarizing applicant pools, LLMs over-weight grammatical fluency — useful for content/copy roles, misleading for design/dev roles where portfolio matters more.
- Do not let an agent send the offer or sign the contract autonomously; mandatory human-in-loop at the contract stage. Misclassification penalties (US ~$1k-25k per contractor) are not LLM-recoverable mistakes.
- Agent-drafted contracts that copy clauses from training data may include unenforceable or jurisdiction-mismatched terms. Always run through `ops-legal-basics` template + human review.
- Token cost: a 40-applicant Upwork pool review is ~30-60k tokens; batch and cache the rubric, score in chunks of 10.
- "Treat as contractor not employee" rule — agents must not auto-schedule the contractor's hours, dictate working tools, or set fixed daily standups; that's a misclassification flag.

## References
- IRS Independent Contractor Defined — https://www.irs.gov/businesses/small-businesses-self-employed/independent-contractor-defined
- Upwork Hiring Guide — https://www.upwork.com/resources/hiring-guide
- Deel API docs — https://developer.deel.com/
- Stripe Connect for contractor payouts — https://stripe.com/docs/connect
- DOL Independent Contractor Final Rule (2024) — https://www.dol.gov/agencies/whd/flsa/misclassification
- Sibling methodology: `ops-contractor-management/README.md`
