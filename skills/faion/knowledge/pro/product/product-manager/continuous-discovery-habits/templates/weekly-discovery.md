# Discovery Week of YYYY-MM-DD

## Outcome
<metric-name>: <current-value> → <target-value> (<change> vs baseline)

## Touchpoints
- Interviews this week: <N> (<participant-hash>, <segment>, <tenure>)
- Diversity vs last 4: <segment-check> | <recency-check> | <tenure-check>
- Feedback queue processed: <N> items (tickets: N, NPS: N, sales-calls: N)

## OST Changes (diff)

<!-- Agent emits diffs; PM reviews and applies with scripts/ost-apply.py -->
+ opportunity opp_<slug> (<N> quotes, segment: <segment>)
~ opportunity opp_<slug> <change description>
- opportunity opp_<slug> parked (no evidence in 60d)

## Assumption Tests Run / Planned
- sol_<slug>: <test-type> test <status> — <owner> due <date>
- sol_<slug>: <test-type> spike — <owner> estimate due <date>

## Roadmap Input

<!-- This is a delta artifact — only changes vs. current Now/Next/Later -->
- Now: ship sol_<slug> (validated, <effort>)
- Next: pilot sol_<slug> (assumption test pending)
- Later: re-evaluate sol_<slug> pending <condition>

## Open Questions for Trio
1. <question 1>
2. <question 2>
