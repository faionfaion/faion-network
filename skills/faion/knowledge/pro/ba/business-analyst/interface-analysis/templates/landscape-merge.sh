#!/usr/bin/env bash
# landscape-merge.sh — seed an integration register from CMDB + gateway dumps.
#
# Inputs:
#   cmdb-apps.json  — array of {id, name, owner}
#   gw-apis.json    — array of {name, upstream_id, downstream_id, traffic_per_day}
#
# Output: register.csv ready for BA enrichment (criticality, sensitivity, SLA)
#
# Usage: bash landscape-merge.sh cmdb-apps.json gw-apis.json [register.csv]
set -euo pipefail

CMDB="${1:?cmdb json required}"
GW="${2:?gateway json required}"
OUT="${3:-register.csv}"

# Build id -> {name, owner} lookup from CMDB
jq -r '.[] | [.id, .name, .owner] | @tsv' "$CMDB" > /tmp/cmdb.tsv

# Emit register rows: IF-id, src, tgt, channel, traffic
awk '
BEGIN {
    OFS = ","
    n = 0
    print "IF-ID,Source,Target,Channel,TrafficPerDay,SourceOwner,TargetOwner,Criticality,Sensitivity,SLA,Notes"
}
NR == FNR {
    owner[$1] = $3
    sysname[$1] = $2
    next
}
{
    n++
    src = sysname[$2]; tgt = sysname[$3]
    if (src == "") src = "CMDB-UNKNOWN-" $2
    if (tgt == "") tgt = "CMDB-UNKNOWN-" $3
    printf "IF-%03d,%s,%s,REST,%s,%s,%s,tbd,unknown,tbd,from-gateway\n",
        n, src, tgt, $4, owner[$2], owner[$3]
}' \
    /tmp/cmdb.tsv \
    <(jq -r '.[] | [.name, .upstream_id, .downstream_id, .traffic_per_day] | @tsv' "$GW") \
    > "$OUT"

echo "Seeded $(wc -l < "$OUT") rows -> $OUT"
echo "BA must fill: Criticality (1-4), Sensitivity, SLA for each row."
echo "Tier-1 criticality requires explicit human sign-off before publishing."
