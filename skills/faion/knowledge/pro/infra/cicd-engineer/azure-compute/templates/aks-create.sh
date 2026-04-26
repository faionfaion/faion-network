#!/bin/bash
# aks-create.sh
# Create AKS cluster with Workload Identity, KEDA, OIDC issuer, and spot node pool.
# Usage: AKS_NAME=my-cluster RG=my-rg ./aks-create.sh

set -euo pipefail

AKS_NAME="${AKS_NAME:-my-aks-cluster}"
RG="${RG:-my-resource-group}"
LOCATION="${LOCATION:-westeurope}"
K8S_VERSION="${K8S_VERSION:-1.29}"
SYSTEM_NODE_SIZE="${SYSTEM_NODE_SIZE:-Standard_D2s_v5}"
USER_NODE_SIZE="${USER_NODE_SIZE:-Standard_D4s_v5}"
SPOT_NODE_SIZE="${SPOT_NODE_SIZE:-Standard_D4s_v5}"

echo "Creating resource group..."
az group create --name "$RG" --location "$LOCATION"

echo "Creating AKS cluster with Workload Identity + KEDA..."
az aks create \
  --name "$AKS_NAME" \
  --resource-group "$RG" \
  --location "$LOCATION" \
  --kubernetes-version "$K8S_VERSION" \
  --node-count 2 \
  --node-vm-size "$SYSTEM_NODE_SIZE" \
  --zones 1 2 3 \
  --network-plugin azure \
  --network-plugin-mode overlay \
  --network-policy calico \
  --enable-oidc-issuer \
  --enable-workload-identity \
  --enable-keda \
  --enable-azure-rbac \
  --enable-azure-policy \
  --enable-defender \
  --auto-upgrade-channel patch \
  --node-os-upgrade-channel NodeImage \
  --maintenance-window-auto-upgrade schedule=weekly day=Sunday startHour=2 \
  --enable-secret-rotation \
  --enable-addons azure-keyvault-secrets-provider \
  --generate-ssh-keys

echo "Adding user node pool with autoscaling..."
az aks nodepool add \
  --cluster-name "$AKS_NAME" \
  --resource-group "$RG" \
  --name user \
  --node-vm-size "$USER_NODE_SIZE" \
  --node-count 2 \
  --min-count 2 \
  --max-count 20 \
  --enable-cluster-autoscaler \
  --zones 1 2 3 \
  --max-surge 33% \
  --labels nodepool-type=user

echo "Adding spot node pool (min=0, scales from zero)..."
az aks nodepool add \
  --cluster-name "$AKS_NAME" \
  --resource-group "$RG" \
  --name spot \
  --node-vm-size "$SPOT_NODE_SIZE" \
  --node-count 0 \
  --min-count 0 \
  --max-count 50 \
  --enable-cluster-autoscaler \
  --priority Spot \
  --eviction-policy Delete \
  --spot-max-price -1 \
  --zones 1 2 3 \
  --node-taints "kubernetes.azure.com/scalesetpriority=spot:NoSchedule" \
  --labels nodepool-type=spot "kubernetes.azure.com/scalesetpriority=spot"

echo "Getting credentials..."
az aks get-credentials --name "$AKS_NAME" --resource-group "$RG"

echo "Done. OIDC issuer URL:"
az aks show --name "$AKS_NAME" --resource-group "$RG" \
  --query oidcIssuerProfile.issuerUrl -o tsv
