# AIOps Examples

## Anomaly Detection Examples

### Example 1: Isolation Forest for Metric Anomalies

```python
# anomaly_detector.py
from sklearn.ensemble import IsolationForest
import pandas as pd
import numpy as np
from prometheus_api_client import PrometheusConnect

class MetricAnomalyDetector:
    """
    Isolation Forest-based anomaly detection for Prometheus metrics.
    """

    def __init__(self, prometheus_url: str, contamination: float = 0.1):
        self.prom = PrometheusConnect(url=prometheus_url)
        self.model = IsolationForest(
            contamination=contamination,
            random_state=42,
            n_estimators=100
        )
        self.baseline_trained = False

    def fetch_metrics(self, query: str, hours: int = 24) -> pd.DataFrame:
        """Fetch metric data from Prometheus."""
        result = self.prom.custom_query_range(
            query=query,
            start_time=pd.Timestamp.now() - pd.Timedelta(hours=hours),
            end_time=pd.Timestamp.now(),
            step="1m"
        )

        if not result:
            return pd.DataFrame()

        data = []
        for metric in result:
            for value in metric["values"]:
                data.append({
                    "timestamp": pd.Timestamp.fromtimestamp(value[0]),
                    "value": float(value[1])
                })

        return pd.DataFrame(data).set_index("timestamp")

    def train_baseline(self, query: str, hours: int = 168):
        """Train on 1 week of historical data."""
        df = self.fetch_metrics(query, hours)

        if len(df) < 100:
            raise ValueError("Insufficient data for training")

        # Feature engineering
        features = self._extract_features(df)
        self.model.fit(features)
        self.baseline_trained = True

    def _extract_features(self, df: pd.DataFrame) -> np.ndarray:
        """Extract features for anomaly detection."""
        df = df.copy()
        df["hour"] = df.index.hour
        df["day_of_week"] = df.index.dayofweek
        df["rolling_mean"] = df["value"].rolling(window=10).mean()
        df["rolling_std"] = df["value"].rolling(window=10).std()
        df = df.dropna()

        return df[["value", "hour", "day_of_week", "rolling_mean", "rolling_std"]].values

    def detect(self, query: str, hours: int = 1) -> list[dict]:
        """Detect anomalies in recent data."""
        if not self.baseline_trained:
            raise RuntimeError("Model not trained. Call train_baseline first.")

        df = self.fetch_metrics(query, hours)
        features = self._extract_features(df)

        # -1 = anomaly, 1 = normal
        predictions = self.model.predict(features)
        scores = self.model.decision_function(features)

        anomalies = []
        for i, (pred, score) in enumerate(zip(predictions, scores)):
            if pred == -1:
                anomalies.append({
                    "timestamp": df.index[i + 4].isoformat(),  # +4 for rolling window
                    "value": float(df.iloc[i + 4]["value"]),
                    "anomaly_score": float(-score),  # Higher = more anomalous
                    "severity": self._classify_severity(score)
                })

        return anomalies

    def _classify_severity(self, score: float) -> str:
        """Classify anomaly severity based on score."""
        if score < -0.3:
            return "critical"
        elif score < -0.2:
            return "warning"
        return "info"


# Usage
if __name__ == "__main__":
    detector = MetricAnomalyDetector("http://prometheus:9090")

    # Train on HTTP request latency
    detector.train_baseline(
        query='histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))',
        hours=168  # 1 week
    )

    # Detect anomalies in last hour
    anomalies = detector.detect(
        query='histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))',
        hours=1
    )

    for a in anomalies:
        print(f"[{a['severity'].upper()}] {a['timestamp']}: {a['value']:.3f}s (score: {a['anomaly_score']:.2f})")
```

### Example 2: SLO-Aware Anomaly Detection

