#!/usr/bin/env bash
# vpat-cells.sh <axe.json>
# Converts axe JSON violations to VPAT 2.5 conformance table rows (markdown).
# Output: | WCAG SC | Conformance | Notes |
# Usage: vpat-cells.sh reports/site/axe.json >> vpat.md
node -e '
const v = JSON.parse(require("fs").readFileSync(process.argv[1])).violations || [];
const map = {};
v.forEach(r => (r.tags || []).filter(t => t.startsWith("wcag")).forEach(t => {
  // Convert "wcag211" → "2.1.1"
  const k = t.replace("wcag", "").replace(/^(\d)(\d)(\d+)$/, "$1.$2.$3")
             .replace(/^(\d)(\d+)$/, "$1.$2");
  map[k] = map[k] || [];
  map[k].push({ rule: r.id, impact: r.impact, count: r.nodes.length });
}));
console.log("| WCAG SC | Conformance | Issue Notes |");
console.log("|---------|-------------|-------------|");
Object.keys(map).sort().forEach(k => {
  const notes = map[k].map(x => x.rule + " (" + x.impact + ", " + x.count + " instances)").join("; ");
  console.log("| " + k + " | Does Not Support | " + notes + " |");
});
' "$1"
