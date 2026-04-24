# Checklist

## Implementation

- [ ] **Events are immutable** - Once stored, events never change
- [ ] **Events are the source of truth** - State is derived from events
- [ ] **Event order matters** - Events must be applied in sequence
- [ ] **Snapshots for performance** - Periodically save state snapshots
- [ ] **Projections for queries** - Build read models from events

