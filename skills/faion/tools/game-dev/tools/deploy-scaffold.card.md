# deploy-scaffold

## Purpose
Emit a systemd unit, an nginx vhost and a `deploy.sh` for one gunicorn app, with every collidable identity namespaced by `--name`.

## Invoke
```
python3 {script} --name {name} --port {port} --domain {host} --root {/opt/dir} [--out-dir {dir}] [--wsgi {pkg.wsgi:application}] [--user {u}] [--group {g}] [--state-dir {path}] [--webroot {path}] [--zone {z}] [--backend {dir}] [--frontend {dir}] [--test-labels {labels}] [--page-route {/path}={file}] [--regex-route {regex}={file}] [--check-local] [--force]
```

## Inputs
- `--name {name}` — service identity, `^[a-z][a-z0-9-]{1,30}$`. Required. Drives unit name, unix user/group, `/var/lib/{name}`, nginx zone `{name}api`.
- `--port {port}` — loopback gunicorn port, 1024-65535. Required.
- `--domain {host}` — public hostname. Required.
- `--root {/opt/dir}` — app directory on the host. Required.
- `--out-dir {dir}` — where the trio is written. Optional, default `deploy`.
- `--wsgi`, `--user`, `--group`, `--state-dir`, `--webroot`, `--zone` — override a derived identity. Optional.
- `--backend` / `--frontend` — repo subdirs. Optional, default `backend` / `frontend`.
- `--page-route {/path}={file}` — exact `location =`. Repeatable, optional.
- `--regex-route {regex}={file}` — regex `location ~`, always emitted quoted. Repeatable, optional.
- `--check-local` — refuse if the unit, state dir or vhost already exists on this machine. Optional.
- `--force` — overwrite existing output files. Optional.

## Outputs
- Files: `{out-dir}/{name}.service`, `{out-dir}/nginx.conf`, `{out-dir}/deploy.sh` (mode 755).
- stdout: `deploy-scaffold: name=… service=… user=…:… port=… zone=… state=… webroot=… -> …` — the identity line to diff against a sibling deploy.
- Exit: `0` written · `1` output files exist and `--force` was not passed · `2` invalid name, domain or port, or a malformed route spec · `3` `--check-local` found the identity taken.

## When NOT to use
- Containerised or PaaS deploys — this targets a single host with systemd and nginx.
- Non-WSGI runtimes (ASGI/uvicorn, Node, Go); the unit hardcodes gunicorn.
- To apply anything: it writes templates, never installs, reloads or restarts.

## Cost
Zero model calls. Instant; pure text generation plus three stat calls under `--check-local`.
