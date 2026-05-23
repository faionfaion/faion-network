<!-- purpose: Channel-evaluation report skeleton: shortlist + tests + tripwires -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~200-1500 tokens when loaded as context -->
# Channel Research: [Product]

## Customer Discovery Research

**Interview insights (N=X):**
- "[How they found a competitor]" — Participant ID INT-XX
- "[Where they discover new tools]" — Participant ID INT-XX

**Top discovery sources:**

| Channel | % of customers | Source type |
|---------|---------------|-------------|
| [Channel 1] | X% | [Interview / Analytics / Attribution survey] |
| [Channel 2] | X% | [Interview / Analytics / Attribution survey] |

## Channel Evaluation

| Channel | Audience | Competitors | Cost | Time | Scale | Capability | Total |
|---------|----------|-------------|------|------|-------|------------|-------|
| [Ch 1]  | 5 | 4 | 3 | 4 | 5 | 4 | 4.2 |
| [Ch 2]  | 4 | 3 | 4 | 3 | 4 | 3 | 3.6 |

_Scored via channel-fit-scorer.py with channels.yaml. Source for audience/competitors scores: [URL, YYYY-MM-DD]._

## Channel Economics (Estimated)

| Channel | CAC Estimate | LTV:CAC | Phase gate | Source |
|---------|-------------|---------|------------|--------|
| [Ch 1]  | $X          | X:1     | Phase 2 if &gt;3:1 | [URL, date] |

_LTV = $X (from business-model.md v1). All numbers [UNVERIFIED] until Phase-1 test data arrives._

## Competitor Channel Analysis

| Competitor | Primary Channel | Secondary | Evidence date |
|------------|-----------------|-----------|--------------|
| [Comp 1]   | [Channel]       | [Channel] | YYYY-MM-DD   |

_Sources: SimilarWeb, Meta Ad Library, LinkedIn Ad Library. Competitor inference only — flag [UNVERIFIED]._

## Recommended Channel Strategy

**Phase 1** (milestone: first 100 sign-ups):
- Primary: [Channel] — budget $X, kill criterion: CAC &gt; $X after $500 spend
- Backup: [Channel 2] — if primary kill criterion fires

**Phase 2** (milestone: $10K MRR):
- Add: [Channel 2] if Phase 1 economics confirmed
- Scale: [Channel 1] with 80% of budget

## Testing Plan

| Channel | Budget | Milestone gate | Success criteria | Kill criterion |
|---------|--------|---------------|-----------------|----------------|
| [Ch 1]  | $X     | 100 sign-ups  | CAC &lt; $X      | CAC &gt; $X after $500 |
| [Ch 2]  | $X     | 100 sign-ups  | X conversions   | 0 conversions after $300 |
