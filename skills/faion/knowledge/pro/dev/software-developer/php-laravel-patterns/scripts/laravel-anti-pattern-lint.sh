#!/usr/bin/env bash
# laravel-anti-pattern-lint.sh — flag banned patterns per the layer rules.
# Usage: laravel-anti-pattern-lint.sh <project-root>
# Exit 1 on critical violations.
set -euo pipefail
root="${1:?usage: laravel-anti-pattern-lint.sh PROJECT_ROOT}"
fail=0
echo "# Laravel pattern audit ($root)"

echo "## Eloquent calls inside Controllers (must be in Service)"
grep -rEn '\b(User|Order|Post|Product)::(where|find|all|create|update|delete)\(' \
  "$root/app/Http/Controllers" --include='*.php' 2>/dev/null \
  | tee /tmp/lp.eloq-ctrl || true
[[ -s /tmp/lp.eloq-ctrl ]] && fail=1

echo "## Inline validation in Controllers (use FormRequest)"
grep -rEn 'Validator::make\(|\$request->validate\(' \
  "$root/app/Http/Controllers" --include='*.php' 2>/dev/null \
  | tee /tmp/lp.val-ctrl || true
[[ -s /tmp/lp.val-ctrl ]] && fail=1

echo "## request() helper inside Services"
grep -rEn '\brequest\(\)' "$root/app/Services" --include='*.php' 2>/dev/null \
  | tee /tmp/lp.req-svc || true
[[ -s /tmp/lp.req-svc ]] && fail=1

echo "## Magic facades inside Services (Cache::, Mail::, Notification::, Bus::)"
grep -rEn '\b(Cache|Mail|Notification|Bus|Event)::' \
  "$root/app/Services" --include='*.php' 2>/dev/null \
  | tee /tmp/lp.facade-svc || true
[[ -s /tmp/lp.facade-svc ]] && fail=1

echo "## DB::transaction wrapping HTTP / queue dispatch"
grep -rEn -A 10 'DB::transaction' "$root/app" --include='*.php' 2>/dev/null \
  | grep -E 'Http::|dispatch\(|Stripe::|->charge\(' \
  | tee /tmp/lp.tx-http || true
[[ -s /tmp/lp.tx-http ]] && fail=1

echo "## Repository wrapping Eloquent without alternate implementation"
find "$root/app" -name '*Repository.php' 2>/dev/null | while read -r f; do
  if grep -qE '::query\(\)|::where\(' "$f" && ! grep -qE 'interface\b|implements\b' "$f"; then
    echo "  $f: wraps Eloquent without abstraction"
  fi
done | tee /tmp/lp.repo || true

exit "$fail"
