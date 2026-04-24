# ELK Stack Examples

## Elasticsearch Configuration

### Cluster Configuration (elasticsearch.yml)

```yaml
# elasticsearch.yml - Production cluster
cluster.name: production-logs
node.name: es-node-1

# Node roles (separate in production)
node.roles: [master, data, ingest]

# Network
network.host: 0.0.0.0
http.port: 9200
transport.port: 9300

# Discovery (3-node cluster)
discovery.seed_hosts: ["es-node-1", "es-node-2", "es-node-3"]
cluster.initial_master_nodes: ["es-node-1", "es-node-2", "es-node-3"]

# Memory
bootstrap.memory_lock: true

# Paths
path.data: /var/lib/elasticsearch
path.logs: /var/log/elasticsearch

# Security (X-Pack)
xpack.security.enabled: true
xpack.security.transport.ssl.enabled: true
xpack.security.transport.ssl.verification_mode: certificate
xpack.security.transport.ssl.keystore.path: /etc/elasticsearch/certs/elastic-certificates.p12
xpack.security.transport.ssl.truststore.path: /etc/elasticsearch/certs/elastic-certificates.p12

xpack.security.http.ssl.enabled: true
xpack.security.http.ssl.keystore.path: /etc/elasticsearch/certs/http.p12
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
      "index.refresh_interval": "5s",
      "index.translog.durability": "async"
    },
    "mappings": {
      "dynamic": "strict",
      "properties": {
        "@timestamp": { "type": "date" },
        "message": { "type": "text" },
        "level": { "type": "keyword" },
        "logger": { "type": "keyword" },
        "service": { "type": "keyword" },
        "version": { "type": "keyword" },
        "environment": { "type": "keyword" },
        "host": {
          "properties": {
            "name": { "type": "keyword" },
            "ip": { "type": "ip" }
          }
        },
        "trace_id": { "type": "keyword" },
        "span_id": { "type": "keyword" },
        "request_id": { "type": "keyword" },
        "user_id": { "type": "keyword" },
        "duration_ms": { "type": "long" },
        "error": {
          "properties": {
            "type": { "type": "keyword" },
            "message": { "type": "text" },
            "stack_trace": { "type": "text", "index": false }
          }
        },
        "http": {
          "properties": {
            "method": { "type": "keyword" },
            "path": { "type": "keyword" },
            "status_code": { "type": "short" }
          }
        }
      }
    }
  }
}
```

### ILM Policy (Hot-Warm-Cold-Delete)

```json
PUT _ilm/policy/logs-policy
{
  "policy": {
    "phases": {
      "hot": {
        "min_age": "0ms",
        "actions": {
          "rollover": {
            "max_primary_shard_size": "50gb",
            "max_age": "1d",
            "max_docs": 100000000
          },
          "set_priority": { "priority": 100 }
        }
      },
      "warm": {
        "min_age": "7d",
        "actions": {
          "shrink": { "number_of_shards": 1 },
          "forcemerge": { "max_num_segments": 1 },
          "set_priority": { "priority": 50 },
          "readonly": {}
        }
      },
      "cold": {
        "min_age": "30d",
        "actions": {
          "searchable_snapshot": {
            "snapshot_repository": "logs-snapshots"
          },
          "set_priority": { "priority": 0 }
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

## Logstash Configuration

### Complete Pipeline

```ruby
# /etc/logstash/conf.d/main.conf
input {
  beats {
    port => 5044
    ssl => true
    ssl_certificate => "/etc/logstash/certs/logstash.crt"
    ssl_key => "/etc/logstash/certs/logstash.key"
    ssl_certificate_authorities => ["/etc/logstash/certs/ca.crt"]
  }

  kafka {
    bootstrap_servers => "kafka:9092"
    topics => ["app-logs"]
    codec => json
    group_id => "logstash-consumer"
    auto_offset_reset => "latest"
  }
}

