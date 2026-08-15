#!/usr/bin/env bash
# purpose: Fail-closed static deploy — an rsync allow-list plus a separate, explicit orphan removal.
# consumes: a built site directory, and connection settings supplied as environment variables.
# produces: the shipped webroot on the target host; nothing else can reach it.
# depends-on: content/01-core-rules.xml rule r6-allow-list-the-rsync
# token-budget-impact: small
#
# Every path below is a placeholder. Substitute the shipped entry points of your
# own site; do not commit hostnames, ports, users or key names into this file.
set -euo pipefail

: "${DEPLOY_HOST:?set DEPLOY_HOST}"        # public name, never an address literal
: "${DEPLOY_USER:?set DEPLOY_USER}"
: "${DEPLOY_PORT:=22}"
: "${DEPLOY_KEY:?path to the private key written from a secret at run time}"
: "${WEBROOT:?absolute path of the webroot on the target}"

SSH="ssh -i ${DEPLOY_KEY} -p ${DEPLOY_PORT} -o StrictHostKeyChecking=accept-new"

# ALLOW-LIST. Only these reach the webroot; the terminal --exclude='*' makes
# everything unnamed fail closed. The exclude-list this replaces shipped 960
# virtualenv files plus every build script, because nobody had named them.
#
# --delete WITHOUT --delete-excluded is deliberate: rsync PROTECTS receiver-side
# files a filter excludes, so this deletes nothing it did not put there. The
# price is orphans, removed below by name.
rsync -az --delete \
  --include='/index.html' \
  --include='/manifest.webmanifest' \
  --include='/sw.js' \
  --include='/assets/***' \
  --exclude='*' \
  -e "$SSH" \
  ./ "${DEPLOY_USER}@${DEPLOY_HOST}:${WEBROOT}/"

# Orphan removal: a separate, deliberate step. One file per line, no globs — a
# glob here would undo the protection the missing --delete-excluded provides.
$SSH "${DEPLOY_USER}@${DEPLOY_HOST}" "cd ${WEBROOT} && rm -f \
  retired-page.html \
  assets/js/retired.js"
