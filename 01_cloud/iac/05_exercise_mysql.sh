#!/usr/bin/env bash
set -euo pipefail

required=(AZ_RESOURCE_GROUP AZ_BRIDGE_CONTAINER_NAME BRIDGE_API_KEY)
for name in "${required[@]}"; do
  [[ -n "${!name:-}" ]] || { echo "Variável obrigatória ausente: $name" >&2; exit 2; }
done

fqdn="$(az container show --resource-group "$AZ_RESOURCE_GROUP" --name "$AZ_BRIDGE_CONTAINER_NAME" --query ipAddress.fqdn --output tsv)"
base_url="http://${fqdn}:8080"

echo "[1/4] Health"
curl --fail --show-error --max-time 20 "$base_url/health"

echo
echo "[2/4] Inserção de execução D+1 Total"
curl --fail --show-error --max-time 20 \
  --request POST \
  --header "Content-Type: application/json" \
  --header "X-Bridge-Key: $BRIDGE_API_KEY" \
  --data '{"horizonte":1,"segmento":"total"}' \
  "$base_url/executions/capture"

echo
echo "[3/4] Consulta das execuções"
curl --fail --show-error --max-time 20 \
  --header "X-Bridge-Key: $BRIDGE_API_KEY" \
  "$base_url/executions?limit=10"

echo
echo "[4/4] Processamento agregado"
curl --fail --show-error --max-time 20 \
  --header "X-Bridge-Key: $BRIDGE_API_KEY" \
  "$base_url/executions/summary"
