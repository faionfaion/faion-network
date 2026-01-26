# ELK Stack Templates

## Elasticsearch Configuration

### elasticsearch.yml (Production)

```yaml
# Cluster
cluster.name: production-logs
node.name: ${HOSTNAME}

# Node roles (choose one per node type)
# Master node:
# node.roles: [master]
# Data node:
# node.roles: [data, ingest]
# Coordinating node:
# node.roles: []

# Current node
node.roles: [master, data, ingest]

# Network
network.host: 0.0.0.0
http.port: 9200
transport.port: 9300

# Discovery
discovery.seed_hosts:
  - es-master-0
  - es-master-1
  - es-master-2
cluster.initial_master_nodes:
  - es-master-0
  - es-master-1
  - es-master-2

# Memory
bootstrap.memory_lock: true

# Paths
path.data: /var/lib/elasticsearch
path.logs: /var/log/elasticsearch

# Security
xpack.security.enabled: true
xpack.security.enrollment.enabled: true

# TLS for transport
xpack.security.transport.ssl.enabled: true
xpack.security.transport.ssl.verification_mode: certificate
xpack.security.transport.ssl.keystore.path: /etc/elasticsearch/certs/elastic-certificates.p12
xpack.security.transport.ssl.truststore.path: /etc/elasticsearch/certs/elastic-certificates.p12

# TLS for HTTP
xpack.security.http.ssl.enabled: true
xpack.security.http.ssl.keystore.path: /etc/elasticsearch/certs/http.p12

# Audit logging (optional)
xpack.security.audit.enabled: true
xpack.security.audit.logfile.events.include: ["authentication_failed", "access_denied", "tampered_request"]
```

### jvm.options

```
## JVM Heap Size
-Xms16g
-Xmx16g

## GC Settings
-XX:+UseG1GC
-XX:G1HeapRegionSize=32m
-XX:+ParallelRefProcEnabled
-XX:MaxGCPauseMillis=200

## GC logging
-Xlog:gc*,gc+age=trace,safepoint:file=/var/log/elasticsearch/gc.log:utctime,pid,tags:filecount=32,filesize=64m

## Heap dump on OOM
-XX:+HeapDumpOnOutOfMemoryError
-XX:HeapDumpPath=/var/lib/elasticsearch

## Temp directory
-Djava.io.tmpdir=/var/lib/elasticsearch/tmp
```

---

## Logstash Configuration

### logstash.yml

```yaml
# Node
node.name: logstash-1

# Pipeline
pipeline.workers: 4
pipeline.batch.size: 125
pipeline.batch.delay: 50

# Paths
path.data: /var/lib/logstash
path.logs: /var/log/logstash
path.config: /etc/logstash/conf.d

# Dead Letter Queue
dead_letter_queue.enable: true
dead_letter_queue.max_bytes: 1gb

# HTTP API
http.host: 0.0.0.0
http.port: 9600

# Monitoring (X-Pack)
xpack.monitoring.enabled: true
xpack.monitoring.elasticsearch.hosts: ["https://elasticsearch:9200"]
xpack.monitoring.elasticsearch.username: logstash_system
xpack.monitoring.elasticsearch.password: ${LOGSTASH_SYSTEM_PASSWORD}
```

### pipelines.yml

```yaml
- pipeline.id: beats-pipeline
  path.config: "/etc/logstash/conf.d/beats.conf"
  pipeline.workers: 2

- pipeline.id: kafka-pipeline
  path.config: "/etc/logstash/conf.d/kafka.conf"
  pipeline.workers: 4
  queue.type: persisted
  queue.max_bytes: 4gb
```

### Pipeline Template

