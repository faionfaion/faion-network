#!/usr/bin/env bash
# purpose: axe + pa11y + lighthouse CI wrapper.
# consumes: see content/02-output-contract.xml inputs for a11y-testing
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml + content/04-procedure.xml
# token-budget-impact: ~200-600 tokens when loaded as context

# Automated layer only (procedure step 2). Layers 2-4 stay "Not Tested" in summary.md
# until the keyboard pass, two screen readers and the user panel are attached (rule four-layer-required).
# Usage: A11Y_OWNER=@<handle> ./a11y-scan.sh <url> [<url> ...]
# Deps: node + npx (fetches @axe-core/cli, pa11y, lighthouse on first run), jq, Chrome/Chromium.
# Exit 1 when any blocker (axe impact=critical) is found. Per-tool exit codes are absorbed so
# every tool runs and every finding keeps its evidence file.
set -euo pipefail

[[ $# -ge 1 ]] || { echo "usage: $0 <url> [<url> ...]" >&2; exit 2; }
command -v jq >/dev/null || { echo "jq is required" >&2; exit 2; }
OWNER="${A11Y_OWNER:-}"
[[ "$OWNER" =~ ^@[A-Za-z0-9_-]+$ ]] || { echo "A11Y_OWNER must be one @handle (not a team)" >&2; exit 2; }

RUN_DATE="$(date +%Y-%m-%d)"
OUT="${OUT_DIR:-a11y-scan/$RUN_DATE}"
AXE_TAGS="wcag2a,wcag2aa,wcag21a,wcag21aa,wcag22aa"   # WCAG 2.2 AA target
CHROME_FLAGS="--headless=new --no-sandbox"
mkdir -p "$OUT"
echo '[]' > "$OUT/findings.json"

# axe impact -> a11y-testing severity enum (rule severity-enum); pa11y type -> same enum.
axe_sev='{"critical":"blocker","serious":"major","moderate":"minor","minor":"informational"}'
pa11y_sev='{"error":"major","warning":"minor","notice":"informational"}'

scan_one() {
  local url="$1" slug
  slug="$(printf '%s' "$url" | sed 's|https\?://||; s|[^A-Za-z0-9]|-|g' | cut -c1-60)"
  local axe="$OUT/$slug.axe.json" pa="$OUT/$slug.pa11y.json" lh="$OUT/$slug.lighthouse.json"
  echo "== $url"

  npx --yes @axe-core/cli "$url" --tags "$AXE_TAGS" --save "$axe" --chrome-options="$CHROME_FLAGS" >/dev/null 2>&1 || true
  npx --yes pa11y "$url" --standard WCAG2AA --reporter json > "$pa" 2>/dev/null || true   # exits 2 on issues
  npx --yes lighthouse "$url" --only-categories=accessibility --output=json --output-path="$lh" \
      --chrome-flags="$CHROME_FLAGS" --quiet >/dev/null 2>&1 || true

  # Every finding carries evidence_url pointing at the raw tool output (rule evidence-attached).
  jq --arg url "$url" --arg ev "file://$(cd "$OUT" && pwd)/$slug.axe.json" --argjson sev "$axe_sev" '
    [ (.[0].violations // [])[] as $v
      | ($v.tags | map(capture("^wcag(?<a>[0-9])(?<b>[0-9])(?<c>[0-9]+)$")? // empty)
         | if length == 0 then [{a:"n",b:"a",c:""}] else . end)[]
      | {layer:"automated", tool:"axe", page:$url, rule:$v.id,
         sc:(if .a=="n" then "best-practice" else "\(.a).\(.b).\(.c)" end),
         severity:($sev[$v.impact] // "informational"),
         nodes:($v.nodes|length), evidence_url:"\($ev)#\($v.id)"} ]' "$axe" > "$OUT/$slug.axe.findings.json" 2>/dev/null || echo '[]' > "$OUT/$slug.axe.findings.json"
  jq --arg url "$url" --arg ev "file://$(cd "$OUT" && pwd)/$slug.pa11y.json" --argjson sev "$pa11y_sev" '
    [ .[]? | {layer:"automated", tool:"pa11y", page:$url, rule:.code,
              sc:((.code|capture("Guideline(?<a>[0-9])_(?<b>[0-9])\\.(?<a2>[0-9])_(?<b2>[0-9])_(?<c>[0-9]+)")?
                   | "\(.a).\(.b).\(.c)") // "unmapped"),
              severity:($sev[.type] // "informational"), selector:.selector, evidence_url:$ev} ]' "$pa" \
      > "$OUT/$slug.pa11y.findings.json" 2>/dev/null || echo '[]' > "$OUT/$slug.pa11y.findings.json"

  jq -s 'add' "$OUT/findings.json" "$OUT/$slug.axe.findings.json" "$OUT/$slug.pa11y.findings.json" > "$OUT/.tmp.json"
  mv "$OUT/.tmp.json" "$OUT/findings.json"

  # axe "incomplete" is untested, never passed; lighthouse score is a hint, not a conformance claim.
  printf '%s | axe incomplete: %s | lighthouse a11y score: %s\n' "$url" \
    "$(jq '.[0].incomplete // [] | length' "$axe" 2>/dev/null || echo '?')" \
    "$(jq '.categories.accessibility.score // "n/a"' "$lh" 2>/dev/null || echo 'n/a')" >> "$OUT/tool-notes.txt"
}

for u in "$@"; do scan_one "$u"; done

# Audit-record skeleton in the 02-output-contract shape; verdict is provisional until all four layers exist.
jq -n --arg id "audit-$RUN_DATE-auto" --arg d "$RUN_DATE" --arg owner "$OWNER" --args '
  { artefact_id:$id, version:"1.1.0", last_reviewed:$d, owner:$owner,
    scope:{flows:$ARGS.positional, wcag_version:"2.2", level:"AA"},
    findings:(input),
    summary:"Automated layer only (axe + pa11y + lighthouse). Manual-keyboard, AT (2 SRs) and user-panel layers: Not Tested.",
    verdict:"partial" }' "$@" < "$OUT/findings.json" > "$OUT/audit-record.json"

BLOCKERS="$(jq '[.[] | select(.severity=="blocker")] | length' "$OUT/findings.json")"
{
  echo "# a11y scan $RUN_DATE (automated layer)"
  echo
  echo "| Severity | Count |"; echo "|---|---|"
  jq -r 'group_by(.severity) | .[] | "| \(.[0].severity) | \(length) |"' "$OUT/findings.json"
  echo; echo "## By WCAG SC"; echo
  jq -r 'group_by(.sc) | sort_by(-length) | .[] | "- \(.[0].sc): \(length) (\([.[].tool]|unique|join(", ")))"' "$OUT/findings.json"
  echo; echo "## Tool notes"; echo; sed 's/^/- /' "$OUT/tool-notes.txt"
  echo; echo "## Layers"; echo
  echo "- automated: done, evidence in $OUT"
  echo "- manual-keyboard: Not Tested"; echo "- AT (NVDA/JAWS + VoiceOver/TalkBack): Not Tested"
  echo "- user-panel (>=3 participants or waiver): Not Tested"
  echo; echo "Diff against the previous release: jq -S '[.[]|{page,rule,sc}]' on both findings.json files."
} > "$OUT/summary.md"

echo "findings: $(jq length "$OUT/findings.json"), blockers: $BLOCKERS, report: $OUT/summary.md"
[[ "$BLOCKERS" -eq 0 ]]
