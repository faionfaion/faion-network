---
name: faion-google-ads-reporting
user-invocable: false
description: ""
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Google Ads API - Reporting & Automation

**Communication: User's language. Docs/code: English.**

## Purpose

Provides patterns and guidance for Google Ads reporting, automation, error handling, and best practices.

## 3-Layer Architecture

```
Layer 1: Domain Skills (faion-marketing-manager) - orchestrator
    |
Layer 2: Agents (faion-ads-agent) - executor
    |
Layer 3: Technical Skills (this) - tool
```

---

# Section 1: Reporting

## GAQL (Google Ads Query Language)

### Query Structure

```sql
SELECT field1, field2, metrics.clicks
FROM resource
WHERE conditions
ORDER BY field
LIMIT n
```

### Common Resources

| Resource | Description |
|----------|-------------|
| campaign | Campaign-level data |
| ad_group | Ad group-level data |
| ad_group_ad | Ad-level data |
| keyword_view | Keyword performance |
| search_term_view | Search query data |
| geographic_view | Geographic performance |
| audience | Audience targeting |

### Key Metrics

| Metric | Description |
|--------|-------------|
| metrics.impressions | Ad impressions |
| metrics.clicks | Ad clicks |
| metrics.cost_micros | Cost in micros (divide by 1M) |
| metrics.ctr | Click-through rate |
| metrics.average_cpc | Average cost per click |
| metrics.conversions | Conversion count |
| metrics.conversions_value | Conversion value |
| metrics.cost_per_conversion | Cost per conversion |
| metrics.conversion_rate | Conversion rate |
| metrics.roas | Return on ad spend |

## Report Examples

### Campaign Performance Report

```python
def get_campaign_performance(client, customer_id, start_date, end_date):
    """Get campaign performance metrics."""
    ga_service = client.get_service("GoogleAdsService")

    query = f"""
        SELECT
            campaign.id,
            campaign.name,
            campaign.status,
            metrics.impressions,
            metrics.clicks,
            metrics.ctr,
            metrics.cost_micros,
            metrics.conversions,
            metrics.cost_per_conversion,
            metrics.conversions_value
        FROM campaign
        WHERE segments.date BETWEEN '{start_date}' AND '{end_date}'
        AND campaign.status != 'REMOVED'
        ORDER BY metrics.cost_micros DESC
    """

    response = ga_service.search_stream(customer_id=customer_id, query=query)

    results = []
    for batch in response:
        for row in batch.results:
            results.append({
                "campaign_id": row.campaign.id,
                "campaign_name": row.campaign.name,
                "status": row.campaign.status.name,
                "impressions": row.metrics.impressions,
                "clicks": row.metrics.clicks,
                "ctr": row.metrics.ctr,
                "cost": row.metrics.cost_micros / 1_000_000,
                "conversions": row.metrics.conversions,
                "cpa": row.metrics.cost_per_conversion / 1_000_000 if row.metrics.cost_per_conversion else 0,
                "conv_value": row.metrics.conversions_value
            })

    return results
```

### Geographic Report

```python
def get_geographic_report(client, customer_id, start_date, end_date):
    """Get performance by geographic location."""
    ga_service = client.get_service("GoogleAdsService")

    query = f"""
        SELECT
            geographic_view.country_criterion_id,
            geographic_view.location_type,
            campaign.name,
            metrics.impressions,
            metrics.clicks,
            metrics.cost_micros,
            metrics.conversions
        FROM geographic_view
        WHERE segments.date BETWEEN '{start_date}' AND '{end_date}'
        ORDER BY metrics.cost_micros DESC
    """

    response = ga_service.search(customer_id=customer_id, query=query)

    locations = []
    for row in response:
        locations.append({
            "country_id": row.geographic_view.country_criterion_id,
            "location_type": row.geographic_view.location_type.name,
            "campaign": row.campaign.name,
            "impressions": row.metrics.impressions,
            "clicks": row.metrics.clicks,
            "cost": row.metrics.cost_micros / 1_000_000,
            "conversions": row.metrics.conversions
        })

    return locations
```

---

# Section 2: Automation Patterns

## Batch Operations

```python
def batch_update_keywords(client, customer_id, updates):
    """Batch update multiple keywords efficiently.

    Args:
        updates: List of dicts with ad_group_id, criterion_id, new_bid
    """
    ad_group_criterion_service = client.get_service("AdGroupCriterionService")

    operations = []
    for update in updates:
        operation = client.get_type("AdGroupCriterionOperation")
        criterion = operation.update
        criterion.resource_name = (
            f"customers/{customer_id}/adGroupCriteria/"
            f"{update['ad_group_id']}~{update['criterion_id']}"
        )
        criterion.cpc_bid_micros = update["new_bid"]

        client.copy_from(
            operation.update_mask,
            protobuf_helpers.field_mask(None, criterion._pb)
        )

        operations.append(operation)

    # Process in batches of 5000 (API limit)
    batch_size = 5000
    results = []

    for i in range(0, len(operations), batch_size):
        batch = operations[i:i + batch_size]
        response = ad_group_criterion_service.mutate_ad_group_criteria(
            customer_id=customer_id,
            operations=batch
        )
        results.extend(response.results)

    return results
```

