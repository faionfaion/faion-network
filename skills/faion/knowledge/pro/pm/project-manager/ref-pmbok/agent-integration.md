# Agent Integration — PMBoK 7 & 8 Reference

## When to use
- Ground-truthing PMBoK terminology in any prompt where domain / principle / process names matter (system prompts, sponsor decks, certification answers).
- Quick-lookup table for EVM formulae, risk-response strategies, RAG status, estimation accuracy bands when an agent is producing a status report.
- Disambiguating PMBoK 6 (process groups + knowledge areas) vs 7 (principles + domains) vs 8 (streamlined principles + non-prescriptive processes) before any content is generated.
- Building a translation layer for teams migrating from PMBoK 6/7 plans into 8.

## When NOT to use
- As a stand-alone methodology to *do* anything. This is a reference; pair it with the operational methodologies (WBS, risk register, schedule, etc.).
- For training data on agentic behaviour — the reference contains zero examples, only definitions.
- For non-PMI methodologies (PRINCE2, IPMA, ISO 21500); concepts overlap but vocabulary differs and a pure PMBoK lens distorts them.

## Where it fails / limitations
- Static reference: PMBoK 8 is in late-draft / early-release at the time of writing; tables here may shift slightly when PMI publishes the final.
- The PMBoK 7 → 8 deltas (12 → 6 principles, 8 → 7 domains) can flip mid-project; agents must know which edition they are anchored to.
- AI-coverage table inside the doc names current SaaS features (Jira Rovo, MS Project Copilot) — those evolve quickly, so links rot.
- EVM formulae assume a baseline exists; if the project is agile with no baseline, EVM is meaningless and the formulas mislead.
- Estimation accuracy bands (analogous, parametric, three-point) are heuristics, not contracts; agents quoting them as guarantees mislead sponsors.

## Agentic workflow
Treat this file as a constants module the agent reads on every PM prompt. Inject the relevant table (domains, principles, EVM, estimation, risk strategies, RAG) into the system prompt to anchor terminology. Cite `ref-pmbok` whenever an agent uses a defined term so reviewers can audit. Keep a `pmbok_edition` field in project context (6/7/8) and drive table selection from it.

### Recommended subagents
- `pm-glossary-resolver` (define inline) — input: free-text PM artefact; output: list of PMBoK terms used + edition + canonical definition.
- `evm-calculator` (define inline) — input: BAC, PV, EV, AC; output: SV, CV, SPI, CPI, EAC, ETC, VAC + RAG.
- `faion-sdd-executor` — when a PM artefact becomes a code task.
- `faion-brainstorm` — to generate domain-specific risk lists by walking the 7/8 domains.

### Prompt pattern
```
You are using PMBoK <edition> as the canonical vocabulary.
Allowed terms: <inject relevant table from ref-pmbok>.
- Replace any synonym in <input_text> with the canonical PMBoK term.
- Flag any term outside the table as "non-canonical".
- For EVM, always show formula AND result; never just the result.
- For risk strategies, always pair the risk with one of:
  threat: [Avoid, Transfer, Mitigate, Accept]
  opportunity: [Exploit, Share, Enhance, Accept]
- Output: { "rewritten_text": "...", "non_canonical": ["..."] }
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pmcalc` (custom Python) | EVM formula calculator | n/a — inline below |
| `numpy` / `scipy.stats` | Three-point distributions for estimation tables | https://scipy.org/ |
| `pandoc` | Render PMBoK reference into DOCX / PDF for sponsor packs | https://pandoc.org/ |
| `mermaid-cli` | Diagrams of domain interactions, principle networks | https://github.com/mermaid-js/mermaid-cli |
| `gh` | Pull issues into EVM as scope baseline | https://cli.github.com/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| PMI Standards Plus | SaaS (subscription) | No — paywalled docs | Authoritative source for PMBoK content |
| MS Project / Project for the Web | SaaS | Yes — Graph API | Native EVM fields, baseline tracking |
| Smartsheet | SaaS | Yes — REST | EVM via formula columns |
| Primavera P6 | Desktop / SaaS | Partial — XER files | Heavy EVM + schedule analytics for capital projects |
| Deltek Cobra / wInsight | SaaS | Partial — REST | Industrial-grade EVM tooling |
| ClickUp / Jira / Asana | SaaS | Yes — REST | Custom-field EVM dashboards |
| Power BI / Looker | SaaS | Yes — SQL/REST | EVM dashboards across portfolios |