```ruby
# /etc/logstash/conf.d/template.conf

input {
  beats {
    port => 5044
    ssl => true
    ssl_certificate => "/etc/logstash/certs/logstash.crt"
    ssl_key => "/etc/logstash/certs/logstash.key"
    ssl_certificate_authorities => ["/etc/logstash/certs/ca.crt"]
    ssl_verify_mode => "force_peer"
  }
}

filter {
  # Add service name from beats field
  if [fields][service] {
    mutate {
      add_field => { "service" => "%{[fields][service]}" }
    }
  }

  # Parse JSON logs
  if [message] =~ /^\{.*\}$/ {
    json {
      source => "message"
      target => "log"
      skip_on_invalid_json => true
    }

    if [log][level] {
      mutate { rename => { "[log][level]" => "level" } }
    }
    if [log][message] {
      mutate { rename => { "[log][message]" => "log_message" } }
    }
    if [log][timestamp] {
      date {
        match => ["[log][timestamp]", "ISO8601"]
        target => "@timestamp"
      }
    }
  }

  # Normalize log levels
  if [level] {
    mutate { uppercase => ["level"] }
    translate {
      field => "level"
      destination => "level"
      override => true
      dictionary => {
        "WARN" => "WARNING"
        "FATAL" => "CRITICAL"
        "DBG" => "DEBUG"
        "INF" => "INFO"
        "ERR" => "ERROR"
      }
      fallback => "%{level}"
    }
  }

  # Remove unnecessary fields
  mutate {
    remove_field => ["agent", "ecs", "input", "log", "@version"]
  }

  # Add processing timestamp
  ruby {
    code => "event.set('processed_at', Time.now.utc.iso8601(3))"
  }
}

output {
  if [@metadata][pipeline] {
    elasticsearch {
      hosts => ["https://elasticsearch:9200"]
      index => "logs-%{[service]}-%{+YYYY.MM.dd}"
      user => "${ES_USER}"
      password => "${ES_PASSWORD}"
      ssl => true
      cacert => "/etc/logstash/certs/ca.crt"
      pipeline => "%{[@metadata][pipeline]}"
    }
  } else {
    elasticsearch {
      hosts => ["https://elasticsearch:9200"]
      index => "logs-%{[service]}-%{+YYYY.MM.dd}"
      user => "${ES_USER}"
      password => "${ES_PASSWORD}"
      ssl => true
      cacert => "/etc/logstash/certs/ca.crt"
    }
  }
}
```

---

## Filebeat Configuration

### filebeat.yml (Full Template)

```yaml
# =========================== Filebeat inputs ===========================
filebeat.inputs:
  # Application logs
  - type: log
    id: app-logs
    enabled: true
    paths:
      - /var/log/app/*.log
      - /var/log/app/**/*.log
    exclude_files: ['\.gz$', '\.zip$']

    fields:
      service: my-application
      environment: ${ENVIRONMENT:production}
    fields_under_root: true

    # JSON parsing
    json:
      keys_under_root: true
      add_error_key: true
      message_key: message

    # Multiline for stack traces
    multiline:
      type: pattern
      pattern: '^\d{4}-\d{2}-\d{2}|^\{|^[A-Z][a-z]{2} \d{2}'
      negate: true
      match: after
      max_lines: 100
      timeout: 5s

    # Harvester settings
    close_inactive: 5m
    clean_removed: true

  # Nginx access logs
  - type: log
    id: nginx-access
    enabled: true
    paths:
      - /var/log/nginx/access.log
    fields:
      service: nginx
      log_type: access
    fields_under_root: true

  # Nginx error logs
  - type: log
    id: nginx-error
    enabled: true
    paths:
      - /var/log/nginx/error.log
    fields:
      service: nginx
      log_type: error
    fields_under_root: true

# ========================= Filebeat modules ===========================
filebeat.modules:
  - module: system
    syslog:
      enabled: true
    auth:
      enabled: true

# ======================= Elasticsearch template =======================
setup.template.enabled: true
setup.template.name: "filebeat"
setup.template.pattern: "filebeat-*"
setup.template.settings:
  index.number_of_shards: 3
  index.number_of_replicas: 1

setup.ilm.enabled: true
setup.ilm.rollover_alias: "filebeat"
setup.ilm.pattern: "{now/d}-000001"
setup.ilm.policy_name: "filebeat-policy"

# =========================== Kibana setup =============================
setup.kibana:
  host: "https://kibana:5601"
  protocol: "https"
  username: "${KIBANA_USER}"
  password: "${KIBANA_PASSWORD}"
  ssl.certificate_authorities: ["/etc/filebeat/ca.crt"]

# ================================ Outputs =============================
output.elasticsearch:
  hosts: ["https://es-node-1:9200", "https://es-node-2:9200", "https://es-node-3:9200"]
  protocol: "https"
  username: "${ES_USER}"
  password: "${ES_PASSWORD}"
  ssl:
    enabled: true
    certificate_authorities: ["/etc/filebeat/ca.crt"]
  index: "filebeat-%{[agent.version]}-%{+yyyy.MM.dd}"

  # Bulk settings
  bulk_max_size: 2048
  compression_level: 5

  # Retry settings
  max_retries: 3
  backoff.init: 1s
  backoff.max: 60s

# ================================ Processors =============================
processors:
  - add_host_metadata:
      when.not.contains.tags: forwarded
  - add_cloud_metadata: ~
  - add_docker_metadata: ~
  - add_kubernetes_metadata: ~

  # Drop debug logs in production
  - drop_event:
      when:
        and:
          - equals:
              level: DEBUG
          - equals:
              environment: production

  # Fingerprint for deduplication
  - fingerprint:
      fields: ["@timestamp", "message", "service"]
      target_field: "@metadata._id"

# ================================ Logging ================================
logging.level: info
logging.to_files: true
logging.files:
  path: /var/log/filebeat
  name: filebeat
  keepfiles: 7
  permissions: 0640
logging.metrics.enabled: true
logging.metrics.period: 30s

# ================================ Monitoring =============================
monitoring.enabled: true
monitoring.elasticsearch:
  hosts: ["https://elasticsearch:9200"]
  username: "${ES_MONITORING_USER}"
  password: "${ES_MONITORING_PASSWORD}"
  ssl.certificate_authorities: ["/etc/filebeat/ca.crt"]
```

