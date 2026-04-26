#!/usr/bin/env bash
# merge-audit.sh — join Screaming Frog crawl CSV with Google Analytics pageview data
# Requires: csvkit (pip install csvkit)
# Usage: bash merge-audit.sh crawl.csv ga-pageviews.csv output.csv
CRAWL="${1:?Usage: $0 <crawl.csv> <ga.csv> <output.csv>}"
GA="${2:?}"
OUT="${3:-audit-merged.csv}"

# Normalize URL column names (Screaming Frog uses "Address", GA uses "Page path")
csvcut -c "Address,Title 1,Word Count,Status Code,Last Modified" "$CRAWL" \
  | python3 -c "
import sys, csv
r = csv.reader(sys.stdin)
h = next(r)
h[0] = 'url'
w = csv.writer(sys.stdout)
w.writerow(h)
for row in r:
    w.writerow(row)
" > /tmp/crawl-norm.csv

csvcut -c "Page path,Sessions" "$GA" \
  | python3 -c "
import sys, csv
r = csv.reader(sys.stdin)
h = next(r)
h[0] = 'url'
w = csv.writer(sys.stdout)
w.writerow(h)
for row in r:
    w.writerow(row)
" > /tmp/ga-norm.csv

csvjoin -c url /tmp/crawl-norm.csv /tmp/ga-norm.csv > "$OUT"
echo "Merged audit written to $OUT"
