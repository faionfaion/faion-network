# Kubernetes Basics Examples

## kubectl Operations

### Resource Management

```bash
# Get resources
kubectl get pods                          # List pods in current namespace
kubectl get pods -o wide                  # Include node and IP info
kubectl get pods -A                       # All namespaces
kubectl get pods -l app=myapp             # Filter by label
kubectl get pods -l 'env in (prod,staging)'  # Label selector
kubectl get pods --field-selector=status.phase=Running
kubectl get pods -o yaml                  # Full YAML output
kubectl get pods -o jsonpath='{.items[*].metadata.name}'  # JSONPath

# Describe (detailed info with events)
kubectl describe pod <pod-name>
kubectl describe deployment <deploy-name>
kubectl describe service <svc-name>
kubectl describe node <node-name>

# Create/Apply resources
kubectl apply -f manifest.yaml            # Apply single file
kubectl apply -f ./manifests/             # Apply all in directory
kubectl apply -f https://example.com/manifest.yaml  # From URL
kubectl apply -k ./kustomize/             # Apply with Kustomize
kubectl apply -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  containers:
  - name: nginx
    image: nginx:1.25
EOF

# Delete resources
kubectl delete -f manifest.yaml
kubectl delete pod <pod-name>
kubectl delete pods -l app=myapp          # Delete by label
kubectl delete pod <pod-name> --grace-period=0 --force  # Force delete (use carefully)
```

### Namespace Operations

```bash
# Create and use namespaces
kubectl create namespace development
kubectl create namespace staging
kubectl create namespace production

# Set default namespace for context
kubectl config set-context --current --namespace=development

# List resources across namespaces
kubectl get pods -n production
kubectl get all -A                        # All resources, all namespaces

# View namespace details
kubectl describe namespace development
kubectl get resourcequotas -n development
kubectl get limitranges -n development
```

### Context Management

```bash
# View contexts
kubectl config get-contexts
kubectl config current-context

# Switch context
kubectl config use-context <context-name>

# Create context alias
kubectl config set-context dev --cluster=my-cluster --namespace=development
kubectl config use-context dev
```

## Deployment Operations

### Creating and Managing Deployments

```bash
# Create deployment imperatively
kubectl create deployment nginx --image=nginx:1.25 --replicas=3

# Scale deployment
kubectl scale deployment nginx --replicas=5

# Autoscale deployment
kubectl autoscale deployment nginx --min=2 --max=10 --cpu-percent=80

# Check HPA status
kubectl get hpa
kubectl describe hpa nginx
```

### Rollout Management

```bash
# Update image (triggers rollout)
kubectl set image deployment/myapp myapp=myapp:2.0.0

# Monitor rollout
kubectl rollout status deployment/myapp
kubectl rollout history deployment/myapp
kubectl rollout history deployment/myapp --revision=2

# Rollback
kubectl rollout undo deployment/myapp              # Previous revision
kubectl rollout undo deployment/myapp --to-revision=1  # Specific revision

# Pause/Resume rollout
kubectl rollout pause deployment/myapp
kubectl rollout resume deployment/myapp

# Restart deployment (rolling restart)
kubectl rollout restart deployment/myapp
```

## Service Operations

### Creating Services

```bash
# Expose deployment as ClusterIP
kubectl expose deployment nginx --port=80 --target-port=8080

# Expose as NodePort
kubectl expose deployment nginx --type=NodePort --port=80 --target-port=8080

# Expose as LoadBalancer
kubectl expose deployment nginx --type=LoadBalancer --port=80 --target-port=8080

# Create headless service (for StatefulSets)
kubectl expose deployment nginx --port=80 --cluster-ip=None
```

### Service Discovery

```bash
# DNS format: <service>.<namespace>.svc.cluster.local
# Examples:
#   myapp.default.svc.cluster.local
#   postgres.database.svc.cluster.local

# Get service endpoints
kubectl get endpoints myapp-service
kubectl describe endpoints myapp-service

# Test service connectivity
kubectl run curl --rm -it --image=curlimages/curl -- curl http://myapp-service:80
kubectl run curl --rm -it --image=curlimages/curl -- curl http://myapp-service.default.svc.cluster.local:80

# Test DNS resolution
kubectl run dnsutils --rm -it --image=tutum/dnsutils -- nslookup myapp-service
```

## ConfigMaps and Secrets

### Creating ConfigMaps

```bash
# From literals
kubectl create configmap myconfig \
  --from-literal=DATABASE_HOST=postgres.db.svc.cluster.local \
  --from-literal=LOG_LEVEL=info

# From file
kubectl create configmap myconfig --from-file=config.properties
kubectl create configmap myconfig --from-file=app-config=config.properties  # Custom key

# From env file
kubectl create configmap myconfig --from-env-file=config.env

# From directory (each file becomes a key)
kubectl create configmap myconfig --from-file=./configs/
```

