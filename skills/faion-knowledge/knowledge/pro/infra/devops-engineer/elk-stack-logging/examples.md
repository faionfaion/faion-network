# ELK Stack Examples

## Elasticsearch Examples

### Cluster Health Check

```bash
# Check cluster health
curl -X GET "localhost:9200/_cluster/health?pretty"

# Check nodes status
curl -X GET "localhost:9200/_nodes/stats?pretty"

# Check indices
curl -X GET "localhost:9200/_cat/indices?v"

# Check shards allocation
curl -X GET "localhost:9200/_cat/shards?v"
```

### Index Template

```json
PUT _index_template/logs-template
{
  "index_patterns": ["logs-*"],
  "priority": 100,
  "template": {
    "settings": {
      "number_of_shards": 3,
      "number_of_replicas": 1,
      "index.lifecycle.name": "logs-policy",
      "index.lifecycle.rollover_alias": "logs",
      "index.refresh_interval": "30s"
    },
    "mappings": {
      "properties": {
        "@timestamp": { "type": "date" },
        "message": { "type": "text" },
        "level": { "type": "keyword" },
        "service": { "type": "keyword" },
        "host": { "type": "keyword" },
        "environment": { "type": "keyword" },
        "trace_id": { "type": "keyword" },
        "span_id": { "type": "keyword" },
        "user_id": { "type": "keyword" },
        "request_id": { "type": "keyword" },
        "duration_ms": { "type": "long" },
        "status_code": { "type": "integer" },
        "error": {
          "properties": {
            "type": { "type": "keyword" },
            "message": { "type": "text" },
            "stack_trace": { "type": "text" }
          }
        },
        "http": {
          "properties": {
            "method": { "type": "keyword" },
            "path": { "type": "keyword" },
            "status": { "type": "integer" }
          }
        },
        "geo": {
          "properties": {
            "country": { "type": "keyword" },
            "city": { "type": "keyword" },
            "location": { "type": "geo_point" }
          }
        }
      }
    }
  }
}
```

### Index Lifecycle Management (ILM) Policy

```json
PUT _ilm/policy/logs-policy
{
  "policy": {
    "phases": {
      "hot": {
        "min_age": "0ms",
        "actions": {
          "rollover": {
            "max_size": "50gb",
            "max_age": "1d",
            "max_docs": 100000000
          },
          "set_priority": {
            "priority": 100
          }
        }
      },
      "warm": {
        "min_age": "7d",
        "actions": {
          "shrink": {
            "number_of_shards": 1
          },
          "forcemerge": {
            "max_num_segments": 1
          },
          "allocate": {
            "require": {
              "data": "warm"
            }
          },
          "set_priority": {
            "priority": 50
          }
        }
      },
      "cold": {
        "min_age": "30d",
        "actions": {
          "allocate": {
            "require": {
              "data": "cold"
            }
          },
          "set_priority": {
            "priority": 0
          }
        }
      },
      "delete": {
        "min_age": "90d",
        "actions": {
          "delete": {}
        }
      }
    }
  }
}
```

### Create Rollover Alias

```json
# Create initial index with alias
PUT logs-000001
{
  "aliases": {
    "logs": {
      "is_write_index": true
    }
  }
}
```

---

## Logstash Examples

### Basic Pipeline

```ruby
# /etc/logstash/conf.d/main.conf

input {
  beats {
    port => 5044
    ssl => true
    ssl_certificate => "/etc/logstash/certs/logstash.crt"
    ssl_key => "/etc/logstash/certs/logstash.key"
  }
}

filter {
  # Parse JSON logs
  if [message] =~ /^\{/ {
    json {
      source => "message"
      target => "parsed"
    }
    mutate {
      rename => { "[parsed][level]" => "level" }
      rename => { "[parsed][msg]" => "log_message" }
    }
  }

  # Parse timestamp
  date {
    match => ["[parsed][timestamp]", "ISO8601", "yyyy-MM-dd HH:mm:ss"]
    target => "@timestamp"
  }

  # Add environment tag
  mutate {
    add_field => { "environment" => "production" }
    remove_field => ["agent", "ecs", "input"]
  }
}

output {
  elasticsearch {
    hosts => ["https://elasticsearch:9200"]
    index => "logs-%{[service]}-%{+YYYY.MM.dd}"
    user => "logstash"
    password => "${LOGSTASH_PASSWORD}"
    ssl_certificate_verification => true
    cacert => "/etc/logstash/certs/ca.crt"
  }
}
```

