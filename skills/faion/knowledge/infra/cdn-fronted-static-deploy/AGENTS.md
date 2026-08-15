# CDN-Fronted Static Deploy

## Summary

**One-sentence:** Ships a static site through a caching CDN proxy the pipeline cannot purge, by making the URL the HTML emits the invalidation lever — content-hashed assets, a versioned service-worker registration, exact-match caching, network-first navigations, an allow-list rsync — and by producing an edge-freshness report that proves what the edge served instead of what CI built.

**One-paragraph:** Everything under `/assets/` served `cache-control: public, max-age=31536000, immutable` behind a CDN proxy outlives any number of deploys. Measured on 2026-07-28, hours after a green deploy: `GET /assets/js/main.js` returned a 735-byte file three days old with `cf-cache-status: HIT` and `age: 280134`, while the origin held the current 10 487-byte file. CI was green throughout, because nothing in a normal pipeline looks at what the edge serves. Purging needs credentials the build does not have; re-pointing the header needs the origin. What the build does control is the URL — and page HTML is `cf-cache-status: DYNAMIC`, never edge-cached — so a content hash in the query string is the one lever that works from inside the pipeline. Four defences protect that lever, each of which cancelled it once in production: `/sw.js` is edge-cached too (measured 7.7 h stale), so the registration URL must be versioned; `cache.match(…, {ignoreSearch:true})` answers a new `?v=` from the old body; stale-while-revalidate on documents makes the first open the previous build, and yesterday's HTML pins yesterday's hashed assets; and an exclude-list rsync shipped 960 virtualenv files onto a public webroot.

**Ефективно для:** static sites and SPAs behind a proxied CDN, PWA kits with a service worker, push-to-live pipelines with no staging, and any team that has watched a green deploy fail to appear for real users.

## Applies If (ALL must hold)

- A caching proxy sits between the origin and the user.
- The deploy pipeline holds no credentials to purge the zone (or purging is not wanted on every deploy).
- Static assets are served with a long `max-age`, ideally `immutable`.
- Page HTML is not edge-cached — verify before relying on anything below.

## Skip If (ANY kills it)

- No CDN or proxy in front of the origin — there is nothing to route around.
- The pipeline can purge the zone and does so on every deploy — invalidate at the edge instead.
- Assets are served with no caching headers — stamping a URL that was never cached buys nothing.
- The HTML itself is edge-cached — the lever is inert; fix the header or get credentials first.

## Prerequisites

| Input artefact | Format | Source |
|---|---|---|
| Built site directory | files on disk | the generator or the repo itself |
| Origin cache-control headers | header values | origin config owner |
| One `curl -I` of a page and of an asset | HTTP response headers | anyone with the public URL |
| Deploy path allow-list | list of shipped paths | the site map |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[edge-and-cdn-strategy]]` | Cache-key design and origin shielding sit upstream of this; that decides the headers this one has to live with. |
| `[[build-generator-discipline]]` | The stamping step belongs to a build that renders everything before writing anything; a half-written site defeats the hash. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 9 rules: content-hash the URL, confirm HTML is DYNAMIC, version the worker registration, exact-match versioned assets, network-first navigations, allow-list rsync, `fetch-depth: 0`, browser-like probe UA, CI must look at what it ships | ~1300 |
| `content/02-output-contract.xml` | essential | JSON Schema for the edge-freshness report + six forbidden patterns, with the 2026-07-28 incident written out as the failing example | ~900 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns (trusting a green deploy, `cache: 'reload'`, global `ignoreSearch`, SWR on documents, exclude-list deploy, `--delete-excluded` as cleanup) + cheap symptoms | ~900 |
| `content/06-decision-tree.xml` | essential | Root: "is there a caching proxy this pipeline cannot purge?" then one branch per lever | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Add stamping to an existing build | sonnet | Mechanical rewrite of `href`/`src` emission. |
| Diagnose "deployed but not live" | sonnet | Pattern-match symptoms against `03-failure-modes.xml`. |
| Rewrite a service-worker fetch handler | opus | The exact-match / `ignoreSearch` split is where the subtle cancellation lives. |
| Produce the edge-freshness report | haiku | Fill the schema from probe output. |

## Templates

| File | Purpose |
|------|---------|
| `templates/rsync-allowlist.sh` | Fail-closed deploy: allow-list rsync with `--delete` and no `--delete-excluded`, plus a separate named orphan-removal step. All identifiers are placeholders. |
| `templates/edge-freshness-report.json` | Filled example of the report artefact, valid against the bundled validator. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-cdn-fronted-static-deploy.py` | Validates an edge-freshness report: byte disagreement outranks a FRESH self-report, an aged HIT is stale, unstamped asset paths fail, PASS cannot sit over a failing gate, and `site` may not carry an address literal. `--self-test` replays seven fixtures including the 2026-07-28 incident. | After every probe run; in CI once probing is wired. |

