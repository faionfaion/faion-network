#!/usr/bin/env bash
# tier-som.sh — decompose SAM/SOM per pricing tier with LTV/CAC sanity check
# Usage: ./tier-som.sh sam_usd tiers.csv share_y3
#
# tiers.csv columns (no header row):
#   name, mix_pct, arpu_usd, gross_margin_pct, cac_usd, churn_monthly_pct
#
# Example tiers.csv:
#   Starter,65,19,75,40,5
#   Pro,28,49,80,120,2
#   Enterprise,7,299,82,800,0.5
set -euo pipefail
sam=$1
csv=$2
share=$3

printf '%-12s %12s %10s %8s %10s %10s %10s\n' \
  tier tier_sam arpu mix_pct tier_som ltv ltv_cac

tail -n +1 "$csv" | while IFS=, read -r name mix arpu gm cac churn; do
  ts=$(awk -v s="$sam" -v m="$mix" 'BEGIN{printf "%.0f", s*m/100}')
  tsom=$(awk -v ts="$ts" -v sh="$share" 'BEGIN{printf "%.0f", ts*sh}')
  ltv=$(awk -v a="$arpu" -v g="$gm" -v c="$churn" \
    'BEGIN{ if(c<=0){print 0; exit} printf "%.0f", (a*g/100)/(c/100) }')
  lc=$(awk -v l="$ltv" -v c="$cac" \
    'BEGIN{ if(c<=0){print "inf"; exit} printf "%.2f", l/c }')
  flag=""
  # Flag tiers where LTV/CAC < 3 (unhealthy)
  is_bad=$(awk -v l="$ltv" -v c="$cac" 'BEGIN{print (c>0 && l/c < 3) ? "1" : "0"}')
  [ "$is_bad" = "1" ] && flag=" [LTV/CAC<3 WARNING]"
  printf '%-12s %12s %10s %8s %10s %10s %10s%s\n' \
    "$name" "$ts" "$arpu" "$mix" "$tsom" "$ltv" "$lc" "$flag"
done
