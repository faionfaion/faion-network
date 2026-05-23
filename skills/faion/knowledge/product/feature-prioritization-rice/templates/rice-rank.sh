#!/usr/bin/env bash
# rice-rank.sh — read a CSV of features and output sorted RICE scores
#
# Input CSV columns (header required): name,reach,impact,confidence,effort
#   confidence: decimal (0.8 for 80%) or percentage (80 — auto-converted)
#   effort: person-months
#
# Usage: bash rice-rank.sh features.csv
# Output: CSV with appended rice column, sorted highest to lowest

set -euo pipefail
input="${1:?usage: rice-rank.sh features.csv}"

awk -F',' '
NR==1 {
    print $0 ",rice"
    next
}
{
    reach  = $2 + 0
    impact = $3 + 0
    conf   = $4 + 0
    effort = $5 + 0

    # auto-convert percentage confidence to decimal
    if (conf > 1) conf = conf / 100

    # guard against zero effort
    if (effort == 0) effort = 0.01

    rice = (reach * impact * conf) / effort
    printf "%s,%.2f\n", $0, rice
}
' "$input" | (
    read -r header
    echo "$header"
    sort -t',' -k6 -gr
)
