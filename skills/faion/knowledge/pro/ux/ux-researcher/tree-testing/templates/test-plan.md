# Tree Testing Plan

**Project:** [Name]
**Date:** [Date]
**IA Version:** [Version number — must match the tree used in the test tool]
**Tool:** [Optimal Workshop Treejack / UXtweak / Maze]

## Objectives
- Validate proposed information architecture before visual design or build
- Identify navigation problems by task
- Compare alternative structures (if testing variants)

## Tree Structure

```
[Paste tree here as text hierarchy — 3-4 levels max, ~100 nodes max, real labels only]
Home
├── [Section 1]
│   ├── [Item 1.1]
│   └── [Item 1.2]
└── [Section 2]
    └── [Item 2.1]
```

## Tasks (10-15)

| # | Scenario | Correct Answer | Acceptable Alternatives | Priority |
|---|----------|----------------|------------------------|----------|
| 1 | "You want to..." | [Section > Subsection] | [Alt path if exists] | High |
| 2 | "Find where to..." | [Section > Subsection] | | High |

**Leak check status:** [ ] Completed — no task contains destination label word-stems

## Participants
- **Target:** 50 (single tree) / 30 per arm (A/B)
- **Criteria:** [Familiarity with product category — describe real user characteristics]
- **Recruitment:** [Platform]
- **Incentive:** [Amount]

## Success Criteria
- Overall success rate: &gt;80%
- No task below 60% success
- Directness: &gt;70%

## Analysis Plan
- Per-task: success rate, directness, first-click correctness, median time
- Path analysis: identify common wrong paths by task
- Report worst 3 tasks explicitly
- Recommendations tied to specific path evidence
