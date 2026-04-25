# Agent Integration — PM Certification Alignment 2026

## When to use
- Preparing for the PMP, CAPM, or PMI Disciplined Agile certifications under the 2026 PMBOK 8 / ECO update.
- Updating internal PM curricula, onboarding docs, or playbooks to reflect the new domain weights (People 33% / Process 41% / Business Environment 26%).
- Mapping existing knowledge base content to the new exam themes (Value Delivery, Governance, Sustainability, Stakeholder Engagement, Practical Decision-Making).
- Designing study plans for a cohort of PMs migrating from PMBOK 6/7 to PMBOK 8 — focused on the +18% Business Environment shift.
- Pairing with `pm-certification-changes-2026/` (delta detail), `pm-framework-focus-areas/` (framework topics), `seven-performance-domains/`, `six-core-principles/`, `value-stream-management/`, `benefits-realization/`.

## When NOT to use
- Practitioners not pursuing a certification — apply PMBOK 7/8 principles directly via the framework methodologies; no exam-prep overhead.
- Pre-2026 study plans that need to ship before the cut-over date — use the prior alignment instead.
- Highly specialized domains (Agile-only teams, regulated construction, defense) — supplement with role-specific guides; this methodology is breadth, not depth.
- One-off content gap fixes — read the official ECO directly rather than re-deriving via this methodology.

## Where it fails / limitations
- Exam outlines (ECO) and PMBOK editions drift; the README is a snapshot. Always cross-reference the live PMI ECO PDF before publishing study materials.
- "Themes" (Value Delivery, Sustainability, etc.) are deliberately abstract — agents tend to fabricate concrete sub-tasks. Bind themes to actual PMBOK sections.
- The People/Process/BE percentages reflect exam questions, not real-world time allocation; using them to allocate PMO effort is a category error.
- Sustainability content is shallow in PMI sources; rely on ISO 14001 / GRI / IFRS S1+S2 for substantive material.
- Practical decision-making and tailoring resist memorization; rote-learning agents perform poorly here. Scenario-based practice is required.
- AI/automation content in PMBOK 8 is general; deep AI-PM coverage lives in `predictive-analytics-pm/`, `pm-tool-selection/`, and the `geek/ai/` skills.

## Agentic workflow
Treat the alignment as a knowledge-graph update task. A subagent maps each existing `methodology/README.md` in this skill to one or more 2026 themes + ECO domains, emits a coverage matrix (`alignment-matrix.csv`), and proposes new content where the matrix has zero coverage. A separate study-plan agent generates per-candidate plans from gap analysis (last-completed methodologies, exam date, current weight distribution). Never let an agent claim a methodology "covers" a theme without citing the PMBOK 8 section it maps to — every claim cites a paragraph or page anchor.

### Recommended subagents
- `faion-sdd-executor-agent` — drives the alignment as SDD tasks: TASK_eco_extract, TASK_methodology_mapping, TASK_gap_report, TASK_study_plan_generator.
- A custom `eco-mapper-agent` (model: sonnet per README Agent Selection): ingests the official ECO PDF + PMBOK 8 ToC, emits a structured map of tasks → enablers → domains.
- A custom `coverage-matrix-agent` (model: sonnet): walks the existing methodology library, maps each to ECO tasks, emits CSV/JSON with gap rows highlighted.
- A custom `study-plan-agent` (model: opus): given candidate profile (experience level, exam date, weak areas), produces a sequenced plan referencing methodologies + ECO sections.
- A custom `practice-question-agent` (model: opus): drafts scenario-based questions per theme; outputs go through human SME review (PMI bans direct ECO scraping; questions must be original).
- `password-scrubber-agent` — runs over study plans before sharing externally; learner profile data is HR-sensitive.

### Prompt pattern
Two stages: ECO map → gap report.

