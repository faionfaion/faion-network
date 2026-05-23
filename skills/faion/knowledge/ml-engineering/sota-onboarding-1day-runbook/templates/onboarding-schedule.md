# purpose: 8-hour SOTA onboarding wall-clock schedule
# consumes: release announcement + adapter pattern + eval set
# produces: filled schedule that drives the day
# depends-on: content/01-core-rules.xml r1-r5
# token-budget-impact: zero at runtime; schedule only

# SOTA Onboarding — YYYY-MM-DD (<lab> <model>)

## Schedule (wall-clock)
08:30  announce-scan, model card, breaking changes
09:30  gateway adapter wired (commit <hash>)
10:30  smoke eval (50 cases)            → pass on X/50
11:30  full bench vs incumbent           → see results
13:30  cost-quality readout              → see results
14:30  GO/NO-GO meeting (15 min)         → decision
15:30  decision record committed
16:30  feature flag enabled at <pct>%