## Scheduled Scripts Pattern

```python
import schedule
import time

def daily_performance_check(client, customer_id, thresholds):
    """Daily check for campaigns exceeding thresholds."""
    campaigns = get_campaign_performance(
        client,
        customer_id,
        get_yesterday(),
        get_yesterday()
    )

    alerts = []
    for campaign in campaigns:
        if campaign["cpa"] > thresholds["max_cpa"]:
            alerts.append(f"High CPA: {campaign['campaign_name']} - ${campaign['cpa']:.2f}")

        if campaign["ctr"] < thresholds["min_ctr"]:
            alerts.append(f"Low CTR: {campaign['campaign_name']} - {campaign['ctr']:.2%}")

    if alerts:
        send_alert_email(alerts)

def auto_pause_poor_performers(client, customer_id, min_conversions, max_cpa):
    """Automatically pause keywords with poor performance."""
    ga_service = client.get_service("GoogleAdsService")

    query = f"""
        SELECT
            ad_group_criterion.resource_name,
            ad_group_criterion.keyword.text,
            metrics.conversions,
            metrics.cost_per_conversion
        FROM keyword_view
        WHERE metrics.impressions > 1000
        AND metrics.conversions < {min_conversions}
        AND metrics.cost_per_conversion > {max_cpa * 1_000_000}
        AND ad_group_criterion.status = 'ENABLED'
    """

    response = ga_service.search(customer_id=customer_id, query=query)

    operations = []
    for row in response:
        operation = client.get_type("AdGroupCriterionOperation")
        criterion = operation.update
        criterion.resource_name = row.ad_group_criterion.resource_name
        criterion.status = client.enums.AdGroupCriterionStatusEnum.PAUSED

        client.copy_from(
            operation.update_mask,
            protobuf_helpers.field_mask(None, criterion._pb)
        )

        operations.append(operation)

    if operations:
        ad_group_criterion_service = client.get_service("AdGroupCriterionService")
        ad_group_criterion_service.mutate_ad_group_criteria(
            customer_id=customer_id,
            operations=operations
        )

# Schedule automation
schedule.every().day.at("08:00").do(daily_performance_check, client, customer_id, thresholds)
schedule.every().day.at("23:00").do(auto_pause_poor_performers, client, customer_id, 1, 50)

while True:
    schedule.run_pending()
    time.sleep(60)
```

## Change History Monitoring

```python
def get_recent_changes(client, customer_id, resource_type, days=7):
    """Get recent changes to account resources."""
    ga_service = client.get_service("GoogleAdsService")

    query = f"""
        SELECT
            change_event.change_date_time,
            change_event.change_resource_type,
            change_event.change_resource_name,
            change_event.client_type,
            change_event.user_email,
            change_event.changed_fields,
            change_event.old_resource,
            change_event.new_resource
        FROM change_event
        WHERE change_event.change_date_time DURING LAST_{days}_DAYS
        AND change_event.change_resource_type = '{resource_type}'
        ORDER BY change_event.change_date_time DESC
        LIMIT 100
    """

    response = ga_service.search(customer_id=customer_id, query=query)

    changes = []
    for row in response:
        changes.append({
            "datetime": row.change_event.change_date_time,
            "resource_type": row.change_event.change_resource_type.name,
            "resource_name": row.change_event.change_resource_name,
            "client": row.change_event.client_type.name,
            "user": row.change_event.user_email,
            "changed_fields": row.change_event.changed_fields
        })

    return changes
```

---

# Section 3: Error Handling

## Common Errors

| Error Code | Description | Solution |
|------------|-------------|----------|
| AUTHENTICATION_ERROR | Invalid credentials | Check tokens, refresh OAuth |
| AUTHORIZATION_ERROR | Insufficient permissions | Verify account access |
| REQUEST_ERROR | Malformed request | Check request structure |
| QUOTA_ERROR | Rate limit exceeded | Implement backoff |
| INTERNAL_ERROR | Server error | Retry with backoff |
| RESOURCE_NOT_FOUND | Invalid resource | Verify resource exists |

## Error Handling Pattern