```python
# slo_anomaly_detector.py
from dataclasses import dataclass
from datetime import datetime, timedelta
import math

@dataclass
class SLO:
    name: str
    target: float  # e.g., 0.999 for 99.9%
    window_days: int  # e.g., 30 for monthly
    burn_rate_threshold: float = 1.0  # Alert when burning faster than this

@dataclass
class ErrorBudget:
    total_budget: float
    consumed: float
    remaining: float
    burn_rate: float  # Current burn rate multiplier
    time_to_exhaustion: timedelta | None

class SLOAnomalyDetector:
    """
    Detect anomalies based on SLO error budget burn rate.
    More intelligent than static thresholds - only alerts when
    error budget is burning abnormally fast.
    """

    def __init__(self, slo: SLO):
        self.slo = slo
        self.total_budget_minutes = (1 - slo.target) * slo.window_days * 24 * 60

    def calculate_error_budget(
        self,
        error_minutes_consumed: float,
        window_elapsed_days: float
    ) -> ErrorBudget:
        """Calculate current error budget status."""

        consumed_ratio = error_minutes_consumed / self.total_budget_minutes
        remaining = max(0, self.total_budget_minutes - error_minutes_consumed)

        # Calculate burn rate
        # Burn rate = 1.0 means consuming budget at expected rate
        # Burn rate = 2.0 means consuming 2x faster than expected
        expected_consumption = (window_elapsed_days / self.slo.window_days) * self.total_budget_minutes

        if expected_consumption > 0:
            burn_rate = error_minutes_consumed / expected_consumption
        else:
            burn_rate = 0

        # Calculate time to exhaustion
        if burn_rate > 0 and remaining > 0:
            remaining_days = self.slo.window_days - window_elapsed_days
            if burn_rate > 1:
                # At current burn rate, when will we exhaust?
                days_to_exhaustion = remaining / (burn_rate * (self.total_budget_minutes / self.slo.window_days))
                time_to_exhaustion = timedelta(days=days_to_exhaustion)
            else:
                time_to_exhaustion = None  # Will not exhaust at current rate
        else:
            time_to_exhaustion = timedelta(0) if remaining == 0 else None

        return ErrorBudget(
            total_budget=self.total_budget_minutes,
            consumed=error_minutes_consumed,
            remaining=remaining,
            burn_rate=burn_rate,
            time_to_exhaustion=time_to_exhaustion
        )

    def detect_anomaly(self, error_budget: ErrorBudget) -> dict | None:
        """
        Detect if current burn rate is anomalous.
        Returns anomaly details or None if normal.
        """

        if error_budget.burn_rate <= self.slo.burn_rate_threshold:
            return None

        # Multi-window burn rate strategy (Google SRE)
        # Fast burn: 14.4x burn rate over 1 hour (exhausts 2% of budget)
        # Slow burn: 3x burn rate over 3 days (exhausts 10% of budget)

        severity = "info"
        if error_budget.burn_rate >= 14.4:
            severity = "critical"  # Fast burn - page immediately
        elif error_budget.burn_rate >= 6:
            severity = "warning"   # Medium burn - alert
        elif error_budget.burn_rate >= 3:
            severity = "info"      # Slow burn - ticket

        return {
            "type": "slo_burn_rate_anomaly",
            "slo_name": self.slo.name,
            "severity": severity,
            "burn_rate": error_budget.burn_rate,
            "budget_remaining_pct": (error_budget.remaining / error_budget.total_budget) * 100,
            "time_to_exhaustion": str(error_budget.time_to_exhaustion) if error_budget.time_to_exhaustion else "N/A",
            "message": f"SLO '{self.slo.name}' burning at {error_budget.burn_rate:.1f}x expected rate"
        }


# Usage
if __name__ == "__main__":
    # Define SLO: 99.9% availability over 30 days
    slo = SLO(name="api-availability", target=0.999, window_days=30)
    detector = SLOAnomalyDetector(slo)

    # Scenario: 10 days into the month, consumed 20 minutes of error budget
    budget = detector.calculate_error_budget(
        error_minutes_consumed=20,  # 20 minutes of errors
        window_elapsed_days=10      # 10 days into window
    )

    print(f"Total budget: {budget.total_budget:.1f} minutes")
    print(f"Consumed: {budget.consumed:.1f} minutes")
    print(f"Remaining: {budget.remaining:.1f} minutes")
    print(f"Burn rate: {budget.burn_rate:.2f}x")

    anomaly = detector.detect_anomaly(budget)
    if anomaly:
        print(f"\n[{anomaly['severity'].upper()}] {anomaly['message']}")
```

