# Checklist

## Planning Phase

- [ ] Identify background work (long-running, scheduled)
- [ ] Design service lifecycle (startup, execution, shutdown)
- [ ] Plan error handling and recovery
- [ ] Design logging strategy
- [ ] Identify performance requirements
- [ ] Plan resource management (database connections)

## BackgroundService Implementation Phase

- [ ] Create class extending BackgroundService
- [ ] Implement ExecuteAsync method
- [ ] Handle CancellationToken for graceful shutdown
- [ ] Implement startup logic if needed
- [ ] Design main processing loop
- [ ] Document service responsibilities

## Dependency Injection Phase

- [ ] Register service in DI container
- [ ] Inject dependencies (repository, logger, etc)
- [ ] Use IServiceProvider for scope management
- [ ] Create scope for database access
- [ ] Dispose resources properly

## Processing Loop Phase

- [ ] Design main processing logic
- [ ] Implement wait/delay between iterations
- [ ] Use PeriodicTimer for scheduled work
- [ ] Handle CancellationToken appropriately
- [ ] Test loop behavior

## Error Handling Phase

- [ ] Catch and log exceptions
- [ ] Implement retry logic if applicable
- [ ] Handle transient failures
- [ ] Implement circuit breaker if needed
- [ ] Implement graceful degradation
- [ ] Alert on critical errors

## Channel-Based Pattern Phase (if needed)

- [ ] Create Channel for work queue
- [ ] Implement IHostedService for writing to channel
- [ ] Implement BackgroundService for reading channel
- [ ] Handle channel completion
- [ ] Test channel communication

## Periodic Work Phase (if needed)

- [ ] Use PeriodicTimer for scheduling
- [ ] Implement work method
- [ ] Handle timer cancellation
- [ ] Test periodic execution
- [ ] Monitor execution timing

## Database Access Phase

- [ ] Create scope for database context
- [ ] Handle database connection pooling
- [ ] Implement transaction handling if needed
- [ ] Test database access works
- [ ] Handle database failures

## Logging Phase

- [ ] Log service startup/shutdown
- [ ] Log execution of work items
- [ ] Log errors with full context
- [ ] Log performance metrics
- [ ] Configure log levels

## Monitoring Phase

- [ ] Implement health checks
- [ ] Monitor service execution time
- [ ] Monitor error rates
- [ ] Set up alerts for failures
- [ ] Create dashboard for service metrics

## Testing Phase

- [ ] Test service starts/stops
- [ ] Test cancellation token handling
- [ ] Test processing logic
- [ ] Test error handling
- [ ] Load test service
- [ ] Test graceful shutdown

## Configuration Phase

- [ ] Configure service in Program.cs/Startup
- [ ] Use IOptions for configuration
- [ ] Support configuration changes if applicable
- [ ] Document configuration options

## Deployment

- [ ] Deploy background service
- [ ] Configure Windows Service or systemd if needed
- [ ] Set up monitoring
- [ ] Create runbook for troubleshooting
- [ ] Document service operation