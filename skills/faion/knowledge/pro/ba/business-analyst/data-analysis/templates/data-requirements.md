# Data Requirements: [Feature or Project Name]

**Version:** [X.X]
**Date:** [Date]
**Analyst:** [Name]
**Snapshot:** [ISO date]

## Data Overview

**Purpose:** [What data supports and why — business context]

### Data Entities

| Entity | Description | Source | New/Existing |
|--------|-------------|--------|--------------|
| [Entity] | [Business description] | [Source system] | New/Existing |

## Detailed Requirements

### [Entity 1]: [Name]

**Description:** [Business description]

**Attributes:**

| Attribute | Type | Size | Required | Description | Validation |
|-----------|------|------|----------|-------------|------------|
| [Name] | [Type] | [Size] | Y/N | [Business meaning] | [Rules] |

**Derived Data:**

| Attribute | Formula | Source Attributes |
|-----------|---------|-------------------|
| [Name] | [Formula] | [Attr1, Attr2] |

## Data Quality Requirements

| Entity | Quality Dimension | Rule | Threshold |
|--------|-------------------|------|-----------|
| [Entity] | [Accuracy/Completeness/etc] | [Rule] | [e.g. error rate < 2%] |

## Data Volumes

| Entity | Current | Expected (1yr) | Expected (3yr) |
|--------|---------|----------------|----------------|
| [Entity] | [Count] | [Count] | [Count] |

## Data Integration

| Source System | Target System | Data | Frequency | Method |
|---------------|---------------|------|-----------|--------|
| [System] | [System] | [Data] | [Frequency] | [API/ETL/file] |

## Data Security

| Entity | Classification | Access Rules |
|--------|----------------|--------------|
| [Entity] | [Public/Internal/Confidential/Restricted] | [Rules] |
