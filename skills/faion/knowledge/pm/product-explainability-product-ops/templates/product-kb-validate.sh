#!/usr/bin/env bash
# purpose: Validate KB page has required schema markup and boundary section
# consumes: CLI arg: KB page markdown path
# produces: exit 0 if valid; exit 1 with violations
# depends-on: grep, awk
# token-budget-impact: low
set -euo pipefail
F="${1:?path to KB page markdown}"
v=0
grep -q 'application/ld+json' "$F" || { echo "VIOLATION: no schema markup"; v=1; }
grep -qE '"@type":\s*"(Product|SoftwareApplication)"' "$F" || { echo "VIOLATION: @type not Product/SoftwareApplication"; v=1; }
grep -qi 'does NOT do\|out of scope\|limitations' "$F" || { echo "VIOLATION: no boundary section"; v=1; }
grep -qE '^owner:' "$F" || { echo "VIOLATION: no owner frontmatter"; v=1; }
grep -qE '^review_cadence:' "$F" || { echo "VIOLATION: no review_cadence frontmatter"; v=1; }
exit "$v"
