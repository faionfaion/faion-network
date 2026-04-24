# Agent Integration — Risk Assessment

## When to use
- Pre-launch go/no-go review for a new product, feature, or market entry.
- Investor / due-diligence ask: produce a credible risk register + mitigations.
- Quarterly business review where assumptions need re-validation.
- After a near-miss incident (security, vendor outage, churn spike) — formalize what almost killed you.
- Pivot decision: comparing risk profiles of two strategic options.
- New regulatory exposure (GDPR, AI Act, SOC2, payment rails) appears on the roadmap.

## When NOT to use
- Idea-stage scribbles where you have <3 customer conversations — talk to humans first; risk theater is procrastination.
- Tactical sprint planning — use a normal issue tracker, not a risk register.
- One-person side projects with <$1k at stake — overhead exceeds value.
- When the team will not assign owners or revisit it monthly — a static register is worse than none (false comfort).

## Where it fails / limitations
- **Probability theater:** H/M/L scoring is anchored on gut feel; absolute probabilities are wrong by an order of magnitude. Use it for relative ranking only.
- **Black-swan blindness:** the framework over-weights known categories (market/product/team/financial/operational). Tail risks (founder health, geopolitics, model regulation) get dropped.
- **Mitigation inflation:** every risk gets a generic "monitor + diversify" plan that nobody executes.
- **Optimism in self-assessment:** founders rate their own product/team risks too low. Without an outside reviewer the register is decorative.
- **Static drift:** risk registers age fast — a 6-month-old register reflects a company that no longer exists.
- **No ROI on mitigation:** cost of mitigation rarely tracked vs. expected loss; teams over-spend on low-EV risks (compliance) and under-spend on high-EV ones (concentration in one channel).

## Agentic workflow
Drive risk assessment as a multi-pass pipeline: (1) a researcher agent enumerates candidate risks across the 5 categories from public data + internal docs; (2) a critic/red-team agent runs a pre-mortem to surface omissions; (3) a scorer agent applies prob×impact with explicit citations; (4) a human owner reviews and assigns mitigations. Persist the register as `.aidocs/product_docs/risk-register.md` and re-run pass (1)+(2) monthly via cron. The framework's Step 5 review cadence (weekly top-3, monthly full, quarterly deep) maps cleanly to scheduled subagent runs.

### Recommended subagents
- `faion-market-researcher-agent` (referenced in README) — enumerates market, competitive, and pricing risks from web research; pulls comparable failure cases.
- `faion-research-agent` (skill-level orchestrator at `skills/faion-knowledge/knowledge/pro/research/researcher/`) — top-level dispatcher when running the `risks` mode.
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — converts high-priority risks into SDD tasks (mitigation actions become `todo/` items).
- A purpose-built **red-team / pre-mortem agent** (not yet in repo, worth creating): instructed to assume the project failed and write a post-mortem; output feeds back into the risk register.
- `password-scrubber-agent` (`agents/password-scrubber-agent.md`) — scrub the register before sharing externally; risk text often leaks vendor names, secrets, internal URLs.

### Prompt pattern
Enumeration pass:
```
You are a risk analyst. Given the product brief in <brief>, enumerate
risks across 5 categories: market, product, team, financial, operational.
For each risk: one-sentence statement, evidence (URL or doc ref),
probability (H/M/L), impact (H/M/L). Output as the Risk Register
markdown table from risk-assessment/README.md. Minimum 3 risks per
category. Cite sources inline.
```

Pre-mortem pass:
```
It is 12 months from today. The launch in <brief> failed. Write a
500-word post-mortem explaining what went wrong. Then convert each
failure mode into a risk row (see Pre-Mortem Template). Be specific:
no "lack of focus" — name the channel, the hire, the assumption.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `riskreg` (custom, see Templates) | Render markdown risk register → sorted table by score | inline script below |
| `dalex` / `risk-tools` (Python) | Quantitative risk modeling (Monte Carlo on financial rows) | `pip install dalex` ; https://dalex.drwhy.ai |
| `openfair` / `openpyxl + FAIR` | FAIR-method loss exposure modeling | https://www.fairinstitute.org |
| `mermaid-cli` | Render risk matrix as diagram from text | `npm i -g @mermaid-js/mermaid-cli` |
| `gh` CLI | Mirror high-priority risks as GitHub issues with `risk:` label | https://cli.github.com |
| `pandoc` | Convert risk register markdown → PDF for board / investors | `apt install pandoc` |
| `claude` (Anthropic CLI) | Run enumeration + pre-mortem prompts headless | https://docs.anthropic.com |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| LogicGate Risk Cloud | SaaS GRC | API yes | Enterprise-heavy, overkill for solo founder. |
| Resolver | SaaS GRC | API limited | Audit + risk; not solo-priced. |
| Vanta / Drata | SaaS compliance | API yes | Auto-tracks operational/security risks (SOC2, ISO). Best agent integration in this list. |
| Notion + a database | SaaS docs | API yes | Pragmatic risk register; scriptable via Notion API. |
| Linear / GitHub Issues | SaaS issue tracker | API yes | Treat each risk as an issue with `risk-high` label; mitigations = subtasks. Agents already drive these. |
| Hyperproof | SaaS compliance | API yes | Mid-market; integrates control mappings. |
| OpenFAIR / FAIR-U | OSS / training | n/a | Methodology + free training, not a SaaS. Use to upgrade prob×impact to $-loss×frequency. |
| Monte Carlo simulation in Jupyter | OSS | yes | Cheapest way to stop H/M/L theater for financial risks. |
| Tracecat | OSS GRC/SOAR | yes | Open-source, self-host, agent-callable APIs. |

## Templates & scripts

The methodology already ships a Risk Register and Pre-Mortem template in `templates.md` / `README.md`. The gap is automation: there is no script to sort/render/lint the register. Inline drop-in (≤50 lines):

```bash
#!/usr/bin/env bash
# riskreg.sh — sort risk register by score, lint missing fields.
# Usage: riskreg.sh path/to/risk-register.md
set -euo pipefail
file="${1:?usage: riskreg.sh REGISTER.md}"
python3 - "$file" <<'PY'
import re, sys, pathlib
src = pathlib.Path(sys.argv[1]).read_text()
score = {"H":3,"M":2,"L":1}
rows, errs = [], []
row_re = re.compile(r"^\|\s*(R\d+)\s*\|([^|]+)\|([^|]+)\|\s*([HML])\s*\|\s*([HML])\s*\|\s*\d*\s*\|([^|]*)\|", re.M)
for m in row_re.finditer(src):
    rid, risk, cat, p, i, status = (s.strip() for s in m.groups())
    s = score[p]*score[i]
    rows.append((s, rid, risk, cat, p, i, status))
    if not status: errs.append(f"{rid}: missing status")
    if s>=6 and "mitigat" not in src.lower().split(rid,1)[-1][:600]:
        errs.append(f"{rid}: high score {s} without 'mitigation' nearby")
