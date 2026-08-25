#!/usr/bin/env bash
set -euo pipefail
: "${AZURE_RESOURCE_GROUP:?Defina AZURE_RESOURCE_GROUP}"
: "${ADF_FACTORY_NAME:?Defina ADF_FACTORY_NAME}"
subscription_id="$(az account show --query id -o tsv)"
base="https://management.azure.com/subscriptions/${subscription_id}/resourceGroups/${AZURE_RESOURCE_GROUP}/providers/Microsoft.DataFactory/factories/${ADF_FACTORY_NAME}"
publish_kind() {
  local directory="$1" endpoint="$2" file name body
  while IFS= read -r -d '' file; do
    name="$(jq -r '.name' "$file")"
    body="$(jq '{properties}' "$file")"
    if [[ "$name" == 'ls_blob_predictfy' ]]; then
      : "${STORAGE_BLOB_ENDPOINT:?Defina STORAGE_BLOB_ENDPOINT para publicar o linked service Blob}"
      body="$(jq --arg value "$STORAGE_BLOB_ENDPOINT" '.properties.typeProperties.serviceEndpoint = $value' <<<"$body")"
    elif [[ "$name" == 'ls_mysql_predictfy' ]]; then
      : "${MYSQL_CONNECTION_STRING:?Defina MYSQL_CONNECTION_STRING para publicar o linked service MySQL}"
      body="$(jq --arg value "$MYSQL_CONNECTION_STRING" '.properties.typeProperties.connectionString.value = $value' <<<"$body")"
    fi
    az rest --method put --url "${base}/${endpoint}/${name}?api-version=2018-06-01" --body "$body" --output none
    printf 'Publicado: %s/%s\n' "$endpoint" "$name"
  done < <(find "$directory" -type f -name '*.json' -print0 | sort -z)
}
publish_kind adf/linkedService linkedservices
publish_kind adf/dataset datasets
publish_kind adf/dataflow dataflows
publish_kind adf/pipeline pipelines
