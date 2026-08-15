---
type: change-request
cr_id: CR-012
title: "Templates that parse cleanly and fail when run"
priority: P0
created: 2026-08-15
status: proposed
affected_components: [faion-network/skills/faion/knowledge/*/*/templates]
blocks: "publication — these are files a customer copies into production"
---

# Change Request: templates that fail when run

Every finding below was **reproduced by executing the code** — against a real PostgreSQL 16
container, a real Redis, a real `docker build`, and `nginx -t`. None was reported from reading.

These files parse. Validator 5 passes them, because it checks the header. Nothing in the corpus
runs them.

## The six that cause damage rather than annoyance

**1. The nightly backup can never succeed.** `backend/backup-recovery/templates/backup.sh:15` runs
`docker exec -t pg_dump -Fc > file`. The `-t` allocates a TTY, which inserts `0x0D` before every
`0x0A` in a **binary** dump. Verified: a 6,436-byte dump arrives as 6,520 bytes and
`pg_restore` fails with "could not read from input file: end of file". The script's own verify step
catches it, prints `CORRUPT`, exits 1 — so steps 2-5 never run: **no Redis snapshot, no config
tarball, no restic offsite, no retention.** The operator gets a nightly CORRUPT mail and has no
backups. Removing `-t` is the entire fix; the control run passes.

**2. The bootstrap script locks you out of a fresh VPS.**
`backend/server-init-bootstrap/templates/bootstrap.sh:49-55` sets `ufw default deny incoming`,
allows `2222`, `80`, `443`, then `ufw --force enable` — **port 22 is never allowed, and SSH is still
on 22**, because the port change is deferred to a `TODO` echo at line 74. Established sessions
survive on conntrack, so it looks fine until you reconnect. Compounding: line 66 writes `port = ssh`
into the fail2ban jail while the sibling `fail2ban-jail.local:17` says `port = 2222` — two templates
in one methodology disagree, so brute-force protection watches the wrong port either way.

**3. The hardening verifier green-lights a vulnerable server.**
`backend/server-init-bootstrap/templates/verify-bootstrap.sh:37` is
`grep -q 'PermitRootLogin no' /etc/ssh/sshd_config` — which **matches the commented-out
`#PermitRootLogin no`**. Verified: a config with `#PermitRootLogin no` followed by
`PermitRootLogin yes` reports `[OK] no root SSH`. Same at line 38 for `PasswordAuthentication`. The
timezone check at line 32 is a no-op that reports OK on an unconfigured box, and line 35 can never
match the rule the bootstrap actually creates, so it always reports FAIL.

**4. A failed deploy reports success, and there is no rollback.**
`backend/deploy-scripts/templates/deploy.sh:31-36` uses `curl -fsS … && break` inside a loop. Under
`set -e` the failure of a non-final command in an AND-list is ignored, so the loop ends and
`echo OK; exit 0` runs. Verified: **10 consecutive failed health probes against a dead port exit 0**,
with the symlink already switched. This breaks three of its own rules — "No-smoke deploy = REJECT",
"keep a `previous` symlink; rollback = one mv" (no `previous` symlink is ever created, though line 1
advertises a rollback path), and "every step MUST propagate exit codes".

**5. The HAR "scrubber" leaves the credentials in, under a `[REDACTED]` label.**
`automation-tooling/puppeteer-output-capture/templates/scrubber.ts:9` matches
`/Authorization:\s*[^\s]+/gi`, which stops at the first whitespace — so it redacts the **scheme** and
keeps the secret. Verified: `Authorization: Basic dXNlcjpzdXBlcnNlY3JldA==` becomes
`Authorization: [REDACTED] dXNlcjpzdXBlcnNlY3JldA==`. **The marker is what makes it dangerous** — a
reviewer sees `[REDACTED]` and trusts the file. Also verified leaking: `x-api-key`, JSON `api_key`,
15-digit Amex and any space- or dash-formatted card number.

**6. The Dockerfile bakes `.env` into a pushed image.** `infra/docker/templates/Dockerfile.python:25`
is `COPY . .`, and there is **not one `.dockerignore` in all 7,340 templates**. Verified by building
against a context containing `.env`: `cat /app/.env` in the resulting image prints the database URL
and the live Stripe key to anyone who can pull it.

## The systemic one

