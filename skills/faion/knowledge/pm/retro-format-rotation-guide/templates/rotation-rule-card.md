<!--
purpose: One-pager — rotation rule + stale-format detector
consumes: facilitator's per-team history
produces: artefact conforming to content/02-output-contract.xml
depends-on: content/01-core-rules.xml
token-budget-impact: ~150-300 tokens when loaded as context
-->
# Rotation Rule + Stale-Format Detector

## Rotation rule

```
next_format = any format NOT in the last 3 retros for this team
```

Closed list of supported formats:
- start-stop-continue
- sailboat
- 4ls
- timeline
- anonymous-async
- mad-sad-glad
- lean-coffee

## Stale-format detector

A format is stale for a team when:

- Used twice in the last 3 retros, OR
- Action-item count dropped by >50% cycle-over-cycle while the same format was used, OR
- Outcome-review notes show contributor engagement dropping (≥2 silent participants).

When stale → rotate to a different format that fits the team state.

## Tie-breaker (team state)

```
distribution == async      → prefer anonymous-async
fatigue == fatigued        → prefer a format last used >= 12 months ago
distribution == in-person  → prefer sailboat or lean-coffee
mid-cycle reflective need  → prefer 4ls
visual + blockers          → prefer sailboat
```
