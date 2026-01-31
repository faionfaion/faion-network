# Checklist

## Schema Design Phase

- [ ] Define root Query type with all queries
- [ ] Define Mutation type if needed
- [ ] Define Subscription type if needed
- [ ] Create types for each resource/entity
- [ ] Create input types for mutations
- [ ] Define enums for constrained values
- [ ] Create interface types for shared fields
- [ ] Document resolver requirements

## Query Implementation Phase

- [ ] Implement field resolvers
- [ ] Handle nested field resolution
- [ ] Implement pagination (cursor-based, Relay-style)
- [ ] Implement filtering capabilities
- [ ] Implement sorting
- [ ] Implement search if needed
- [ ] Test query execution and results

## Mutation Implementation Phase

- [ ] Implement create mutations
- [ ] Implement update mutations
- [ ] Implement delete mutations
- [ ] Add input validation
- [ ] Return appropriate response types
- [ ] Handle errors and validation
- [ ] Test all mutations

## N+1 Prevention Phase

- [ ] Implement DataLoader for batching
- [ ] Use batch loading for relationships
- [ ] Test query performance (avoid N+1)
- [ ] Monitor query depth
- [ ] Test with large datasets

## Error Handling Phase

- [ ] Define error types/extensions
- [ ] Implement custom error codes
- [ ] Provide meaningful error messages
- [ ] Include error context/details
- [ ] Test error scenarios
- [ ] Document error codes

## Authorization Phase

- [ ] Implement field-level authorization
- [ ] Check permissions in resolvers
- [ ] Return null or error for forbidden fields
- [ ] Implement role-based access
- [ ] Test authorization rules

## Validation Phase

- [ ] Validate input types
- [ ] Validate field constraints
- [ ] Validate business rules
- [ ] Implement custom validators
- [ ] Return validation errors clearly

## Performance Phase

- [ ] Implement query complexity analysis
- [ ] Set depth limits to prevent DoS
- [ ] Implement timeout on queries
- [ ] Cache resolver results where appropriate
- [ ] Test with large datasets

## Testing Phase

- [ ] Test all queries execute correctly
- [ ] Test all mutations work
- [ ] Test pagination works correctly
- [ ] Test filtering/sorting
- [ ] Test error cases
- [ ] Test authorization

## Documentation Phase

- [ ] Export schema and publish
- [ ] Create schema documentation
- [ ] Provide query examples
- [ ] Document pagination format
- [ ] Document error codes
- [ ] Create API explorer/playground

## Client Generation Phase

- [ ] Generate TypeScript types from schema
- [ ] Generate client SDKs if applicable
- [ ] Create code generation pipeline
- [ ] Test generated clients work

## Deployment

- [ ] Deploy GraphQL server
- [ ] Set up schema versioning
- [ ] Monitor query performance
- [ ] Track most used queries