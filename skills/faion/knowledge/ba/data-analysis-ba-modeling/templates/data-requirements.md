<!-- purpose: data requirements skeleton (per-feature entity + field shortlist) -->
<!-- consumes: feature spec + data dictionary version pin -->
<!-- produces: subset spec referencing dictionary fields -->
<!-- depends-on: content/01-core-rules.xml r5 (version pin) -->
<!-- token-budget-impact: ~200 tokens -->

# Data Requirements: <feature_project_name>

**Version:** 1.0
**Analyst:** <name>

## Data Overview

**Purpose:** [What business capability this data supports]

### Data Entities

| Entity | Description | Source | New/Existing |
|--------|-------------|--------|--------------|
| [Entity] | [Description] | [System] | New / Existing |

## Detailed Requirements

### <entity_1>: <name>

**Description:** <business_description>

**Attributes:**

| Attribute | Type | Size | Required | Description | Validation |
|-----------|------|------|----------|-------------|------------|
| [Name] | [Type] | [Size] | Y/N | [Description] | <rule> |

**Derived Data:**

| Attribute | Formula | Source Attributes |
|-----------|---------|-------------------|
| [Name] | [Formula] | [Source fields] |

## Data Quality Requirements

| Entity | Quality Rule | Threshold |
|--------|--------------|-----------|
| [Entity] | <rule_description> | [e.g. < 1% null values] |

## Data Volumes

| Entity | Current | Expected (1yr) | Expected (3yr) |
|--------|---------|----------------|----------------|
| [Entity] | <count> | <count> | <count> |

## Data Integration

| Source System | Target System | Data | Frequency | Method |
|---------------|---------------|------|-----------|--------|
| [System] | [System] | <data_elements> | <batch_real_time> | <api_etl_cdc> |

## Data Security

| Entity | Classification | Access Rules |
|--------|----------------|--------------|
| [Entity] | Public / Internal / Confidential / Restricted | [Role-based access rules] |
