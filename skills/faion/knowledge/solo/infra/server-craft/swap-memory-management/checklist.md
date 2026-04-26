# Swap and Memory Optimization Checklist

## Swap Setup

- [ ] Check current swap status: `swapon --show`
- [ ] Check available disk space: `df -h /`
- [ ] Determine swap size (recommended: 4GB for 30GB RAM server)
- [ ] Create swap file: `sudo fallocate -l 4G /swapfile`
- [ ] Set permissions: `sudo chmod 600 /swapfile`
- [ ] Format swap: `sudo mkswap /swapfile`
- [ ] Enable swap: `sudo swapon /swapfile`
- [ ] Add to /etc/fstab: `/swapfile none swap sw 0 0`
- [ ] Verify fstab: `sudo findmnt --verify`
- [ ] Verify swap active: `free -h` shows swap line

## vm.swappiness Tuning

- [ ] Check current swappiness: `cat /proc/sys/vm/swappiness`
- [ ] Set swappiness to 10 (AI/API server recommendation)
- [ ] Create config file: `/etc/sysctl.d/99-memory.conf`
- [ ] Include `vm.swappiness=10`
- [ ] Include `vm.vfs_cache_pressure=50`
- [ ] Include `vm.min_free_kbytes=65536`
- [ ] Apply: `sudo sysctl --system`
- [ ] Verify: `sysctl vm.swappiness`

## OOM Killer Configuration

- [ ] Identify critical services that must not be killed
- [ ] Set OOMScoreAdjust for PostgreSQL: -900
- [ ] Set OOMScoreAdjust for Redis: -700
- [ ] Set OOMScoreAdjust for RabbitMQ: -600
- [ ] Set OOMScoreAdjust for API services: -300
- [ ] Set OOMScoreAdjust for workers: 0 (default)
- [ ] Verify OOM scores: `cat /proc/$(pidof postgres)/oom_score_adj`
- [ ] Run `systemctl --user daemon-reload` after service file changes

## PAM Limits

- [ ] Review current limits: `ulimit -a`
- [ ] Set nofile (open files) soft limit: 65536
- [ ] Set nofile (open files) hard limit: 65536
- [ ] Set nproc (processes) soft limit: 4096
- [ ] Set nproc (processes) hard limit: 4096
- [ ] Edit `/etc/security/limits.conf` with above values
- [ ] Verify after relogin: `ulimit -n` shows 65536

## systemd Memory Limits (cgroups v2)

- [ ] Verify cgroups v2 is active: `mount | grep cgroup2`
- [ ] For each service, determine appropriate MemoryMax
- [ ] For each service, set MemoryHigh (soft limit, ~75% of MemoryMax)
- [ ] Consider MemorySwapMax for services that should not use swap
- [ ] Set OOMPolicy=stop for services that should stop cleanly on OOM
- [ ] Run `systemctl --user daemon-reload` after changes
- [ ] Verify limits active: `systemd-cgtop`

## Memory Limits Per Service

| Service | MemoryMax | MemoryHigh | Set? |
|---------|-----------|------------|------|
| nero-core (Celery) | 8G | 6G | [ ] |
| nero-channel-web | 2G | 1500M | [ ] |
| nero-channel-tg | 1G | 768M | [ ] |
| nero-web (serve) | 512M | 384M | [ ] |

## Memory Monitoring Setup

- [ ] `htop` installed for interactive monitoring
- [ ] `free -h` shows expected values
- [ ] Memory alert script created and tested
- [ ] Log rotation configured for monitoring logs
- [ ] Baseline memory usage documented per service
- [ ] Know how to check per-process swap usage

## Verification After Setup

- [ ] Reboot server and verify swap mounts automatically
- [ ] Verify swappiness persists after reboot: `sysctl vm.swappiness`
- [ ] All services start with correct memory limits
- [ ] OOM scores are correct for all services
- [ ] No services are using excessive swap under normal load
- [ ] `free -h` output matches expectations

## Troubleshooting Readiness

- [ ] Know how to identify OOM kills: `dmesg | grep -i "oom\|killed"`
- [ ] Know how to check journal for OOM: `journalctl -k | grep -i oom`
- [ ] Know how to find memory-hungry processes: `ps aux --sort=-%mem | head`
- [ ] Know how to check swap usage per process
- [ ] Know how to temporarily disable swap: `sudo swapoff -a`
- [ ] Know how to resize swap file
