# Bash Aliases Examples

Real-world alias usage examples from the NERO AI platform server.

## Example 1: NERO Platform Daily Operations

### Quick Status Check

```bash
# Instead of: systemctl --user status nero-core nero-channel-web nero-channel-tg nero-web
$ nero-status
# Shows status of all 4 NERO services in one command

# Instead of: curl -s http://127.0.0.1:8100/health | python3 -m json.tool
$ nero-health
{
    "status": "healthy",
    "uptime": "45678 seconds"
}

# Instead of: journalctl --user -f -u 'nero-*'
$ nero-logs
# Follow all NERO service logs
```

### Quick Deploy

```bash
# Instead of: bash ~/workspace/deploy/deploy.sh nero-core
$ nero-deploy nero-core

# Instead of: bash ~/workspace/deploy/deploy.sh all
$ nero-deploy all

# Instead of: bash ~/workspace/deploy/deploy.sh all --rebuild-venv
$ nero-deploy all --rebuild-venv
```

## Example 2: Docker Management

### Quick Container Status

```bash
# Instead of: docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
$ dk-ps
NAMES           STATUS          PORTS
nero-postgres   Up 3 days       127.0.0.1:5432->5432/tcp
nero-redis      Up 3 days       127.0.0.1:6379->6379/tcp
nero-rabbitmq   Up 3 days       127.0.0.1:5672->5672/tcp, 127.0.0.1:15672->15672/tcp
nero-flower     Up 3 days       127.0.0.1:5555->5555/tcp

# Instead of: docker stats --no-stream --format 'table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}'
$ dk-stats
NAME            CPU %   MEM USAGE / LIMIT
nero-postgres   0.05%   125MiB / 29.4GiB
nero-redis      0.10%   12MiB / 29.4GiB
nero-rabbitmq   0.30%   180MiB / 29.4GiB
nero-flower     0.02%   45MiB / 29.4GiB
```

### Docker Compose Shortcuts

```bash
# Navigate + manage infrastructure
$ cd ~/workspace/repos/nero-infra

# Instead of: docker compose up -d
$ dc-up

# Instead of: docker compose logs -f --tail 100
$ dc-logs

# Instead of: docker compose ps
$ dc-ps

# Instead of: docker compose down && docker compose up -d
$ dc-down && dc-up
```

## Example 3: Git Workflow

### Quick Status and Log

```bash
# Instead of: git status -sb
$ gs
## main...origin/main
 M src/nero_core/worker.py
?? tests/test_new_feature.py

# Instead of: git log --oneline -20
$ gl
a1b2c3d fix: handle connection timeout
d4e5f6g feat: add message retry logic
g7h8i9j refactor: extract message parser

# Instead of: git log --graph --oneline --decorate -20
$ glg
* a1b2c3d (HEAD -> main) fix: handle connection timeout
* d4e5f6g feat: add message retry logic
| * x1y2z3a (feature/retry) WIP: retry mechanism
|/
* g7h8i9j refactor: extract message parser
```

### Common Git Operations

```bash
# Stage all + commit
$ gaa && gc "fix: handle edge case in parser"

# Quick diff
$ gd          # unstaged changes
$ gds         # staged changes

# Undo last commit (keep changes)
$ gundo

# Fetch all remotes, prune deleted branches
$ gf
```

## Example 4: System Administration

### Port and Connection Analysis

```bash
# Instead of: sudo ss -tlnp | column -t
$ ports
State   Recv-Q  Send-Q  Local   Address:Port  Peer  Address:Port  Process
LISTEN  0       4096    127.0.0.1:5432   0.0.0.0:*     users:(("docker-proxy"))
LISTEN  0       4096    127.0.0.1:6379   0.0.0.0:*     users:(("docker-proxy"))
LISTEN  0       128     127.0.0.1:8100   0.0.0.0:*     users:(("python3"))
LISTEN  0       128     0.0.0.0:2222     0.0.0.0:*     users:(("sshd"))
LISTEN  0       511     0.0.0.0:80       0.0.0.0:*     users:(("nginx"))
LISTEN  0       511     0.0.0.0:443      0.0.0.0:*     users:(("nginx"))

# Instead of: sudo lsof -i :8100
$ port 8100
COMMAND  PID USER FD  TYPE DEVICE SIZE/OFF NODE NAME
python3  1234 nero 5u  IPv4 12345  0t0      TCP 127.0.0.1:8100 (LISTEN)
```

