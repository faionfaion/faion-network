# AIOps Examples

Real-world configurations and implementation patterns.

## Anomaly Detection

### Prometheus Anomaly Detection Rules

```yaml
# prometheus-rules.yaml
groups:
  - name: aiops-anomaly-detection
    rules:
      # CPU anomaly using z-score
      - alert: CPUAnomalyDetected
        expr: |
          (
            node_cpu_seconds_total{mode="idle"}
            - avg_over_time(node_cpu_seconds_total{mode="idle"}[7d])
          ) / stddev_over_time(node_cpu_seconds_total{mode="idle"}[7d]) > 3
        for: 5m
        labels:
          severity: warning
          category: aiops
        annotations:
          summary: "CPU usage anomaly detected on {{ $labels.instance }}"

      # Memory anomaly with seasonality awareness
      - alert: MemoryAnomalyDetected
        expr: |
          (
            node_memory_MemAvailable_bytes
            - avg_over_time(node_memory_MemAvailable_bytes[7d] offset 1w)
          ) / node_memory_MemTotal_bytes < -0.2
        for: 10m
        labels:
          severity: warning
          category: aiops

      # Request latency deviation
      - alert: LatencyAnomalyDetected
        expr: |
          histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))
          > 2 * histogram_quantile(0.99, avg_over_time(rate(http_request_duration_seconds_bucket[5m])[7d:1h]))
        for: 5m
        labels:
          severity: critical
          category: aiops
```

### Python Isolation Forest Detector

```python
# anomaly_detector.py
from sklearn.ensemble import IsolationForest
import pandas as pd
import numpy as np
from prometheus_api_client import PrometheusConnect

class AIOpsAnomalyDetector:
    def __init__(self, prometheus_url: str):
        self.prom = PrometheusConnect(url=prometheus_url)
        self.models = {}

    def train_baseline(self, metric_name: str, days: int = 14):
        """Train anomaly detection model on historical data."""
        query = f'{metric_name}[{days}d]'
        data = self.prom.custom_query(query)

        values = np.array([d['values'] for d in data]).flatten()
        df = pd.DataFrame({'value': values})

        # Add time-based features for seasonality
        df['hour'] = pd.to_datetime(df.index, unit='s').hour
        df['day_of_week'] = pd.to_datetime(df.index, unit='s').dayofweek

        model = IsolationForest(
            contamination=0.05,  # Expected 5% anomalies
            random_state=42,
            n_estimators=100
        )
        model.fit(df[['value', 'hour', 'day_of_week']])
        self.models[metric_name] = model

    def detect_anomaly(self, metric_name: str, current_value: float) -> dict:
        """Detect if current value is anomalous."""
        if metric_name not in self.models:
            return {'is_anomaly': False, 'reason': 'No baseline'}

        from datetime import datetime
        now = datetime.now()

        features = np.array([[
            current_value,
            now.hour,
            now.weekday()
        ]])

        prediction = self.models[metric_name].predict(features)
        score = self.models[metric_name].score_samples(features)[0]

        return {
            'is_anomaly': prediction[0] == -1,
            'anomaly_score': score,
            'confidence': min(abs(score) * 100, 100)
        }

# Multi-signal convergence
class ConvergentAnomalyDetector:
    def __init__(self, min_signals: int = 2):
        self.min_signals = min_signals
        self.detectors = {}

    def add_detector(self, name: str, detector: AIOpsAnomalyDetector):
        self.detectors[name] = detector

    def evaluate(self, metrics: dict) -> dict:
        """Evaluate multiple signals for convergent anomaly."""
        anomalies = []

        for name, detector in self.detectors.items():
            if name in metrics:
                result = detector.detect_anomaly(name, metrics[name])
                if result['is_anomaly']:
                    anomalies.append({
                        'signal': name,
                        **result
                    })

        is_incident = len(anomalies) >= self.min_signals

        return {
            'is_incident': is_incident,
            'anomaly_count': len(anomalies),
            'anomalies': anomalies,
            'recommendation': self._get_recommendation(anomalies) if is_incident else None
        }
```

