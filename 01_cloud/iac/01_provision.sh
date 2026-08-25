#!/usr/bin/env bash
set -euo pipefail

# Provisiona a infraestrutura acadêmica do Predictfy na Azure.
# Não remove recursos e não modifica o repositório locaweb.

required=(
  AZ_LOCATION AZ_RESOURCE_GROUP AZ_ACR_NAME AZ_MYSQL_SERVER AZ_CONTAINER_NAME
  AZ_DNS_LABEL AZ_LOG_WORKSPACE AZ_APP_INSIGHTS AZ_MYSQL_DATABASE
  AZ_MYSQL_ADMIN MYSQL_ADMIN_PASSWORD CHAT_SESSION_SECRET
  ENTRA_API_CLIENT_ID ENTRA_SPA_CLIENT_ID CORS_ALLOWED_ORIGINS
)

for name in "${required[@]}"; do
  if [[ -z "${!name:-}" ]]; then
    echo "Variável obrigatória ausente: $name" >&2
    exit 2
  fi
done

command -v az >/dev/null || { echo "Azure CLI não encontrada." >&2; exit 2; }
az account show >/dev/null || { echo "Execute 'az login' antes do provisionamento." >&2; exit 2; }

tags=(Project=Predictfy Sprint=3 Discipline=Cloud Environment=academic)
mysql_location="${AZ_MYSQL_LOCATION:-$AZ_LOCATION}"

echo "[1/6] Resource Group"
az group create \
  --name "$AZ_RESOURCE_GROUP" \
  --location "$AZ_LOCATION" \
  --tags "${tags[@]}" \
  --output table

echo "[2/6] Log Analytics Workspace"
az monitor log-analytics workspace create \
  --resource-group "$AZ_RESOURCE_GROUP" \
  --workspace-name "$AZ_LOG_WORKSPACE" \
  --location "$AZ_LOCATION" \
  --tags "${tags[@]}" \
  --output table

subscription_id="$(az account show --query id --output tsv)"
workspace_resource_id="/subscriptions/${subscription_id}/resourceGroups/${AZ_RESOURCE_GROUP}/providers/Microsoft.OperationalInsights/workspaces/${AZ_LOG_WORKSPACE}"

echo "[3/6] Application Insights"
az extension add --name application-insights --upgrade --yes >/dev/null
az monitor app-insights component create \
  --app "$AZ_APP_INSIGHTS" \
  --location "$AZ_LOCATION" \
  --resource-group "$AZ_RESOURCE_GROUP" \
  --kind web \
  --application-type web \
  --workspace "$workspace_resource_id" \
  --tags "${tags[@]}" \
  --output table

echo "[4/6] Azure Container Registry"
az acr create \
  --resource-group "$AZ_RESOURCE_GROUP" \
  --name "$AZ_ACR_NAME" \
  --location "$AZ_LOCATION" \
  --sku Basic \
  --admin-enabled true \
  --tags "${tags[@]}" \
  --output table

echo "[5/6] Azure Database for MySQL Flexible Server"
if ! az mysql flexible-server show --resource-group "$AZ_RESOURCE_GROUP" --name "$AZ_MYSQL_SERVER" >/dev/null 2>&1; then
  az mysql flexible-server create \
    --resource-group "$AZ_RESOURCE_GROUP" \
    --name "$AZ_MYSQL_SERVER" \
    --location "$mysql_location" \
    --admin-user "$AZ_MYSQL_ADMIN" \
    --admin-password "$MYSQL_ADMIN_PASSWORD" \
    --tier Burstable \
    --sku-name Standard_B1ms \
    --storage-size 32 \
    --backup-retention 1 \
    --version 8.0.21 \
    --public-access 0.0.0.0 \
    --tags "${tags[@]}" \
    --yes \
    --output table
fi

az mysql flexible-server db create \
  --resource-group "$AZ_RESOURCE_GROUP" \
  --server-name "$AZ_MYSQL_SERVER" \
  --database-name "$AZ_MYSQL_DATABASE" \
  --output table

# Necessário para a demonstração via ACI. O valor 0.0.0.0 permite recursos Azure;
# não abre indiscriminadamente todos os IPs da Internet.
az mysql flexible-server firewall-rule create \
  --resource-group "$AZ_RESOURCE_GROUP" \
  --name "$AZ_MYSQL_SERVER" \
  --rule-name AllowAzureServicesForSprint3 \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 0.0.0.0 \
  --output table

echo "[6/6] Recursos provisionados"
az resource list \
  --resource-group "$AZ_RESOURCE_GROUP" \
  --query '[].{Nome:name,Tipo:type,Regiao:location}' \
  --output table

echo "Provisionamento-base concluído. Execute 02_build_and_deploy.sh a partir da pasta predictfy-locaweb."
