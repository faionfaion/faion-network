# direnv + mise LLM Prompts

## Version Management Setup

```
Set up mise + direnv for my multi-project server.

Server: Ubuntu 24.04
Projects:
[LIST WITH RUNTIME REQUIREMENTS, e.g.:
- ~/workspace/repos/nero-core/: Python 3.12
- ~/workspace/repos/nero-web/: Node 22
- ~/projects/meetingtax/be/: Python 3.11
- ~/projects/meetingtax/fe/: Node 22
]

Requirements:
- Automatic version switching when entering project directories
- Automatic virtualenv activation for Python projects
- .env loading for secrets
- No conflict between projects

Provide:
1. mise installation and configuration
2. direnv installation and configuration
3. ~/.bashrc integration (correct order)
4. .tool-versions or mise.toml for each project
5. .envrc for each project
6. .gitignore additions
7. Verification steps
```

## Environment Troubleshooting

```
Help me troubleshoot my direnv/mise setup.

Problem: [DESCRIBE, e.g., "wrong Python version in project dir", "venv not activating", "env vars not loading"]

Current setup:
- ~/.bashrc contains: [show relevant lines]
- Project .envrc: [show content]
- Project .tool-versions: [show content]
- `mise current` output: [show output]
- `direnv status` output: [show output]
- `which python` output: [show path]
- `python --version` output: [show version]

Error messages (if any):
[PASTE ERRORS]

Please:
1. Diagnose the root cause
2. Provide step-by-step fix
3. Verification commands to confirm it's working
4. Common pitfalls to check for this type of issue
```

## Per-Project Environment Design

```
Design the .envrc and mise.toml for my project.

Project type: [e.g., "Python FastAPI backend with PostgreSQL and Redis"]
Project directory: [PATH]
Python version needed: [VERSION]
Node version needed: [VERSION or "none"]

Requirements:
- Auto-activate virtualenv when entering directory
- Load .env for database and API credentials
- Set Python-specific environment variables
- Add project scripts to PATH
- Reload when requirements.txt or pyproject.toml changes
- Print status message showing active runtime versions

Provide:
1. Complete .envrc file with comments
2. .tool-versions or mise.toml
3. mise.toml with useful task definitions (lint, test, format, dev server)
4. .gitignore additions
5. How to set up for the first time (commands to run)
```

## Migrate from pyenv/nvm to mise

```
Help me migrate from pyenv + nvm to mise.

Current setup:
- pyenv manages Python versions (installed versions: [LIST])
- nvm manages Node.js versions (installed versions: [LIST])
- Each project has .python-version or .node-version files

Target:
- Single tool (mise) managing all runtimes
- Compatible with direnv for environment activation
- Minimal disruption to existing projects

Provide:
1. mise installation
2. Install existing versions via mise
3. Convert .python-version to .tool-versions
4. Convert .node-version to .tool-versions
5. Update .bashrc (remove pyenv/nvm, add mise)
6. Remove pyenv and nvm safely
7. Verification for each project
```

## direnv for Monorepo

```
Set up direnv for a monorepo or workspace with multiple sub-projects.

Structure:
[DESCRIBE DIRECTORY LAYOUT, e.g.:
~/workspace/
├── .env (master secrets)
├── repos/
│   ├── nero-sdk/ (Python library)
│   ├── nero-core/ (Python + Celery)
│   ├── nero-channel-web/ (Python + FastAPI)
│   └── nero-web/ (Node + React)
]

Requirements:
- Master .env loaded at workspace level
- Each sub-project gets its own virtualenv
- Each sub-project can have different Python/Node version
- Entering a sub-project automatically activates its environment
- Exiting a sub-project deactivates everything

Provide:
1. Workspace-level .envrc
2. Per-project .envrc (for each sub-project type)
3. How direnv inheritance works (source_env)
4. Avoiding conflicts between parent and child .envrc
5. Security considerations
```

## mise Tasks Configuration

```
Create mise.toml with useful development tasks for my Python project.

Project: [NAME]
Tools: [e.g., "ruff for linting, pytest for testing, alembic for migrations"]
Framework: [e.g., "FastAPI with uvicorn"]

I want tasks for:
1. lint - run linter
2. format - format code
3. test - run tests
4. test-cov - run tests with coverage
5. dev - start development server
6. migrate - run database migrations
7. shell - interactive Python shell with project loaded
8. clean - remove __pycache__, .pyc, etc.

Provide a complete mise.toml with all tasks, environment variables, and tool versions.
Show how to run tasks: `mise run <task>`.
```
