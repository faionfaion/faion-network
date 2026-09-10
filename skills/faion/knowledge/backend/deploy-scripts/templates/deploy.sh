#!/usr/bin/env bash
# purpose: Deploy script template with atomic switch + smoke check + rollback path.
# consumes: see content/02-output-contract.xml inputs
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200-600 tokens when loaded as context

set -euo pipefail

PROJECT=${1:?usage: deploy.sh <project>}
SRC=~/workspace/projects/$PROJECT
RT=/srv/$PROJECT
TS=$(date -u +%Y%m%dT%H%M%SZ)

echo "[1/5] lint+tests in $SRC"
(cd "$SRC" && ruff check . && pytest -x)

echo "[2/5] rsync to release dir"
mkdir -p "$RT/releases/$TS"
rsync -a --delete --exclude .venv --exclude __pycache__ "$SRC/" "$RT/releases/$TS/"

echo "[3/5] install editable"
(cd "$RT/releases/$TS" && python3 -m venv .venv && .venv/bin/pip install -e .)

echo "[4/5] switch symlinks"
# Keep the outgoing release addressable before replacing it. The methodology's
# own rule is "keep a `previous` symlink; rollback = one mv", and nothing here
# used to create one, while line 1 advertised a rollback path.
if [ -e "$RT/current" ]; then
  ln -sfn "$(readlink -f "$RT/current")" "$RT/previous.new"
  mv -T "$RT/previous.new" "$RT/previous"
fi
ln -sfn "$RT/releases/$TS" "$RT/current.new"
mv -T "$RT/current.new" "$RT/current"
systemctl --user reload "$PROJECT"

echo "[5/5] smoke check"
# `curl -fsS … && break` is what made this script lie. Under `set -e` the
# failure of a non-final command in an AND-list is IGNORED, so ten dead probes
# fell out of the loop and reached `echo OK` with the symlink already switched.
# Verified against a closed port: exit 0, every time.
healthy=0
for _ in $(seq 1 10); do
  if curl -fsS http://127.0.0.1:8000/health >/dev/null; then
    healthy=1
    break
  fi
  sleep 1
done

if [ "$healthy" -ne 1 ]; then
  echo "smoke check FAILED after 10 probes — rolling back" >&2
  if [ -e "$RT/previous" ]; then
    ln -sfn "$(readlink -f "$RT/previous")" "$RT/current.new"
    mv -T "$RT/current.new" "$RT/current"
    systemctl --user reload "$PROJECT"
    echo "rolled back to $(readlink -f "$RT/current")" >&2
  else
    echo "no previous release to roll back to; $RT/current still points at $TS" >&2
  fi
  exit 1
fi

echo OK
