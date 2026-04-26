#!/usr/bin/env bash
# Fail the build if any legacy Python config file exists alongside pyproject.toml.
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
