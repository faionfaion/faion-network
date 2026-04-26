#!/usr/bin/env bash
# pick-framework.sh — rule-based framework selection from market-context.yml
# Input:  .aidocs/product_docs/market-context.yml
# Output: .aidocs/product_docs/framework-choice.md (versioned via git)
# Usage:  ./pick-framework.sh
# Note:   Rule-based (not LLM) so the choice is auditable; LLM fills exit-criteria stubs.
set -euo pipefail

ctx=".aidocs/product_docs/market-context.yml"
out=".aidocs/product_docs/framework-choice.md"

[ -f "$ctx" ] || { echo "missing $ctx — run market-researcher agent first" >&2; exit 2; }
mkdir -p "$(dirname "$out")"

python3 - "$ctx" "$out" <<'PY'
import sys, yaml, datetime

ctx = yaml.safe_load(open(sys.argv[1]))
out = sys.argv[2]

m = ctx.get("market_condition", "").lower()
b = ctx.get("buyer", "").lower()
diff = ctx.get("differentiator", "").lower()
tech = ctx.get("tech_uncertainty", False)
risk = ctx.get("risk_profile", "").lower()

rules = [
    (lambda: tech,                                          "MFP", "Technical feasibility unknown — prove infra first."),
    (lambda: "enterprise" in b or "b2b" in b,              "MMP", "Enterprise buyer needs a sellable surface before MVP."),
    (lambda: "crowded" in m or "red ocean" in m,           "MLP", "Crowded market — emotional differentiation required to switch users."),
    (lambda: "premium" in diff or "luxury" in diff,        "MDP", "Premium positioning requires exceeding expectations."),
    (lambda: "high uncertainty" in risk,                   "RAT", "Validate riskiest assumption before scoping full build."),
    (lambda: "consumer" in b and "simple" in diff,         "SLC", "Consumer + simplicity — Simple, Lovable, Complete."),
    (lambda: True,                                          "MVP", "Default: blue ocean, low cost, fast learning."),
]

chosen, why = next((f, w) for cond, f, w in rules if cond())

with open(out, "w") as fh:
    fh.write(f"# Framework Choice — {datetime.date.today().isoformat()}\n\n")
    fh.write(f"**Chosen:** {chosen}\n\n**Rationale:** {why}\n\n")
    fh.write("## Inputs\n\n```yaml\n" + yaml.safe_dump(ctx) + "```\n\n")
    fh.write("## Exit Criteria\n\n- TODO: define metric + threshold + measurement window\n- TODO: define kill criterion\n\n")
    fh.write("## History\n\n- " + datetime.date.today().isoformat() + f": initial pick = {chosen}\n")

print(f"Written: {out}  Chosen: {chosen}")
PY

git add "$out"
echo "Staged: $out"
