# Data Requirements: [Feature/Project Name]

**Version:** 1.0
**Analyst:** [Name]

## Data Overview

**Purpose:** [What business capability this data supports]

### Data Entities

| Entity | Description | Source | New/Existing |
|--------|-------------|--------|--------------|
| [Entity] | [Description] | [System] | New / Existing |

## Detailed Requirements

### [Entity 1]: [Name]

**Description:** [Business description]

**Attributes:**

| Attribute | Type | Size | Required | Description | Validation |
|-----------|------|------|----------|-------------|------------|
| [Name] | [Type] | [Size] | Y/N | [Description] | [Rule] |

**Derived Data:**

| Attribute | Formula | Source Attributes |
|-----------|---------|-------------------|
| [Name] | [Formula] | [Source fields] |

## Data Quality Requirements

| Entity | Quality Rule | Threshold |
|--------|--------------|-----------|
| [Entity] | [Rule description] | [e.g. < 1% null values] |

## Data Volumes

| Entity | Current | Expected (1yr) | Expected (3yr) |
|--------|---------|----------------|----------------|
| [Entity] | [Count] | [Count] | [Count] |

## Data Integration

| Source System | Target System | Data | Frequency | Method |
|---------------|---------------|------|-----------|--------|
| [System] | [System] | [Data elements] | [Batch/Real-time] | [API/ETL/CDC] |

## Data Security

| Entity | Classification | Access Rules |
|--------|----------------|--------------|
| [Entity] | Public / Internal / Confidential / Restricted | [Role-based access rules] |
