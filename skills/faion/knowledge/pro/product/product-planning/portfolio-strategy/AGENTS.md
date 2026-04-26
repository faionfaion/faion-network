# Portfolio Strategy (70/20/10)

## Summary

The Three Horizons portfolio model allocates engineering capacity across H1 (Core, 70%), H2
(Adjacent, 20%), and H3 (Transformational, 10%), with ratios adjustable to macro conditions
(Growth 60/25/15, Stable 70/20/10, Recession 80/15/5). Every initiative is tagged H1/H2/H3
with a revenue-evidence string. Allocation tracks engineering cost (loaded $ or person-weeks),
not ticket count. H3 bets ship with a pre-committed kill threshold. Re-classify quarterly.

## Why

Economic uncertainty requires balanced product bets. A portfolio without explicit horizon
allocation drifts toward H1 under pressure (all maintenance) or H3 theater (all moonshots,
zero revenue defense). The 70/20/10 model provides a numeric handle for allocation debates with
finance or board. The macro-condition lever (Growth/Stable/Recession) makes ratio changes
automatic and uncontroversial when conditions shift.

## When To Use

- Annual/quarterly roadmap planning where multiple bets compete for the same engineering capacity
- Multi-product company or solopreneur with 3+ shipped products needing a defensible split
- Macro shock (recession signal, funding cut, churn spike) forcing re-allocation from H3/H2 to H1
- Investor/leadership update showing the portfolio is neither all moonshots nor all maintenance
- Backlog sizing: tag every initiative H1/H2/H3 and verify sum matches target ratios

## When NOT To Use

- Single-product seed-stage startup with one bet — no portfolio yet; allocate 100% to PMF
- Pure services / agency revenue where there is no product backlog to allocate against
- Engineering-only resource planning (sprints, on-call, infra) — use capacity planning instead
- Sub-feature prioritization inside one product — RICE / WSJF / Kano are sharper at that grain
- Crisis quarters where survival demands 100% on one fire

## Content

| File | What's inside |
|------|---------------|
| `content/01-horizons.xml` | Three Horizons model, allocation table, macro adjustments, limitations |
| `content/02-agent-usage.xml` | Two-pass agentic workflow, classifier prompt, rebalancer prompt, gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/portfolio-allocate.sh` | Bash+Python: compute current vs target horizon allocation from a CSV backlog |
