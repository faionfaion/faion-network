# Agent Integration — PM Certification 2026 Alignment (PM Traditional)

## When to use
- Mapping an existing PM curriculum, study guide, or in-house playbook against the 2026 PMP Exam Content Outline themes (Value Delivery, Governance, Sustainability, Stakeholder Engagement, Practical Decision-Making).
- Re-tagging methodology libraries against the new domain weights (People 33% / Process 41% / Business Environment 26%).
- Auditing whether content covers Project Management Framework 8 emphasis areas: business case, benefits realization, strategic alignment, organizational change, value stream mapping, AI-in-PM, sustainability.
- Generating tailored study tracks for candidates who already hold PMP6 or PRINCE2 and need bridge content.
- Building a corporate "PMP-ready" path that aligns project ops with cert content.

## When NOT to use
- General project execution work — alignment is academic; for delivery use `performance-domains-overview` + per-domain methodologies.
- Pre-July 2026 candidates who must take the old exam form (42/50/8 weighting).
- Non-PMI certifications (PRINCE2 2025, IPMA, ISO 21502 conformity) with their own content outlines.
- Candidates on the project-manager track who already passed PMP after 2021; the renewal CCRs are a different process.

## Where it fails / limitations
- Methodology readme is a stub (~45 lines). It pairs with `pm-certification-changes-2026` and is incomplete on its own.
- "Tailoring" is the exam's hot phrase but ill-defined; LLMs tend to pick a methodology by name match, not by tailoring decision.
- Sustainability theme aggregates ESG, ISO 14001, GPM-P5, UN SDGs, climate-aware project planning — agents pick whichever is in training data.
- Governance theme overlaps PMO operations, PfMP / PgMP scope, and SOX-style controls; agents conflate them.
- Stakeholder engagement integration with comms management is doctrinal in 2026, but old prep books treat them as separate; alignment risk.
- AI-in-PM topic is moving target; ECO updates quarterly while exam materials lag.

## Agentic workflow
The agent is a curriculum aligner and gap analyst. (1) Ingest: read the 2026 ECO PDF, parse tasks per domain. (2) Crosswalk: tag existing content (training modules, methodology pages, internal playbooks) against ECO tasks. (3) Gap report: list ECO tasks with no content; rank by exam weight × candidate weakness. (4) Tailor: produce a per-candidate or per-cohort study path emphasising under-covered themes. Humans verify ECO version, sign off content edits, and own pedagogical sequencing.

### Recommended subagents
- `eco-fetcher` — fetches PMI Exam Content Outline PDF, parses domains/tasks/enablers into JSON.
- `crosswalk-builder` — embeds ECO tasks + content chunks, tags coverage with similarity threshold.
- `gap-prioritizer` — orders gaps by (exam_weight × candidate_weakness × content_coverage_gap).
- `tailoring-advisor` — emits the "tailoring decision tree" recommended by the exam: predictive vs adaptive vs hybrid for given inputs.
- `sustainability-mapper` — maps sustainability theme to a chosen reference standard (ISO 21502 / GPM-P5 / UN SDGs).

### Prompt pattern
```
Inputs:
- eco.json: PMI 2026 ECO parsed
- content_corpus: list of {id, title, text, tags, domain}
- candidate_profile (optional): {strengths:[domain], weaknesses:[domain]}

Output JSON:
{ "coverage_pct_by_domain": {"people":..., "process":..., "BE":...},
  "uncovered_eco_tasks": [{task_id, domain, weight}],
  "recommended_study_order": [{task_id, content_ids:[...]}],
  "sustainability_reference": "ISO 21502 | GPM-P5 | both",
  "ai_in_pm_topics": [...],
  "tailoring_decisions_to_practice": [...] }

Rules:
- Pin ECO version date in output.
- For BE domain, require evidence of coverage in: business case,
  benefits realization, strategic alignment, sustainability, AI-in-PM,
  governance, value-stream-mapping. If <5/7 covered, flag major gap.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pdfplumber` / `pypdf` | Parse the PMI ECO PDF | https://github.com/jsvine/pdfplumber |
