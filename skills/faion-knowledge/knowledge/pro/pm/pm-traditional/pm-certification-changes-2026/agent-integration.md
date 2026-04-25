# Agent Integration — PM Certification Exam Changes 2026

## When to use
- Preparing PMP/CAPM candidates for the July 1 2026 exam revision (People 33% / Process 41% / Business Environment 26%).
- Updating internal PM training curricula, study-guide repos, or learning paths to reflect the +18% Business Environment shift.
- Building a study-companion agent (flashcards, mock exams, weak-area drilling) that needs a current domain weight map.
- Auditing existing exam prep materials (Rita Mulcahy, PM PrepCast, internal slide decks) to find content gaps against the new outline.
- Pair with `pm-certification-alignment-2026/` (curriculum side) and `benefits-realization/` + `value-stream-management/` (Business Environment topics).

## When NOT to use
- Candidates sitting before the July 1 2026 cutover — the old outline is still authoritative; do not retro-fit them.
- Non-PMI certifications (PRINCE2, IPMA, AgilePM, Scrum.org) — different bodies, different outlines.
- General PM coaching that is not exam-bound — exam weights distort real-world emphasis.
- Practitioners who already passed; this content is exam-shaped, not job-shaped.

## Where it fails / limitations
- The README is a single-page summary; it omits the actual ECO (Examination Content Outline) tasks/enablers per domain. Agents that quote percentages without ECO tasks produce shallow study plans.
- "Sustainability" and "Tailoring" are PMI buzzwords; LLMs hallucinate plausible-sounding but non-PMI definitions. Anchor to PMI Standard for Earned Value (2024), PMBOK 7e, Agile Practice Guide, and the published 2026 ECO PDF.
- Domain weights are not exam question counts; PMI uses scaled scoring per domain. Agents that promise "you must get 26% of Business Environment correct" are wrong.
- Exam item bank evolves continuously after July 2026; static content goes stale within months of release.
- Regional language exams (UA, RU, ES, ZH) lag English by 1–3 quarters; weights are the same but examples differ.

## Agentic workflow
A `cert-curriculum-curator` ingests the official 2026 ECO PDF plus PMBOK 7e / Agile Practice Guide / Process Groups Practice Guide, builds a topic graph (domain → task → enabler → study resources). A `gap-analyzer` diffs current course materials against the graph and outputs a missing-topic list. A `mock-exam-author` generates situational questions weighted to the new domain split, with rationales that cite source pages. A `weak-area-coach` reads candidate quiz history, identifies low-confidence enablers, and queues targeted drills. Human PMP-certified instructor reviews every mock question before it ships — never publish auto-generated PMP items unreviewed.

### Recommended subagents
- `cert-curriculum-curator` (sonnet) — owns the ECO graph, reconciles drift versus PMI announcements.
- `gap-analyzer` (sonnet) — diffs internal materials against the 2026 ECO; emits missing-topic backlog.
- `mock-exam-author` (sonnet) — drafts situational questions, four answer choices, distractor design, source citation.
- `weak-area-coach` (haiku) — chats with candidate, picks next 5 questions from the bank by skill gap.
- `policy-watch-agent` (haiku, scheduled) — polls PMI announcements + PM Network blog for ECO addenda.

### Prompt pattern
```
You are a mock-exam-author. Generate ONE situational question for ECO domain
"Business Environment", task "T1 Plan and Manage Project Compliance", enabler
"identify regulatory requirements". Return STRICT JSON:
{ "stem": "...", "options": ["A","B","C","D"], "correct": "B",
  "rationale": "...", "source": "PMBOK 7e p.NN", "difficulty": "medium" }
Rules: scenario must be 4–6 sentences, distractors must be plausible PMI
language, no trick wording, no time-bound details that go stale.
```

