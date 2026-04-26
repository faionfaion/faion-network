#!/usr/bin/env bash
# decomp-rails-lint.sh — fail if Rails decomposition convention is broken.
# Usage: decomp-rails-lint.sh app/
set -euo pipefail
ROOT="${1:-app}"
fail=0
check() {
  local pattern="$1" max="$2" label="$3"
  while IFS= read -r f; do
    n=$(wc -l <"$f")
    if [ "$n" -gt "$max" ]; then
      echo "FAIL $label: $f has $n lines (max $max)"
      fail=1
    fi
  done < <(find "$ROOT" -path "$pattern" -type f)
}
check "*/controllers/*.rb"    150 "Controller"
check "*/models/*.rb"         150 "Model"
check "*/services/*/*.rb"     100 "Service"
check "*/queries/*/*.rb"       80 "Query"
check "*/serializers/*.rb"    100 "Serializer"
check "*/policies/*.rb"        80 "Policy"
controllers=$(find "$ROOT/controllers" -name '*_controller.rb' 2>/dev/null | wc -l)
services=$(find "$ROOT/services" -name '*.rb' 2>/dev/null | wc -l)
if [ "$controllers" -gt 5 ] && [ "$services" -eq 0 ]; then
  echo "FAIL: ${controllers} controllers but app/services/ is empty"
  fail=1
fi
exit "$fail"