### System Overview

```bash
# Custom function: system info at a glance
$ sysinfo
=== nero-hetzner ===
Uptime: up 45 days, 3 hours
Memory: 8.2Gi/29Gi
Disk:   63G/150G (42%)
Load:   0.15 0.10 0.08
IPs:    168.119.x.x 2a01:xxxx::1
```

## Example 5: nginx Management

```bash
# Quick test + reload (safe)
$ ng-reload
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful

# List active sites
$ ng-sites
lrwxrwxrwx 1 root root 43 Mar 15 nero.faion.net -> /etc/nginx/sites-available/nero.faion.net
lrwxrwxrwx 1 root root 42 Mar 10 meetingtax.io -> /etc/nginx/sites-available/meetingtax.io
lrwxrwxrwx 1 root root 42 Mar 10 eulaguard.com -> /etc/nginx/sites-available/eulaguard.com

# Follow error logs
$ ng-errors
```

## Example 6: Log Analysis

```bash
# Follow user service logs
$ sc-logs nero-core
# Shows: journalctl --user -f -u nero-core

# Check SSH auth attempts
$ auth-log
# Shows last hour of SSH events

# fail2ban quick status
$ f2b-status
Status
|- Number of jail:      4
`- Jail list:   nginx-botsearch, nginx-limit-req, recidive, sshd
```

## Example 7: Function Aliases in Action

### mkcd (Create and Enter Directory)

```bash
$ mkcd ~/projects/new-experiment
# Creates ~/projects/new-experiment/ and cd's into it
$ pwd
/home/nero/projects/new-experiment
```

### extract (Universal Archive Extraction)

```bash
$ extract backup.tar.gz
# Automatically detects format and extracts

$ extract archive.zip
# Works with zip too

$ extract data.tar.xz
# And xz, bz2, 7z...
```

### serve (Quick HTTP Server)

```bash
# Serve current directory on port 8080
$ serve
Serving HTTP on 0.0.0.0 port 8080 ...

# Serve on custom port
$ serve 9000
Serving HTTP on 0.0.0.0 port 9000 ...
```

## Example 8: Alias Discovery

```bash
# Find all Docker-related aliases
$ alias | grep dk
alias dk='docker'
alias dk-exec='docker exec -it'
alias dk-imgs='docker images --format ...'
alias dk-logs='docker logs -f --tail 100'
alias dk-ps='docker ps --format ...'
alias dk-psa='docker ps -a --format ...'
alias dk-prune='docker system prune -af'
alias dk-rm='docker rm'
alias dk-rmi='docker rmi'
alias dk-stats='docker stats --no-stream --format ...'
alias dk-stop='docker stop'
alias dk-vol='docker volume ls'

# Find all NERO-related aliases
$ alias | grep nero
alias nero-deploy='bash ~/workspace/deploy/deploy.sh'
alias nero-health='curl -s http://127.0.0.1:8100/health | python3 -m json.tool'
alias nero-infra='cd ~/workspace/repos/nero-infra && docker compose ps'
alias nero-logs='journalctl --user -f -u nero-*'
alias nero-restart='systemctl --user restart nero-core nero-channel-web nero-channel-tg nero-web'
alias nero-status='systemctl --user status nero-core nero-channel-web nero-channel-tg nero-web'

# Count total aliases and functions
$ grep -c "^alias\|^[a-z_-]*() {" ~/.bash_aliases
68
```
