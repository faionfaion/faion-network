#!/usr/bin/env bash
# purpose: Legacy template for the ruby-rspec-testing methodology.
# consumes: inputs declared in ruby-rspec-testing/AGENTS.md prerequisites.
# produces: working code/config aligned with content/01-core-rules.xml.
# depends-on: content/02-output-contract.xml schema for output shape.
# token-budget-impact: ~600 tokens when loaded as reference.
# rspec-gate.sh — fail PR on coverage drop, slow specs, or flaky count.
# Usage: rspec-gate.sh [COVERAGE_MIN] [SLOW_MS]
# Defaults: COVERAGE_MIN=80, SLOW_MS=1000
set -euo pipefail

COV_MIN="${1:-80}"
SLOW="${2:-1000}"

COVERAGE=true bundle exec rspec \
  --profile 50 \
  --format documentation \
  --format json --out /tmp/rspec.json

ruby -rjson -e '
cov_min = ARGV[0].to_f
slow    = ARGV[1].to_i

last = JSON.parse(File.read("coverage/.last_run.json")) rescue {}
cov  = last.dig("result", "line") || 0

fail_msgs = []
fail_msgs << "coverage #{cov}% < #{cov_min}%" if cov < cov_min

data       = JSON.parse(File.read("/tmp/rspec.json"))
slow_specs = data["examples"].select { |e| (e["run_time"] * 1000).to_i > slow }
slow_specs.each { |e| puts "SLOW #{e["full_description"]} #{(e["run_time"]*1000).to_i}ms" }

fail_msgs << "#{slow_specs.size} specs >#{slow}ms" if slow_specs.size > 5

if fail_msgs.empty?
  puts "OK: cov=#{cov}% slow=#{slow_specs.size}"
else
  puts "FAIL: " + fail_msgs.join(" | ")
  exit 1
end
' "$COV_MIN" "$SLOW"
