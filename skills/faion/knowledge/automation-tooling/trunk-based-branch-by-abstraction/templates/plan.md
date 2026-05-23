<!-- purpose: Branch-by-Abstraction five-step playbook skeleton -->
<!-- consumes: input artefacts described in AGENTS.md ## Prerequisites -->
<!-- produces: artefact conforming to content/02-output-contract.xml for trunk-based-branch-by-abstraction -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~200-1200 tokens when loaded as context -->

# Branch by Abstraction — <plan_id>

Flag: `<area>.<verb>_<thing>`
Cleanup ticket: `OPS-XXX` (filed at step 1)

## Step 1 — Introduce abstraction
- PR #__
- Protocol / interface name: `Xxx`

## Step 2 — Wrap old implementation
- PR #__

## Step 3 — Implement new behind interface
- PR #__
- Flag default: off

## Step 4 — Flag-gated swap with dark launch
- PR #__
- Ramp: 0% → <1% (diurnal cycle) → 10% → 50% → 100%
- Compare metric: <match_rate, error_rate, latency>

## Step 5 — Remove old + collapse abstraction
- PR #__
- Cleanup ticket closed: ✅