### Advanced Filter Pipeline

```ruby
filter {
  # Parse different log formats
  if [service] == "nginx" {
    grok {
      match => {
        "message" => '%{IPORHOST:client_ip} - %{DATA:user} \[%{HTTPDATE:timestamp}\] "%{WORD:method} %{DATA:request} HTTP/%{NUMBER:http_version}" %{NUMBER:status} %{NUMBER:bytes} "%{DATA:referrer}" "%{DATA:user_agent}"'
      }
    }
  } else if [service] == "application" {
    json {
      source => "message"
    }
  }

  # Add GeoIP information
  if [client_ip] {
    geoip {
      source => "client_ip"
      target => "geo"
      fields => ["country_name", "city_name", "location"]
    }
  }

  # Parse user agent
  if [user_agent] {
    useragent {
      source => "user_agent"
      target => "ua"
    }
  }

  # Mask sensitive data
  mutate {
    gsub => [
      "message", "password=\S+", "password=[REDACTED]",
      "message", "\b\d{16}\b", "[CARD_REDACTED]",
      "message", "Bearer\s+\S+", "Bearer [REDACTED]"
    ]
  }

  # Normalize log levels
  mutate {
    uppercase => ["level"]
  }
  translate {
    field => "level"
    destination => "level"
    override => true
    dictionary => {
      "WARN" => "WARNING"
      "FATAL" => "CRITICAL"
    }
  }

  # Calculate response time category
  if [duration_ms] {
    if [duration_ms] < 100 {
      mutate { add_field => { "response_category" => "fast" } }
    } else if [duration_ms] < 1000 {
      mutate { add_field => { "response_category" => "normal" } }
    } else {
      mutate { add_field => { "response_category" => "slow" } }
    }
  }
}
```

### Dead Letter Queue Handling

```ruby
output {
  elasticsearch {
    hosts => ["https://elasticsearch:9200"]
    index => "logs-%{+YYYY.MM.dd}"
    user => "logstash"
    password => "${LOGSTASH_PASSWORD}"
  }

  # Write failed events to file
  if "_grokparsefailure" in [tags] or "_jsonparsefailure" in [tags] {
    file {
      path => "/var/log/logstash/failed/%{+YYYY-MM-dd}.json"
      codec => json_lines
    }
  }
}
```

---

## Filebeat Examples

### Application Log Collection

```yaml
# /etc/filebeat/filebeat.yml
filebeat.inputs:
  - type: log
    enabled: true
    paths:
      - /var/log/app/*.log
    fields:
      service: my-app
      environment: production
    fields_under_root: true

    # Multiline: stack traces
    multiline:
      pattern: '^\d{4}-\d{2}-\d{2}|^\{'
      negate: true
      match: after
      max_lines: 50

    # JSON parsing
    json:
      keys_under_root: true
      add_error_key: true

processors:
  - add_host_metadata: ~
  - add_cloud_metadata: ~
  - drop_fields:
      fields: ["agent.ephemeral_id", "agent.hostname"]

output.elasticsearch:
  hosts: ["https://elasticsearch:9200"]
  protocol: "https"
  username: "filebeat"
  password: "${FILEBEAT_PASSWORD}"
  ssl:
    certificate_authorities: ["/etc/filebeat/ca.crt"]
  index: "filebeat-%{[agent.version]}-%{+yyyy.MM.dd}"
```

### Kubernetes DaemonSet

```yaml
filebeat.autodiscover:
  providers:
    - type: kubernetes
      node: ${NODE_NAME}
      hints.enabled: true
      hints.default_config:
        type: container
        paths:
          - /var/log/containers/*${data.kubernetes.container.id}.log
      templates:
        - condition:
            equals:
              kubernetes.namespace: production
          config:
            - type: container
              paths:
                - /var/log/containers/*${data.kubernetes.container.id}.log
              processors:
                - add_kubernetes_metadata:
                    host: ${NODE_NAME}
                - decode_json_fields:
                    fields: ["message"]
                    target: ""
                    overwrite_keys: true
```

---

## Kibana Query Examples

### KQL (Kibana Query Language)

