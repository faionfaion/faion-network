# Implement Health Checks and Auto-Heal Checklist

## Health Endpoint Implementation

- [ ] Add `/health` endpoint to each HTTP service
- [ ] Return JSON: `{"status": "ok", "checks": {...}}`
- [ ] Check database connectivity (with latency)
- [ ] Check Redis connectivity (with latency)
- [ ] Check RabbitMQ connectivity (if applicable)
- [ ] Return 200 for healthy, 503 for unhealthy/degraded
- [ ] Include service version in response
- [ ] Include uptime in response
- [ ] Health check completes within 5 seconds
- [ ] No authentication required for health endpoints

## Service-Specific Health Checks

### HTTP Services (FastAPI, etc.)
- [ ] `/health` endpoint responds
- [ ] `/health/live` for simple liveness (200 OK)
- [ ] Deep checks verify all dependencies
- [ ] Degraded state reported (not just ok/error)

### Celery Workers
- [ ] `celery inspect ping` returns pong
- [ ] Active task count is reasonable
- [ ] Queue depth is not growing unbounded
- [ ] Worker memory usage is within limits

### Docker Services
- [ ] PostgreSQL: `pg_isready` healthcheck configured
- [ ] Redis: `redis-cli ping` healthcheck configured
- [ ] RabbitMQ: `rabbitmq-diagnostics check_running` configured
- [ ] Docker Compose healthcheck intervals set
- [ ] depends_on with condition: service_healthy

### Background Services (bots, etc.)
- [ ] systemd is-active check
- [ ] Process exists (pidof or pgrep)
- [ ] Log file recently written (if applicable)

## systemd Watchdog

- [ ] WatchdogSec configured in service file (e.g., 30s)
- [ ] Service Type=notify (for watchdog support)
- [ ] Application sends WATCHDOG=1 notification periodically
- [ ] Notification interval = half of WatchdogSec
- [ ] Restart=on-failure configured
- [ ] RestartSec=5 configured
- [ ] StartLimitIntervalSec and StartLimitBurst set (prevent restart loops)

## Auto-Heal Watcher

- [ ] Watcher script created (Python or bash)
- [ ] Check interval configured (60s recommended)
- [ ] Each service has a check function
- [ ] Failed check triggers restart command
- [ ] Restart cooldown implemented (5min between restarts)
- [ ] Maximum restart count per hour (3 recommended)
- [ ] Exceeded max restarts triggers alert (not more restarts)
- [ ] Watcher itself runs as systemd service
- [ ] Watcher has Restart=always

## Health Check Script

- [ ] Script checks all services in sequence
- [ ] Exit code 0 = all healthy
- [ ] Exit code 1 = one or more unhealthy
- [ ] Output identifies which services are unhealthy
- [ ] Can be run manually: `bash health-check.sh`
- [ ] Can be used by cron or monitoring

## Alerting

- [ ] Alert mechanism chosen (Telegram, email, webhook)
- [ ] Alert script created and tested
- [ ] Alerts fire on service failure
- [ ] Alerts fire when max restarts exceeded
- [ ] Alerts include: hostname, service name, timestamp, error
- [ ] Alert rate limiting (no alert storm)

## Docker HEALTHCHECK

For each Docker service in docker-compose.yml:
- [ ] healthcheck.test command configured
- [ ] healthcheck.interval set (10-30s)
- [ ] healthcheck.timeout set (3-10s)
- [ ] healthcheck.retries set (3-5)
- [ ] healthcheck.start_period set (for slow-starting services)
- [ ] dependent services use `condition: service_healthy`

## Monitoring Dashboard (Optional)

- [ ] Real-time service status visible
- [ ] Memory usage per service tracked
- [ ] CPU usage per service tracked
- [ ] Response time (latency) tracked
- [ ] Error rate tracked
- [ ] Queue depth tracked (RabbitMQ)

## Testing

- [ ] Simulate service crash: `systemctl --user stop <service>`
- [ ] Verify auto-heal restarts the service
- [ ] Verify alert fires on failure
- [ ] Simulate dependency failure (stop Redis)
- [ ] Verify health endpoint returns degraded/error
- [ ] Verify restart cooldown works
- [ ] Verify max restart limit works
- [ ] Verify watcher recovers after its own restart

## Verification

- [ ] All health endpoints return 200 under normal operation
- [ ] Watcher service is running: `systemctl --user status nero-watcher`
- [ ] No false positive restarts in logs
- [ ] Health check script passes: `bash health-check.sh`
- [ ] Alerts work: test with a manual service stop