```
You are the eco-mapper agent. Inputs:
1. PMI ECO 2026 PDF text (paragraphs).
2. PMBOK 8 table of contents.
3. List of existing methodology slugs in this skill.

Emit STRICT JSON:
[
  { "domain": "People|Process|Business Environment",
    "task_id": "<official>",
    "enablers": ["..."],
    "themes": ["Value Delivery"|"Governance"|"Sustainability"|"Stakeholder Engagement"|"Practical Decision-Making"],
    "covered_by": ["<methodology-slug>", ...],   # may be empty
    "evidence_anchor": "ECO p.NN / PMBOK 8 §x.y" }
]

Rules: never claim coverage without an anchor. Empty covered_by = gap. Do not
invent task IDs. Cite verbatim ECO wording in evidence_anchor.
```

Study plan prompt: `Given candidate profile and gap report, produce a 12-week plan: week → themes → methodologies → practice questions count. Front-load the candidate's lowest-coverage domain. Cite source IDs for every recommendation.`

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pdftotext` (poppler-utils) | Extract ECO/PMBOK PDF text for parsing | `apt install poppler-utils` |
| `pandoc` | Convert PMBOK exports / candidate notes between formats | https://pandoc.org |
| `marker` / `unstructured` | Higher-fidelity PDF → markdown for tables and lists | `pip install marker-pdf unstructured` |
| `git` + `git log` | Track alignment-matrix changes; diffs reveal coverage shifts over editions | preinstalled |
| `csvkit` / `duckdb` | Slice and query the coverage matrix | `pip install csvkit duckdb` |
| `mermaid-cli` (`mmdc`) | Render domain → theme → methodology graphs | `npm i -g @mermaid-js/mermaid-cli` |
| `anki-cli` / `genanki` | Generate spaced-repetition decks for cohort study | https://github.com/kerrickstaley/genanki |
| `obsidian` (vault on disk) | PM-friendly study notebook backed by markdown the agent can read/write | https://obsidian.md |
| `pre-commit` | Block changes to `alignment-matrix.csv` without evidence_anchor | https://pre-commit.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| PMI Online Learning + ATPs | SaaS | None public | Authoritative source; agents cannot scrape. Use as human-checked reference. |
| Project Management Academy / PrepCast / Andrew Ramdayal courses | SaaS | None public | Common cohort training providers. |
| LinkedIn Learning / Coursera / Udemy | SaaS | Limited API (LinkedIn) | Course inventory; agent can curate but not consume content automatically. |
| Anki / RemNote / Mochi | SaaS / OSS | File-based / CLI | Spaced-repetition; agents generate decks. |
| Notion / Obsidian / Logseq | SaaS / OSS | REST / file | Candidate study vault; agents can update. |
| Google Workspace (Docs/Forms) | SaaS | Google APIs | Drafts and quizzes for cohort delivery. |
| Coda | SaaS | REST | Hosts the alignment matrix + study plans with formula support. |
| Khanmigo / NotebookLM | SaaS | None public | Useful for self-study; not agent-driven. |
| Synthesia / Descript | SaaS | REST | Generate explainer videos for difficult themes; PMI-owned content cannot be reused without licensing. |

## Templates & scripts
The README provides the domain-weight delta table and exam themes. Inline below: a script that loads the alignment matrix and prints uncovered ECO tasks.

```python
#!/usr/bin/env python3
"""coverage_gaps.py — list ECO tasks with no methodology coverage."""
from __future__ import annotations
import csv
import pathlib
import sys

def main(path: str = "alignment-matrix.csv") -> int:
    rows = list(csv.DictReader(pathlib.Path(path).open()))
    gaps = [r for r in rows if not r.get("covered_by", "").strip()]
    if not gaps:
        sys.stdout.write("All ECO tasks covered.\n")
        return 0
    by_domain: dict[str, int] = {}
    for r in gaps:
        by_domain[r["domain"]] = by_domain.get(r["domain"], 0) + 1
        print(f"GAP {r['domain']:>22} | {r['task_id']:<10} | {r['themes']}")
    print()
    for d, n in sorted(by_domain.items()):
        print(f"  {d}: {n} gap(s)")
    return 1