## Templates & scripts
See `templates.md` for the EVM dashboard skeleton. Inline EVM calculator (Python, ≤50 lines):

```python
#!/usr/bin/env python3
"""EVM calculator. Inputs in dollars except SPI/CPI."""
import json, sys
def evm(bac, pv, ev, ac, today_pct=None):
    sv = ev - pv
    cv = ev - ac
    spi = ev / pv if pv else float("nan")
    cpi = ev / ac if ac else float("nan")
    eac = bac / cpi if cpi else float("nan")
    etc = eac - ac
    vac = bac - eac
    rag = ("green" if spi >= 0.95 and cpi >= 0.95
           else "amber" if spi >= 0.85 and cpi >= 0.85
           else "red")
    return {"SV": round(sv, 2), "CV": round(cv, 2),
            "SPI": round(spi, 3), "CPI": round(cpi, 3),
            "EAC": round(eac, 2), "ETC": round(etc, 2),
            "VAC": round(vac, 2), "RAG": rag}
if __name__ == "__main__":
    inp = json.load(open(sys.argv[1]))
    print(json.dumps(evm(**inp), indent=2))
```

## Best practices
- Pin the PMBoK edition in every project charter; never let an agent assume.
- Quote formulas alongside results; agents that emit only "$92K EAC" cannot be audited.
- Use RAG sparingly: if more than 50% of projects are amber, the threshold is wrong, not the projects.
- Translate predictive metrics for agile contexts (use cycle time + flow efficiency; do not force EVM where there is no baseline).
- Keep a single source-of-truth file for PMBoK terminology in the repo; never hard-code definitions in multiple agent prompts.
- For PMBoK 8, treat sustainability as a first-class metric, not a paragraph; pick a measurable proxy (CO₂ per release, accessibility audit pass rate).

## AI-agent gotchas
- PMBoK 6 is heavily over-represented in LLM training data; agents will say "Integration Management" by default. Force PMBoK 7/8 vocabulary in the system prompt.
- "Quality Management" sneaks back as a process; in 7/8 it is integrated. Reject outputs that name a Quality domain.
- Estimation accuracy bands are quoted as facts; they are heuristics — caveat in output.
- EVM formulas with zero / near-zero PV or AC blow up; clamp denominators and emit `null` not `inf`.
- LLM arithmetic on > 5 EVM rows drifts — always do math in code.
- "RAG" overloads with "retrieval-augmented generation"; in PM contexts disambiguate by spelling out (Red/Amber/Green) on first use.
- Agents drop the AI-in-PM table because it cites SaaS features that change quickly; refresh the table semi-annually.

## References
- PMI — A Guide to the PMBOK 7th Edition: https://www.pmi.org/standards/pmbok
- PMI — PMBOK 8th Edition (Standards Plus, in development): https://www.pmi.org/standards/pmbok
- PMI — Practice Standard for Earned Value Management (3rd ed.): https://www.pmi.org/standards/earned-value-management
- PMI — Practice Standard for Project Estimating: https://www.pmi.org/learning/library/practice-standard-project-estimating
- PMI — Practice Standard for Project Risk Management: https://www.pmi.org/standards/risk
- AACE International Recommended Practices (for estimation classes): https://www.aacei.org/resources/recommended-practices
- Mike Griffiths — "PMBOK 7th vs 6th Edition" (Leading Answers blog)
- Praxis Framework (open alternative): https://www.praxisframework.org/
