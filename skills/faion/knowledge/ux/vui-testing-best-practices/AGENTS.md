# VUI Testing Best Practices

## Summary

**One-sentence:** Produces a four-layer VUI test plan — unit (intent accuracy), integration (dialog flow completion), user (≥5 moderated real users), stress (noise + accents + interruptions) — with subgroup accuracy buckets and deterministic LLM-voice seeds for regression.

**One-paragraph:** Voice products demand a four-layer test plan: unit (intent accuracy per utterance), integration (dialog flow completion end-to-end), user (≥5 moderated real users), stress (kitchen noise + accents + interruptions). Subgroup accuracy buckets (by accent / age / gender) reveal 15-30 pp fairness gaps that overall accuracy hides. 'Completion at attempt N' must be tracked (N=2 acceptable; N=4 = failure). For LLM-voice agents, seeds must be locked for deterministic regression. This methodology emits a test-plan config consumed by QA.

**Ефективно для:**

- Pre-launch voice QA plan з 4 layers + subgroup buckets.
- Regression locking для LLM-voice agents (seeds, prompts).
- Completion-at-attempt-N metric tracking.
- Stress testing під noise + accents + interruption conditions.

## Applies If (ALL must hold)

- Voice product is going to launch or major release.
- Audience has accent / age / gender diversity.
- QA can recruit ≥5 moderated users.

## Skip If (ANY kills it)

- Internal prototype with single tester.
- Pure dictation tool without intent classification.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Intent + dialog spec | JSON | VUI designer |
| User panel access | vendor or panel | research ops |
| Test corpus | labeled audio | QA |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[voice-ui]] | intent + slot vocabulary upstream |
| [[vui-conversation-design]] | dialog state machine to flow-test |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: four-layer-mandatory, subgroup-buckets, completion-at-attempt-n, user-test-min-5, stress-conditions-min-3, seeds-locked-llm | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the produced artefact + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 900 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals -> rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `declare-layers` | haiku | Mechanical layer declaration. |
| `build-corpus` | sonnet | Subgroup balance. |
| `user-test-plan` | sonnet | Recruiting + script. |

## Templates

| File | Purpose |
|------|---------|
| `templates/test-plan.json` | Skeleton test plan |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-vui-testing-best-practices.py` | Validate the artefact against the schema | Pre-commit; CI on each artefact change |

## Related

- [[voice-ui]]
- [[vui-conversation-design]]
- [[vui-accessibility-inclusivity]]

## Decision tree

See `content/06-decision-tree.xml`. Branches by product stage and audience; enforces 4-layer + ≥5-user + locked seeds. Each leaf cites a rule from `01-core-rules.xml`.
