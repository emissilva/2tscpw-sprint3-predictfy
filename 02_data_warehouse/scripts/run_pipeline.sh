#!/usr/bin/env bash
set -euo pipefail
: "${AZURE_RESOURCE_GROUP:?Defina AZURE_RESOURCE_GROUP}"
: "${ADF_FACTORY_NAME:?Defina ADF_FACTORY_NAME}"
subscription_id="$(az account show --query id -o tsv)"
run_url="https://management.azure.com/subscriptions/${subscription_id}/resourceGroups/${AZURE_RESOURCE_GROUP}/providers/Microsoft.DataFactory/factories/${ADF_FACTORY_NAME}/pipelines/pl_ingestao_incidentes_predictfy/createRun?api-version=2018-06-01"
run_id="$(az rest --method post --url "$run_url" --body '{}' --query runId -o tsv)"
printf 'RunId: %s\n' "$run_id"
while :; do
  status="$(az datafactory pipeline-run show --resource-group "$AZURE_RESOURCE_GROUP" --factory-name "$ADF_FACTORY_NAME" --run-id "$run_id" --query status -o tsv)"
  printf 'Status: %s\n' "$status"
  case "$status" in Succeeded) break;; Failed|Cancelled) exit 1;; esac
  sleep 20
done
az datafactory activity-run query-by-pipeline-run --resource-group "$AZURE_RESOURCE_GROUP" --factory-name "$ADF_FACTORY_NAME" --run-id "$run_id" --last-updated-after '2000-01-01T00:00:00Z' --last-updated-before '2100-01-01T00:00:00Z' -o json
