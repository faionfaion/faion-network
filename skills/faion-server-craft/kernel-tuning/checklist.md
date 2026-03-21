# Kernel Tuning Checklist

Step-by-step checklist for tuning kernel parameters on Ubuntu 24.04 for web server + AI agent workload.

## Prerequisites

- [ ] Root or sudo access
- [ ] Know your RAM size: `free -h | awk '/Mem:/{print $2}'`
- [ ] Know your workload type (web server, AI agents, Docker, databases)
- [ ] Backup existing sysctl configs

## Phase 1: Audit Current State

- [ ] **Check current TCP congestion control**
  ```bash
  sysctl net.ipv4.tcp_congestion_control
  sysctl net.core.default_qdisc
  ```

- [ ] **Check current inotify limits**
  ```bash
  sysctl fs.inotify.max_user_watches
  sysctl fs.inotify.max_user_instances
  ```

- [ ] **Check current memory settings**
  ```bash
  sysctl vm.swappiness
  sysctl vm.dirty_ratio
  sysctl vm.dirty_background_ratio
  sysctl vm.max_map_count
  ```

- [ ] **Check current security settings**
  ```bash
  sysctl kernel.kptr_restrict
  sysctl kernel.yama.ptrace_scope
  sysctl kernel.randomize_va_space
  ```

- [ ] **Check file descriptor limits**
  ```bash
  sysctl fs.file-max
  ulimit -n
  cat /proc/sys/fs/file-nr
  ```

- [ ] **Check existing sysctl.d files**
  ```bash
  ls -la /etc/sysctl.d/
  ```

## Phase 2: Network Performance

- [ ] **Enable TCP BBR**
  ```bash
  sudo tee /etc/sysctl.d/60-network-perf.conf << 'EOF'
  # TCP BBR congestion control
  net.core.default_qdisc = fq
  net.ipv4.tcp_congestion_control = bbr

  # TCP buffer sizes (optimized for 30GB RAM)
  net.core.rmem_max = 16777216
  net.core.wmem_max = 16777216
  net.ipv4.tcp_rmem = 4096 87380 16777216
  net.ipv4.tcp_wmem = 4096 65536 16777216

  # Connection handling
  net.core.somaxconn = 65535
  net.core.netdev_max_backlog = 5000
  net.ipv4.tcp_max_syn_backlog = 65535

  # TCP keepalive (detect dead connections faster)
  net.ipv4.tcp_keepalive_time = 600
  net.ipv4.tcp_keepalive_intvl = 60
  net.ipv4.tcp_keepalive_probes = 5

  # TCP fastopen (client + server)
  net.ipv4.tcp_fastopen = 3

  # Reuse TIME_WAIT sockets
  net.ipv4.tcp_tw_reuse = 1

  # Increase local port range
  net.ipv4.ip_local_port_range = 1024 65535
  EOF
  ```
  Verify: `sudo sysctl -p /etc/sysctl.d/60-network-perf.conf`

- [ ] **Verify BBR is active**
  ```bash
  sysctl net.ipv4.tcp_congestion_control
  # Should show: bbr
  ```

## Phase 3: AI Agent Tuning

- [ ] **Increase inotify limits**
  ```bash
  sudo tee /etc/sysctl.d/60-agent-tuning.conf << 'EOF'
  # inotify watches — high for Claude Code / file watchers
  fs.inotify.max_user_watches = 524288
  fs.inotify.max_user_instances = 1024
  fs.inotify.max_queued_events = 32768

  # File descriptors — high for many concurrent files
  fs.file-max = 2097152

  # Process limits
  kernel.pid_max = 131072
  kernel.threads-max = 131072
  EOF
  ```
  Verify: `sudo sysctl -p /etc/sysctl.d/60-agent-tuning.conf`

- [ ] **Set per-user file descriptor limits**
  ```bash
  sudo tee /etc/security/limits.d/99-nero.conf << 'EOF'
  nero  soft  nofile  65535
  nero  hard  nofile  65535
  nero  soft  nproc   65535
  nero  hard  nproc   65535
  EOF
  ```
  Verify (after re-login): `ulimit -n`

## Phase 4: Memory Management

