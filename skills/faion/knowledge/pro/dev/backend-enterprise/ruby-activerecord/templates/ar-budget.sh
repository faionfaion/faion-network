#!/usr/bin/env bash
# purpose: CI helper running Prosopite N+1 assertions across request spec suite
# consumes: per-spec query budget number + RSpec / Minitest config
# produces: pass/fail gate per n-plus-one-gate-in-ci rule
# depends-on: content/01-core-rules.xml rule n-plus-one-gate-in-ci
# token-budget-impact: ~250 tokens when loaded as context
# ar-budget.sh — fail CI on N+1 or queries over per-spec budget.
# Usage: ar-budget.sh [BUDGET]
# Requires: bullet and prosopite gems in test group.
set -euo pipefail
BUDGET="${1:-15}"
export BULLET=true PROSOPITE=true
LOG=$(mktemp)
bundle exec rspec --format documentation 2>&1 | tee "$LOG"
ruby -e '
budget = ARGV[0].to_i
log = File.read(ARGV[1])
fails = []
log.scan(/^(.+?_spec\.rb:\d+).*?queries:\s*(\d+)/m) do |loc, n|
  fails << [loc, n.to_i] if n.to_i > budget
end
nplus1 = log.scan(/USE eager loading detected.*$/).length \
  + log.scan(/Prosopite::NPlusOneQueriesError/).length
unless fails.empty? && nplus1.zero?
  puts "FAIL: #{nplus1} N+1, #{fails.size} budget breaches"
  fails.each { |loc, n| puts "  #{loc}: #{n} queries (>#{budget})" }
  exit 1
end
puts "OK: zero N+1, all specs within #{budget} queries"
' "$BUDGET" "$LOG"
bundle exec rake lol_dba:missing_indexes || true
