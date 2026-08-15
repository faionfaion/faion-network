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
    echo "       [--python <exe>] [--force] [--self-test]" >&2
    exit 2
}

# --- self-test -------------------------------------------------------------
# Drives this script's own CLI in a temp tree and asserts exit codes and
# summary fields. It never installs from a network index: the only pip call is
# against an empty requirements file, which resolves nothing.
CHECKS=0
FAILURES=0

st_expect() { # <label> <want-exit> <command...>
    label=$1; want=$2; shift 2
    CHECKS=$((CHECKS + 1))
    got=0
    ST_OUT=$("$@" 2>/dev/null) || got=$?
    [ "$got" -eq "$want" ] || {
        echo "venv-bootstrap: self-test: $label: exit $got, wanted $want" >&2
        FAILURES=$((FAILURES + 1))
    }
}

st_contains() { # <label> <needle>  (against the last st_expect stdout)
    CHECKS=$((CHECKS + 1))
    case "$ST_OUT" in
        *"$2"*) ;;
        *) echo "venv-bootstrap: self-test: $1: output lacks '$2'" >&2
           FAILURES=$((FAILURES + 1)) ;;
    esac
}

self_test() {
    T=$(mktemp -d) || { echo "venv-bootstrap: self-test: no tempdir" >&2; return 1; }
    trap 'rm -rf "$T"' EXIT
    mkdir -p "$T/proj"

    st_expect "no --dir"          2 "$0"
    st_expect "unknown argument"  2 "$0" --dir "$T/proj" --nope
    st_expect "--dir missing"     2 "$0" --dir "$T/absent"
    st_expect "--requirements missing" 2 "$0" --dir "$T/proj" --requirements "$T/absent.txt"
    st_expect "--python missing"  2 "$0" --dir "$T/proj" --python "no-such-interpreter-xyz"

    st_expect "first run creates" 0 "$0" --dir "$T/proj"
    st_contains "first run creates" "created=yes"
    st_expect "second run reuses" 0 "$0" --dir "$T/proj"
    st_contains "second run reuses" "created=no"

    st_expect "stdlib import ok"  0 "$0" --dir "$T/proj" --verify-import json,os
    st_contains "stdlib import ok" "imports=ok(2)"
    st_expect "bogus import fails" 1 "$0" --dir "$T/proj" --verify-import no_such_module_xyz

    # A relative --venv resolves under the project, not the caller's cwd.
    st_expect "relative --venv"   0 "$0" --dir "$T/proj" --venv subenv
    st_contains "relative --venv" "$T/proj/subenv"

    # An empty requirements file exercises the stamp without reaching an index.
    : > "$T/proj/empty.txt"
    st_expect "requirements install" 0 "$0" --dir "$T/proj" --requirements "$T/proj/empty.txt"
    st_contains "requirements install" "installed=yes"
    st_expect "requirements stamped" 0 "$0" --dir "$T/proj" --requirements "$T/proj/empty.txt"
    st_contains "requirements stamped" "installed=skipped"
    st_expect "--force reinstalls" 0 "$0" --dir "$T/proj" --requirements "$T/proj/empty.txt" --force
    st_contains "--force reinstalls" "installed=yes"

    echo "venv-bootstrap: self-test checks=$CHECKS failures=$FAILURES"
    [ "$FAILURES" -eq 0 ] || return 1
    return 0
}

case "${1:-}" in
    --self-test) self_test; exit $? ;;
esac

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
