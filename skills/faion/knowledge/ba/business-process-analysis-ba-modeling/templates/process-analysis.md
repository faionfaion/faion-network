<!-- purpose: process-analysis report skeleton (current + analysis + future + signoff) -->
<!-- consumes: process evidence (SOPs, tickets, transcripts) + named stakeholders -->
<!-- produces: report artefact conforming to 02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml, content/02-output-contract.xml -->
<!-- token-budget-impact: ~400 tokens loaded as template context -->

# Process Analysis: <process_name>

**Date:** <date>
**Analyst:** <name>
**Stage:** 3 / 5 — Analysis

## Value Classification

VA/BN/NVA rubric:
- VA = customer would pay for this step
- BN = required by law/policy/system but no customer value
- NVA = waiting, rework, transport, duplicate data entry

| Step | Activity | Value Type | Time (cite or "Data not available") | Notes |
|------|----------|------------|--------------------------------------|-------|
| 1 | <activity> | VA/BN/NVA | <value_source> | |

**Summary:**
- Value-Adding: <x>
- Business Necessary: <x>
- Non-Value-Adding: <x>

## Pain Points

| Issue | Impact | Frequency (cite or "Data not available") | Root Cause |
|-------|--------|------------------------------------------|------------|
| <issue> | [Impact] | <frequency> | [Cause] |

## Bottlenecks

| Location | Wait Time (cite or "Data not available") | Cause | Impact |
|----------|------------------------------------------|-------|--------|
| [Step] | <time> | [Cause] | [Impact] |

## Top-3 Candidates for Elimination

Ranked by NVA-minutes × frequency:

| Rank | Step | NVA minutes | Frequency/day | Composite score | Change type |
|------|------|-------------|---------------|-----------------|-------------|
| 1 | [Step] | [Min] | [Freq] | [Min×Freq] | eliminate/automate/simplify |
| 2 | [Step] | [Min] | [Freq] | [Min×Freq] | |
| 3 | [Step] | [Min] | [Freq] | [Min×Freq] | |

## Improvement Opportunities (max 5, ranked by effort/benefit)

| Opportunity | Change Type | NVA×freq saved | Effort (H/M/L) | Benefit (H/M/L) |
|-------------|-------------|----------------|----------------|-----------------|
| <opportunity> | eliminate/automate/simplify/integrate/parallelize | <score> | H/M/L | H/M/L |
