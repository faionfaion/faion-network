# Monitoring & Logging Checklist

## journald Configuration

- [ ] Set `Storage=persistent` in `/etc/systemd/journald.conf`
- [ ] Set `SystemMaxUse` to reasonable limit (e.g., 2G)
- [ ] Set `MaxRetentionSec` (e.g., 30d)
- [ ] Enable compression: `Compress=yes`
- [ ] Restart journald: `sudo systemctl restart systemd-journald`
- [ ] Verify: `journalctl --disk-usage`

## Log Rotation

- [ ] journald configured with size and time limits
- [ ] Docker daemon.json has log rotation (max-size, max-file)
- [ ] Application log files have logrotate config (if writing to files)
- [ ] Test logrotate: `sudo logrotate -d /etc/logrotate.d/nero-platform`

## Health Check Script

- [ ] Create health-check.sh covering:
  - [ ] Docker containers (postgres, redis, rabbitmq)
  - [ ] systemd user services (all application services)
  - [ ] HTTP endpoints (API health, frontend)
  - [ ] Disk usage threshold (>80% warn, >90% error)
  - [ ] Memory usage threshold
  - [ ] CPU load threshold
- [ ] Test script manually
- [ ] Script returns non-zero exit code on failure

## Alerting

### Telegram Bot Setup

- [ ] Create Telegram bot via @BotFather
- [ ] Get bot token
- [ ] Get chat ID (personal or group)
- [ ] Store credentials in .env
- [ ] Create notify-telegram.sh script
- [ ] Test: `./notify-telegram.sh "Test alert"`

### Alert Configuration

- [ ] Alert on service failure (any nero-* service down)
- [ ] Alert on Docker container failure
- [ ] Alert on disk usage >90%
- [ ] Alert on API health check failure
- [ ] Alert on backup failure
- [ ] Alert on certificate expiry (<14 days)

## Monitoring Scripts

### Hourly Health Check

- [ ] Create hourly health check script (FLOW-style)
- [ ] Only sends alerts when issues found (not on success)
- [ ] Add to cron: `0 * * * *`
- [ ] Test by stopping a service temporarily

### Daily Report

- [ ] Create daily report script
- [ ] Includes: service uptime, resource usage, backup status, error count
- [ ] Add to cron (e.g., 22:00)
- [ ] Sends to Telegram as formatted message

### Startup Heartbeat

- [ ] Create startup script that runs at boot
- [ ] Reports server reboot to Telegram
- [ ] Add to cron: `@reboot`

## tmux Dashboard (Optional)

- [ ] Create tmux monitoring session script
- [ ] Includes htop or top pane
- [ ] Includes service status pane
- [ ] Includes Docker stats pane
- [ ] Includes log tail pane

## Process Monitoring

- [ ] Monitor for zombie processes (periodic check)
- [ ] Monitor open file descriptors (warn if near limit)
- [ ] Monitor memory per service (detect leaks over time)

## Verification

- [ ] All cron monitoring jobs run successfully
- [ ] Telegram alerts delivered within 1 minute of issue
- [ ] Logs are being rotated (old logs removed)
- [ ] Journal disk usage is within configured limits
- [ ] Health check catches all failure scenarios
- [ ] Dashboard displays correctly in tmux

## Maintenance

- [ ] Review alert thresholds quarterly
- [ ] Check log storage usage monthly
- [ ] Update health check when services change
- [ ] Verify Telegram bot is still active
- [ ] Review and archive old logs
