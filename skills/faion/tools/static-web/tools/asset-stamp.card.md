# asset-stamp

## Purpose
Appends each static asset's own content hash to the URL the HTML emits, so a CDN edge holding an
`immutable` copy is forced to fetch the new bytes while unchanged assets keep their URL and stay
cached. Use it as the last build step, and in `--check` mode as a CI gate that fails when a page
still points at an unstamped or stale asset. It implements the first lever of the
`cdn-fronted-static-deploy` methodology, which carries the measured incident behind it and the
service-worker and rsync rules this tool does not cover.

## Invoke
```
python3 {script} --dir {build} --root {webroot} [--prefix {/assets/}] [--glob {*.html}] [--check] [--self-test]
```

## Inputs
- `--dir {path}` — directory of HTML files to stamp, searched recursively. Required.
- `--root {path}` — web root the asset URLs resolve against. Often the same as `--dir`. Required.
- `--prefix {url}` — URL prefix treated as an asset path. Optional, default `/assets/`.
- `--glob {pattern}` — which files under the directory to stamp. Optional, default `*.html`.
- `--check` — report drift and write nothing. Optional.
- `--self-test` — run the built-in fixtures and exit. Optional.

## Outputs
- Files: the HTML under `{dir}` is rewritten in place, unless `--check` is passed.
- stdout: `asset-stamp: pages=N stamped=M findings=F` (`drifted=` in place of `stamped=` under `--check`).
- stderr: one line per finding — an asset URL with no file behind it, or a page whose URLs are stale.
- Exit: `0` every asset URL is stamped and current · `1` a finding was reported · `2` the tool could not run (missing or non-directory `--dir`/`--root`, unreadable page).

## When NOT to use
- Verifying what the CDN actually serves. This tool never opens a socket; it guarantees only that the HTML addresses the bytes you built. Fetch the URL yourself to prove the edge caught up.
- Asset paths built inside JavaScript string literals. Only `href="…"` and `src="…"` attributes are matched, deliberately — rewriting a value the page later compares or keys on turns a cache fix into a data bug.
- Assets served without a long `max-age`. Stamping a URL that was never cached buys nothing and adds a diff to every build.

## Cost
Zero model calls. Zero network calls. One sha256 per referenced asset, one pass per page; milliseconds for a site of a few hundred pages.
