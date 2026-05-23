# AI-Assisted Interview Note Synthesis

## Summary

**One-sentence:** Synthesizes raw user-interview notes into a structured insight report with quotes, themes, and confidence ratings using staged LLM passes + human verification.

**One-paragraph:** Synthesizes raw user-interview notes into a structured insight report with quotes, themes, and confidence ratings using staged LLM passes + human verification. The methodology is testable end-to-end: each artefact it produces conforms to the JSON Schema in `content/02-output-contract.xml`, every claim in the body resolves to a rule in `content/01-core-rules.xml`, and the decision-tree in `content/06-decision-tree.xml` routes observable inputs to the right rule.

**Ефективно для:**

- 5-15 інтерв'ю за тиждень — потрібен синтез без 2 днів ручного coding.
- Theme extraction з прив'язкою до verbatim quotes + interview-id.
- Confidence rating H/M/L за кількістю респондентів, що підтверджують тему.
- Human-in-the-loop: LLM пропонує, дослідник верифікує — не auto-publish.

## Applies If (ALL must hold)

- ≥5 транскриптів інтерв'ю однієї cohort з тією ж темою дослідження.
- Транскрипти у тексті або з timestamp + speaker labels.
- Дослідник доступний для верифікації перед публікацією звіту.

## Skip If (ANY kills it)

- 1-2 інтерв'ю — ручний синтез швидший і точніший.
- Інтерв'ю містять PII/sensitive content без redaction policy.
- Stakes < $10k decision — overhead звіту > value.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| transcripts | Markdown or JSON {interview_id, text} | interview platform |
| research question | one sentence | PI |
| cohort metadata | YAML {N, segments, recruit_criteria} | recruiter |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[ai-interview-analysis]] | single-interview analysis available upstream |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom/root-cause/fix) | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure (input/action/output/decision-gate) | 900 |
| `content/05-examples.xml` | essential | One worked example end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule in 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| classify-input | sonnet | Light judgment; identifies branch in decision tree. |
| draft-output | sonnet | Drafting the output artefact per schema. |
| validate-output | haiku | Mechanical schema validation via script. |

## Templates

| File | Purpose |
|------|---------|
| `templates/synthesis-report.md` | Final synthesis report skeleton |
| `templates/synthesis.json` | Machine-readable synthesis matching schema |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-interview-note-synthesis-ai.py` | Validate output artefact against schema in 02-output-contract.xml | CI on each artefact change; pre-commit |

## Related

- [[ai-interview-analysis]]
- [[ai-coding-of-qualitative-data-protocol]]
- [[ai-assisted-persona-building]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from the question "Do we have N >= 3 interviews and a redaction policy?" and routes observable input signals to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Apply it whenever the input shape changes or before scaling a pilot run.
