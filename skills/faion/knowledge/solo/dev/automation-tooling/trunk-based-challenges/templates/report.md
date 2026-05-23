<!-- purpose: Diagnostic report skeleton -->
<!-- consumes: input artefacts described in AGENTS.md ## Prerequisites -->
<!-- produces: artefact conforming to content/02-output-contract.xml for trunk-based-challenges -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~200-1200 tokens when loaded as context -->

# Trunk-based diagnostic — <date>

## Metrics (last 4 weeks)
| Metric | Value |
|--------|-------|
| trunk break freq | <lt_1 / 1_3 / gt_3> per week |
| PR size p95 | <NN> lines |
| CI p95 wall time | <NN> min |
| Review p95 | <NN> hours |
| Branch protection complete | yes / no |

## Ordered checklist walk
1. Branch protection includes all CI jobs: <PASS/FAIL>
2. CI < 10 min: <PASS/FAIL>
3. Flags tracked + non-stale: <PASS/FAIL>
4. PR < 200 lines (p95): <PASS/FAIL>
5. Review SLA < 4h (p95): <PASS/FAIL>

## First failing check
<name>

## Recommended fix
<one concrete action>

## Re-evaluation
<date 2-4 weeks out>
