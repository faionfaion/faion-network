# Git Server Workflow LLM Prompts

## Setup

### Prompt: Design Git-Based Deploy Workflow

```
Design a git-based deployment workflow for my VPS platform.

Platform:
- Server: [OS, specs]
- Services: [list with languages/frameworks]
- Shared libraries: [if any]
- Database: [if migrations needed]

Current state:
- Code is in: [GitHub / local only]
- Currently deploying by: [manual copy / no process / etc.]
- Services managed by: [systemd / Docker / supervisor]

Requirements:
- Workspace/runtime separation: [Yes/No]
- Automated deploy on push: [Yes/No]
- Rollback capability: [Yes/No]
- Multi-repo coordination: [Yes/No]
- Database migrations: [Yes/No]
- Build step needed: [for which services]

Provide:
1. Directory structure (workspace + runtime)
2. Complete deploy.sh script
3. Deploy order for multi-repo platforms
4. Rollback procedure and script
5. How to handle dependency changes
6. How to handle database migrations
7. Verification steps after deploy
```

### Prompt: Create Deploy Script

```
Create a deploy script for my application.

Application details:
- Name: [service name]
- Language: [Python/Node.js/Go/etc.]
- Source location: [workspace path]
- Runtime location: [runtime path]
- Virtual env / package manager: [pip/npm/go mod]
- Service manager: [systemd user / system / Docker]
- Build step: [none / npm run build / go build / etc.]
- Database migration: [alembic / prisma / none]
- Shared dependencies: [SDK / shared library path]

Deploy steps:
1. Sync source code (rsync)
2. Install dependencies (if changed)
3. Run build (if needed)
4. Run migrations (if needed)
5. Restart service
6. Verify

The script should:
- Accept service name as argument
- Support "all" for deploying everything
- Support --rebuild-venv for full dependency rebuild
- Handle errors gracefully
- Log deployment
- Return non-zero on failure
```

## Troubleshooting

### Prompt: Debug Failed Deployment

```
My deployment failed. Help me diagnose.

Deploy command: [what was run]
Deploy script output:
[paste output]

Service status after deploy:
[paste systemctl status output]

Service logs after deploy:
[paste journalctl output]

Recent changes:
- Code changes: [describe what changed]
- Dependency changes: [any requirements.txt / package.json changes]
- Config changes: [any .env or config changes]

Previous deployment: [was the last deploy successful?]

Diagnose:
1. Did rsync succeed?
2. Did dependency installation succeed?
3. Did the service start?
4. Is it an import error, config error, or runtime error?
5. Provide specific fix
```

### Prompt: Fix Broken Deploy Workflow

```
My deploy workflow has issues. Help me fix it.

Current deploy approach:
[describe how you currently deploy]

Problems:
- [e.g., "Old code sometimes runs after deploy"]
- [e.g., "Venv gets corrupted after updates"]
- [e.g., "Can't rollback quickly"]
- [e.g., "Deploy takes too long"]

Current deploy script (if any):
[paste script]

Service configuration:
[paste systemd unit file]

Directory structure:
[describe current layout]

Help me:
1. Identify root causes of each problem
2. Redesign the deploy workflow
3. Write a better deploy script
4. Set up proper rollback
5. Add verification steps
```

## Advanced Patterns

### Prompt: Setup Multi-Repo Deploy

```
I have multiple repos that depend on each other. Help me set up coordinated deployment.

Repositories:
[For each repo:]
- Name: [repo name]
- Language: [Python/Node/etc.]
- Depends on: [other repos]
- Deploy artifacts: [source / built binary / static files]

Dependency graph:
[describe which repos depend on which]

Deployment requirements:
- Deploy order must respect dependencies
- SDK/library changes should trigger dependent redeployment
- Each service can be deployed independently
- "deploy all" should work in the right order
- Rollback should be possible per-service

Provide:
1. Deploy order determination (topological sort)
2. Master deploy script with "all" support
3. How to handle SDK changes propagation
4. Rollback considerations for multi-repo
5. Testing strategy after multi-repo deploy
```

### Prompt: Setup Push-to-Deploy

```
I want to set up automatic deployment when I push to the main branch.

Current setup:
- Code repos: [on GitHub / local]
- Server: [address]
- Deploy script: [path, or describe what it does]
- Services: [list]

Options I'm considering:
1. Git bare repo + post-receive hook
2. GitHub webhook
3. Cron-based pull + deploy

For my setup, recommend the best approach and provide:
1. Complete setup instructions
2. Hook/webhook script
3. Error handling and logging
4. How to deploy only on main branch pushes
5. How to handle deploy failures (notification, rollback)
6. Security considerations
```

### Prompt: Design Rollback Strategy

```
I need a reliable rollback strategy for my platform.

Current deploy method:
[describe]

Services:
[list with their data stores]

Database migration tool: [alembic / prisma / none]

Rollback scenarios:
1. Bad code change (need to revert to previous commit)
2. Bad migration (need to revert database schema)
3. Bad dependency update (need old requirements)
4. Full platform rollback (multiple services)

Provide:
1. Rollback script for code changes
2. Database rollback procedure
3. Dependency rollback approach
4. Multi-service coordinated rollback
5. How to verify rollback was successful
6. Prevention: pre-deploy checks to avoid needing rollbacks
```