| `chromadb` / `qdrant` | Embedding store for ECO ↔ content crosswalk | https://www.trychroma.com/ |
| `sentence-transformers` | Generate embeddings | https://www.sbert.net/ |
| `pandas` | Coverage tables, gap reports | https://pandas.pydata.org/ |
| `pandoc` | Render gap reports → PDF | https://pandoc.org/ |
| `git` | Version-control study path + content tags | https://git-scm.com/ |
| `obsidian-cli` | Sync the curriculum into a study vault | https://github.com/Yakitrak/obsidian-cli |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| PMI ATP content | SaaS | Limited | Authoritative; mostly proprietary |
| Disciplined Agile Browser | SaaS | No | PMI member access, decision tables |
| PrepCast / PMTraining | SaaS | Limited | Verify post-2026 update date before use |
| Coursera / LinkedIn Learning | SaaS | No | Variable freshness |
| Anki + AnkiConnect | OSS | Yes — REST | Spaced repetition; programmable card creation |
| Obsidian + Spaced Repetition | OSS | Yes — file | Curriculum vault |
| GitBook / Notion | SaaS | Yes — REST | Public-facing curriculum |
| Brainscape / Quizlet | SaaS | Limited | Card decks |

## Templates & scripts
See `templates.md` for crosswalk and study-track templates. Coverage scorer (~25 lines):

```python
def coverage(eco_tasks, content_chunks, embed, threshold=0.72):
    covered = []
    uncovered = []
    for task in eco_tasks:
        t_emb = embed(task["text"])
        best = max((cos(t_emb, embed(c["text"])) for c in content_chunks),
                   default=0)
        (covered if best >= threshold else uncovered).append(
            {**task, "best_sim": round(best, 3)})
    by_domain = {}
    for task in eco_tasks:
        d = task["domain"]
        by_domain.setdefault(d, {"total": 0, "covered": 0})
        by_domain[d]["total"] += 1
    for task in covered:
        by_domain[task["domain"]]["covered"] += 1
    return {"by_domain": {d: round(v["covered"]/v["total"], 2)
                          for d, v in by_domain.items()},
            "uncovered": uncovered}
```

## Best practices
- Pin the ECO version date; ECO updates quarterly and curricula must declare which version they target.
- Allocate study/content effort proportional to (exam_weight × current_gap), not to weight alone.
- Treat sustainability + AI-in-PM as first-class themes; they sit inside Business Environment and are easy to under-cover.
- Practice tailoring decisions explicitly: build flashcards "given context X, choose predictive/agile/hybrid because…".
- When updating training content for the 2026 exam, version the docs with a `eco_version: 2026-Q3` front-matter field for traceability.
- Do not collapse Process and Business Environment into "PM theory"; the new exam has distinct question styles per domain.

## AI-agent gotchas
- LLMs trained pre-2025 emit old weights confidently (42/50/8). Force the new split (33/41/26) in system prompt.
- Sustainability standard hallucination: agents cite "PMI Sustainability Standard" which doesn't exist as a single doc; clarify GPM-P5 vs ISO 21502 vs ISO 14001 explicitly.
- Crosswalk threshold sensitivity: 0.7 vs 0.75 cosine similarity changes coverage by 20+%. Pin and document.
- PDF parsing of ECO drops table structure; always validate parsed tasks against page count.
- Tailoring suggestions reduce to "use Scrum if uncertain" — agents over-recommend agile. Force trade-off rationale citing PMBOK7 principles.
- AI-in-PM topic surface area is unstable; freeze a topic list per ECO version rather than letting the agent re-derive.
- Content tags drift across authors; require a fixed tag taxonomy aligned to ECO domain/task IDs.

## References
- PMI Exam Content Outline (PMP, July 2026 update).
- PMBOK Guide 7th Ed. + *Standard for Project Management*.
- *Process Groups: A Practice Guide* (PMI, 2022) — bridges PMBOK6 process groups to PMBOK7.
- ISO 21502:2020 — Project, programme and portfolio management.
- GPM P5 Standard for Sustainability v2.0.
- PMI Disciplined Agile (DA) Toolkit.
- "Generative AI in Project Management" — PMI 2024 white paper.
- companion methodology: `pm-certification-changes-2026` for weight-shift detail.