---

## Kibana Configuration

### kibana.yml

```yaml
# Server
server.host: "0.0.0.0"
server.port: 5601
server.name: "kibana"
server.publicBaseUrl: "https://kibana.example.com"

# Elasticsearch
elasticsearch.hosts: ["https://es-node-1:9200", "https://es-node-2:9200", "https://es-node-3:9200"]
elasticsearch.username: "kibana_system"
elasticsearch.password: "${KIBANA_PASSWORD}"
elasticsearch.ssl.certificateAuthorities: ["/etc/kibana/certs/ca.crt"]
elasticsearch.ssl.verificationMode: full

# SSL/TLS
server.ssl.enabled: true
server.ssl.certificate: /etc/kibana/certs/kibana.crt
server.ssl.key: /etc/kibana/certs/kibana.key

# Security
xpack.security.enabled: true
xpack.encryptedSavedObjects.encryptionKey: "your-32-character-encryption-key!"
xpack.reporting.encryptionKey: "your-32-character-reporting-key!"
xpack.security.encryptionKey: "your-32-character-security-key!!"

# Session
xpack.security.session.idleTimeout: "1h"
xpack.security.session.lifespan: "24h"

# Spaces
xpack.spaces.enabled: true

# Alerting
xpack.alerting.healthCheck.interval: "1m"

# Logging
logging.dest: /var/log/kibana/kibana.log
logging.json: true
logging.verbose: false

# Telemetry
telemetry.enabled: false
```

---

## Docker Compose Template

### docker-compose.yml

```yaml
version: '3.8'

services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.12.0
    container_name: elasticsearch
    environment:
      - node.name=es01
      - cluster.name=docker-cluster
      - discovery.type=single-node
      - bootstrap.memory_lock=true
      - "ES_JAVA_OPTS=-Xms4g -Xmx4g"
      - xpack.security.enabled=true
      - ELASTIC_PASSWORD=${ELASTIC_PASSWORD}
      - xpack.security.http.ssl.enabled=false
    ulimits:
      memlock:
        soft: -1
        hard: -1
      nofile:
        soft: 65536
        hard: 65536
    volumes:
      - elasticsearch-data:/usr/share/elasticsearch/data
    ports:
      - "9200:9200"
      - "9300:9300"
    networks:
      - elk
    healthcheck:
      test: ["CMD-SHELL", "curl -s http://localhost:9200 | grep -q 'cluster_name'"]
      interval: 30s
      timeout: 10s
      retries: 5

  logstash:
    image: docker.elastic.co/logstash/logstash:8.12.0
    container_name: logstash
    volumes:
      - ./logstash/pipeline:/usr/share/logstash/pipeline:ro
      - ./logstash/config/logstash.yml:/usr/share/logstash/config/logstash.yml:ro
    ports:
      - "5044:5044"
      - "5000:5000/tcp"
      - "5000:5000/udp"
      - "9600:9600"
    environment:
      - "LS_JAVA_OPTS=-Xms1g -Xmx1g"
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
      - ELASTICSEARCH_USER=elastic
      - ELASTICSEARCH_PASSWORD=${ELASTIC_PASSWORD}
    depends_on:
      elasticsearch:
        condition: service_healthy
    networks:
      - elk

  kibana:
    image: docker.elastic.co/kibana/kibana:8.12.0
    container_name: kibana
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
      - ELASTICSEARCH_USERNAME=kibana_system
      - ELASTICSEARCH_PASSWORD=${KIBANA_PASSWORD}
      - xpack.security.enabled=true
    ports:
      - "5601:5601"
    depends_on:
      elasticsearch:
        condition: service_healthy
    networks:
      - elk
    healthcheck:
      test: ["CMD-SHELL", "curl -s http://localhost:5601/api/status | grep -q 'available'"]
      interval: 30s
      timeout: 10s
      retries: 5

  filebeat:
    image: docker.elastic.co/beats/filebeat:8.12.0
    container_name: filebeat
    user: root
    volumes:
      - ./filebeat/filebeat.yml:/usr/share/filebeat/filebeat.yml:ro
      - /var/lib/docker/containers:/var/lib/docker/containers:ro
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - /var/log:/var/log:ro
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
      - ELASTICSEARCH_USER=elastic
      - ELASTICSEARCH_PASSWORD=${ELASTIC_PASSWORD}
    depends_on:
      elasticsearch:
        condition: service_healthy
    networks:
      - elk

volumes:
  elasticsearch-data:
    driver: local

networks:
  elk:
    driver: bridge
```