## Automated Remediation

### Kubernetes Self-Healing Operator

```yaml
# auto-remediation-operator.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: aiops-remediation-rules
  namespace: aiops
data:
  rules.yaml: |
    remediations:
      - name: pod-restart
        trigger:
          type: metric
          query: "container_memory_usage_bytes > 0.9 * container_spec_memory_limit_bytes"
          duration: 5m
        action:
          type: restart
          target: pod
        trust_level: auto  # No approval needed

      - name: horizontal-scale
        trigger:
          type: metric
          query: "avg(container_cpu_usage_seconds_total) > 0.8"
          duration: 10m
        action:
          type: scale
          target: deployment
          min: 2
          max: 10
          increment: 2
        trust_level: auto

      - name: rollback-deployment
        trigger:
          type: event
          source: prometheus
          alert: HighErrorRate
        action:
          type: rollback
          target: deployment
          revisions_back: 1
        trust_level: human_approve  # Requires approval
```

### Python Auto-Remediation Engine

```python
# auto_remediation.py
from kubernetes import client, config
from slack_sdk import WebClient
import logging

class RemediationEngine:
    TRUST_LEVELS = {
        'auto': 0,
        'recommend': 1,
        'human_approve': 2,
        'manual_only': 3
    }

    def __init__(self, k8s_config_path: str = None, slack_token: str = None):
        if k8s_config_path:
            config.load_kube_config(k8s_config_path)
        else:
            config.load_incluster_config()
        self.apps_v1 = client.AppsV1Api()
        self.core_v1 = client.CoreV1Api()
        self.slack = WebClient(token=slack_token) if slack_token else None

    async def execute_remediation(self, incident: dict, action: dict) -> dict:
        """Execute remediation with appropriate trust level."""
        trust_level = self.TRUST_LEVELS.get(action.get('trust_level', 'manual_only'))

        if trust_level == 0:  # Auto
            return await self._execute_action(action)
        elif trust_level == 1:  # Recommend
            return await self._recommend_action(incident, action)
        elif trust_level == 2:  # Human approve
            return await self._request_approval(incident, action)
        else:
            return {'status': 'manual_required', 'action': action}

    async def _execute_action(self, action: dict) -> dict:
        """Execute remediation action."""
        action_type = action['type']

        if action_type == 'restart':
            return await self._restart_pod(action)
        elif action_type == 'scale':
            return await self._scale_deployment(action)
        elif action_type == 'rollback':
            return await self._rollback_deployment(action)
        else:
            raise ValueError(f"Unknown action type: {action_type}")

    async def _restart_pod(self, action: dict) -> dict:
        """Restart a pod by deleting it (relies on deployment to recreate)."""
        namespace = action.get('namespace', 'default')
        pod_name = action['pod_name']

        self.core_v1.delete_namespaced_pod(
            name=pod_name,
            namespace=namespace
        )

        logging.info(f"Restarted pod {pod_name} in {namespace}")
        return {'status': 'success', 'action': 'restart', 'target': pod_name}

    async def _scale_deployment(self, action: dict) -> dict:
        """Scale a deployment horizontally."""
        namespace = action.get('namespace', 'default')
        deployment = action['deployment']

        current = self.apps_v1.read_namespaced_deployment(deployment, namespace)
        current_replicas = current.spec.replicas
        new_replicas = min(
            current_replicas + action.get('increment', 1),
            action.get('max', 10)
        )

        current.spec.replicas = new_replicas
        self.apps_v1.patch_namespaced_deployment(deployment, namespace, current)

        logging.info(f"Scaled {deployment} from {current_replicas} to {new_replicas}")
        return {
            'status': 'success',
            'action': 'scale',
            'target': deployment,
            'from': current_replicas,
            'to': new_replicas
        }

    async def _rollback_deployment(self, action: dict) -> dict:
        """Rollback deployment to previous revision."""
        namespace = action.get('namespace', 'default')
        deployment = action['deployment']

        # Get revision history
        revisions = self.apps_v1.list_namespaced_replica_set(
            namespace=namespace,
            label_selector=f"app={deployment}"
        )

        # Sort by revision and get previous
        sorted_revisions = sorted(
            revisions.items,
            key=lambda x: int(x.metadata.annotations.get('deployment.kubernetes.io/revision', 0)),
            reverse=True
        )

        if len(sorted_revisions) < 2:
            return {'status': 'failed', 'reason': 'No previous revision available'}

        previous = sorted_revisions[1]

        # Patch deployment with previous template
        patch = {
            'spec': {
                'template': previous.spec.template
            }
        }

        self.apps_v1.patch_namespaced_deployment(deployment, namespace, patch)

        logging.info(f"Rolled back {deployment} to previous revision")
        return {'status': 'success', 'action': 'rollback', 'target': deployment}

    async def _request_approval(self, incident: dict, action: dict) -> dict:
        """Request human approval via Slack."""
        if not self.slack:
            return {'status': 'approval_required', 'channel': 'manual'}

        message = self._build_approval_message(incident, action)

        response = self.slack.chat_postMessage(
            channel="#incident-response",
            blocks=message['blocks'],
            text=message['text']
        )

        return {
            'status': 'pending_approval',
            'message_ts': response['ts'],
            'channel': response['channel']
        }
```

