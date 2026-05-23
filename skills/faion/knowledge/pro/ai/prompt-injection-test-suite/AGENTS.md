---
slug: prompt-injection-test-suite
tier: pro
group: ai
domain: ai-core
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Maintains a CI-gated test suite covering OWASP LLM Top 10 attack classes (jailbreak / prompt-injection / data-exfil / system-prompt-leak / tool-misuse) that blocks merge when an AI feature regresses against any class.
content_id: "73b712527b3fd0a7"
complexity: deep
produces: code
est_tokens: 5500
tags: [ai, security, prompt-injection, owasp-llm-top-10, qa, ci]
---
# Prompt Injection Test Suite

## Summary

**One-sentence:** Maintains a CI-gated test suite covering OWASP LLM Top 10 attack classes (jailbreak / prompt-injection / data-exfil / system-prompt-leak / tool-misuse) that blocks merge when an AI feature regresses against any class.

**One-paragraph:** Maintains a CI-gated test suite covering OWASP LLM Top 10 attack classes (jailbreak / prompt-injection / data-exfil / system-prompt-leak / tool-misuse) that blocks merge when an AI feature regresses against any class. The methodology pins the artefact shape, ties every conclusion to a rule, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- AI-фіча на user-facing surface: chat, agent, RAG search.
- OWASP LLM Top 10 #1 — prompt injection: corpus має базовий coverage.
- Continuous security: кожна зміна prompt чи model виклика test suite.
- Pentest-like fuzzing: attack vectors зростають quarterly, тест suite має growth-discipline.

## Applies If (ALL must hold)

- AI feature has user-input → LLM API path.
- CI pipeline exists that can run test suites on PR.
- Suite owner is named and has authority to add new attack vectors.
- OWASP LLM Top 10 list is referenced and tracked.

## Skip If (ANY kills it)

- No user-facing AI surface — attack surface is empty.
- Feature uses no LLM API (pure deterministic NLP).
- Existing security-testing methodology already enforces OWASP LLM Top 10.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| OWASP LLM Top 10 list | PDF / Markdown | OWASP site (versioned) |
| CVE / CWE feed for LLM attacks | JSON feed | MITRE / NIST / vendor advisories |
| Suite root directory | Git directory | Eng team |
| CI runner with secret-redaction policy | GitHub Actions / GitLab CI | Infra team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ai/AGENTS.md` | Parent domain context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules with rationale + source + skip rule | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end with decision gates | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-prompt-injection-test-suite` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/test-case.py` | Python test-case scaffold (pytest-style) wired to the output contract |
| `templates/suite-config.yaml` | Suite-level config: per-attack-class or per-pattern coverage thresholds |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-prompt-injection-test-suite.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/ai/AGENTS.md`
- [[llm-hallucination-test-patterns]]
- [[prompt-versioning-and-ab-framework]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
