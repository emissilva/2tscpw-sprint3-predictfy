#!/usr/bin/env bash
set -euo pipefail

key="$(</tmp/predictfy_bridge_key_260823)"
base="http://predictfy-bridge-260823es.eastus2.azurecontainer.io:8080"

echo "PREDICTFY — ML + MYSQL: INSERT, SELECT E PROCESSAMENTO"
echo
echo "1_INSERT_D+1_TOTAL"
curl -sS -X POST \
  -H 'Content-Type: application/json' \
  -H "X-Bridge-Key: $key" \
  -d '{"horizonte":1,"segmento":"total"}' \
  "$base/executions/capture" | jq

echo
echo "2_SELECT"
curl -sS -H "X-Bridge-Key: $key" "$base/executions?limit=1" | jq

echo
echo "3_GROUP_BY_COUNT_AVG"
curl -sS -H "X-Bridge-Key: $key" "$base/executions/summary" | jq
