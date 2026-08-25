#!/usr/bin/env bash
set -euo pipefail

# Uso: executar a partir de predictfy-locaweb ou informar PREDICTFY_SOURCE_DIR.
source_dir="${PREDICTFY_SOURCE_DIR:-locaweb}"

required=(
  AZ_RESOURCE_GROUP AZ_ACR_NAME AZ_CONTAINER_NAME AZ_DNS_LABEL AZ_LOG_WORKSPACE
  AZ_APP_INSIGHTS CHAT_SESSION_SECRET ENTRA_API_CLIENT_ID ENTRA_SPA_CLIENT_ID
  CORS_ALLOWED_ORIGINS
)
for name in "${required[@]}"; do
  if [[ -z "${!name:-}" ]]; then
    echo "Variável obrigatória ausente: $name" >&2
    exit 2
  fi
done

if [[ ! -f "$source_dir/api/Dockerfile" || ! -f "$source_dir/api/main.py" ]]; then
  echo "Fonte somente leitura não localizada em: $source_dir" >&2
  exit 2
fi

image_tag="predictfy-api:${PREDICTFY_IMAGE_TAG:-sprint3}"

echo "[1/4] Build remoto no ACR"
if [[ "${SKIP_ACR_BUILD:-false}" == "true" ]]; then
  echo "Imagem existente será reutilizada: $image_tag"
else
  az acr build \
    --registry "$AZ_ACR_NAME" \
    --image "$image_tag" \
    --file "$source_dir/api/Dockerfile" \
    "$source_dir"
fi

login_server="$(az acr show --name "$AZ_ACR_NAME" --query loginServer --output tsv)"
acr_username="$(az acr credential show --name "$AZ_ACR_NAME" --query username --output tsv)"
acr_password="$(az acr credential show --name "$AZ_ACR_NAME" --query 'passwords[0].value' --output tsv)"
workspace_id="$(az monitor log-analytics workspace show --resource-group "$AZ_RESOURCE_GROUP" --workspace-name "$AZ_LOG_WORKSPACE" --query customerId --output tsv)"
workspace_key="$(az monitor log-analytics workspace get-shared-keys --resource-group "$AZ_RESOURCE_GROUP" --workspace-name "$AZ_LOG_WORKSPACE" --query primarySharedKey --output tsv)"
app_insights_connection="$(az monitor app-insights component show --resource-group "$AZ_RESOURCE_GROUP" --app "$AZ_APP_INSIGHTS" --query connectionString --output tsv)"

echo "[2/4] Remoção controlada somente do ACI anterior com o mesmo nome"
if az container show --resource-group "$AZ_RESOURCE_GROUP" --name "$AZ_CONTAINER_NAME" >/dev/null 2>&1; then
  az container delete --resource-group "$AZ_RESOURCE_GROUP" --name "$AZ_CONTAINER_NAME" --yes
fi

echo "[3/4] Deploy do container"
az container create \
  --resource-group "$AZ_RESOURCE_GROUP" \
  --name "$AZ_CONTAINER_NAME" \
  --image "${login_server}/${image_tag}" \
  --registry-login-server "$login_server" \
  --registry-username "$acr_username" \
  --registry-password "$acr_password" \
  --os-type Linux \
  --cpu 1 \
  --memory 2 \
  --ports 8000 \
  --ip-address Public \
  --dns-name-label "$AZ_DNS_LABEL" \
  --restart-policy Always \
  --log-analytics-workspace "$workspace_id" \
  --log-analytics-workspace-key "$workspace_key" \
  --environment-variables \
    CHAT_LLM_PROVIDER=openai \
    OPENAI_MODEL=gpt-5.6-luna \
    CHAT_ALLOW_LOCAL_DEV=false \
    ENTRA_TENANT_ID=common \
    ENTRA_API_CLIENT_ID="$ENTRA_API_CLIENT_ID" \
    ENTRA_SPA_CLIENT_ID="$ENTRA_SPA_CLIENT_ID" \
    ENTRA_REQUIRED_SCOPE=access_as_user \
    CORS_ALLOWED_ORIGINS="$CORS_ALLOWED_ORIGINS" \
    APPLICATIONINSIGHTS_CONNECTION_STRING="$app_insights_connection" \
  --secure-environment-variables \
    CHAT_SESSION_SECRET="$CHAT_SESSION_SECRET" \
    OPENAI_API_KEY="${OPENAI_API_KEY:-}" \
  --output table

echo "[4/4] Endpoint"
fqdn="$(az container show --resource-group "$AZ_RESOURCE_GROUP" --name "$AZ_CONTAINER_NAME" --query ipAddress.fqdn --output tsv)"
echo "API: http://${fqdn}:8000/api/health"
echo "Observação: para produção, publicar atrás de uma camada HTTPS."