---

## Kubernetes Templates (ECK)

### Elasticsearch Cluster

```yaml
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: production-logs
  namespace: elastic-system
spec:
  version: 8.12.0

  nodeSets:
    # Master nodes
    - name: master
      count: 3
      config:
        node.roles: ["master"]
        xpack.security.enabled: true
      podTemplate:
        spec:
          containers:
            - name: elasticsearch
              resources:
                requests:
                  memory: 4Gi
                  cpu: 2
                limits:
                  memory: 4Gi
                  cpu: 2
      volumeClaimTemplates:
        - metadata:
            name: elasticsearch-data
          spec:
            accessModes: ["ReadWriteOnce"]
            storageClassName: fast-ssd
            resources:
              requests:
                storage: 50Gi

    # Hot data nodes
    - name: data-hot
      count: 3
      config:
        node.roles: ["data_hot", "data_content", "ingest"]
        node.attr.data: hot
      podTemplate:
        spec:
          containers:
            - name: elasticsearch
              resources:
                requests:
                  memory: 16Gi
                  cpu: 4
                limits:
                  memory: 16Gi
                  cpu: 4
      volumeClaimTemplates:
        - metadata:
            name: elasticsearch-data
          spec:
            accessModes: ["ReadWriteOnce"]
            storageClassName: fast-ssd
            resources:
              requests:
                storage: 500Gi

    # Warm data nodes
    - name: data-warm
      count: 2
      config:
        node.roles: ["data_warm"]
        node.attr.data: warm
      podTemplate:
        spec:
          containers:
            - name: elasticsearch
              resources:
                requests:
                  memory: 8Gi
                  cpu: 2
                limits:
                  memory: 8Gi
                  cpu: 2
      volumeClaimTemplates:
        - metadata:
            name: elasticsearch-data
          spec:
            accessModes: ["ReadWriteOnce"]
            storageClassName: standard
            resources:
              requests:
                storage: 1Ti

  http:
    tls:
      selfSignedCertificate:
        disabled: false
---
apiVersion: kibana.k8s.elastic.co/v1
kind: Kibana
metadata:
  name: production-kibana
  namespace: elastic-system
spec:
  version: 8.12.0
  count: 2
  elasticsearchRef:
    name: production-logs
  http:
    tls:
      selfSignedCertificate:
        disabled: false
  podTemplate:
    spec:
      containers:
        - name: kibana
          resources:
            requests:
              memory: 1Gi
              cpu: 500m
            limits:
              memory: 2Gi
              cpu: 1
```

### Filebeat DaemonSet

```yaml
apiVersion: beat.k8s.elastic.co/v1beta1
kind: Beat
metadata:
  name: filebeat
  namespace: elastic-system
spec:
  type: filebeat
  version: 8.12.0
  elasticsearchRef:
    name: production-logs
  kibanaRef:
    name: production-kibana
  config:
    filebeat.autodiscover:
      providers:
        - type: kubernetes
          node: ${NODE_NAME}
          hints.enabled: true
          hints.default_config:
            type: container
            paths:
              - /var/log/containers/*${data.kubernetes.container.id}.log
    processors:
      - add_cloud_metadata: {}
      - add_host_metadata: {}
      - add_kubernetes_metadata:
          host: ${NODE_NAME}
  daemonSet:
    podTemplate:
      spec:
        serviceAccountName: filebeat
        automountServiceAccountToken: true
        terminationGracePeriodSeconds: 30
        dnsPolicy: ClusterFirstWithHostNet
        hostNetwork: true
        containers:
          - name: filebeat
            securityContext:
              runAsUser: 0
            volumeMounts:
              - name: varlogcontainers
                mountPath: /var/log/containers
              - name: varlogpods
                mountPath: /var/log/pods
              - name: varlibdockercontainers
                mountPath: /var/lib/docker/containers
            env:
              - name: NODE_NAME
                valueFrom:
                  fieldRef:
                    fieldPath: spec.nodeName
        volumes:
          - name: varlogcontainers
            hostPath:
              path: /var/log/containers
          - name: varlogpods
            hostPath:
              path: /var/log/pods
          - name: varlibdockercontainers
            hostPath:
              path: /var/lib/docker/containers
```
