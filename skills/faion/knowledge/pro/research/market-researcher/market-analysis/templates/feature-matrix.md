# Feature Matrix: [Market / Product Name]

**Date:** YYYY-MM-DD  
**Snapshot date:** YYYY-MM-DD (must match competitor snapshots)  
**Valid until:** YYYY-MM-DD (90 days from snapshot date — flag and re-run after)  
**Competitors evaluated:** [list names]

Legend: Y = present | N = absent | P = partial / on roadmap

---

## Matrix

| Feature | [Comp 1] | [Comp 2] | [Comp 3] | [Comp 4] | [Comp 5] | Classification |
|---------|----------|----------|----------|----------|----------|----------------|
| [Feature A] | Y | Y | Y | Y | Y | Table stakes |
| [Feature B] | Y | Y | N | P | N | Opportunity |
| [Feature C] | N | N | N | N | N | Validate demand |
| [Feature D] | Y | N | N | N | N | Opportunity |

*Process: chunk to ≤5 competitors per invocation to avoid long-context degradation.*

---

## Classification Reference

| Class | Definition | Action |
|-------|------------|--------|
| Table stakes | Y at all top-5 | Required to compete; not a differentiator |
| Opportunity | Y at 1-2, N or P at others | Validate demand before building |
| Validate demand | N at all | Check reviews — gap may be intentional |

---

## Opportunity Features — Demand Validation

For each feature classified as Opportunity or Validate demand, document evidence before claiming whitespace.

### [Feature B]

**Classification:** Opportunity

| Evidence source | Quote / vote count | URL | Date |
|----------------|-------------------|-----|------|
| G2 review | "[buyer quote about needing X]" | [URL] | |
| Capterra review | | | |
| Reddit r/[subreddit] | "[post title]" / X upvotes | [URL] | |
| Competitor forum | X votes on request | [URL] | |
| Competitor roadmap | [listed / not listed] | [URL] | |

**Demand confirmed?** [Yes — ≥5 sources / No — insufficient evidence]  
**Competitor roadmap risk:** [Feature closes before you ship? Y/N — source]  
**Why competitors lack it:** [technical difficulty / low priority / unaware of demand]

---

### [Feature C]

**Classification:** Validate demand

[repeat structure above]

---

## Gap Summary

| Feature | Demand confirmed | Roadmap risk | Recommended action |
|---------|-----------------|--------------|-------------------|
| Feature B | Yes (7 sources) | Low | Build — differentiation |
| Feature C | No (2 sources) | N/A | Hold — insufficient evidence |

---

## Refresh Log

| Date | Changes since last run | Re-run trigger |
|------|------------------------|----------------|
| YYYY-MM-DD | [initial] | — |
| | | [competitor shipped X / 90 days elapsed] |
