# Agent Integration — PM Certification Exam Changes 2026

## When to use
- Helping a PMP candidate plan a study schedule that targets the new domain weights (People 33%, Process 41%, Business Environment 26%).
- Auditing existing PMP / CAPM training content for gaps in Business Environment topics (governance, sustainability, value delivery, AI in PM).
- Re-tagging an in-house knowledge base of PM methodologies against the post-July-2026 weighting so coverage matches the exam.
- Building a question-bank generator that respects the new weights when sampling practice items.
- Comparing two cert paths (PMP vs Disciplined Agile vs Prince2 2025) for a candidate considering the PMI track.

## When NOT to use
- General project execution work — exam alignment is academic, not operational. Use `performance-domains-overview` and the per-domain methodologies instead.
- Candidates sitting before July 1, 2026 — they take the old form (People 42, Process 50, BE 8). The new weights mislead.
- Non-PMI certifications (Prince2, IPMA, AgilePM); the weight shift is PMI-specific.

## Where it fails / limitations
- Methodology readme is a stub (~45 lines) — there is no example bank, no question-style guidance, no tailoring case studies. Treat it as a pointer, not a study plan.
- The +18% Business Environment shift covers a heterogeneous set of topics (sustainability, governance, AI, value delivery) — agents over-index on whichever is in their training data.
- LLMs trained pre-2025 still echo the old weights and the "5 process groups + 10 knowledge areas" framing; explicit re-prompting is needed.
- "Sustainability in projects" lacks a single canonical reference; PMI cites the GPM P5 Standard, ISO 21502, ISO 14001 — agents pick whichever they saw most.
- Cert content outlines change between announcement and exam launch; always fetch the latest PMI ECO PDF, do not rely on cached training data.

## Agentic workflow
The agent is a study-plan generator and gap analyst, not a tutor. Inputs: candidate's exam date, current knowledge state (self-assessment per domain), available study capacity per week. Output: a weighted study plan that allocates time proportional to new domain weights, plus a gap report flagging Business Environment topics where coverage is thin. A second agent samples practice questions from a verified question bank with the new weight distribution. Humans verify cert-board accuracy via the official PMI ECO before trusting numbers.

### Recommended subagents
- `eco-fetcher` — fetches the PMI Exam Content Outline PDF, parses tasks per domain, emits structured JSON.
- `study-planner` — given candidate state + ECO, outputs a weekly plan honouring the 33/41/26 split.
- `gap-analyst` — compares a knowledge base against the ECO, reports uncovered tasks.
- `question-sampler` — samples N items from a question bank with the new weight distribution, balancing People/Process/BE.

### Prompt pattern
```
Inputs:
- exam_date: "2026-07-15"
- candidate_state: {"people": 0.6, "process": 0.5, "business_environment": 0.2}
                   # 0.0 = none, 1.0 = mastered
- weekly_hours: 8
- weights: {"people": 0.33, "process": 0.41, "business_environment": 0.26}

Output JSON:
{ "weeks_until_exam": <int>,
  "weekly_plan": [{"week": 1, "focus": "...", "hours": {...}}],
  "gap_topics": ["sustainability", "governance", ...],
  "recommended_resources": [{"title":"...","url":"...","domain":"..."}] }

Rules:
- Allocate hours proportional to (weight - mastery), not weight alone.
- Cite ECO task IDs when listing topics.
- Refuse to invent question banks; require user-provided source.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pdfplumber` / `pypdf` | Parse the PMI ECO PDF into structured tasks | https://github.com/jsvine/pdfplumber |
| `gh` / `git` | Version-control study plans + gap analyses | https://cli.github.com/ |
| `pandoc` | Convert study plan markdown → Anki / PDF | https://pandoc.org/ |
| `genanki` (Python) | Generate Anki decks weighted to new exam | https://github.com/kerrickstaley/genanki |
| `obsidian-cli` | Sync notes into Obsidian vault for spaced repetition | https://github.com/Yakitrak/obsidian-cli |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| PMI Authorized Training Partner content | SaaS | Limited | Official source; mostly proprietary |
| PrepCast / PMTraining | SaaS | Limited | Question banks; check post-2026 update date |
| Pocket Prep / PMP Exam Prep | Mobile/SaaS | No | Question quality varies; verify weights |
| Anki / RemNote | OSS / Freemium | Yes — file format | Spaced repetition, scriptable |
| Notion / Obsidian | SaaS / OSS | Yes — file/REST | Study notebook |
| Coursera / LinkedIn Learning | SaaS | No | Course content; check publish date |
| GoalQuest / Mometrix | SaaS | No | Practice tests |
| Disciplined Agile Browser (PMI) | SaaS | No | DA decision tables, free with PMI membership |

## Templates & scripts
See `templates.md` for a study schedule template. Inline weight-aware sampler (~20 lines):

```python
import random
WEIGHTS_2026 = {"people": 0.33, "process": 0.41, "business_environment": 0.26}
def sample_questions(bank, n):
    by_domain = {d: [q for q in bank if q["domain"] == d] for d in WEIGHTS_2026}
    out = []
    for d, w in WEIGHTS_2026.items():
        k = round(n * w)
        if k > len(by_domain[d]):
            raise ValueError(f"insufficient {d} questions: need {k}")
        out += random.sample(by_domain[d], k)
    return out
```

## Best practices
- Pin the ECO version date in your study plan (Q3 2025 outline → July 2026 exam). Do not let agents conflate ECO versions.
- Allocate study time proportional to (weight × gap), not weight alone. A candidate strong in People should still spend less time there.
- Budget 30%+ of practice items on Business Environment despite its 26% weight; many candidates underweight the new section.
- Read the PMI Exam Reference List (the published source list); skip third-party content that does not cite it.
- The shift to Business Environment correlates with case-study-style scenario questions; practice scenario interpretation, not flashcards.
- Track sustainability + AI-in-PM topics separately — they are easy to miss inside the broad Business Environment label.

## AI-agent gotchas
- LLMs trained before mid-2025 emit old weights (42/50/8) confidently; force-feed the new split in the system prompt.
- "Business Environment" is also a SOC term and an ITIL term; LLMs cross-pollinate concepts — restrict to PMI vocabulary.
- Sustainability content varies (GPM-P5 vs ISO 21502 vs PRiSM); pin one reference per generated answer.
- ECO PDFs change layout each cycle; brittle PDF parsers break — re-validate parsing with a known-good fixture.
- Practice questions generated by agents drift toward old wording ("processes" vs "principles"); ground them in the 2026 ECO sample items.
- The methodology readme is itself thin; agents will hallucinate detail — require external citations or refuse.
- AI-in-PM is now a tested topic; agents must distinguish AI as exam content vs AI used in studying.

## References
- PMI Exam Content Outline (PMP, July 2026 update) — the authoritative source.
- PMBOK Guide 7th Ed. and *Standard for Project Management* (2021).
- PMI Code of Ethics and Professional Conduct.
- ISO 21502:2020 — Project, programme and portfolio management.
- GPM P5 Standard for Sustainability in Project Management v2.0.
- PMI Pulse of the Profession (annual) — value delivery and Business Environment context.
- Andrew Ramdayal / David McLachlan / Aileen Ellis (current PMP prep authors with 2026-aligned content).
