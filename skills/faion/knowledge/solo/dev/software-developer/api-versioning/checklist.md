# Checklist

## Planning Phase

- [ ] Choose versioning strategy (URL path vs header vs query param)
- [ ] Define version lifecycle (deprecation schedule)
- [ ] Plan version support window (typically 2 concurrent versions)
- [ ] Document breaking changes for each version
- [ ] Define migration path for clients
- [ ] Plan deprecation warnings and timeline

## Implementation Phase

- [ ] Implement URL routing with version prefix (/v1, /v2)
- [ ] Create routers/blueprints per version
- [ ] Duplicate endpoints that change between versions
- [ ] Keep shared logic in common services/utilities
- [ ] Add deprecation headers (Deprecation, Sunset, Link)
- [ ] Include version warnings in v1 responses
- [ ] Create version-specific request/response DTOs
- [ ] Add API documentation for each version

## Testing Phase

- [ ] Test v1 backward compatibility
- [ ] Test v2 new features/changes
- [ ] Verify responses from each version match spec
- [ ] Test client migration path with examples
- [ ] Load test both versions under same traffic
- [ ] Test deprecation headers are sent correctly

## Communication Phase

- [ ] Publish deprecation notice 6+ months before sunset
- [ ] Provide migration guide with code examples
- [ ] Create changelog documenting v1 vs v2 differences
- [ ] Monitor v1 API usage to track migration progress
- [ ] Set reminders for version sunset date

## Deployment

- [ ] Deploy both versions side-by-side
- [ ] Monitor v1 vs v2 usage rates
- [ ] Plan v1 decommission date
- [ ] Update API documentation for end-of-life versions