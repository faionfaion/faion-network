# PM Certification Exam Changes 2026

## Summary

The PMP exam form active from July 1, 2026 shifts domain weights significantly: People drops from 42% to 33%, Process from 50% to 41%, and Business Environment rises from 8% to 26% (+18pp). Business Environment now covers strategic alignment, governance, sustainability, value delivery measurement, and AI in project management. Study plans must front-load Business Environment, which most candidates have historically under-prepared.

## Why

LLMs trained before mid-2025 emit the old weights (42/50/8) confidently and frame PMP content around "5 process groups + 10 knowledge areas" from PMBoK 6. A candidate using pre-2026 materials without explicit weight correction will systematically under-prepare Business Environment and fail the new exam distribution. The shift correlates with PMBoK 8 emphasis on value delivery, governance, and sustainability.

## When To Use

- Helping a PMP candidate plan a study schedule targeting the new domain weights
- Auditing existing PMP/CAPM training content for Business Environment topic gaps
- Re-tagging an in-house PM knowledge base to match the post-July-2026 weighting
- Building a practice question sampler that respects the new 33/41/26 distribution
- Comparing PMP vs Disciplined Agile vs PRINCE2 2025 cert paths

## When NOT To Use

- General project execution work — exam alignment is academic, not operational; use performance-domains-overview instead
- Candidates sitting before July 1, 2026 — they take the old form; new weights are misleading
- Non-PMI certifications (PRINCE2, IPMA, AgilePM) — the weight shift is PMI-specific

## Content

| File | What's inside |
|------|---------------|
| `content/01-weight-changes.xml` | Domain weight table (old vs new), new emphasis areas, study allocation formula, agent prompt constraints |
| `content/02-rules.xml` | Rules for avoiding stale-weight errors, study plan discipline, gotchas for LLM-generated study content |

## Templates

| File | Purpose |
|------|---------|
| `templates/study-plan.md` | Weekly study plan template with hours allocated per domain by weight x gap |
