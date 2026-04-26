# Market Sizing: [Market / Product Name]

**Date:** YYYY-MM-DD
**Geography:** [e.g., US, EU, Global]
**Segment:** [e.g., SMB SaaS, enterprise healthcare IT]

---

## Top-Down Sizing

### TAM

| Number | Source | Year | Geography | Notes |
|--------|--------|------|-----------|-------|
| $X B | [Analyst / URL] | 20XX | [Region] | [Definition used] |

TAM definition: [exact scope — who counts, what counts as revenue]

### SAM

Constraints applied (remove rows that do not apply):

| Constraint | Rationale | Reduction factor |
|------------|-----------|-----------------|
| Geography (exclude X) | [reason] | ×0.XX |
| Language (English-only) | [reason] | ×0.XX |
| Company size (>50 employees) | [reason] | ×0.XX |
| Tech stack (API-first only) | [reason] | ×0.XX |
| Industry vertical | [reason] | ×0.XX |

**Top-down SAM:** $X M (= TAM × [product of reduction factors])

---

## Bottom-Up Sizing

### Step 1 — Countable customer universe

| Source | Count | Notes |
|--------|-------|-------|
| LinkedIn Sales Navigator: [query] | X,XXX | [date of count] |
| [Industry database]: [query] | X,XXX | [date] |
| **Overlap-adjusted total** | ~X,XXX | [dedup method] |

### Step 2 — Reachable fraction

| Channel | Reachable accounts | CAC ceiling | Notes |
|---------|--------------------|-------------|-------|
| Outbound (SDR) | X% of universe → X accounts | $X CAC | [basis] |
| Content / SEO | X% | $X | [basis] |
| **Total reachable** | ~X,XXX | — | [combined, no double-count] |

### Step 3 — Conversion and revenue

| Stage | Rate | Basis |
|-------|------|-------|
| Reachable → Trial | X% | [comparable product / cohort] |
| Trial → Paid | X% | [basis] |
| ARPU | $X / mo | [pricing tier assumption] |

**Year 1 SOM:** [reachable] × [trial rate] × [paid rate] × $ARPU × 12 = **$X M**
**Year 3 SOM:** [model assumption for growth] = **$X M**

**Bottom-up SAM check:** [reachable universe] × ARPU × 12 = **$X M**

---

## Divergence Check

| Metric | Top-Down | Bottom-Up | Ratio | Status |
|--------|----------|-----------|-------|--------|
| SAM | $X M | $X M | X.Xx | [OK / FLAG >2x] |

**If flagged:** [document the specific constraint or definitional mismatch causing the gap]

---

## Named Account Sanity Check

Can you name 100 specific target accounts? List at least 10 here as a spot-check:

1.
2.
3.
...

[If you cannot name 10, the SAM definition is too broad — narrow the constraints above.]

---

## Summary

| Metric | Value | Confidence |
|--------|-------|------------|
| TAM | $X B | [High/Med/Low] — [source quality] |
| SAM | $X M | [High/Med/Low] |
| SOM Year 1 | $X M | [High/Med/Low] |
| SOM Year 3 | $X M | [High/Med/Low] |
| CAGR | X% | [source] — rounded to nearest 1% |
