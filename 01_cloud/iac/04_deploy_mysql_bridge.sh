#!/usr/bin/env bash
set -euo pipefail

# Executar a partir da raiz predictfy-locaweb para que o build possa ler,
# sem alterar, os snapshots governados em locaweb/outputs.
required=(
  AZ_RESOURCE_GROUP AZ_ACR_NAME AZ_BRIDGE_CONTAINER_NAME AZ_BRIDGE_DNS_LABEL
  AZ_LOG_WORKSPACE AZ_APP_INSIGHTS AZ_MYSQL_SERVER AZ_MYSQL_DATABASE
  AZ_MYSQL_ADMIN MYSQL_ADMIN_PASSWORD BRIDGE_API_KEY
)
for name in "${required[@]}"; do
  [[ -n "${!name:-}" ]] || { echo "Variável obrigatória ausente: $name" >&2; exit 2; }
done

[[ -f "Sprint 3/01_cloud/app_mysql/Dockerfile" ]] || {
  echo "Execute este script a partir de predictfy-locaweb." >&2
  exit 2
}

image_tag="predictfy-mysql-bridge:${BRIDGE_IMAGE_TAG:-sprint3}"

echo "[1/4] Build do bridge no ACR"
if [[ "${SKIP_ACR_BUILD:-false}" == "true" ]]; then
  echo "Imagem existente será reutilizada: $image_tag"
else
  az acr build \
    --registry "$AZ_ACR_NAME" \
    --image "$image_tag" \
    --file "Sprint 3/01_cloud/app_mysql/Dockerfile" \
    .
fi

login_server="$(az acr show --name "$AZ_ACR_NAME" --query loginServer --output tsv)"
acr_username="$(az acr credential show --name "$AZ_ACR_NAME" --query username --output tsv)"
acr_password="$(az acr credential show --name "$AZ_ACR_NAME" --query 'passwords[0].value' --output tsv)"
workspace_id="$(az monitor log-analytics workspace show --resource-group "$AZ_RESOURCE_GROUP" --workspace-name "$AZ_LOG_WORKSPACE" --query customerId --output tsv)"
workspace_key="$(az monitor log-analytics workspace get-shared-keys --resource-group "$AZ_RESOURCE_GROUP" --workspace-name "$AZ_LOG_WORKSPACE" --query primarySharedKey --output tsv)"
app_insights_connection="$(az monitor app-insights component show --resource-group "$AZ_RESOURCE_GROUP" --app "$AZ_APP_INSIGHTS" --query connectionString --output tsv)"
mysql_host="$(az mysql flexible-server show --resource-group "$AZ_RESOURCE_GROUP" --name "$AZ_MYSQL_SERVER" --query fullyQualifiedDomainName --output tsv)"

echo "[2/4] Substituição controlada do bridge com mesmo nome"
if az container show --resource-group "$AZ_RESOURCE_GROUP" --name "$AZ_BRIDGE_CONTAINER_NAME" >/dev/null 2>&1; then
  az container delete --resource-group "$AZ_RESOURCE_GROUP" --name "$AZ_BRIDGE_CONTAINER_NAME" --yes
fi

echo "[3/4] Deploy do bridge"
az container create \
  --resource-group "$AZ_RESOURCE_GROUP" \
  --name "$AZ_BRIDGE_CONTAINER_NAME" \
  --image "${login_server}/${image_tag}" \
  --registry-login-server "$login_server" \
  --registry-username "$acr_username" \
  --registry-password "$acr_password" \
  --os-type Linux \
  --cpu 1 \
  --memory 1.5 \
  --ports 8080 \
  --ip-address Public \
  --dns-name-label "$AZ_BRIDGE_DNS_LABEL" \
  --restart-policy Always \
  --log-analytics-workspace "$workspace_id" \
  --log-analytics-workspace-key "$workspace_key" \
  --environment-variables \
    MYSQL_HOST="$mysql_host" \
    MYSQL_PORT=3306 \
    MYSQL_USER="$AZ_MYSQL_ADMIN" \
    MYSQL_DATABASE="$AZ_MYSQL_DATABASE" \
    APPLICATIONINSIGHTS_CONNECTION_STRING="$app_insights_connection" \
  --secure-environment-variables \
    MYSQL_PASSWORD="$MYSQL_ADMIN_PASSWORD" \
    BRIDGE_API_KEY="$BRIDGE_API_KEY" \
  --output table

echo "[4/4] Endpoint do bridge"
fqdn="$(az container show --resource-group "$AZ_RESOURCE_GROUP" --name "$AZ_BRIDGE_CONTAINER_NAME" --query ipAddress.fqdn --output tsv)"
echo "Bridge: http://${fqdn}:8080/health"