## Related

- [[edge-and-cdn-strategy]] — the upstream decision: cache keys, shielding, what gets a long `max-age` at all
- [[build-generator-discipline]] — the build that has to emit the stamped URLs atomically
- [[gha-deployment-patterns]] — the workflow this rsync step drops into
- `../../../tools/static-web/tools/asset-stamp.card.md` — the executable gate implementing rule `r1-content-hash-the-url`; run it as the last build step and again with `--check` in CI

## Decision tree

See `content/06-decision-tree.xml`. It gates on one observable — is there a proxy this pipeline cannot purge — then routes each remaining signal (HTML edge status, stamping, worker registration, match options, navigation strategy, rsync filter style, checkout depth, probe 403s) to the single rule that fixes it.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/rsync-allowlist.sh`

```bash
set -euo pipefail
: "${DEPLOY_HOST:?set DEPLOY_HOST}"        # public name, never an address literal
: "${DEPLOY_USER:?set DEPLOY_USER}"
: "${DEPLOY_PORT:=22}"
: "${DEPLOY_KEY:?path to the private key written from a secret at run time}"
: "${WEBROOT:?absolute path of the webroot on the target}"
SSH="ssh -i ${DEPLOY_KEY} -p ${DEPLOY_PORT} -o StrictHostKeyChecking=accept-new"
# ALLOW-LIST: everything unnamed fails closed. --delete WITHOUT --delete-excluded
# is deliberate — rsync protects receiver-side excluded paths, so the deploy can
# only remove what it placed.
rsync -az --delete \
  --include='/index.html' \
  --include='/manifest.webmanifest' \
  --include='/sw.js' \
  --include='/assets/***' \
  --exclude='*' \
  -e "$SSH" \
  ./ "${DEPLOY_USER}@${DEPLOY_HOST}:${WEBROOT}/"
# Orphan removal: separate step, one file per line, no globs.
$SSH "${DEPLOY_USER}@${DEPLOY_HOST}" "cd ${WEBROOT} && rm -f \
  retired-page.html \
  assets/js/retired.js"
```

### `templates/edge-freshness-report.json`

```json
{
  "artefact_id": "release-2026-08-15-edge-probe",
  "generated": "2026-08-15",
  "site": "example.test",
  "max_age_budget_seconds": 300,
  "probes": [
    {"url": "/index.html", "edge_status": "DYNAMIC", "edge_age_seconds": 0,
     "edge_bytes": 24310, "origin_bytes": 24310, "stamped": true, "verdict": "FRESH"},
    {"url": "/assets/js/main.js?v=9f21c0ab41", "edge_status": "MISS", "edge_age_seconds": 0,
     "edge_bytes": 10487, "origin_bytes": 10487, "stamped": true, "verdict": "FRESH"},
    {"url": "/sw.js?v=3ab0f5c912", "edge_status": "MISS", "edge_age_seconds": 0,
     "edge_bytes": 5218, "origin_bytes": 5218, "stamped": true, "verdict": "FRESH"}
  ],
  "gates": {"asset_stamp_check": true, "deploy_allow_list": true,
            "sw_registration_versioned": true, "navigations_network_first": true},
  "verdict": "PASS"
}
```
