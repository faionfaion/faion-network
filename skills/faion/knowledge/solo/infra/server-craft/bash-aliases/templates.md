# Bash Aliases Templates

Complete, organized ~/.bash_aliases file with 60+ aliases.

## Template 1: Complete ~/.bash_aliases

File: `~/.bash_aliases`

```bash
# ~/.bash_aliases — Organized shell aliases and functions
# Categories: System, Navigation, Files, Git, Docker, Systemd, nginx, Network, Logs, NERO

# =============================================================
# SYSTEM
# =============================================================
alias update="sudo apt update && sudo apt upgrade -y"
alias install="sudo apt install -y"
alias remove="sudo apt remove -y"
alias autoremove="sudo apt autoremove -y"
alias reboot-needed="[ -f /var/run/reboot-required ] && echo 'YES' || echo 'NO'"

# Safety
alias rm="rm -i"
alias mv="mv -i"
alias cp="cp -i"

# Info
alias meminfo="free -h"
alias cpuinfo="lscpu | head -15"
alias diskinfo="df -h | grep -v tmpfs"
alias uptime="uptime -p"
alias myip="curl -s ifconfig.me && echo"
alias weather="curl -s 'wttr.in/?format=3'"

# Processes
alias psg="ps aux | grep -v grep | grep -i"
alias psmem="ps aux --sort=-%mem | head -15"
alias pscpu="ps aux --sort=-%cpu | head -15"
alias ports="sudo ss -tlnp | column -t"
alias listening="sudo ss -tlnp"

# Quick edit
alias ea="vim ~/.bash_aliases && source ~/.bash_aliases"
alias eb="vim ~/.bashrc && source ~/.bashrc"
alias et="vim ~/.tmux.conf && tmux source ~/.tmux.conf"

# Reload
alias reload="source ~/.bashrc"
alias realias="source ~/.bash_aliases"

# =============================================================
# NAVIGATION
# =============================================================
alias ..="cd .."
alias ...="cd ../.."
alias ....="cd ../../.."
alias ~="cd ~"
alias ws="cd ~/workspace"
alias repos="cd ~/workspace/repos"
alias scripts="cd ~/workspace/scripts"

# =============================================================
# FILES (modern tools if available)
# =============================================================
if command -v eza &>/dev/null; then
    alias ls="eza --color=always --group-directories-first"
    alias ll="eza -la --color=always --group-directories-first --git"
    alias lt="eza --tree --level=2 --color=always --group-directories-first"
    alias lt3="eza --tree --level=3 --color=always --group-directories-first"
    alias la="eza -a --color=always --group-directories-first"
    alias l="eza -1 --color=always"
else
    alias ll="ls -alF --color=auto"
    alias la="ls -A --color=auto"
    alias l="ls -CF --color=auto"
fi

if command -v bat &>/dev/null; then
    alias cat="bat --paging=never"
fi

if command -v duf &>/dev/null; then
    alias df="duf --only local"
fi

if command -v dust &>/dev/null; then
    alias du="dust"
fi

if command -v btop &>/dev/null; then
    alias top="btop"
fi

alias grep="grep --color=auto"
alias diff="diff --color=auto"

# =============================================================
# GIT
# =============================================================
alias g="git"
alias gs="git status -sb"
alias gl="git log --oneline -20"
alias glg="git log --graph --oneline --decorate -20"
alias gd="git diff"
alias gds="git diff --staged"
alias ga="git add"
alias gaa="git add -A"
alias gc="git commit -m"
alias gca="git commit --amend --no-edit"
alias gco="git checkout"
alias gb="git branch -vv"
alias gp="git push"
alias gpl="git pull"
alias gf="git fetch --all --prune"
alias gst="git stash"
alias gstp="git stash pop"
alias gcp="git cherry-pick"
alias gundo="git reset --soft HEAD~1"

# =============================================================
# DOCKER
# =============================================================
alias dk="docker"
alias dk-ps="docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'"
alias dk-psa="docker ps -a --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'"
alias dk-imgs="docker images --format 'table {{.Repository}}\t{{.Tag}}\t{{.Size}}'"
alias dk-stats="docker stats --no-stream --format 'table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}'"
alias dk-logs="docker logs -f --tail 100"
alias dk-exec="docker exec -it"
alias dk-stop="docker stop"
alias dk-rm="docker rm"
alias dk-rmi="docker rmi"
alias dk-prune="docker system prune -af"
alias dk-vol="docker volume ls"

# Docker Compose
alias dc="docker compose"
alias dc-up="docker compose up -d"
alias dc-down="docker compose down"
alias dc-restart="docker compose restart"
alias dc-logs="docker compose logs -f --tail 100"
alias dc-ps="docker compose ps"
alias dc-build="docker compose build --no-cache"
alias dc-pull="docker compose pull"

# =============================================================
# SYSTEMD
# =============================================================
alias sc="systemctl"
alias scu="systemctl --user"
alias sc-status="systemctl --user status"
alias sc-start="systemctl --user start"
alias sc-stop="systemctl --user stop"
alias sc-restart="systemctl --user restart"
alias sc-enable="systemctl --user enable"
alias sc-disable="systemctl --user disable"
alias sc-list="systemctl --user list-units --type=service --state=running"
alias sc-failed="systemctl --user --failed"
alias sc-reload="systemctl --user daemon-reload"
alias sc-logs="journalctl --user -f -u"

# System-level systemd
alias scs="sudo systemctl"
alias scs-status="sudo systemctl status"
alias scs-restart="sudo systemctl restart"

# =============================================================
# NGINX
# =============================================================
alias ng="sudo nginx"
alias ng-test="sudo nginx -t"
alias ng-reload="sudo nginx -t && sudo systemctl reload nginx"
alias ng-restart="sudo systemctl restart nginx"
alias ng-status="sudo systemctl status nginx"
alias ng-sites="ls -la /etc/nginx/sites-enabled/"
alias ng-logs="sudo tail -f /var/log/nginx/access.log"
alias ng-errors="sudo tail -f /var/log/nginx/error.log"
alias ng-edit="sudo vim /etc/nginx/sites-available/"

# =============================================================
# NETWORK
# =============================================================
alias ping="ping -c 5"
alias ports="sudo ss -tlnp | column -t"
alias connections="ss -tn | awk '{print $4}' | cut -d: -f1 | sort | uniq -c | sort -rn | head -10"
alias fw="sudo ufw status numbered"
alias fw-allow="sudo ufw allow"
alias fw-deny="sudo ufw deny"
alias fw-delete="sudo ufw delete"

# =============================================================
# LOGS
# =============================================================
alias jctl="journalctl --no-pager"
alias jf="journalctl -f"
alias jfu="journalctl --user -f"
alias auth-log="sudo journalctl -u ssh --since '1 hour ago'"
alias fail2ban-log="sudo tail -50 /var/log/fail2ban.log"
alias f2b-status="sudo fail2ban-client status"

# =============================================================
# NERO PLATFORM
# =============================================================
alias nero-status="systemctl --user status nero-core nero-channel-web nero-channel-tg nero-web"
alias nero-restart="systemctl --user restart nero-core nero-channel-web nero-channel-tg nero-web"
alias nero-logs="journalctl --user -f -u 'nero-*'"
alias nero-health="curl -s http://127.0.0.1:8100/health | python3 -m json.tool"
alias nero-deploy="bash ~/workspace/deploy/deploy.sh"
alias nero-infra="cd ~/workspace/repos/nero-infra && docker compose ps"

# =============================================================
# FUNCTIONS
# =============================================================

# Create directory and cd into it
mkcd() { mkdir -p "$1" && cd "$1"; }

# Check what's using a port
port() { sudo lsof -i ":${1}" 2>/dev/null || echo "Nothing on port $1"; }

# Extract any archive
extract() {
    if [ -f "$1" ]; then
        case "$1" in
            *.tar.bz2) tar xjf "$1" ;;
            *.tar.gz)  tar xzf "$1" ;;
            *.tar.xz)  tar xJf "$1" ;;
            *.bz2)     bunzip2 "$1" ;;
            *.gz)      gunzip "$1" ;;
            *.tar)     tar xf "$1" ;;
            *.tbz2)    tar xjf "$1" ;;
            *.tgz)     tar xzf "$1" ;;
            *.zip)     unzip "$1" ;;
            *.7z)      7z x "$1" ;;
            *)         echo "Cannot extract '$1'" ;;
        esac
    else
        echo "'$1' is not a valid file"
    fi
}

# Quick HTTP server
serve() { python3 -m http.server "${1:-8080}"; }

# Show system overview
sysinfo() {
    echo "=== $(hostname) ==="
    echo "Uptime: $(uptime -p)"
    echo "Memory: $(free -h | awk '/Mem:/{print $3 "/" $2}')"
    echo "Disk:   $(df -h / | awk 'NR==2{print $3 "/" $2 " (" $5 ")"}')"
    echo "Load:   $(cat /proc/loadavg | awk '{print $1, $2, $3}')"
    echo "IPs:    $(hostname -I | tr ' ' '\n' | head -3 | tr '\n' ' ')"
}

# SSH tunnel shortcut
tunnel() {
    local port="${1:?Usage: tunnel <port> [remote_host]}"
    local host="${2:-127.0.0.1}"
    echo "Tunneling localhost:$port -> $host:$port"
    ssh -L "$port:$host:$port" nero
}
```

## Template 2: Alias Discovery Script

```bash
#!/bin/bash
# show-aliases.sh — Display all aliases grouped by category

echo "=== Bash Aliases ==="
echo ""

while IFS= read -r line; do
    if [[ "$line" =~ ^#\ ===.*===$ ]]; then
        echo ""
        echo "$line"
    elif [[ "$line" =~ ^alias\ ]]; then
        NAME=$(echo "$line" | sed 's/alias \([^=]*\)=.*/\1/')
        VALUE=$(echo "$line" | sed 's/alias [^=]*=//' | tr -d '"')
        printf "  %-20s %s\n" "$NAME" "$VALUE"
    fi
done < ~/.bash_aliases
```