rows.sort(reverse=True)
print(f"# Risk Register — sorted ({len(rows)} risks)\n")
print("| Score | ID | Risk | Cat | P | I | Status |")
print("|------:|----|------|-----|---|---|--------|")
for s,rid,risk,cat,p,i,st in rows:
    print(f"| {s} | {rid} | {risk} | {cat} | {p} | {i} | {st} |")
if errs:
    print("\n## Lint errors"); [print("-",e) for e in errs]; sys.exit(1)
PY
```

Wire this into `pre-commit` for any repo that owns a `risk-register.md` so stale or unsorted registers fail CI.

## Best practices
- **Force evidence per row.** Reject any risk without a URL, conversation reference, or internal metric. Stops vibes-based registers.
- **Cap at 10 active risks.** Anything below score 4 goes to an `Accepted` archive section, not the live table.
- **Owner ≠ author.** Risks owned by "the team" are unowned. Single name + single trigger metric per high-priority risk.
- **Pre-mortem before launch is mandatory.** The pre-mortem template in this README is the highest-leverage artifact; do it as a 30-minute exercise, not a doc.
- **Track mitigation cost vs. expected loss.** If a mitigation costs more than `prob × impact_$`, accept the risk instead.
- **Diff registers across reviews.** Keep monthly snapshots in git; the delta (new risks, retired risks, score changes) is the actual signal.
- **Outside-view reviewer.** Have someone who is not on the team review the register quarterly. Founders systemically under-rate team and product risks.
- **Tie risks to assumptions.** Each risk should reference an explicit assumption from the spec/design — when the assumption is invalidated, the risk changes state automatically.

## AI-agent gotchas
- **Hallucinated probabilities.** LLMs will assign H/M/L confidently with no basis. Force the agent to cite a source or comparable case for any score; reject ungrounded rows.
- **Category bias.** Agents over-produce market and product risks (well-represented in training data) and under-produce financial / legal / vendor risks. Enforce a quota: ≥2 risks per category.
- **Recency bias from web search.** Researcher agents will pull last week's headlines (e.g., "OpenAI outage") and over-weight them. Cross-check against historical base rates.
- **Optimism leak from system prompts.** If the brief is enthusiastic ("groundbreaking platform"), the agent inherits the tone and scores risks lower. Use a neutral, redacted brief for the risk pass, or flip the agent into adversarial role explicitly.
- **Mitigation handwaving.** Agents default to "improve monitoring" / "diversify" / "stay agile" — banned phrases. Require an action verb + owner + measurable trigger.
- **Risk register drift on re-runs.** Re-running the enumeration agent yields a different ID set every time; agents do not preserve `R1, R2, ...` across runs. Use stable hashes (e.g., slug of risk statement) instead of sequential IDs, or have the agent diff-merge instead of regenerate.
- **No human checkpoint on `Avoid` decisions.** "Avoid" means killing a feature or market — never let an agent autonomously execute that response. Hard human-in-the-loop gate.
- **Confidentiality leak.** Risk statements often contain customer names, vendor terms, or unlaunched plans. Run the scrubber agent before any external sharing or before piping into a 3rd-party SaaS.
- **Agent can't run the pre-mortem alone.** Pre-mortems need divergent perspectives — solo agent runs collapse to one viewpoint. Use 3+ agents with different system prompts (skeptic, customer, competitor) and consolidate.

## References
- Klein, G. (2007). "Performing a Project Premortem." Harvard Business Review. https://hbr.org/2007/09/performing-a-project-premortem
- ISO 31000:2018 — Risk management guidelines. https://www.iso.org/iso-31000-risk-management.html
- NIST SP 800-30 — Guide for Conducting Risk Assessments. https://csrc.nist.gov/pubs/sp/800/30/r1/final
- The Open Group — FAIR (Factor Analysis of Information Risk). https://www.opengroup.org/forum/security/riskanalysis
- Hubbard, D. (2020). "The Failure of Risk Management." Wiley. (Why H/M/L scoring is mathematically broken.)
- Y Combinator — "How to Lose Money in SaaS" risk catalog. https://www.ycombinator.com/library
- a16z — "16 Startup Metrics" (financial risk triggers). https://a16z.com/16-startup-metrics/
- Sibling methodologies in this repo: `pro/pm/pm-traditional/risk-management/`, `pro/pm/pm-traditional/risk-register/`, `pro/research/market-researcher/risk-assessment/`.