```python
from google.ads.googleads.errors import GoogleAdsException
import time

def with_retry(func, max_retries=3, initial_delay=1):
    """Retry decorator for API calls."""
    def wrapper(*args, **kwargs):
        delay = initial_delay
        last_exception = None

        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except GoogleAdsException as ex:
                last_exception = ex

                # Check if retryable
                for error in ex.failure.errors:
                    error_code = error.error_code

                    # Quota errors - always retry
                    if error_code.quota_error:
                        time.sleep(delay)
                        delay *= 2
                        continue

                    # Internal errors - retry
                    if error_code.internal_error:
                        time.sleep(delay)
                        delay *= 2
                        continue

                    # Authentication - don't retry
                    if error_code.authentication_error:
                        raise

                    # Authorization - don't retry
                    if error_code.authorization_error:
                        raise

                # Log and continue retry
                print(f"Attempt {attempt + 1} failed: {ex.message}")
                time.sleep(delay)
                delay *= 2

        raise last_exception

    return wrapper

def handle_api_error(ex):
    """Process GoogleAdsException and return actionable info."""
    errors = []

    for error in ex.failure.errors:
        error_info = {
            "code": str(error.error_code),
            "message": error.message,
            "trigger": error.trigger.string_value if error.trigger else None,
            "location": error.location.field_path_elements if error.location else None
        }
        errors.append(error_info)

    return {
        "request_id": ex.request_id,
        "errors": errors
    }
```

## Rate Limiting

```python
import threading
from collections import deque
from datetime import datetime, timedelta

class RateLimiter:
    """Rate limiter for Google Ads API calls."""

    def __init__(self, max_requests_per_day=15000):
        self.max_requests = max_requests_per_day
        self.requests = deque()
        self.lock = threading.Lock()

    def acquire(self):
        """Acquire permission to make a request."""
        with self.lock:
            now = datetime.now()
            day_ago = now - timedelta(days=1)

            # Remove old requests
            while self.requests and self.requests[0] < day_ago:
                self.requests.popleft()

            # Check limit
            if len(self.requests) >= self.max_requests:
                wait_time = (self.requests[0] + timedelta(days=1) - now).total_seconds()
                raise Exception(f"Rate limit reached. Wait {wait_time:.0f} seconds.")

            # Record request
            self.requests.append(now)

    def remaining(self):
        """Get remaining requests for today."""
        with self.lock:
            now = datetime.now()
            day_ago = now - timedelta(days=1)

            while self.requests and self.requests[0] < day_ago:
                self.requests.popleft()

            return self.max_requests - len(self.requests)
```

---

# Section 4: Best Practices

## Account Structure

- Use Manager Accounts (MCC) for multi-account management
- Organize campaigns by objective (brand, non-brand, remarketing)
- Use consistent naming conventions
- Limit ad groups to 15-20 keywords each

## API Usage

- Use `search_stream` for large result sets
- Batch operations (up to 5000 per request)
- Implement exponential backoff for retries
- Cache frequently accessed data
- Use partial responses to reduce payload

## Performance Optimization

```python
# Use search_stream for large queries
def get_large_report(client, customer_id, query):
    ga_service = client.get_service("GoogleAdsService")

    # search_stream returns batches, more efficient for large data
    stream = ga_service.search_stream(customer_id=customer_id, query=query)

    results = []
    for batch in stream:
        for row in batch.results:
            results.append(process_row(row))

    return results

# Select only needed fields
def efficient_query():
    # Good - specific fields
    return """
        SELECT campaign.id, campaign.name, metrics.clicks
        FROM campaign
    """

    # Bad - too many fields
    # SELECT * FROM campaign

# Use parallel requests for independent operations
from concurrent.futures import ThreadPoolExecutor

def get_multiple_reports(client, customer_ids, query):
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {
            executor.submit(get_report, client, cid, query): cid
            for cid in customer_ids
        }

        results = {}
        for future in futures:
            cid = futures[future]
            results[cid] = future.result()

        return results
```

## Security

- Store credentials in environment variables or secrets manager
- Use service accounts for server-to-server auth
- Implement audit logging for all changes
- Review access permissions regularly
- Never expose developer tokens in client-side code

---

# Quick Reference

## API Versions

| Version | Status | End of Life |
|---------|--------|-------------|
| v18 | Current | Active |
| v17 | Supported | TBD |
| v16 | Deprecated | Soon |

*Technical Skill (Layer 3)*
*Part of: faion-google-ads-skill*

## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Implement methodology | haiku | Pattern application and configuration |
| Review implementation | sonnet | Code analysis and verification |
| Design strategy | opus | Complex decision-making |

## Sources

- [Google Ads API Documentation](https://developers.google.com/google-ads/api)
- [Google Ads Reporting Guide](https://support.google.com/google-ads/answer/2375431)
- [GAQL Reference](https://developers.google.com/google-ads/api/docs/query)

---

*faion-google-ads-reporting v1.0*
*Technical Skill (Layer 3)*
*Part of: faion-google-ads-skill*
