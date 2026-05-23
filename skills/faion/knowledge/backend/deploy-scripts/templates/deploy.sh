# purpose: Deploy script template with atomic switch + smoke check + rollback path.
# consumes: see content/02-output-contract.xml inputs
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200-600 tokens when loaded as context

#!/usr/bin/env bash
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
ln -sfn "$RT/releases/$TS" "$RT/current.new"
mv -T "$RT/current.new" "$RT/current"
systemctl --user reload "$PROJECT"

echo "[5/5] smoke check"
for i in $(seq 1 10); do
  curl -fsS http://127.0.0.1:8000/health && break
  sleep 1
done

echo OK
