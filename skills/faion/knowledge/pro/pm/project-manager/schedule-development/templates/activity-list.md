# Activity List — [Project Name]

| ID | Activity | O (days) | M (days) | P (days) | Expected | Predecessors | Resources |
|----|----------|----------|----------|----------|----------|--------------|-----------|
| A1 | [Verb+noun] | [O] | [M] | [P] | =(O+4M+P)/6 | None | [Role] |
| A2 | [Verb+noun] | [O] | [M] | [P] | =(O+4M+P)/6 | A1 (FS) | [Role] |
| A3 | [Verb+noun] | [O] | [M] | [P] | =(O+4M+P)/6 | A1 (FS) | [Role] |

<!-- Dependency types: FS (default) | FF | SS | SF (rare, document justification) -->
<!-- Lag notation: A1 (FS+2d) means start 2 days after A1 finishes -->
<!-- Resources: use role names, not individual names, for schedule flexibility -->

## Critical Path Analysis
- Critical path: [A1 → A2 → A4 → ...] = [N] days total float 0
- Near-critical paths (float &lt; 2 days): [list]
- Project buffer: [N days at project end]
- Feeding buffers: [location and size]
