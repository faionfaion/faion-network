# Agent Integration — PMBoK 8 Six Core Principles

## When to use
- Anchoring agentic decision-making with a small, stable rubric: every PM-relevant LLM call can be evaluated against six yes/no questions.
- Drafting / reviewing a project charter, decision log, or change request — verify each principle is honoured.
- Auditing an existing plan for principle gaps (e.g. no sustainability section, no value statement).
- Migrating a PMBoK 7 plan with 12 principles to PMBoK 8 with 6: the agent collapses redundant items into the new structure.
- Authoring agent system prompts for any PM-domain task — bake the six questions into a final-self-check step.

## When NOT to use
- Tactical execution work where the principles are too abstract to bite (sprint planning, individual ticket triage); use methodology checklists instead.
- Non-PMI environments (PRINCE2, IPMA, SAFe) — vocabulary clashes; map to those frameworks' own principles.
- Audit / compliance contexts requiring a specific named standard (ISO 21500, ISO 21502); PMBoK principles are guidance, not certification.
- Work that calls for technical depth (architecture review, security threat modelling) — principles do not substitute for domain expertise.

## Where it fails / limitations
- Six principles are abstract; without a concrete decision framework they degrade into platitudes ("focus on value").
- "Sustainability" measurement is unspecified; teams adopt the word and skip the metric (CO₂, accessibility, social impact proxies).
- Principles overlap (Holistic View ↔ Systems Thinking; Lead Accountably ↔ Build Empowered Teams) — agents weight them inconsistently across runs.
- "Empowered teams" can be invoked to justify lack of governance; counter-pressure required.
- LLMs treat the six as a checklist and tick all six even when one is clearly violated; needs forced negative evidence.

## Agentic workflow
Every PM-domain agent ends with a self-check: re-read the produced artefact and answer six binary questions, with one-sentence evidence each. Output the artefact + the six-line audit. If any principle is violated, regenerate or escalate. Keep the rubric short: one paragraph, six bullets — not a long policy.

### Recommended subagents
- `principle-auditor` (define inline) — input: any PM artefact; output: 6 × {principle, pass/fail, evidence, fix-if-fail}.
- `value-checker` (define inline) — input: deliverable list; output: outcomes ↔ deliverables map (which deliverables ladder to which value).
- `sustainability-tagger` (define inline) — input: project plan; output: sustainability metric proposals per phase.
- `faion-improver` — feed the audit fails into the improver loop for periodic remediation.
- `faion-sdd-executor` — when a fix becomes a code task.

### Prompt pattern
```
Audit this artefact against the PMBoK 8 six principles.
For each principle return:
{ "principle": "Holistic View|Focus on Value|Embed Quality|
                Lead Accountably|Integrate Sustainability|
                Build Empowered Teams",
  "passed": bool,
  "evidence": "≤ 1 sentence quoting the artefact",
  "fix": "imperative if failed, else null" }
Constraints:
- "passed: true" requires positive evidence; absence of failure is not pass.
- Use exactly the six canonical names above.
- If the artefact is incompatible with a principle (e.g. non-PM doc), emit "n/a" for that principle.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `yq` | Validate audit YAML in CI | https://github.com/mikefarah/yq |
| `pandoc` | Convert audit markdown to DOCX / PDF for governance pack | https://pandoc.org/ |
| `markdownlint-cli` | Catch missing principle sections in charter docs | https://github.com/igorshubovych/markdownlint-cli |
| `mermaid-cli` | Render principle-violation summaries as heatmaps | https://github.com/mermaid-js/mermaid-cli |
| `gh pr comment` | Post audit results back into a PR | https://cli.github.com/manual/gh_pr_comment |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Confluence / Notion | SaaS | Yes — REST | Where principle-audit results live |
| Jira / Linear | SaaS | Yes — REST | Audit failures as issues with principle label |
| GitHub / GitLab PRs | SaaS / on-prem | Yes — REST | Audit posted as PR comment |
| Power BI / Looker | SaaS | Yes — SQL | Cross-portfolio principle compliance |
| WatershedClimate / Persefoni | SaaS | Partial — REST | Sustainability metrics for Integrate Sustainability |
| Plan A / Greenly | SaaS | Partial — REST | CO₂ footprint per project |

## Templates & scripts
See `templates.md` for the audit-report skeleton. Inline charter principle-coverage check (Python, ≤50 lines):

```python
#!/usr/bin/env python3
"""Check that a charter document addresses each PMBoK 8 principle."""
import sys, re
PRINCIPLES = [
    ("Holistic View",          r"holistic|system|broader|context"),
    ("Focus on Value",         r"value|outcome|benefit"),
    ("Embed Quality",          r"quality|definition of done|acceptance"),
    ("Lead Accountably",       r"accountab|govern|escalation|integrity"),
    ("Integrate Sustainability", r"sustain|environment|social|carbon|esg"),
    ("Build Empowered Teams",  r"team|empower|autonom|psychological safety"),
]
def main(path):
    text = open(path).read().lower()
    fails = []
    for name, pat in PRINCIPLES:
        if not re.search(pat, text):
            fails.append(name)
    if fails:
        for f in fails:
            print(f"MISSING: {f}")
        sys.exit(1)
    print("Charter covers all 6 PMBoK 8 principles")
if __name__ == "__main__":
    main(sys.argv[1])
```

## Best practices
- Keep the rubric to six bullets in any system prompt — one principle per line — to make it scannable.
- Pair each principle with a concrete indicator (Value → "outcomes table"; Sustainability → "CO₂ proxy"; Quality → "DoD"); avoid measuring abstractions.
- Embed the audit in the gate-review pack so steering committees see it without asking.
- For fast / lightweight projects, run the audit once at charter and once at closure — six checks, twelve minutes.
- Use the audit as a *rejection* gate, not a *score*: any "fail" stops the gate.
- Refresh sustainability indicators yearly as standards evolve (GHG Protocol scope updates, ESRS, ISSB).

## AI-agent gotchas
- LLMs default to "all six pass" because they want to be helpful — force negative evidence and reject all-pass outputs without quotes.
- Sustainability is treated as a paragraph, not a measurement; require a numeric proxy.
- "Empowered teams" gets invoked to justify lack of process; require an offset (working agreements, decision rights).
- Principles get reordered between runs; pin canonical order so diffs are readable.
- "Quality" leaks back as a separate domain (PMBoK 6 muscle memory); reject any audit that names a Quality domain.
- Agents conflate "Holistic View" with "Systems Thinking" (former is PMBoK 8, latter is PMBoK 7); lock the edition in the prompt.
- Audit verdicts drift over time toward all-green; calibrate by sampling a fixed % for human review.

## References
- PMI — A Guide to the PMBOK 8th Edition (in development): https://www.pmi.org/standards/pmbok
- PMI — A Guide to the PMBOK 7th Edition (12 principles): https://www.pmi.org/standards/pmbok
- ISO 21500 — Guidance on Project Management: https://www.iso.org/standard/50003.html
- ISO 21502 — Project, programme and portfolio management — Guidance on project management
- GHG Protocol — Corporate Standard (sustainability metrics): https://ghgprotocol.org/
- ESRS / ISSB sustainability reporting standards (overview): https://www.efrag.org/ , https://www.ifrs.org/groups/international-sustainability-standards-board/
- Mike Griffiths — "What's new in PMBOK 8" (Leading Answers blog)
