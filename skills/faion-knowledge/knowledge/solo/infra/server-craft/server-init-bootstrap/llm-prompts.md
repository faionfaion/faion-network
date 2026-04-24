# Server Init Bootstrap LLM Prompts

## Bootstrap New Server

```
I need to bootstrap a new Ubuntu 24.04 VPS from scratch.

Server details:
- Provider: [Hetzner/DigitalOcean/Linode/Vultr]
- Specs: [CPUs, RAM, Disk]
- IP: [SERVER_IP]
- Access: root SSH with [password/key]
- Purpose: [DESCRIBE: e.g., "AI agent platform, multiple Python services"]

I need to:
1. Create non-root user with SSH key access
2. Harden SSH (disable root, password auth)
3. Set up firewall (UFW)
4. Install essential packages
5. Configure swap
6. Set up systemd user services
7. Install Docker
8. Set hostname and timezone

Please provide:
- Complete step-by-step commands
- A bootstrap.sh script I can run in one go
- Verification commands after each phase
- What to do if something goes wrong (recovery steps)

Important: Emphasize testing SSH access as the new user BEFORE disabling root login.
```

## Cloud-Init Configuration

```
Create a cloud-init.yml for automated server provisioning.

Provider: [Hetzner Cloud / DigitalOcean / etc.]
Target OS: Ubuntu 24.04 LTS

User: [USERNAME]
SSH public key: [KEY or "I'll add it"]
Hostname: [HOSTNAME]
Timezone: [TIMEZONE]

Packages to install:
[LIST or "standard development packages for Python/Node"]

Additional setup:
- Firewall (UFW) with ports [22, 80, 443, plus any others]
- Fail2ban for SSH protection
- Swap: [SIZE, e.g., 4GB]
- Docker: [yes/no]
- systemd linger for user services

Provide:
1. Complete cloud-init.yml
2. How to paste it into the provider's console
3. How to verify it ran successfully after server boots
4. What to do manually after cloud-init (if anything)
```

## Initial Hardening

```
Review and harden my Ubuntu 24.04 server security.

Current state:
- Fresh install, root access via SSH key
- User [USERNAME] created with sudo
- UFW: [enabled/not enabled]
- Fail2ban: [installed/not installed]
- SSH config: [paste relevant lines or "default"]

Please audit and fix:
1. SSH configuration (/etc/ssh/sshd_config)
   - Disable root login
   - Disable password authentication
   - Set max auth tries
   - Configure allowed users
2. Firewall rules (only needed ports open)
3. Fail2ban configuration for SSH
4. Automatic security updates (unattended-upgrades)
5. File permissions audit (sensitive files)
6. Remove unnecessary packages
7. Disable unnecessary services
8. Kernel hardening (sysctl)

Provide:
- Current risk assessment
- Exact commands for each fix
- Verification after applying changes
- Monthly security maintenance checklist
```

## Package Selection

```
Recommend essential packages to install on my new Ubuntu 24.04 server.

Purpose: [DESCRIBE, e.g., "Development server for Python web services and AI agents"]

Categories I need:
1. Build tools and compilers
2. Network utilities
3. Monitoring and debugging
4. Text processing
5. File management
6. Python development
7. Node.js development (if applicable)
8. Docker (if applicable)
9. Security tools
10. Shell productivity

For each package:
- Name and one-line description
- Why it's needed
- apt install command

Group by priority:
- Essential (install immediately)
- Recommended (install when needed)
- Optional (nice to have)

Format as a single apt install command for essentials.
```

## Post-Bootstrap Verification

```
Create a verification script for my bootstrapped Ubuntu 24.04 server.

The script should check:
1. User configuration
   - Non-root user exists and has sudo
   - SSH key authentication works
   - Password authentication is disabled
2. System configuration
   - Hostname is set
   - Timezone is correct
   - Locale is UTF-8
   - NTP is syncing
3. Security
   - UFW is active with correct rules
   - Fail2ban is running
   - Root SSH login is disabled
   - Unattended upgrades configured
4. Resources
   - Swap is active and correct size
   - Swappiness is tuned
   - Open file limits are increased
5. Services
   - systemd linger is enabled
   - Docker is running (if installed)
   - All expected services are active
6. Packages
   - All essential packages installed

Output format: [PASS]/[FAIL] for each check, summary at end.
Script should be idempotent and safe to run multiple times.
```

## Server Migration Plan

```
Help me plan migrating from my current server to a new one.

Current server:
- [PROVIDER, SPECS]
- Services running: [LIST]
- Data: [Databases, file storage]
- Domains: [LIST with DNS provider]

New server:
- [PROVIDER, SPECS]
- Same OS: Ubuntu 24.04

I need a migration plan covering:
1. Pre-migration checklist
2. What to back up (databases, configs, .env, SSL certs)
3. Bootstrap the new server
4. Restore data (PostgreSQL dump/restore, Redis dump)
5. Deploy application code
6. DNS cutover strategy (minimize downtime)
7. Post-migration verification
8. Rollback plan (if new server has issues)

Constraints:
- Minimal downtime (< 30 minutes ideal)
- Must preserve database data
- Must maintain SSL certificates
- [Any other constraints]
```