filter {
  # Parse JSON logs
  if [message] =~ /^\{/ {
    json {
      source => "message"
      skip_on_invalid_json => true
    }
  }

  # Parse common log formats
  if "_jsonparsefailure" in [tags] or ![level] {
    grok {
      match => {
        "message" => [
          "%{TIMESTAMP_ISO8601:timestamp} \[%{LOGLEVEL:level}\] %{DATA:logger} - %{GREEDYDATA:log_message}",
          "%{TIMESTAMP_ISO8601:timestamp} %{LOGLEVEL:level} %{GREEDYDATA:log_message}",
          "%{COMBINEDAPACHELOG}"
        ]
      }
      tag_on_failure => ["_grokparsefailure"]
    }
  }

  # Parse dates
  if [timestamp] {
    date {
      match => ["timestamp", "ISO8601", "yyyy-MM-dd HH:mm:ss,SSS", "yyyy-MM-dd HH:mm:ss"]
      target => "@timestamp"
      remove_field => ["timestamp"]
    }
  }

  # Add GeoIP for client IPs
  if [client_ip] {
    geoip {
      source => "client_ip"
      target => "geo"
      database => "/etc/logstash/GeoLite2-City.mmdb"
    }
  }

  # Normalize log levels
  if [level] {
    mutate {
      uppercase => ["level"]
    }
  }

  # Add environment and service tags
  mutate {
    add_field => {
      "[@metadata][index_prefix]" => "logs"
    }
  }

  # Extract service name from Kubernetes metadata
  if [kubernetes][labels][app] {
    mutate {
      add_field => { "service" => "%{[kubernetes][labels][app]}" }
    }
  }

  # Mask sensitive data
  mutate {
    gsub => [
      "message", "password[=:]\s*\S+", "password=[REDACTED]",
      "message", "api[_-]?key[=:]\s*\S+", "api_key=[REDACTED]",
      "message", "\b\d{16}\b", "[CARD_NUMBER_REDACTED]",
      "message", "\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "[EMAIL_REDACTED]"
    ]
  }

  # Remove unnecessary fields
  mutate {
    remove_field => ["agent", "ecs", "input", "log", "host.os"]
  }
}

output {
  elasticsearch {
    hosts => ["https://elasticsearch:9200"]
    index => "%{[@metadata][index_prefix]}-%{[service]}-%{+YYYY.MM.dd}"
    user => "logstash_writer"
    password => "${LOGSTASH_PASSWORD}"
    ssl => true
    ssl_certificate_verification => true
    cacert => "/etc/logstash/certs/ca.crt"
    action => "create"
  }

  # Dead letter queue for failed events
  if "_grokparsefailure" in [tags] or "_jsonparsefailure" in [tags] {
    file {
      path => "/var/log/logstash/failed-%{+YYYY-MM-dd}.json"
      codec => json_lines
    }
  }

  # Debug output (disable in production)
  # stdout { codec => rubydebug }
}
```

### Pipeline Settings

```yaml
# /etc/logstash/pipelines.yml
- pipeline.id: main
  path.config: "/etc/logstash/conf.d/*.conf"
  pipeline.workers: 4
  pipeline.batch.size: 250
  pipeline.batch.delay: 50
  queue.type: persisted
  queue.max_bytes: 4gb
```

## Filebeat Configuration

### Standard Configuration

```yaml
# /etc/filebeat/filebeat.yml
filebeat.inputs:
  # Application logs
  - type: log
    id: app-logs
    enabled: true
    paths:
      - /var/log/app/*.log
      - /var/log/app/**/*.log
    fields:
      service: my-application
      environment: production
    fields_under_root: true
    multiline:
      type: pattern
      pattern: '^\d{4}-\d{2}-\d{2}'
      negate: true
      match: after
      max_lines: 100
    processors:
      - add_host_metadata: ~
      - add_cloud_metadata: ~

  # Container logs
  - type: container
    id: container-logs
    enabled: true
    paths:
      - /var/lib/docker/containers/*/*.log
    processors:
      - add_docker_metadata: ~

  # Syslog
  - type: log
    id: syslog
    enabled: true
    paths:
      - /var/log/syslog
      - /var/log/messages
    fields:
      log_type: system

# Modules
filebeat.modules:
  - module: nginx
    access:
      enabled: true
      var.paths: ["/var/log/nginx/access.log*"]
    error:
      enabled: true
      var.paths: ["/var/log/nginx/error.log*"]

# Output to Elasticsearch
output.elasticsearch:
  hosts: ["https://elasticsearch:9200"]
  protocol: "https"
  username: "${FILEBEAT_USER}"
  password: "${FILEBEAT_PASSWORD}"
  ssl:
    enabled: true
    certificate_authorities: ["/etc/filebeat/certs/ca.crt"]
  index: "filebeat-%{[agent.version]}-%{+yyyy.MM.dd}"
  bulk_max_size: 2048

# Output to Logstash (alternative)
# output.logstash:
#   hosts: ["logstash:5044"]
#   ssl.enabled: true
#   ssl.certificate_authorities: ["/etc/filebeat/certs/ca.crt"]

# Kibana setup
setup.kibana:
  host: "https://kibana:5601"
  ssl:
    enabled: true
    certificate_authorities: ["/etc/filebeat/certs/ca.crt"]

# Index lifecycle management
setup.ilm.enabled: true
setup.ilm.rollover_alias: "filebeat"
setup.ilm.pattern: "{now/d}-000001"

# Logging
logging.level: info
logging.to_files: true
logging.files:
  path: /var/log/filebeat
  name: filebeat
  keepfiles: 7
  permissions: 0640

# Monitoring
monitoring.enabled: true
monitoring.elasticsearch:
  hosts: ["https://elasticsearch:9200"]
  username: "${FILEBEAT_USER}"
  password: "${FILEBEAT_PASSWORD}"
```

### Kubernetes Autodiscover

```yaml
# Kubernetes Filebeat DaemonSet configuration
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
        # Application with JSON logging
        - condition:
            contains:
              kubernetes.labels.log-format: "json"
          config:
            - type: container
              paths:
                - /var/log/containers/*${data.kubernetes.container.id}.log
              json.keys_under_root: true
              json.add_error_key: true

        # Java applications with multiline stack traces
        - condition:
            contains:
              kubernetes.labels.app-type: "java"
          config:
            - type: container
              paths:
                - /var/log/containers/*${data.kubernetes.container.id}.log
              multiline:
                type: pattern
                pattern: '^\d{4}-\d{2}-\d{2}|^[A-Z][a-z]{2} \d{2}'
                negate: true
                match: after

# Required RBAC for Kubernetes metadata
# Apply via kubectl before deploying Filebeat
```

## Kibana Configuration

### kibana.yml

```yaml
# Server
server.host: "0.0.0.0"
server.port: 5601
server.name: "kibana-prod"
server.basePath: ""
server.publicBaseUrl: "https://kibana.example.com"

# Elasticsearch connection
elasticsearch.hosts: ["https://elasticsearch:9200"]
elasticsearch.username: "kibana_system"
elasticsearch.password: "${KIBANA_SYSTEM_PASSWORD}"
elasticsearch.ssl.certificateAuthorities: ["/etc/kibana/certs/ca.crt"]
elasticsearch.ssl.verificationMode: certificate

# Security
xpack.security.enabled: true
xpack.security.encryptionKey: "your-32-character-encryption-key-here"
xpack.security.session.idleTimeout: "1h"
xpack.security.session.lifespan: "24h"

# Saved objects encryption
xpack.encryptedSavedObjects.encryptionKey: "another-32-character-key-here"

# Reporting (optional)
xpack.reporting.encryptionKey: "yet-another-32-character-key"

# Logging
logging.dest: /var/log/kibana/kibana.log
logging.root.level: info
```

## KQL Query Examples

```
# Find errors in specific service
level: ERROR AND service: "user-service"

# Time range with multiple log levels
@timestamp >= "2024-01-15" AND level: (ERROR OR WARN)

# Full text search in message
message: "connection timeout" OR message: "database error"

# Exists check (find logs with trace_id)
trace_id: *

# Range query for slow requests
duration_ms > 1000 AND http.method: "GET"

# Complex query with wildcards
(level: ERROR OR level: WARN) AND service: "api-*" AND NOT host.name: "test-*"

# Find specific HTTP errors
http.status_code >= 500 AND http.status_code < 600

# User activity
user_id: "user-12345" AND @timestamp >= now-24h

# Stack trace search
error.type: "NullPointerException" OR error.message: *null*
```

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
        "search_type": "query_then_fetch",
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
    "compare": { "ctx.payload.hits.total.value": { "gt": 100 } }
  },
  "throttle_period": "15m",
  "actions": {
    "slack_notification": {
      "slack": {
        "account": "monitoring",
        "message": {
          "to": ["#alerts"],
          "text": "High error rate detected: {{ctx.payload.hits.total.value}} errors in last 5 minutes"
        }
      }
    },
    "email_notification": {
      "email": {
        "to": ["ops-team@example.com"],
        "subject": "ELK Alert: High Error Rate",
        "body": {
          "text": "Detected {{ctx.payload.hits.total.value}} errors in the last 5 minutes. Please investigate."
        }
      }
    }
  }
}
```

## Structured Log Format Example

```json
{
  "@timestamp": "2024-01-15T10:30:00.000Z",
  "level": "ERROR",
  "logger": "com.example.service.UserService",
  "message": "Failed to process user request",
  "service": "user-service",
  "version": "1.2.3",
  "environment": "production",
  "host": {
    "name": "pod-abc123",
    "ip": "10.0.1.42"
  },
  "trace_id": "abc123def456",
  "span_id": "span789",
  "request_id": "req-67890",
  "user_id": "user-12345",
  "duration_ms": 1523,
  "error": {
    "type": "ValidationException",
    "message": "Invalid email format",
    "stack_trace": "com.example.ValidationException: Invalid email format\n\tat com.example.UserService.validate(UserService.java:42)..."
  },
  "http": {
    "method": "POST",
    "path": "/api/users",
    "status_code": 400
  }
}
```

---

*ELK Stack Examples | faion-cicd-engineer*