```
# Find errors in specific service
level: ERROR AND service: "user-service"

# Time range with log level
@timestamp >= "2025-01-01" AND level: (ERROR OR WARN)

# Full text search
message: "connection timeout"

# Exists check
trace_id: *

# Range query
duration_ms > 1000

# Wildcard
service: "api-*"

# Negation
level: ERROR AND NOT host: "test-*"

# Combined complex query
(level: ERROR OR level: WARN) AND service: "api-*" AND NOT host: "test-*" AND environment: "production"

# HTTP status errors
http.status >= 400 AND http.status < 600

# Slow requests
duration_ms > 5000 AND http.method: "POST"
```

### Elasticsearch DSL Queries

```json
# Search errors in last hour
GET logs-*/_search
{
  "query": {
    "bool": {
      "filter": [
        { "range": { "@timestamp": { "gte": "now-1h" } } },
        { "term": { "level": "ERROR" } }
      ]
    }
  },
  "sort": [{ "@timestamp": { "order": "desc" } }],
  "size": 100
}

# Aggregation: errors by service
GET logs-*/_search
{
  "size": 0,
  "query": {
    "bool": {
      "filter": [
        { "range": { "@timestamp": { "gte": "now-24h" } } },
        { "term": { "level": "ERROR" } }
      ]
    }
  },
  "aggs": {
    "by_service": {
      "terms": {
        "field": "service",
        "size": 20
      }
    }
  }
}

# Percentiles: response time
GET logs-*/_search
{
  "size": 0,
  "query": {
    "range": { "@timestamp": { "gte": "now-1h" } }
  },
  "aggs": {
    "response_percentiles": {
      "percentiles": {
        "field": "duration_ms",
        "percents": [50, 90, 95, 99]
      }
    }
  }
}
```

---

## Alerting Examples

### Watcher Alert (Error Rate)

```json
PUT _watcher/watch/high_error_rate
{
  "trigger": {
    "schedule": { "interval": "5m" }
  },
  "input": {
    "search": {
      "request": {
        "indices": ["logs-*"],
        "body": {
          "size": 0,
          "query": {
            "bool": {
              "filter": [
                { "range": { "@timestamp": { "gte": "now-5m" } } },
                { "term": { "level": "ERROR" } }
              ]
            }
          }
        }
      }
    }
  },
  "condition": {
    "compare": {
      "ctx.payload.hits.total.value": { "gt": 100 }
    }
  },
  "actions": {
    "notify_slack": {
      "webhook": {
        "scheme": "https",
        "host": "hooks.slack.com",
        "port": 443,
        "method": "post",
        "path": "/services/XXX/YYY/ZZZ",
        "body": "{\"text\": \"High error rate: {{ctx.payload.hits.total.value}} errors in 5 minutes\"}"
      }
    }
  }
}
```

### Kibana Alerting Rule (YAML-like config)

```yaml
# Alert: No logs from service
name: "Missing Logs Alert"
consumer: "alerts"
rule_type_id: ".es-query"
schedule:
  interval: "5m"
params:
  index:
    - "logs-*"
  timeField: "@timestamp"
  esQuery: |
    {
      "bool": {
        "filter": [
          { "range": { "@timestamp": { "gte": "now-10m" } } },
          { "term": { "service": "critical-service" } }
        ]
      }
    }
  threshold:
    - 1
  thresholdComparator: "<"
  timeWindowSize: 10
  timeWindowUnit: "m"
actions:
  - group: "default"
    id: "slack-action"
    params:
      message: "No logs from critical-service in last 10 minutes!"
```

---

## Structured Log Format

### Recommended JSON Log Format

```json
{
  "@timestamp": "2025-01-15T10:30:00.000Z",
  "level": "ERROR",
  "logger": "com.example.service.UserService",
  "message": "Failed to process user request",
  "service": "user-service",
  "version": "1.2.3",
  "environment": "production",
  "host": "pod-abc123",
  "trace_id": "abc123def456",
  "span_id": "span789",
  "user_id": "user-12345",
  "request_id": "req-67890",
  "duration_ms": 1523,
  "error": {
    "type": "ValidationException",
    "message": "Invalid email format",
    "stack_trace": "com.example.ValidationException: Invalid email format\n\tat ..."
  },
  "http": {
    "method": "POST",
    "path": "/api/users",
    "status": 400,
    "client_ip": "192.168.1.100"
  },
  "context": {
    "correlation_id": "corr-11111",
    "tenant_id": "tenant-xyz"
  }
}
```
