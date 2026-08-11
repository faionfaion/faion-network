#!/bin/sh
# venv-bootstrap.sh — create/refresh a project .venv and prove it imports.
#
# Input:  --dir <project> [--venv <path>] [--requirements <path>]
#         [--verify-import <mod[,mod...]>] [--python <exe>] [--force]
# Output: one summary line on stdout; exit 0 ok / 1 build or import failed /
#         2 usage or environment error.
#
# Idempotent: a second run with an unchanged requirements file reinstalls
# nothing (a checksum stamp inside the venv is compared, not a timestamp).
#
# Why this exists: pipelines repeatedly ran `manage.py test` with no venv at
# all, read the resulting ImportError as a code defect, and burned fix-rounds
# on a phantom failure. Bootstrap first, then gate.
set -eu

PROJECT=""
VENV=""
REQ=""
IMPORTS=""
PY="python3"
FORCE=0

usage() {
    echo "usage: venv-bootstrap.sh --dir <project> [--venv <path>]" >&2
    echo "       [--requirements <path>] [--verify-import <mod[,mod...]>]" >&2
    echo "       [--python <exe>] [--force]" >&2
    exit 2
}

while [ $# -gt 0 ]; do
    case "$1" in
        --dir) PROJECT="${2:-}"; shift 2 ;;
        --venv) VENV="${2:-}"; shift 2 ;;
        --requirements) REQ="${2:-}"; shift 2 ;;
        --verify-import) IMPORTS="${2:-}"; shift 2 ;;
        --python) PY="${2:-}"; shift 2 ;;
        --force) FORCE=1; shift ;;
        -h|--help) usage ;;
        *) echo "venv-bootstrap: unknown argument: $1" >&2; usage ;;
    esac
done

[ -n "$PROJECT" ] || usage
if [ ! -d "$PROJECT" ]; then
    echo "venv-bootstrap: not a directory: $PROJECT" >&2
    exit 2
fi
PROJECT=$(cd "$PROJECT" && pwd)
[ -n "$VENV" ] || VENV="$PROJECT/.venv"
case "$VENV" in /*) ;; *) VENV="$PROJECT/$VENV" ;; esac

# Default requirements: <project>/requirements.txt when present.
if [ -z "$REQ" ] && [ -f "$PROJECT/requirements.txt" ]; then
    REQ="$PROJECT/requirements.txt"
fi
if [ -n "$REQ" ] && [ ! -f "$REQ" ]; then
    echo "venv-bootstrap: requirements file not found: $REQ" >&2
    exit 2
fi

CREATED=no
if [ ! -x "$VENV/bin/python" ]; then
    command -v "$PY" >/dev/null 2>&1 || {
        echo "venv-bootstrap: interpreter not found: $PY" >&2
        exit 2
    }
    "$PY" -m venv "$VENV" >/dev/null 2>&1 || {
        echo "venv-bootstrap: venv creation failed at $VENV" >&2
        exit 1
    }
    CREATED=yes
fi
VPY="$VENV/bin/python"

INSTALLED=skipped
if [ -n "$REQ" ]; then
    STAMP="$VENV/.faion-req-stamp"
    SUM=$(cksum < "$REQ" | tr -s ' ' | cut -d' ' -f1,2)
    PREV=""
    [ -f "$STAMP" ] && PREV=$(cat "$STAMP")
    if [ "$FORCE" -eq 1 ] || [ "$SUM" != "$PREV" ]; then
        if "$VPY" -m pip install -q --disable-pip-version-check -r "$REQ"; then
            printf '%s' "$SUM" > "$STAMP"
            INSTALLED=yes
        else
            echo "venv-bootstrap: pip install failed for $REQ" >&2
            exit 1
        fi
    fi
fi

NIMP=0
if [ -n "$IMPORTS" ]; then
    OLDIFS=$IFS
    IFS=,
    for m in $IMPORTS; do
        [ -n "$m" ] || continue
        if ! "$VPY" -c "import $m" >/dev/null 2>&1; then
            IFS=$OLDIFS
            echo "venv-bootstrap: import failed in $VENV: $m" >&2
            exit 1
        fi
        NIMP=$((NIMP + 1))
    done
    IFS=$OLDIFS
fi

echo "venv-bootstrap: venv=$VENV created=$CREATED installed=$INSTALLED imports=ok($NIMP)"
