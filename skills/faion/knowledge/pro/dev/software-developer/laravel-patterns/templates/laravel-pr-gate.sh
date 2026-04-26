#!/usr/bin/env bash
# laravel-pr-gate.sh
# Runs after every Laravel PR. Fails if any gate is violated.
# Usage: ./templates/laravel-pr-gate.sh
set -euo pipefail

composer install --no-progress --prefer-dist
vendor/bin/pint --test
vendor/bin/phpstan analyse --memory-limit=1G --no-progress

php artisan config:clear
php artisan route:list --json > /tmp/routes.json

# Enforce FormRequest on all mutation routes
jq -r '.[] | select(.method | test("POST|PUT|PATCH|DELETE")) | .action' /tmp/routes.json |
  grep -v 'FormRequest' | grep -v 'Closure' | grep . && {
    echo "ERROR: mutation route without FormRequest"; exit 1; } || true

# Warn on unguarded get()/all() in controllers
grep -RIn --include='*.php' '::all()\|->get()' app/Http/Controllers && {
  echo "WARN: explicit get()/all() — verify eager-load with()"; }

# Enforce $fillable on every model
grep -RIn --include='*.php' 'extends Model' app/Models | while read -r line; do
  f=${line%%:*}
  grep -q '\$fillable\|\$guarded' "$f" || {
    echo "ERROR: $f missing fillable/guarded"; exit 1; }
done

vendor/bin/pest --parallel --coverage --min=70
echo "Laravel gate OK"
