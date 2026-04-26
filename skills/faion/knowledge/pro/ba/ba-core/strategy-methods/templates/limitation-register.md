# Solution Limitation Register: <Solution>

**Date:** [Date]
**Sources:** [defect tickets URL] + [telemetry dashboard] + [user research ref]

## Identified Limitations

| ID | Description | Category | Severity formula | Severity | Evidence |
|----|-------------|----------|-----------------|----------|----------|
| L-001 | [description] | functional\|performance\|usability\|security\|data | users_affected x freq x impact = [N x N x N] | critical\|high\|medium\|low | [ticket/telemetry ref] |

Category options: functional, performance, usability, security, data.
Severity must show the formula calculation; assertion-only rows are rejected.

## Root Cause Analysis

Each limitation requires a minimum 3-entry 5-whys chain. Root cause string must differ from the description.

| ID | 5-Whys chain | Root cause category | Evidence |
|----|--------------|---------------------|----------|
| L-001 | (1) X → (2) Y → (3) Z | technical\|process\|organizational | [ref] |

## Remediation Options

"Accept" remediation requires all cheaper options to be explicitly listed and rejected first.

| ID | Option | Effort (S/M/L) | Impact | Recommendation |
|----|--------|----------------|--------|----------------|
| L-001 | A: Fix in v2 | L | high | Implement |
| L-001 | B: Workaround | S | medium | Accept for now |
| L-001 | C: Accept | — | — | Only if A and B are rejected |
