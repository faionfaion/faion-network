# purpose: 1-page SOTA onboarding decision record
# consumes: bench + cost-quality readout
# produces: markdown record matching 02-output-contract schema
# depends-on: content/01-core-rules.xml r3, r4, r5
# token-budget-impact: zero at runtime; doc only

# SOTA Onboarding Decision — <model>

Owner: <name>
Date: YYYY-MM-DD
Revisit: YYYY-MM-DD

## Results
                       incumbent       candidate
Eval-set (n=<N>):        <x>%             <y>%       (Δpp)
p50 latency:             <a>s             <b>s
p95 latency:             <a>s             <b>s
$/1k input tokens:       $<x>             $<y>
$/1k output tokens:      $<x>             $<y>

## Decision: GO | NO-GO | DEFER
- Flag: model.<id>
- Rollout: <pct>%
- Rationale: <one paragraph>
- Rollback: flip flag to 0%; adapter stays merged.
