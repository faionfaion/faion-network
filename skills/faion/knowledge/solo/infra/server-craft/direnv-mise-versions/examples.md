# direnv + mise Examples

## Example 1: NERO Project .envrc

The NERO platform's workspace uses direnv to auto-load secrets and activate the correct Python version.

### Workspace-Level .envrc

```bash
# ~/workspace/.envrc
# Auto-load master .env when entering workspace
dotenv_if_exists .env

log_status "NERO workspace env loaded"
```

### Per-Repo .envrc (nero-core)

```bash
# ~/workspace/repos/nero-core/.envrc
# Full project environment setup

# Runtime versions from .tool-versions
use mise

# Python virtualenv
layout python-venv .venv

# Inherit workspace secrets
source_env ../../.envrc

# Reload triggers
watch_file requirements.txt
watch_file pyproject.toml

# Python settings
export PYTHONDONTWRITEBYTECODE=1
export PYTHONUNBUFFERED=1
export CELERY_CONCURRENCY=2  # Dev: fewer workers

log_status "nero-core | Python $(python --version 2>&1 | cut -d' ' -f2) | venv: .venv"
```

### .tool-versions

```
# ~/workspace/repos/nero-core/.tool-versions
python 3.12.8
```

### What Happens When You `cd` into the Directory

```bash
$ cd ~/workspace/repos/nero-core
direnv: loading ~/workspace/repos/nero-core/.envrc
direnv: loading ~/workspace/.envrc
direnv: export +ANTHROPIC_API_KEY +CELERY_CONCURRENCY +DATABASE_URL ...
nero-core | Python 3.12.8 | venv: .venv

$ which python
/home/nero/workspace/repos/nero-core/.venv/bin/python

$ python --version
Python 3.12.8

$ echo $DATABASE_URL
postgresql://nero:***@localhost:5432/nero

$ cd ~
direnv: unloading

$ which python
/home/nero/.local/share/mise/installs/python/3.12.8/bin/python

$ echo $DATABASE_URL
(empty - unloaded by direnv)
```

## Example 2: Multi-Python-Version Setup

Running different Python versions for different projects on the same server.

### Install Multiple Versions

```bash
$ mise install python@3.11.11
$ mise install python@3.12.8

$ mise ls
Tool    Version   Status   Source
python  3.11.11            ~/.tool-versions
python  3.12.8   active    ~/.tool-versions
```

### Project A: NERO (Python 3.12)

```bash
# ~/workspace/repos/nero-core/.tool-versions
python 3.12.8
```

```bash
$ cd ~/workspace/repos/nero-core
$ python --version
Python 3.12.8
```

### Project B: MeetingTax (Python 3.11)

```bash
# ~/projects/meetingtax/be/.tool-versions
python 3.11.11
```

```bash
$ cd ~/projects/meetingtax/be
$ python --version
Python 3.11.11
```

### Switching Between Projects

```bash
$ cd ~/workspace/repos/nero-core
direnv: loading .envrc
nero-core | Python 3.12.8 | venv: .venv

$ python --version
Python 3.12.8

$ cd ~/projects/meetingtax/be
direnv: unloading
direnv: loading .envrc
meetingtax-be | Python 3.11.11 | venv: .venv

$ python --version
Python 3.11.11

# Each project has its own venv with its own dependencies
$ pip list | head -3
Package    Version
---------- -------
fastapi    0.115.6
```

## Example 3: Full-Stack Project (Python + Node)

A project that needs both Python (backend) and Node.js (frontend) with automatic environment switching.

### Directory Structure

```
~/projects/meetingtax/
├── be/                    # Python FastAPI backend
│   ├── .envrc
│   ├── .tool-versions     # python 3.11.11
│   ├── .venv/
│   └── pyproject.toml
├── fe/                    # Next.js frontend
│   ├── .envrc
│   ├── .tool-versions     # node 22.12.0
│   └── package.json
└── .env                   # Shared secrets
```

### Backend .envrc

```bash
# ~/projects/meetingtax/be/.envrc
use mise
layout python-venv .venv
dotenv_if_exists ../.env
export PYTHONDONTWRITEBYTECODE=1

log_status "meetingtax-be | Python $(python --version 2>&1 | cut -d' ' -f2)"
```

### Frontend .envrc

```bash
# ~/projects/meetingtax/fe/.envrc
use mise
dotenv_if_exists ../.env
PATH_add node_modules/.bin
export NODE_ENV=development
export NEXT_PUBLIC_API_URL=http://localhost:8200

log_status "meetingtax-fe | Node $(node --version 2>&1)"
```

### Switching Between Backend and Frontend

```bash
$ cd ~/projects/meetingtax/be
direnv: loading .envrc
meetingtax-be | Python 3.11.11
$ which python
/home/nero/projects/meetingtax/be/.venv/bin/python

$ cd ../fe
direnv: unloading
direnv: loading .envrc
meetingtax-fe | Node v22.12.0
$ which node
/home/nero/.local/share/mise/installs/node/22.12.0/bin/node
$ which next
/home/nero/projects/meetingtax/fe/node_modules/.bin/next
```

## Example 4: mise Tasks for Project Automation

Using mise.toml tasks for common project operations.

```toml
# ~/workspace/repos/nero-core/mise.toml

[tools]
python = "3.12.8"

[env]
PYTHONDONTWRITEBYTECODE = "1"
PYTHONUNBUFFERED = "1"

[tasks.lint]
run = "ruff check src/"
description = "Run linter"

[tasks.format]
run = "ruff format src/"
description = "Format code"

[tasks.test]
run = "pytest tests/ -x -q"
description = "Run tests"

[tasks.test-cov]
run = "pytest tests/ --cov=nero_core --cov-report=term-missing"
description = "Run tests with coverage"

[tasks.worker]
run = "celery -A nero_core worker --loglevel=debug --concurrency=2"
description = "Start Celery worker (dev)"

[tasks.shell]
run = "python -c 'import nero_core; print(\"nero-core shell ready\")'; python"
description = "Interactive Python shell with project loaded"
```

```bash
$ mise run lint
All checks passed!

$ mise run test
5 passed in 1.2s

$ mise run worker
[2026-03-21 10:00:00] celery worker starting...
```

## Example 5: Troubleshooting Common Issues

### Issue: direnv Not Loading After Shell Start

```bash
$ cd ~/workspace/repos/nero-core
# Nothing happens - no direnv message

# Check: is direnv hooked?
$ type _direnv_hook
-bash: type: _direnv_hook: not found

# Fix: add hook to .bashrc
$ echo 'eval "$(direnv hook bash)"' >> ~/.bashrc
$ source ~/.bashrc
$ cd . # Trigger reload
direnv: loading .envrc
```

### Issue: Wrong Python Version

```bash
$ python --version
Python 3.10.12  # System Python, not mise-managed!

# Check mise
$ mise current
python  3.12.8  ~/.tool-versions

# The problem: mise shell hook not active
$ which python
/usr/bin/python  # System Python

# Fix: add mise activation before direnv in .bashrc
$ cat ~/.bashrc | grep -E "mise|direnv"
eval "$(mise activate bash)"
eval "$(direnv hook bash)"

$ source ~/.bashrc
$ python --version
Python 3.12.8  # Correct!
```

### Issue: .envrc Blocked (Untrusted)

```bash
$ cd ~/workspace/repos/nero-core
direnv: error /home/nero/workspace/repos/nero-core/.envrc is blocked. Run `direnv allow` to approve its content

# This happens after editing .envrc or cloning a new repo
$ direnv allow
direnv: loading .envrc
nero-core | Python 3.12.8 | venv: .venv
```
