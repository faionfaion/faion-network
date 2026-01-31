# Checklist

## Implementation

- [ ] **Separate models** - Commands and queries use different models
- [ ] **Commands change state** - Commands return void or ID, never data
- [ ] **Queries return data** - Queries never modify state
- [ ] **Eventual consistency** - Read models may lag behind writes
- [ ] **Projections** - Build read models from events