---

## Root Cause Analysis Examples

### Example 3: Topology-Aware RCA

```python
# root_cause_analyzer.py
from dataclasses import dataclass
from datetime import datetime
from collections import defaultdict
import networkx as nx

@dataclass
class Event:
    timestamp: datetime
    service: str
    event_type: str  # anomaly, error, change, scale
    severity: str
    details: dict

@dataclass
class RCAResult:
    probable_cause: str
    confidence: float
    evidence: list[str]
    affected_services: list[str]
    suggested_actions: list[str]

class TopologyAwareRCA:
    """
    Root Cause Analysis using service topology and event correlation.
    """

    def __init__(self):
        self.topology = nx.DiGraph()
        self.events: list[Event] = []

    def add_service(self, name: str, tier: str = "application"):
        """Add service to topology."""
        self.topology.add_node(name, tier=tier)

    def add_dependency(self, caller: str, callee: str, criticality: str = "high"):
        """Add dependency edge (caller depends on callee)."""
        self.topology.add_edge(caller, callee, criticality=criticality)

    def add_event(self, event: Event):
        """Add event for correlation."""
        self.events.append(event)

    def analyze(self, incident_service: str, time_window_minutes: int = 30) -> RCAResult:
        """
        Perform root cause analysis for an incident.
        """

        # Get relevant events within time window
        incident_time = max(e.timestamp for e in self.events if e.service == incident_service)
        window_start = incident_time - timedelta(minutes=time_window_minutes)

        relevant_events = [
            e for e in self.events
            if window_start <= e.timestamp <= incident_time
        ]

        # Get upstream services (potential root causes)
        upstream = self._get_upstream_services(incident_service)

        # Score each service as potential root cause
        scores = defaultdict(float)
        evidence = defaultdict(list)

        for event in relevant_events:
            if event.service in upstream or event.service == incident_service:
                # Weight by severity
                severity_weight = {"critical": 3, "warning": 2, "info": 1}.get(event.severity, 1)

                # Weight by event type (changes are often root causes)
                type_weight = {"change": 3, "error": 2, "anomaly": 1.5, "scale": 1}.get(event.event_type, 1)

                # Weight by topology distance (closer = more likely)
                try:
                    distance = nx.shortest_path_length(self.topology, incident_service, event.service)
                    distance_weight = 1 / (1 + distance * 0.5)
                except nx.NetworkXNoPath:
                    distance_weight = 0.5

                # Weight by timing (earlier events in window more likely root cause)
                time_diff = (incident_time - event.timestamp).total_seconds() / 60
                timing_weight = 1 + (time_diff / time_window_minutes) * 0.5

                score = severity_weight * type_weight * distance_weight * timing_weight
                scores[event.service] += score
                evidence[event.service].append(
                    f"{event.timestamp.strftime('%H:%M:%S')} - {event.event_type}: {event.details.get('message', 'N/A')}"
                )

        # Determine probable cause
        if not scores:
            return RCAResult(
                probable_cause="Unknown",
                confidence=0,
                evidence=[],
                affected_services=[incident_service],
                suggested_actions=["Investigate manually - no correlated events found"]
            )

        # Normalize scores to confidence
        max_score = max(scores.values())
        probable_cause = max(scores, key=scores.get)
        confidence = min(scores[probable_cause] / (max_score * 1.5), 1.0)

        # Determine affected services (downstream from root cause)
        affected = self._get_downstream_services(probable_cause)

        # Generate suggested actions
        actions = self._generate_actions(probable_cause, evidence[probable_cause])

        return RCAResult(
            probable_cause=probable_cause,
            confidence=confidence,
            evidence=evidence[probable_cause],
            affected_services=affected,
            suggested_actions=actions
        )

    def _get_upstream_services(self, service: str) -> set[str]:
        """Get all services that this service depends on (direct and transitive)."""
        upstream = set()
        try:
            for successor in nx.descendants(self.topology, service):
                upstream.add(successor)
        except nx.NetworkXError:
            pass
        return upstream

    def _get_downstream_services(self, service: str) -> list[str]:
        """Get all services that depend on this service."""
        downstream = [service]
        try:
            for predecessor in nx.ancestors(self.topology, service):
                downstream.append(predecessor)
        except nx.NetworkXError:
            pass
        return downstream

    def _generate_actions(self, cause: str, evidence: list[str]) -> list[str]:
        """Generate suggested remediation actions based on evidence."""
        actions = []

        for e in evidence:
            if "change" in e.lower() or "deploy" in e.lower():
                actions.append(f"Consider rolling back recent deployment to {cause}")
            if "memory" in e.lower():
                actions.append(f"Check memory usage and consider restarting {cause}")
            if "timeout" in e.lower():
                actions.append(f"Check {cause} response times and dependencies")
            if "error rate" in e.lower():
                actions.append(f"Review {cause} error logs for exceptions")

        if not actions:
            actions.append(f"Investigate {cause} logs and metrics")

        return list(set(actions))


# Usage
if __name__ == "__main__":
    rca = TopologyAwareRCA()

    # Build topology
    rca.add_service("frontend", tier="edge")
    rca.add_service("api-gateway", tier="edge")
    rca.add_service("user-service", tier="application")
    rca.add_service("order-service", tier="application")
    rca.add_service("payment-service", tier="application")
    rca.add_service("postgres", tier="data")
    rca.add_service("redis", tier="data")

    rca.add_dependency("frontend", "api-gateway")
    rca.add_dependency("api-gateway", "user-service")
    rca.add_dependency("api-gateway", "order-service")
    rca.add_dependency("order-service", "payment-service")
    rca.add_dependency("user-service", "postgres")
    rca.add_dependency("order-service", "postgres")
    rca.add_dependency("user-service", "redis")

    # Add events
    now = datetime.now()

    rca.add_event(Event(
        timestamp=now - timedelta(minutes=25),
        service="postgres",
        event_type="change",
        severity="info",
        details={"message": "Configuration change: max_connections increased"}
    ))

    rca.add_event(Event(
        timestamp=now - timedelta(minutes=15),
        service="postgres",
        event_type="anomaly",
        severity="warning",
        details={"message": "Connection pool exhaustion detected"}
    ))

    rca.add_event(Event(
        timestamp=now - timedelta(minutes=10),
        service="user-service",
        event_type="error",
        severity="critical",
        details={"message": "Database connection timeout"}
    ))

    rca.add_event(Event(
        timestamp=now,
        service="frontend",
        event_type="anomaly",
        severity="critical",
        details={"message": "Error rate spike to 25%"}
    ))

    # Analyze
    result = rca.analyze("frontend")

    print(f"Probable Cause: {result.probable_cause}")
    print(f"Confidence: {result.confidence:.0%}")
    print(f"\nEvidence:")
    for e in result.evidence:
        print(f"  - {e}")
    print(f"\nAffected Services: {', '.join(result.affected_services)}")
    print(f"\nSuggested Actions:")
    for a in result.suggested_actions:
        print(f"  - {a}")
```

