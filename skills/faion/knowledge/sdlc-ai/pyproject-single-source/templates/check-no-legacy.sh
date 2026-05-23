#!/usr/bin/env bash
# purpose: CI script that fails the build when legacy Python config files exist beside pyproject.toml
# consumes: repo file listing
# produces: config (exit code 1 if legacy companions found)
# depends-on: content/01-core-rules.xml (no-legacy-companions, ci-check-no-legacy)
# token-budget-impact: low — ~100 tokens when loaded as context
# Drop into CI as: `bash check-no-legacy.sh`.
set -euo pipefail

forbidden=(
  setup.cfg
  .flake8
  pytest.ini
  tox.ini
  mypy.ini
  .coveragerc
  requirements.txt
  requirements-dev.txt
)

found=()
for f in "${forbidden[@]}"; do
  [[ -f "$f" ]] && found+=("$f")
done

if (( ${#found[@]} > 0 )); then
  echo "ERROR: legacy config file(s) present; move config into pyproject.toml:" >&2
  printf '  %s\n' "${found[@]}" >&2
  exit 1
fi

[[ -f pyproject.toml ]] || { echo "ERROR: pyproject.toml missing." >&2; exit 1; }
echo "OK: pyproject.toml is the single source of config."
