#!/usr/bin/env bash
# score-niche.sh <scorecard.json>
# Validates that criteria weights sum to 1.0 and recomputes the weighted total.
# Exits 1 if weights are invalid or any score is null (uncited criterion).
# Input JSON schema:
#   {niche: str, criteria: [{name, score, weight, justification, sources:[url]}], total?, decision?}
set -euo pipefail
F="${1:?usage: score-niche.sh scorecard.json}"

jq -e '
  . as $c
  | (.criteria | map(.weight) | add) as $w
  | (.criteria | map(if .score == null then 0 else .score * .weight end) | add) as $t
  | if ($w - 1.0 | fabs) > 0.001
      then error("weights sum to \($w), not 1.0")
    elif (.criteria | any(.score == null))
      then error("null score in: \([.criteria[] | select(.score==null) | .name] | join(","))")
    elif (.criteria | any((.sources // []) | length == 0))
      then error("missing sources in: \([.criteria[] | select((.sources//[])|length==0) | .name] | join(","))")
    else
      {niche: .niche,
       total: ($t | . * 100 | round / 100),
       decision: (if $t >= 7.5 then "STRONG"
                  elif $t >= 5.5 then "CAUTION"
                  elif $t >= 3.5 then "RISK"
                  else "PASS" end),
       criteria: .criteria}
    end
' "$F"