---

## Incident Management Examples

### Example 4: Auto-Remediation with Approval Gates

```python
# auto_remediation.py
import asyncio
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Awaitable
import logging

logger = logging.getLogger(__name__)

class RemediationRisk(Enum):
    LOW = "low"       # Can execute automatically
    MEDIUM = "medium" # Requires async approval (Slack)
    HIGH = "high"     # Requires sync approval (PagerDuty ack)

@dataclass
class RemediationAction:
    name: str
    risk: RemediationRisk
    description: str
    execute: Callable[[], Awaitable[bool]]
    rollback: Callable[[], Awaitable[bool]] | None = None

@dataclass
class Incident:
    id: str
    service: str
    severity: str
    detected_at: str
    symptoms: list[str]

class AutoRemediator:
    """
    Auto-remediation engine with human-in-the-loop approval gates.
    """

    def __init__(
        self,
        slack_client=None,
        pagerduty_client=None,
        approval_timeout_seconds: int = 300
    ):
        self.slack = slack_client
        self.pagerduty = pagerduty_client
        self.approval_timeout = approval_timeout_seconds
        self.actions: dict[str, list[RemediationAction]] = {}
        self.executed_actions: list[tuple[str, RemediationAction]] = []

    def register_action(self, symptom: str, action: RemediationAction):
        """Register remediation action for a symptom pattern."""
        if symptom not in self.actions:
            self.actions[symptom] = []
        self.actions[symptom].append(action)

    async def remediate(self, incident: Incident) -> dict:
        """
        Execute remediation for an incident.
        Returns result with actions taken and outcomes.
        """

        results = {
            "incident_id": incident.id,
            "actions_attempted": [],
            "actions_succeeded": [],
            "actions_failed": [],
            "requires_manual": []
        }

        # Find matching actions
        matching_actions = []
        for symptom in incident.symptoms:
            for pattern, actions in self.actions.items():
                if pattern.lower() in symptom.lower():
                    matching_actions.extend(actions)

        if not matching_actions:
            results["requires_manual"].append("No matching remediation actions found")
            return results

        # Sort by risk (low first)
        matching_actions.sort(key=lambda a: list(RemediationRisk).index(a.risk))

        for action in matching_actions:
            results["actions_attempted"].append(action.name)

            try:
                # Check approval based on risk
                approved = await self._get_approval(incident, action)

                if not approved:
                    results["requires_manual"].append(
                        f"{action.name}: Approval denied or timed out"
                    )
                    continue

                # Execute action
                logger.info(f"Executing remediation: {action.name}")
                success = await action.execute()

                if success:
                    results["actions_succeeded"].append(action.name)
                    self.executed_actions.append((incident.id, action))

                    # Verify remediation worked (wait and check)
                    await asyncio.sleep(30)

                    # If still unhealthy and rollback available, rollback
                    # (In production, check actual health here)

                else:
                    results["actions_failed"].append(action.name)

                    # Try rollback if available
                    if action.rollback:
                        await action.rollback()

            except Exception as e:
                logger.error(f"Remediation failed: {action.name} - {e}")
                results["actions_failed"].append(f"{action.name}: {str(e)}")

        return results

    async def _get_approval(self, incident: Incident, action: RemediationAction) -> bool:
        """Get approval based on action risk level."""

        if action.risk == RemediationRisk.LOW:
            # Auto-approve low-risk actions
            logger.info(f"Auto-approving low-risk action: {action.name}")
            return True

        elif action.risk == RemediationRisk.MEDIUM:
            # Async approval via Slack
            return await self._slack_approval(incident, action)

        else:  # HIGH
            # Sync approval via PagerDuty
            return await self._pagerduty_approval(incident, action)

    async def _slack_approval(self, incident: Incident, action: RemediationAction) -> bool:
        """Request async approval via Slack."""

        if not self.slack:
            logger.warning("Slack not configured, auto-denying")
            return False

        message = {
            "text": f"Remediation Approval Request",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Incident:* {incident.id}\n*Service:* {incident.service}\n*Action:* {action.name}\n*Description:* {action.description}"
                    }
                },
                {
                    "type": "actions",
                    "elements": [
                        {"type": "button", "text": {"type": "plain_text", "text": "Approve"}, "value": "approve", "style": "primary"},
                        {"type": "button", "text": {"type": "plain_text", "text": "Deny"}, "value": "deny", "style": "danger"}
                    ]
                }
            ]
        }

        # In production: send message and wait for response
        # response = await self.slack.send_and_wait(message, timeout=self.approval_timeout)
        # return response == "approve"

        # Placeholder
        logger.info(f"[MOCK] Slack approval requested for {action.name}")
        return True

    async def _pagerduty_approval(self, incident: Incident, action: RemediationAction) -> bool:
        """Request sync approval via PagerDuty."""

        if not self.pagerduty:
            logger.warning("PagerDuty not configured, auto-denying")
            return False

        # In production: create PD incident and wait for ack
        logger.info(f"[MOCK] PagerDuty approval requested for {action.name}")
        return True


# Example actions
async def restart_pods(namespace: str, deployment: str) -> bool:
    """Restart pods via kubectl."""
    import subprocess

    cmd = f"kubectl rollout restart deployment/{deployment} -n {namespace}"
    result = subprocess.run(cmd.split(), capture_output=True)
    return result.returncode == 0

async def scale_deployment(namespace: str, deployment: str, replicas: int) -> bool:
    """Scale deployment."""
    import subprocess

    cmd = f"kubectl scale deployment/{deployment} -n {namespace} --replicas={replicas}"
    result = subprocess.run(cmd.split(), capture_output=True)
    return result.returncode == 0

async def rollback_deployment(namespace: str, deployment: str) -> bool:
    """Rollback to previous revision."""
    import subprocess

    cmd = f"kubectl rollout undo deployment/{deployment} -n {namespace}"
    result = subprocess.run(cmd.split(), capture_output=True)
    return result.returncode == 0


# Usage
if __name__ == "__main__":
    remediator = AutoRemediator()

    # Register actions
    remediator.register_action(
        "CrashLoopBackOff",
        RemediationAction(
            name="restart-pods",
            risk=RemediationRisk.LOW,
            description="Restart pods to recover from crash loop",
            execute=lambda: restart_pods("production", "api-service")
        )
    )

    remediator.register_action(
        "high CPU",
        RemediationAction(
            name="scale-up",
            risk=RemediationRisk.LOW,
            description="Scale deployment to handle load",
            execute=lambda: scale_deployment("production", "api-service", 5),
            rollback=lambda: scale_deployment("production", "api-service", 3)
        )
    )

    remediator.register_action(
        "error rate spike",
        RemediationAction(
            name="rollback-deployment",
            risk=RemediationRisk.MEDIUM,
            description="Rollback to previous stable version",
            execute=lambda: rollback_deployment("production", "api-service")
        )
    )

    # Simulate incident
    incident = Incident(
        id="INC-001",
        service="api-service",
        severity="critical",
        detected_at="2026-01-26T10:00:00Z",
        symptoms=["error rate spike to 25%", "latency increased"]
    )

    # Run remediation
    result = asyncio.run(remediator.remediate(incident))
    print(f"Remediation result: {result}")
```