**57 shell templates carry the shebang on line 7**, below the metadata header. Under `execve` — a
systemd `ExecStart`, or Python `subprocess` without a shell — this is
`OSError: [Errno 8] Exec format error`. Under cron, `/bin/sh` is dash, and **49 of the 57 die on
their first executable line** with `set: Illegal option -o pipefail`.
`backup-recovery/templates/backup.sh` documents itself as *"Run daily from cron"* and fails exactly
that way.

Same class, different language: 9 Python templates cannot be imported at all (a second docstring
sits between the header and `from __future__ import annotations`, which must be the first
statement); 7 Terraform templates fail `terraform init` (`;` as an attribute separator); 3 JS
templates start with a `#` shell comment.

## Templates that break their own methodology's rules

This is the sharpest category, because the document contradicts itself in a file the customer runs.

| Template | Rule it breaks |
|---|---|
| `architecture/api-gateway-patterns/bff-aggregator.py` | Bare `asyncio.gather` with one global timeout and a hardcoded `"X-Request-ID": "generated-uuid"`, against rules mandating partial degradation, per-service timeouts, and a unique request id. Verified: one refused upstream returns 500; the partial-degradation branches never execute |
| `dev/structured-logging-as-code/logger.py` | `REDACT_FIELDS` covers **0 of the 5 PII categories** its own rule names (email, phone, name, payment token, IP); matching is exact and case-sensitive, so `Authorization`, `access_token`, `cardNumber` all serialise in the clear — and the message body is never filtered at all |
| `dev/caching-strategy/cache-aside.py` | Its header claims "jittered TTL + single-flight"; it has **neither**. Fixed `setex`, unguarded loader. A hot key at 500 rps with a 1.8 s loader sends ~900 concurrent queries the moment the TTL lapses — the stampede the rule forbids |
| `dev/caching-strategy/cache-singleflight.py` | `finally: delete(lock_key)` without an ownership check. Verified against real Redis: with a 1 s lock TTL and a 2 s load, **two loaders ran concurrently**, and a slow worker deletes the lock a *different* worker now holds. Single-flight breaks precisely when the origin is slow |
| `backend/django-celery/task-idempotent.py` | Reads the flag, sends the email, *then* does the atomic UPDATE — the guard is on the wrong side of the side effect. With `acks_late` + 5 retries and no idempotency key on the POST, one reset re-sends up to 6 times |
| `dev/django-coding-standards/service-stub.py` | Advertised as "skeleton with `@transaction.atomic`" and has no `atomic` anywhere. Verified on Django 6.1: outside a transaction `on_commit` fires **immediately**, so the Celery task dispatches before the row exists — the exact incident `django-celery`'s `on-commit-dispatch` rule cites. `select_for_update()` additionally raises on PostgreSQL and is a silent no-op on SQLite |
| `infra/github-actions-cicd` ×3 templates | Its own rule: *"never `@v4`, `@main` or any mutable tag."* `reusable-deploy.yml:43` uses `actions/download-artifact@v4` **in the workflow holding `secrets.DEPLOY_KEY`** |
| `sdlc-ai/sec-trivy-pinned-supply-chain-scan/trivy-action.yml` | The pin is **41 hex characters**. A git SHA is 40, so it can never resolve — and the file's subject is pinning |
| `infra/terraform/versions.tf` | Rule requires the `=` operator; ships `>=` and `~>`. Corpus-wide **0 of 16** provider constraints use `=` |
| `sdd/cd-basics/expand_contract_migration.sql` | Phase 3 drops `email_old`, a column no phase creates and which appears nowhere else in the methodology |

## What this means for the gate

Nothing in `f066-validate-all.sh` executes a template. Validator 5 reads its header; the parse
sweep added today reads its syntax. **A file can be syntactically perfect, header-complete, and
destroy a production database.**

The cheap checks that would have caught most of the above, in order of value per line:

1. **Shebang must be line 1 in every `.sh`** — 57 findings, zero judgement, one regex.
2. **`.py` templates must import** — 9 findings, `compile()` already runs in the parse sweep.
3. **`terraform fmt -check` / `node --check` / `nginx -t`** where the tool exists — 12 findings.
4. **A template must not contradict a rule in its own `01-core-rules.xml`** — not mechanisable in
   general, but the specific pairs above are, and they are the highest-value class.

## Recommendation

**Fix the six damage-causing templates today**; they are single-line changes in five of six cases.
Then the 57 shebangs and the 19 import/parse failures, which are mechanical. The
rule-contradiction set is real editorial work and belongs with CR-011, since both are the same
underlying problem: **the corpus was generated, and nobody ran it.**
