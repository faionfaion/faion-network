<!-- purpose: step-by-step fork-pin procedure once FORK-PIN action selected -->
<!-- consumes: FixDecision + library name -->
<!-- produces: Renovate config + branch + sunset checklist -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~250 tokens when loaded as reference -->

# Fork-pin playbook for `<library>`

## Setup

1. Fork the upstream repo into the org. Branch name MUST be `vX-faion-fork` (matches major version).
2. Pin the dependency: in `package.json` / `pyproject.toml` / `Cargo.toml`, point at the fork ref (commit SHA or tag).
3. Open the corresponding upstream PR in parallel (per r3 strategic override when applicable).

## Renovate config

```yaml
extends: ["config:base"]
packageRules:
  - matchPackageNames: ["<library>"]
    sourceUrl: "https://github.com/faionfaion/<library>"
    branchPrefix: "renovate-fork-"
    rebaseWhen: behind-base-branch
schedule: "every weekday"
```

## Re-rebase cadence

- Monthly: rebase the fork branch against upstream `main`. Track in calendar.
- Quarterly: rerun fork-vs-fix decision — is the fork still needed?

## Sunset criterion

Choose one and write it into the FixDecision:

- "When upstream PR https://github.com/<owner>/<repo>/pull/NNN merges, drop the fork."
- "By 2027-Q1 — escalate to replacement if upstream hasn't merged by then."

## Rollback plan

If the fork breaks production:

1. Revert the version pin to the last public release.
2. Apply the bridging workaround captured in the original FixDecision.
3. Open an incident; escalate to UPSTREAM-PR or REPLACE in the next quarter.
