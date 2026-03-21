# systemd User Services LLM Prompts

## Service Creation

### Prompt: Create a systemd User Service

```
Create a systemd user service unit file for the following application.

Application details:
- Name: [e.g., myapp-api]
- Type: [Python/Node.js/Go/Rust/Shell script]
- Command: [e.g., uvicorn main:app --port 8000]
- Working directory: [e.g., /srv/myapp/api]
- Virtual env: [path if Python, e.g., /srv/myapp/api/.venv]
- Environment file: [e.g., /home/user/workspace/.env]
- Port: [if listening, e.g., 8000]
- User: [e.g., nero]

Requirements:
- Auto-restart on failure: [Yes/No]
- Start on boot: [Yes/No]
- Memory limit: [e.g., 512M]
- CPU limit: [e.g., 200%]
- Dependencies: [other services it needs, e.g., network, database]

Provide:
1. Complete .service unit file
2. Installation commands (copy, daemon-reload, enable, start)
3. Verification commands
4. Log viewing commands
```

### Prompt: Convert Docker Service to systemd

```
I want to run an application as a systemd user service instead of in Docker.

Current Docker setup:
[paste docker-compose service definition or docker run command]

Application:
- Language: [e.g., Python 3.12]
- Dependencies: [e.g., PostgreSQL, Redis]
- Environment variables: [list key ones]
- Volumes/mounts needed: [list]

Provide:
1. Steps to set up the application outside Docker
2. Virtual environment / runtime setup
3. Complete systemd unit file
4. Environment file template
5. Migration steps (move data if needed)
6. Verification that it works the same as Docker version
```

## Debugging

### Prompt: Debug Failing Service

```
My systemd user service is failing. Help me diagnose.

Service name: [name]
Service file: [paste unit file contents]

`systemctl --user status name` output:
[paste output]

`journalctl --user -u name --since "10 min ago"` output:
[paste relevant log lines]

Symptoms:
- Service status: [activating, failed, inactive]
- Exit code: [if shown]
- How often it restarts: [immediately, after RestartSec, reaches limit]
- When it started failing: [always, after update, after reboot]

Diagnose:
1. Parse the exit code and error messages
2. Check unit file for configuration issues
3. Verify paths and permissions
4. Check environment variable loading
5. Suggest specific fixes
```

### Prompt: Service Stops After Logout

```
My systemd user services stop when I disconnect from SSH.

Setup:
- OS: [e.g., Ubuntu 24.04]
- User: [username]
- Service files location: ~/.config/systemd/user/
- Linger status: [loginctl show-user output]
- Services: [list services]

`loginctl show-user $USER` output:
[paste]

`systemctl --user status` output:
[paste]

When I SSH in, services work. When I disconnect, they stop.

Diagnose and fix this issue.
```

### Prompt: Service Restart Loop

```
My service is stuck in a restart loop and has been rate-limited.

Service: [name]
Error from status: "Start request repeated too quickly"
or "start-limit-hit"

Service file:
[paste unit file]

Recent logs:
[paste journalctl output showing the failures]

Help me:
1. Understand why the service keeps crashing
2. Reset the failure counter
3. Fix the root cause
4. Set appropriate StartLimitBurst/StartLimitIntervalSec values
```

## Resource Management

### Prompt: Tune Service Resource Limits

```
Help me set appropriate resource limits for my services.

Server specs:
- CPU: [e.g., 16 cores]
- RAM: [e.g., 30GB]
- OS: [e.g., Ubuntu 24.04]

Services running:
[For each service, list:]
- Name: [name]
- Type: [web server, worker, bot, etc.]
- Current memory usage: [from `systemctl --user status` or `ps aux`]
- Expected peak memory: [estimate]
- CPU pattern: [steady / bursty / CPU-intensive]
- Concurrency: [workers, threads, connections]

Other processes on server:
- Docker containers: [list with resource usage]
- System services: [any notable ones]

Provide recommended limits for each service:
1. MemoryMax and MemoryHigh
2. CPUQuota (if needed)
3. TasksMax
4. LimitNOFILE
5. Total resource allocation vs server capacity
6. OOM priority considerations
```

### Prompt: Investigate OOM Kill

```
My service was OOM-killed by systemd. Help me investigate.

Service: [name]
Service file: [paste, especially MemoryMax setting]

`journalctl --user -u name` relevant output:
[paste OOM-related log entries]

`dmesg | grep -i oom` output:
[paste if available]

Application details:
- What it does: [e.g., Celery worker processing LLM API calls]
- Concurrency: [e.g., 20 gevent workers]
- Each task uses approximately: [memory estimate]

Help me:
1. Confirm it was MemoryMax enforcement vs kernel OOM
2. Analyze if the limit is too low or if the app has a memory leak
3. Recommend appropriate MemoryMax/MemoryHigh values
4. Suggest application-level memory optimization if needed
```

## Advanced Patterns

### Prompt: Service Dependency Design

```
I have multiple services that depend on each other. Help me design the systemd dependency graph.

Services:
[For each service:]
- Name: [name]
- Depends on: [what must be running]
- Provides: [what others depend on]
- Start order: [when relative to others]

Infrastructure dependencies:
- Docker containers: [PostgreSQL, Redis, RabbitMQ, etc.]
- Network: [need internet for API calls?]

Design:
1. After/Wants/Requires directives for each service
2. Whether to use a target unit to group services
3. Start ordering diagram
4. Failure propagation behavior
5. Group restart capability
```

### Prompt: Create systemd Timer

```
I want to replace a cron job with a systemd timer.

Current cron entry:
[paste crontab line]

Or describe the schedule:
- Frequency: [e.g., every day at 3 AM, every 15 minutes]
- Script to run: [path]
- Environment needed: [env file path]
- Expected duration: [how long the job runs]
- On failure: [ignore, retry, alert]

Provide:
1. Timer unit file (.timer)
2. Service unit file (.service)
3. Installation and activation commands
4. How to check next run time
5. How to manually trigger
6. How to view run history and results
```

### Prompt: Migrate from System to User Services

```
I want to migrate system-level services to user-level services.

Current system services:
[list services in /etc/systemd/system/]

User: [username]
Application paths: [where the apps live]

Reasons for migration:
- Don't need root privileges
- Want user-level control without sudo
- Simplify deployment

Provide:
1. Step-by-step migration plan (zero-downtime if possible)
2. Modified unit files for user scope
3. Linger setup
4. Permission adjustments
5. Deploy script updates
6. Monitoring adjustments
7. Rollback plan
```