### Creating Secrets

```bash
# Generic secret from literals
kubectl create secret generic mysecret \
  --from-literal=username=admin \
  --from-literal=password='s3cr3t!'

# TLS secret
kubectl create secret tls mytls-secret --cert=tls.crt --key=tls.key

# Docker registry secret
kubectl create secret docker-registry regcred \
  --docker-server=https://index.docker.io/v1/ \
  --docker-username=myuser \
  --docker-password=mypassword \
  --docker-email=myuser@example.com

# View secret (base64 decoded)
kubectl get secret mysecret -o jsonpath='{.data.password}' | base64 -d
```

## Debugging and Troubleshooting

### Pod Debugging

```bash
# Get logs
kubectl logs <pod-name>                   # Current logs
kubectl logs <pod-name> -c <container>    # Specific container
kubectl logs <pod-name> --previous        # Previous instance (after crash)
kubectl logs <pod-name> -f                # Follow logs
kubectl logs <pod-name> --tail=100        # Last 100 lines
kubectl logs <pod-name> --since=1h        # Last hour
kubectl logs -l app=myapp --all-containers  # All pods with label

# Execute commands
kubectl exec <pod-name> -- ls /app
kubectl exec -it <pod-name> -- /bin/sh
kubectl exec -it <pod-name> -c <container> -- /bin/bash

# Copy files
kubectl cp <pod-name>:/path/to/file ./local-file
kubectl cp ./local-file <pod-name>:/path/to/file
kubectl cp <pod-name>:/var/log/app.log ./app.log -c <container>

# Port forwarding
kubectl port-forward pod/<pod-name> 8080:80
kubectl port-forward svc/<service-name> 8080:80
kubectl port-forward deployment/<deploy-name> 8080:80
```

### Debug Containers

```bash
# Debug running pod with ephemeral container
kubectl debug <pod-name> -it --image=busybox

# Debug with specific container name
kubectl debug <pod-name> -it --image=nicolaka/netshoot --target=<container>

# Debug node
kubectl debug node/<node-name> -it --image=ubuntu

# Create debug copy of pod
kubectl debug <pod-name> -it --copy-to=<pod-name>-debug --container=debugger --image=busybox
```

### Events and Status

```bash
# View cluster events
kubectl get events --sort-by='.lastTimestamp'
kubectl get events -A --field-selector type=Warning
kubectl get events -w                     # Watch events

# Resource status with custom columns
kubectl get pods -o custom-columns=\
NAME:.metadata.name,\
STATUS:.status.phase,\
RESTARTS:.status.containerStatuses[0].restartCount,\
NODE:.spec.nodeName

# API resources
kubectl api-resources                     # List all resources
kubectl api-resources --namespaced=true   # Only namespaced resources
kubectl explain pod.spec.containers       # Explain field
kubectl explain deployment.spec.strategy --recursive
```

### Network Debugging

```bash
# Test DNS
kubectl run dnsutils --rm -it --image=tutum/dnsutils -- nslookup kubernetes

# Test connectivity
kubectl run curl --rm -it --image=curlimages/curl -- curl -v http://service:port

# Network debug pod
kubectl run netshoot --rm -it --image=nicolaka/netshoot -- /bin/bash

# Check network policies
kubectl get networkpolicies -A
kubectl describe networkpolicy <name>
```

### Resource Monitoring

```bash
# Node resources
kubectl top nodes
kubectl describe node <node-name> | grep -A5 "Allocated resources"

# Pod resources
kubectl top pods
kubectl top pods --containers
kubectl top pods -l app=myapp

# Resource quotas
kubectl describe resourcequota -n <namespace>
kubectl describe limitrange -n <namespace>
```

## Useful One-Liners

```bash
# Delete all evicted pods
kubectl get pods -A --field-selector=status.phase=Failed | grep Evicted | awk '{print $2 " -n " $1}' | xargs -L1 kubectl delete pod

# Get all images in cluster
kubectl get pods -A -o jsonpath='{.items[*].spec.containers[*].image}' | tr ' ' '\n' | sort -u

# Find pods not running
kubectl get pods -A --field-selector=status.phase!=Running

# Get pods sorted by restart count
kubectl get pods --sort-by='.status.containerStatuses[0].restartCount'

# Watch pod status changes
kubectl get pods -w

# Get pod resource usage vs requests
kubectl top pods --containers | sort -k3 -h
```

---

*k8s-basics/examples.md | kubectl commands and operations*