- [ ] **Tune memory parameters**
  ```bash
  sudo tee /etc/sysctl.d/60-memory.conf << 'EOF'
  # Swap behavior — prefer RAM, swap only under pressure
  vm.swappiness = 10

  # Dirty page writeback
  vm.dirty_ratio = 15
  vm.dirty_background_ratio = 5

  # Cache pressure — keep inode/dentry caches longer
  vm.vfs_cache_pressure = 50

  # Max memory map areas (needed by many apps)
  vm.max_map_count = 1048576

  # Minimum free memory (kB) — keep 256MB free for emergencies
  vm.min_free_kbytes = 262144

  # Overcommit — heuristic mode (default, safest)
  vm.overcommit_memory = 0
  EOF
  ```
  Verify: `sudo sysctl -p /etc/sysctl.d/60-memory.conf`

## Phase 5: Security Hardening

- [ ] **Apply security kernel parameters**
  ```bash
  sudo tee /etc/sysctl.d/60-security.conf << 'EOF'
  # Hide kernel addresses from non-root
  kernel.kptr_restrict = 1

  # Restrict dmesg to root
  kernel.dmesg_restrict = 1

  # PTRACE — only direct children
  kernel.yama.ptrace_scope = 1

  # Full ASLR
  kernel.randomize_va_space = 2

  # SysRq — limited to sync + remount + reboot
  kernel.sysrq = 176

  # SYN flood protection
  net.ipv4.tcp_syncookies = 1

  # ICMP hardening
  net.ipv4.conf.all.accept_redirects = 0
  net.ipv4.conf.default.accept_redirects = 0
  net.ipv4.conf.all.send_redirects = 0
  net.ipv6.conf.all.accept_redirects = 0
  net.ipv6.conf.default.accept_redirects = 0

  # Log martian packets
  net.ipv4.conf.all.log_martians = 1

  # Source address validation
  net.ipv4.conf.all.rp_filter = 2
  net.ipv4.conf.default.rp_filter = 2

  # Ignore ICMP broadcasts
  net.ipv4.icmp_echo_ignore_broadcasts = 1
  net.ipv4.icmp_ignore_bogus_error_responses = 1

  # Protect zero page
  vm.mmap_min_addr = 65536
  EOF
  ```
  Verify: `sudo sysctl -p /etc/sysctl.d/60-security.conf`

## Phase 6: Apply and Verify

- [ ] **Apply all settings**
  ```bash
  sudo sysctl --system
  ```

- [ ] **Verify critical settings**
  ```bash
  echo "=== Network ==="
  sysctl net.ipv4.tcp_congestion_control net.core.default_qdisc
  echo ""
  echo "=== inotify ==="
  sysctl fs.inotify.max_user_watches fs.inotify.max_user_instances
  echo ""
  echo "=== Memory ==="
  sysctl vm.swappiness vm.dirty_ratio vm.max_map_count
  echo ""
  echo "=== Security ==="
  sysctl kernel.kptr_restrict kernel.dmesg_restrict kernel.randomize_va_space
  ```

- [ ] **Verify settings survive reboot**
  ```bash
  sudo reboot
  # After reboot:
  sysctl net.ipv4.tcp_congestion_control
  sysctl fs.inotify.max_user_watches
  sysctl vm.swappiness
  ```

## Phase 7: Monitor Impact

- [ ] **Check network performance**
  ```bash
  # TCP connections summary
  ss -s

  # Socket statistics
  cat /proc/net/sockstat
  ```

- [ ] **Check memory usage**
  ```bash
  free -h
  cat /proc/meminfo | grep -E "Dirty|Writeback|SwapTotal|SwapFree"
  ```

- [ ] **Check inotify usage**
  ```bash
  # Count watches per process
  find /proc/*/fd -lname anon_inode:inotify 2>/dev/null | \
    cut -d/ -f3 | sort -n | uniq -c | sort -rn | head -5
  ```

## Rollback

If a setting causes issues:

```bash
# Remove the problematic config file
sudo rm /etc/sysctl.d/60-problematic.conf

# Reapply remaining configs
sudo sysctl --system

# Or revert a single setting to default
sudo sysctl -w net.ipv4.tcp_congestion_control=cubic
```