```
You are a gap-analyzer. Inputs: 2026 ECO graph (JSON) and our course outline
(markdown). Output a table of (domain, task, enabler, status, evidence_link)
where status ∈ {covered, partial, missing}. Cite specific course slides.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pdftotext` (poppler) | Extract ECO PDF for ingestion into curriculum graph | `apt install poppler-utils` |
| `pandoc` | Convert course materials between markdown / docx / pptx for diffing | https://pandoc.org |
| `jq` / `yq` | Manipulate the ECO topic graph as JSON/YAML | `apt install jq yq` |
| `anki-cli` / `genanki` (Python) | Generate flashcard decks from enabler list | https://github.com/kerrickstaley/genanki |
| `pytest` | Run a test that validates every mock question has a source citation | `pip install pytest` |
| `git` + branch-per-cohort | Track curriculum versions per exam window | preinstalled |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| PMI.org (CCRS, exam scheduling) | SaaS | Limited API | No public mock-exam API; CCRS PDU submission is web only. |
| Pearson VUE | SaaS | No | Exam delivery vendor; no agent integration. |
| PrepCast / PM Edu | SaaS | No | Closed content; reference only. |
| Anki (AnkiWeb / AnkiConnect) | OSS | Yes | Local API for deck push from `mock-exam-author`. |
| Notion / Confluence | SaaS | REST API | Host the ECO graph + study notes. |
| GitHub / GitLab | SaaS/OSS | Yes | Curriculum repo, PR-based review of generated questions. |
| Quizlet | SaaS | Limited | Sets API deprecated; avoid for new builds. |
| Kahoot / Mentimeter | SaaS | REST | Cohort live-quiz delivery during instructor-led sessions. |

## Templates & scripts
See README for the domain-weight summary table. Inline below: a script that scores a candidate session against the new domain weights.

```python
#!/usr/bin/env python3
"""score_session.py — weighted exam-style scoring per 2026 ECO."""
from __future__ import annotations
import json, sys, pathlib

WEIGHTS = {"people": 0.33, "process": 0.41, "business_environment": 0.26}

def main(path: str) -> int:
    rows = json.loads(pathlib.Path(path).read_text())
    by_dom: dict[str, list[int]] = {k: [] for k in WEIGHTS}
    for r in rows:
        d = r["domain"].lower().replace(" ", "_")
        by_dom.setdefault(d, []).append(1 if r["correct"] else 0)
    weighted = 0.0
    for d, w in WEIGHTS.items():
        items = by_dom.get(d) or [0]
        weighted += w * (sum(items) / len(items))
    print(f"Weighted score: {weighted:.1%}")
    for d, items in by_dom.items():
        if items:
            print(f"  {d}: {sum(items)}/{len(items)} ({sum(items)/len(items):.0%})")
    return 0 if weighted >= 0.61 else 1  # PMI passing band approximation

if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
```

Use as a sanity check, not a pass/fail oracle — PMI scaled scoring is not public.

## Best practices
- Anchor every generated question to a primary PMI source (PMBOK 7e, Agile Practice Guide, PfMP/PgMP standards) with page citation; reject questions without citations.
- Rebuild the ECO graph from the official 2026 PDF on each PMI revision announcement; never edit it by hand.
- Track candidate weak areas at the enabler level, not the domain level — domain-level coaching is too coarse.
- Human-review 100% of auto-generated mock items before they reach candidates; PMP brand exposure to bad items is a credibility risk.
- Maintain language parity for at least UA + EN if your audience is bilingual; translate stems with PMI vocabulary, not literal translation.
- Pair certification prep with a real-project simulation (kanban board, risk register, EVM exercise) so candidates do not become test-taker-only PMs.
- Sunset old (2021 outline) materials with a clear date stamp; do not silently overwrite — auditors and re-takers need both versions.

## AI-agent gotchas
- LLMs invent PMI vocabulary that "sounds right" (e.g., "Strategic Tailoring Index"). Force a glossary check against PMBOK 7e index before accepting any term.
- Domain weight drift: agents fed old outlines (42/50/8) will silently regress; pin the 33/41/26 weights in the system prompt, not a retrieval doc that can be evicted.
- "Business Environment" is the largest growth area and most under-represented in legacy material — quotas alone do not fix shallow content; require new examples per enabler, not paraphrases.
- Distractor design is hard for LLMs — they often produce options that are obviously wrong or two-correct. Run a self-critique pass.
- Region/language: same weights, different idioms. Translation agents that copy English idioms into UA/PT lose realism.
- Citation hallucination: LLMs love fake page numbers. Validate citations by retrieving the cited PDF page text and checking for keyword overlap before publishing.
- Never let an agent decide if a candidate is "ready"; emit readiness signals (sub-domain confidence, mock score trend) and let a human instructor make the call.
- PDU/CCRS reporting: do not auto-submit PDUs on a candidate's behalf — PMI compliance issue; agents only draft.

## References
- PMI Examination Content Outline (PMP) — 2026 revision PDF (PMI.org/certifications/project-management-pmp).
- PMBOK Guide 7e (2021), PMI.
- Agile Practice Guide (2017, joint PMI/Agile Alliance).
- Process Groups: A Practice Guide (2022).
- PMI Standard for Earned Value Management (2024).
- Sibling methodology in this repo: `pm-certification-alignment-2026/` (curriculum mapping side).
