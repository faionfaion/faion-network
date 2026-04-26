# RACI Matrix — [Project Name]

**Version:** 1.0  
**Date:** [YYYY-MM-DD]  
**Owner (Accountable for this matrix):** [Role]

## Role-to-Person Mapping

| Role | Person | Contact |
|------|--------|---------|
| [Role 1] | [Name] | [email] |
| [Role 2] | [Name] | [email] |
| [Role 3] | [Name] | [email] |

## Matrix

| Task / Deliverable | [Role 1] | [Role 2] | [Role 3] | [Role 4] | [Role 5] |
|--------------------|----------|----------|----------|----------|----------|
| [Task 1]           | A        | R        | C        | I        | I        |
| [Task 2]           | I        | A        | R        | C        | I        |
| [Task 3]           | A        | C        | R        | I        | I        |
| [Task 4]           | C        | I        | C        | A/R      | I        |
| [Task 5]           | A        | I        | I        | C        | R        |

**Legend:**  
R = Responsible (does the work)  
A = Accountable (one per row, final decision-maker)  
C = Consulted (input before decision, two-way)  
I = Informed (notified after decision, one-way)

## Escalation Path

If an Accountable role is unavailable for more than 24 hours, escalation owner is: [Role / Person].

## Validation Checklist

- [ ] Every row has exactly one A
- [ ] Every row has at least one R
- [ ] No row has more than 3 C values
- [ ] All roles are named by role, not by person
- [ ] Escalation path documented
- [ ] raci-lint.py passes on this file
