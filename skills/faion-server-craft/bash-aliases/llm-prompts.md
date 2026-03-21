# Bash Aliases LLM Prompts

Prompts for AI assistants to create, organize, and optimize bash aliases.

## Prompt 1: Alias Audit and Organization

```
Audit and organize the bash aliases on this server.

Steps:
1. Read current ~/.bash_aliases: `cat ~/.bash_aliases`
2. Read current ~/.bashrc for alias definitions: `grep "^alias" ~/.bashrc`
3. List all active aliases: run `alias` command
4. List all shell functions: `declare -F`

Analyze:
- Are aliases organized by category?
- Are there duplicate or conflicting aliases?
- Are common operations missing shortcuts?
- Are there safety aliases for rm/mv/cp?
- Are there project-specific aliases?

Provide:
1. Reorganized ~/.bash_aliases with categories
2. New aliases for common operations that are missing
3. Recommendations for removing unused aliases
4. Function aliases for multi-step operations
```

## Prompt 2: Generate Project Aliases

```
Generate bash aliases for the following project:

Project: {name}
Type: {web app / API / CLI / etc.}
Services: {list services}
Deploy method: {describe}
Log locations: {describe}
Common operations: {list things you do often}

For each operation, create:
- An alias with a clear, short name
- A comment explaining what it does
- Test command to verify it works

Group aliases by:
- Service management (start, stop, restart, status)
- Logs (view, follow, search)
- Deploy (build, deploy, rollback)
- Debug (health check, connections, errors)

Output as a block that can be appended to ~/.bash_aliases.
```

## Prompt 3: Alias Creation Helper

```
I want a bash alias/function for: {describe what you want to do}

Consider:
1. Is a simple alias sufficient, or do I need a function?
2. Does it need parameters?
3. Should it have tab completion?
4. Are there error cases to handle?
5. Should it have a confirmation prompt (destructive operation)?

Create the alias/function with:
- Clear name (short but descriptive)
- Comment explaining purpose
- Error handling if needed
- Usage example
```

## Prompt 4: Productivity Audit

```
Analyze my shell history and suggest aliases for frequently used commands.

Steps:
1. Read shell history: `history | awk '{$1=""; print $0}' | sort | uniq -c | sort -rn | head -30`
2. Identify commands used more than 5 times
3. For each frequent command:
   - Suggest an alias name
   - Show the alias definition
   - Estimate keystrokes saved per use

Output as a table:
| Frequency | Command | Suggested Alias | Keystrokes Saved |
|-----------|---------|-----------------|-----------------|

Then output the alias definitions ready to add to ~/.bash_aliases.
```

## Prompt 5: Docker Alias Set

```
Create a comprehensive set of Docker aliases for daily container management.

Include aliases for:
1. Container management (ps, start, stop, restart, rm, exec)
2. Image management (ls, pull, rm, prune)
3. Docker Compose (up, down, restart, logs, ps, build)
4. Monitoring (stats, logs, inspect)
5. Cleanup (prune, remove unused)
6. Networking (list networks, inspect)
7. Volumes (list, inspect, prune)

Naming convention: dk-{action} for docker, dc-{action} for compose

Format each alias with:
- The alias definition
- A short comment
- What it replaces

Also create helper functions:
- dk-shell: exec into container with bash/sh
- dk-ip: get container IP address
- dk-env: show container environment variables
```

## Prompt 6: Systemd Alias Set

```
Create bash aliases for systemd service management, tailored for a server running:
- User services (systemctl --user): {list services}
- System services (sudo systemctl): nginx, ssh, fail2ban, docker

Include:
1. User service management (start, stop, restart, status, enable, disable)
2. System service management (with sudo)
3. Log viewing (journalctl shortcuts)
4. Unit file editing (systemctl edit)
5. Status overview (list running, list failed)
6. Timer management (list-timers)

Naming convention: sc-{action} for user, scs-{action} for system

Include a function that shows status of all project services at once.
```

## Prompt 7: Safety and Confirmation Aliases

```
Create safety aliases and functions that prevent accidental damage.

Include:
1. rm with confirmation: `rm -i`
2. mv with confirmation: `mv -i`
3. cp with confirmation: `cp -i`
4. Trash function: move to trash instead of delete
5. Safe deploy: require confirmation before deploying to production
6. Safe restart: show service status before and after restart
7. Database backup before destructive operations

For each safety alias:
- Show the alias definition
- Explain what danger it prevents
- Show how to bypass it when needed (backslash prefix)
```

## Prompt 8: Migration Between Machines

```
Export my bash aliases to another machine.

Steps:
1. Read current ~/.bash_aliases
2. Check which aliases depend on installed tools:
   - Docker aliases (need docker)
   - eza aliases (need eza)
   - bat aliases (need bat)
   - Project-specific aliases (need project files)

3. Create two versions:
   A. Universal aliases (work everywhere)
   B. Full aliases (with tool-specific ones wrapped in `command -v` checks)

4. Create an install script:
   - Back up existing ~/.bash_aliases on target
   - Copy new aliases
   - Source them
   - Report which aliases need additional tool installation

Output:
- The universal ~/.bash_aliases
- The install script
- List of tools to install for full functionality
```
