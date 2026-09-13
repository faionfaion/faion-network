# Decisions — numeric and advice disagreements left visible by the fold (2026-09-13)

Each row is a place where a hand-written extra and its generated canonical rule state the same thing with different numbers or opposite advice. The fold kept BOTH sentences verbatim (the preservation rule forbade rewriting either) and wrote a governing note into the canonical rule's rationale. The stricter or the canonical one governs until the owner picks; picking is a one-word edit per row.

| Slug | Canonical rule (governs) | Its statement | The other rule | Its statement |
|---|---|---|---|---|
| `marketing/ads-budget-optimization` | `step-rule-20-percent` | Single-step budget change MUST NOT exceed 20% per week unless backed by incrementality test or sample-size threshold. | `scaling-increment-30-percent` | Never increase a campaign budget by more than 30% in a single step; wait 3-5 days before the next increase. |
| `sdd/design-docs-big-tech` | `r5-llm-assist-limit` | LLM may draft prose but MUST NOT author the alternatives section; humans pick alternatives. | — | (see rationale) |
| `sdd/design-docs-patterns` | `r2-required-sections` | Doc MUST contain all of {context, goals, non-goals, proposed, alternatives, open-questions}; missing sections rejected. | — | (see rationale) |
| `sdd/design-docs-patterns` | `r3-non-goals-explicit` | Non-goals section MUST be non-empty; un-stated non-goals invite scope creep. | — | (see rationale) |
| `sdd/mistake-memory` | `r1-immediate-writeback` | Mistake MUST be written within 30 min of detection; later writeback rejected. | — | (see rationale) |
| `sdd/mistake-memory` | `r5-second-occurrence-ci-rule` | Second occurrence of the same mistake MUST trigger an automatic CI rule. | — | (see rationale) |
| `sdd/writing-implementation-plans` | `r5-wave-grouping` | Tasks are grouped into numbered waves; wave 0 has no deps; later waves depend only on earlier ones. | — | (see rationale) |
| `ux/a11y-testing` | `at-pair-minimum` | AT testing covers at least two screen readers — minimum: one desktop (NVDA or JAWS) + one mobile (VoiceOver iOS or TalkBack). | — | (see rationale) |
| `ux/a11y-testing` | `severity-enum` | Severity per finding is one of: blocker / major / minor / informational. Free-form severity strings are forbidden. | — | (see rationale) |
| `ux/card-sorting-ux-research` | `r4-ambiguous-flagged` | Items with <60% agreement MUST be flagged for re-test, not silently assigned. | — | (see rationale) |
| `ux/card-sorting-ux-research` | `r10-similarity-thresholds` | Use similarity matrix thresholds to determine grouping confidence: above 70% = definite grouping; 40-70% = consider grouping; below 40% = ke | — | (see rationale) |
