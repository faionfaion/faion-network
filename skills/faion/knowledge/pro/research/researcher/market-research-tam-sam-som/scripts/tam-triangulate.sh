#!/usr/bin/env bash
# tam-triangulate.sh — flags divergence across three sizing methods.
# Usage: ./tam-triangulate.sh <topdown> <bottomup> <competitor>
# Values in any consistent unit (e.g. USD millions).
# Exits 0 if spread <= 2x (median is defensible), exits 1 if spread > 2x (flag and investigate).
set -euo pipefail
td=${1:?usage: tam-triangulate.sh TOPDOWN BOTTOMUP COMPETITOR}
bu=${2:?missing bottom-up value}
cp=${3:?missing competitor-based value}
min=$(printf '%s\n' "$td" "$bu" "$cp" | sort -g | head -1)
max=$(printf '%s\n' "$td" "$bu" "$cp" | sort -g | tail -1)
ratio=$(awk -v a="$max" -v b="$min" 'BEGIN{printf "%.2f", a/b}')
median=$(printf '%s\n' "$td" "$bu" "$cp" | sort -g | awk 'NR==2')
echo "top-down=$td  bottom-up=$bu  competitor=$cp"
echo "median=$median  spread=${ratio}x"
awk -v r="$ratio" 'BEGIN{ exit !(r > 2.0) }' \
    && echo "FLAG: spread > 2x — do not average, investigate gap driver" \
    || echo "OK: within 2x, median is defensible"
