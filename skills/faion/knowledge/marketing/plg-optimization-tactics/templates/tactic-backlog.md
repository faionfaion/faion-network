<!-- purpose: Markdown report skeleton for the PLG ranked tactic backlog -->
<!-- consumes: validated JSON per content/02-output-contract.xml -->
<!-- produces: human-reviewable backlog report (markdown) -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~600 tokens when filled -->

# PLG Tactic Backlog — <funnel_stage>

**Baseline:** `<METRIC>` = `<VALUE>` as of `<AS_OF>`
**Generated:** `<GENERATED_AT>`

## Ranked tactics

| # | Tactic | Source | Impact | Confidence | Ease | ICE | Bucket |
|---|--------|--------|--------|------------|------|-----|--------|
| 1 | <name> | <SECTION> | <I> | <c> | <e> | <sum> | <bucket> |
| 2 | ... |  |  |  |  |  |  |

## Per-tactic details

### 1. <name>

- **Hypothesis:** <HYPOTHESIS>
- **Source section:** <SECTION>
- **Instrumentation:** <INSTRUMENTATION>
- **CTA variant (if applicable):** <cta_text>

## Sign-off queue

Tactics requiring finance + retention review (free-tier limit changes):

- [ ] <name> — owner: <owner>

## Notes

- Rules enforced: baseline-required, prompt-at-80-percent, no-first-session-prompt, named-customer-copy, banned-cta-text, balanced-free-tier.