### Slack Approval Workflow

```python
# slack_approval.py
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

app = App(token="xoxb-your-token")

@app.action("approve_remediation")
def handle_approve(ack, body, client, logger):
    """Handle approval button click."""
    ack()

    action_id = body['actions'][0]['value']
    user = body['user']['username']

    # Execute the approved action
    result = remediation_engine.execute_approved_action(action_id)

    # Update the message
    client.chat_update(
        channel=body['container']['channel_id'],
        ts=body['container']['message_ts'],
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Approved by @{user}*\nResult: {result['status']}"
                }
            }
        ]
    )

@app.action("reject_remediation")
def handle_reject(ack, body, client, logger):
    """Handle rejection button click."""
    ack()

    user = body['user']['username']

    client.chat_update(
        channel=body['container']['channel_id'],
        ts=body['container']['message_ts'],
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Rejected by @{user}*\nNo action taken."
                }
            }
        ]
    )
```

## Predictive Analytics

### Capacity Forecasting

```python
# capacity_forecasting.py
from prophet import Prophet
import pandas as pd
from prometheus_api_client import PrometheusConnect

class CapacityForecaster:
    def __init__(self, prometheus_url: str):
        self.prom = PrometheusConnect(url=prometheus_url)

    def forecast_resource(
        self,
        metric_name: str,
        days_history: int = 30,
        days_forecast: int = 7
    ) -> dict:
        """Forecast resource usage using Prophet."""

        # Fetch historical data
        query = f'{metric_name}[{days_history}d]'
        data = self.prom.custom_query(query)

        # Prepare data for Prophet
        df = pd.DataFrame({
            'ds': pd.to_datetime([d['values'][0] for d in data], unit='s'),
            'y': [float(d['values'][1]) for d in data]
        })

        # Train model
        model = Prophet(
            daily_seasonality=True,
            weekly_seasonality=True,
            yearly_seasonality=False
        )
        model.fit(df)

        # Make forecast
        future = model.make_future_dataframe(periods=days_forecast * 24, freq='H')
        forecast = model.predict(future)

        # Analyze forecast
        max_predicted = forecast['yhat_upper'].max()
        threshold = self._get_threshold(metric_name)

        return {
            'metric': metric_name,
            'current_value': df['y'].iloc[-1],
            'predicted_max': max_predicted,
            'threshold': threshold,
            'days_until_threshold': self._days_until_threshold(forecast, threshold),
            'recommendation': self._get_recommendation(max_predicted, threshold)
        }

    def _days_until_threshold(self, forecast: pd.DataFrame, threshold: float) -> int:
        """Calculate days until threshold is breached."""
        above_threshold = forecast[forecast['yhat'] > threshold]
        if above_threshold.empty:
            return -1  # Never
        return (above_threshold['ds'].iloc[0] - pd.Timestamp.now()).days
```