---

## Kubernetes Integration Example

### Example 5: K8s Event-Driven AIOps

```yaml
# aiops-controller.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: aiops-controller
  namespace: aiops
spec:
  replicas: 1
  selector:
    matchLabels:
      app: aiops-controller
  template:
    metadata:
      labels:
        app: aiops-controller
    spec:
      serviceAccountName: aiops-controller
      containers:
      - name: controller
        image: aiops/controller:latest
        env:
        - name: PROMETHEUS_URL
          value: "http://prometheus.monitoring:9090"
        - name: SLACK_WEBHOOK_URL
          valueFrom:
            secretKeyRef:
              name: aiops-secrets
              key: slack-webhook
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "500m"
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: aiops-controller
  namespace: aiops
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: aiops-controller
rules:
- apiGroups: [""]
  resources: ["pods", "events"]
  verbs: ["get", "list", "watch"]
- apiGroups: ["apps"]
  resources: ["deployments", "replicasets"]
  verbs: ["get", "list", "watch", "update", "patch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: aiops-controller
subjects:
- kind: ServiceAccount
  name: aiops-controller
  namespace: aiops
roleRef:
  kind: ClusterRole
  name: aiops-controller
  apiGroup: rbac.authorization.k8s.io
```

```python
# k8s_aiops_controller.py
from kubernetes import client, config, watch
from kubernetes.client.rest import ApiException
import logging

logger = logging.getLogger(__name__)

class K8sAIOpsController:
    """
    Kubernetes controller that watches events and triggers AIOps actions.
    """

    def __init__(self):
        # Load in-cluster config or local kubeconfig
        try:
            config.load_incluster_config()
        except config.ConfigException:
            config.load_kube_config()

        self.core_v1 = client.CoreV1Api()
        self.apps_v1 = client.AppsV1Api()

        self.remediation_rules = {
            "CrashLoopBackOff": self._handle_crash_loop,
            "OOMKilled": self._handle_oom,
            "ImagePullBackOff": self._handle_image_pull,
        }

    def watch_events(self, namespace: str = ""):
        """Watch Kubernetes events and trigger remediation."""

        w = watch.Watch()

        for event in w.stream(
            self.core_v1.list_namespaced_event if namespace else self.core_v1.list_event_for_all_namespaces,
            namespace=namespace if namespace else None,
            timeout_seconds=0
        ):
            k8s_event = event["object"]

            if k8s_event.type == "Warning":
                reason = k8s_event.reason

                if reason in self.remediation_rules:
                    logger.info(f"Detected {reason} for {k8s_event.involved_object.name}")

                    try:
                        self.remediation_rules[reason](k8s_event)
                    except Exception as e:
                        logger.error(f"Remediation failed: {e}")

    def _handle_crash_loop(self, event):
        """Handle CrashLoopBackOff by checking restart count and potentially recreating pod."""

        pod_name = event.involved_object.name
        namespace = event.involved_object.namespace

        # Get pod details
        pod = self.core_v1.read_namespaced_pod(pod_name, namespace)

        # Check restart count
        restart_count = sum(
            cs.restart_count
            for cs in (pod.status.container_statuses or [])
        )

        if restart_count > 5:
            logger.warning(f"Pod {pod_name} has restarted {restart_count} times")

            # Check if part of deployment
            owner_ref = next(
                (ref for ref in (pod.metadata.owner_references or [])
                 if ref.kind == "ReplicaSet"),
                None
            )

            if owner_ref:
                # Delete pod to force recreation with fresh state
                logger.info(f"Deleting pod {pod_name} to force recreation")
                self.core_v1.delete_namespaced_pod(pod_name, namespace)

    def _handle_oom(self, event):
        """Handle OOMKilled by increasing memory limits."""

        pod_name = event.involved_object.name
        namespace = event.involved_object.namespace

        # Find owning deployment
        pod = self.core_v1.read_namespaced_pod(pod_name, namespace)

        for ref in (pod.metadata.owner_references or []):
            if ref.kind == "ReplicaSet":
                rs = self.apps_v1.read_namespaced_replica_set(ref.name, namespace)

                for dep_ref in (rs.metadata.owner_references or []):
                    if dep_ref.kind == "Deployment":
                        # Log recommendation (don't auto-modify resources)
                        logger.warning(
                            f"Deployment {dep_ref.name} experiencing OOM. "
                            f"Consider increasing memory limits."
                        )

    def _handle_image_pull(self, event):
        """Handle ImagePullBackOff - usually requires manual intervention."""

        logger.warning(
            f"ImagePullBackOff for {event.involved_object.name}. "
            f"Check image name, registry credentials, and network connectivity."
        )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    controller = K8sAIOpsController()

    logger.info("Starting K8s AIOps controller...")
    controller.watch_events()
```
