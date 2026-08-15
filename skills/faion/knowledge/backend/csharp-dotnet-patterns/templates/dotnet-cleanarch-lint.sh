#!/usr/bin/env bash
# purpose: grep-level Clean Architecture lint for the checks NetArchTest cannot see
# consumes: solution root containing src/*.Domain, src/*.Application, controllers
# produces: exit 1 plus a per-check report when any canonical antipattern is present
# depends-on: content/01-core-rules.xml rules layer-direction, rich-domain-no-setters,
#             no-entity-in-api, validators-on-commands
# token-budget-impact: ~450 tokens when loaded as context
#
# Usage: dotnet-cleanarch-lint.sh <solution-root>
# Wire into `dotnet build` via an MSBuild BeforeTargets="Build" target, or into a
# pre-commit hook. Pair with `dotnet format --verify-no-changes` for style drift.
set -euo pipefail
root="${1:?usage: dotnet-cleanarch-lint.sh SOLUTION_ROOT}"
fail=0

echo "# .NET Clean Arch lint ($root)"

echo "## Controllers returning Domain entities (no-entity-in-api)"
grep -rEn 'public async Task<(User|Order|Product|Organization|Post)>' "$root/src" \
  --include='*Controller.cs' | tee /tmp/da.ctrl-ent || true
[[ -s /tmp/da.ctrl-ent ]] && fail=1

echo "## Aggregates with public setters other than Id (rich-domain-no-setters)"
grep -rEn 'public (string|int|Guid|DateTime|decimal|bool) \w+ \{ get; set; \}' \
  "$root"/src/*.Domain --include='*.cs' | grep -v 'Id { get;' \
  | tee /tmp/da.pub-set || true
[[ -s /tmp/da.pub-set ]] && fail=1

echo "## Domain project referencing EF Core or AspNetCore (layer-direction)"
grep -rEn 'Microsoft\.(EntityFrameworkCore|AspNetCore)' "$root"/src/*.Domain \
  --include='*.csproj' | tee /tmp/da.dom-leak || true
[[ -s /tmp/da.dom-leak ]] && fail=1

echo "## Application project referencing AspNetCore or EF Core (layer-direction)"
grep -rEn 'Microsoft\.(AspNetCore|EntityFrameworkCore)' "$root"/src/*.Application \
  --include='*.csproj' | tee /tmp/da.app-leak || true
[[ -s /tmp/da.app-leak ]] && fail=1

echo "## Handlers reading HttpContext (dbcontext-behind-interface)"
grep -rEn 'IHttpContextAccessor|HttpContext' "$root"/src/*.Application --include='*.cs' \
  | tee /tmp/da.http-in-app || true
[[ -s /tmp/da.http-in-app ]] && fail=1

echo "## Handle methods without a CancellationToken (cqrs-record-request-per-handler)"
grep -rEn 'Task<[^>]+> Handle\([^)]*\)' "$root/src" --include='*Handler.cs' \
  | grep -v 'CancellationToken' | tee /tmp/da.no-ct || true
[[ -s /tmp/da.no-ct ]] && fail=1

echo "## Commands missing a FluentValidation Validator (validators-on-commands)"
find "$root/src" -name '*Command.cs' | while read -r f; do
  base="${f%Command.cs}"
  [[ -f "${base}CommandValidator.cs" ]] || echo "missing validator: $f"
done | tee /tmp/da.no-val || true
[[ -s /tmp/da.no-val ]] && fail=1

exit "$fail"
