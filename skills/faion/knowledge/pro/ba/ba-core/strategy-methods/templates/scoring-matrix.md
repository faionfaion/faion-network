# Solution Options Analysis: <Decision>

## Options

| # | Option | Description | Is baseline (do-nothing)? |
|---|--------|-------------|--------------------------|
| A | [name] | [description] | No |
| B | [name] | [description] | No |
| C | Status quo | Do nothing | Yes |

## Evaluation Criteria and Weights

Weights must be locked before scoring. Sum must equal 100%.

| Criterion | Weight | Anchored rubric (1=worst, 5=best) |
|-----------|--------|-----------------------------------|
| Strategic fit | 25% | 5=exceeds target by >=20%, 1=direct conflict |
| Technical feasibility | 20% | 5=proven in org, 1=requires new capability |
| Cost | 20% | 5=<=50% of budget, 1=exceeds budget |
| Time to value | 20% | 5=value in <1 sprint, 1=>6 months |
| Risk | 15% | 5=fully mitigated, 1=no mitigation available |

Weight sum check: 25+20+20+20+15 = 100% ✓

## Scoring Matrix

Each cell requires >= 1 evidence_url. Cells without evidence: score=3, confidence=low.

| Criterion | Weight | Opt A score | Opt A weighted | Opt B score | Opt B weighted | Opt C score | Opt C weighted |
|-----------|--------|-------------|----------------|-------------|----------------|-------------|----------------|
| Strategic fit | 25% | | | | | | |
| Technical feasibility | 20% | | | | | | |
| Cost | 20% | | | | | | |
| Time to value | 20% | | | | | | |
| Risk | 15% | | | | | | |
| **Total** | | | | | | | |

## Sensitivity Analysis

Run sensitivity.py before publishing. If winner flips under <=10% perturbation: mark brittleness=high, require human review.

- Brittleness: [low | medium | high]
- Flips under +/-10%: [yes/no, which criteria]

## Recommendation

**Option:** [winner]
**Conditions:** [list conditions]
**Do-nothing consequences:** [explicit cost of inaction]
**Rationale:** [max 120 words]