if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
```

Wire to weekly CI; failure opens an issue assigned to the PM curriculum owner.

## Best practices
- Anchor every coverage claim to a verbatim quote from the ECO/PMBOK with page or section reference; reject any "summary" claim without an anchor.
- Keep the alignment matrix in git as CSV/JSON; treat it as the system of record. The wiki is generated from it, not the other way around.
- Re-run the mapping after each PMI update (typically annual ECO refresh, every 4–6 years for PMBOK editions).
- For the +18% Business Environment shift: prioritize `benefits-realization/`, `value-stream-management/`, `change-control/`, `pm-framework-focus-areas/` before re-doing People/Process content.
- Practice with scenario-based questions, not memorization; PMP is closed-book reasoning, not rote.
- Allocate study time inversely to current confidence × domain weight — biggest payoff on weakest high-weight area.
- Mix question banks from at least two reputable sources; single-bank patterns over-fit.
- Pair with mentors / study cohorts; the People domain (33%) penalizes solo learners.
- Update internal templates (charters, status reports, lessons learned) to reflect 2026 themes — do not let learners read modern doctrine and use a 2017 template at work.
- Mock exam ≥ 2 weeks before the real one, full-length and timed; calibrate study plan based on results.
- Refresh the alignment with the official PMI errata and ECO updates twice a year.

## AI-agent gotchas
- Agents confidently cite "PMBOK 8 §3.4" without verifying the section exists; force a verification pass against an indexed PMBOK extract.
- Generated practice questions often plagiarize ECO wording or PMI question banks — copyright + cheating risk. Force >2x rephrasing, then human SME review before publishing.
- Domain-weight arithmetic is misleading: agents will recommend 33% of study time on People when a candidate is already strong there. Weight-by-gap, not absolute weight.
- Tailoring questions trip agents — they tend to recommend "use both predictive and agile" generically. Force the agent to cite specific situational triggers.
- Sustainability and ESG topics are shallow in PMI sources; agents fabricate plausible-sounding ISO clauses. Cross-reference ISO/GRI/IFRS only.
- Sample exam questions cannot include verbatim ECO wording — train agents to paraphrase and to add scenario context.
- Study plans hallucinate dates ("Week 5: Mar 12") that misalign with candidate's exam date. Force date arithmetic via Python tool, not LLM.
- Long-context drift: feeding entire PMBOK into one prompt blows context. Page by chapter; persist summaries to disk and rehydrate.
- Cohort-level personalization: agents leak one candidate's profile into another's plan when run in parallel; isolate state per candidate.
- Human-in-the-loop checkpoints (mandatory): publishing a coverage matrix as canonical, releasing practice questions externally, declaring a candidate "ready", any change to weight allocation in a cohort plan.
- PMI prohibits posting verbatim exam content; agents must never quote real exam questions even if surfaced via web search.

## References
- PMI Examination Content Outline (ECO) — current PMP/CAPM exam outline (always check live URL).
- PMBOK Guide 8th Edition (PMI, expected 2026) — definitive content reference.
- PMBOK Guide 7th Edition (PMI, 2021) — 12 principles + 8 performance domains baseline.
- PMI Agile Practice Guide — paired with PMBOK 7+ for hybrid coverage.
- ISO 21500 / 21502 / 21503 — international PM standards (governance, sustainability).
- ISO 14001 / GRI / IFRS S1+S2 — sustainability framework references.
- Sibling methodologies: `pm-certification-changes-2026/`, `pm-framework-focus-areas/`, `seven-performance-domains/`, `six-core-principles/`, `value-stream-management/`, `benefits-realization/`.
- PMI Authorized Training Partner (ATP) program — https://www.pmi.org/certifications/training