### Failure Prediction Model

```python
# failure_prediction.py
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler

class FailurePredictionModel:
    def __init__(self):
        self.model = GradientBoostingClassifier(
            n_estimators=100,
            max_depth=5,
            random_state=42
        )
        self.scaler = StandardScaler()
        self.feature_names = [
            'cpu_usage', 'memory_usage', 'disk_io',
            'network_latency', 'error_rate', 'request_rate',
            'gc_pause_time', 'thread_count'
        ]

    def train(self, historical_metrics: pd.DataFrame, failure_labels: pd.Series):
        """Train on historical metrics with failure labels."""
        X = historical_metrics[self.feature_names]
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, failure_labels)

    def predict_failure(self, current_metrics: dict) -> dict:
        """Predict probability of failure in next hour."""
        features = np.array([[current_metrics.get(f, 0) for f in self.feature_names]])
        features_scaled = self.scaler.transform(features)

        probability = self.model.predict_proba(features_scaled)[0][1]

        # Get feature importance for explainability
        importances = dict(zip(
            self.feature_names,
            self.model.feature_importances_
        ))

        top_factors = sorted(
            importances.items(),
            key=lambda x: x[1],
            reverse=True
        )[:3]

        return {
            'failure_probability': probability,
            'risk_level': self._get_risk_level(probability),
            'top_contributing_factors': top_factors,
            'recommendation': self._get_recommendation(probability, top_factors)
        }

    def _get_risk_level(self, probability: float) -> str:
        if probability > 0.8:
            return 'critical'
        elif probability > 0.5:
            return 'high'
        elif probability > 0.3:
            return 'medium'
        return 'low'
```

## CI/CD Integration

### GitHub Actions AIOps Workflow

```yaml
# .github/workflows/aiops-analysis.yml
name: AIOps Pre-Deployment Analysis

on:
  pull_request:
    types: [opened, synchronize]
  push:
    branches: [main]

jobs:
  risk-analysis:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Analyze Change Risk
        id: risk
        run: |
          # Count changed files by category
          INFRA_CHANGES=$(git diff --name-only origin/main | grep -E '(terraform|k8s|helm)' | wc -l)
          DB_CHANGES=$(git diff --name-only origin/main | grep -E '(migration|schema)' | wc -l)

          # Calculate risk score
          RISK_SCORE=$((INFRA_CHANGES * 3 + DB_CHANGES * 5))

          if [ $RISK_SCORE -gt 10 ]; then
            echo "risk_level=high" >> $GITHUB_OUTPUT
          elif [ $RISK_SCORE -gt 5 ]; then
            echo "risk_level=medium" >> $GITHUB_OUTPUT
          else
            echo "risk_level=low" >> $GITHUB_OUTPUT
          fi

      - name: AIOps Deployment Recommendation
        uses: actions/github-script@v7
        with:
          script: |
            const riskLevel = '${{ steps.risk.outputs.risk_level }}';

            const recommendations = {
              high: 'Consider staged rollout with canary deployment',
              medium: 'Enable enhanced monitoring during deployment',
              low: 'Standard deployment approved'
            };

            await github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body: `## AIOps Analysis\n\n**Risk Level:** ${riskLevel}\n\n**Recommendation:** ${recommendations[riskLevel]}`
            });
```

---

*AIOps Examples | faion-cicd-engineer*
