#!/usr/bin/env bash
set -euo pipefail

required=(AZ_RESOURCE_GROUP AZ_CONTAINER_NAME AZ_ACR_NAME AZ_MYSQL_SERVER AZ_LOG_WORKSPACE AZ_APP_INSIGHTS)
for name in "${required[@]}"; do
  [[ -n "${!name:-}" ]] || { echo "Variável obrigatória ausente: $name" >&2; exit 2; }
done

echo "Recursos"
az resource list --resource-group "$AZ_RESOURCE_GROUP" --query '[].{Nome:name,Tipo:type,Regiao:location}' --output table

echo "Imagem ACR"
az acr repository show-tags --name "$AZ_ACR_NAME" --repository predictfy-api --output table

echo "Container"
az container show --resource-group "$AZ_RESOURCE_GROUP" --name "$AZ_CONTAINER_NAME" \
  --query '{Estado:instanceView.state,FQDN:ipAddress.fqdn,IP:ipAddress.ip,Imagem:containers[0].image}' --output table

fqdn="$(az container show --resource-group "$AZ_RESOURCE_GROUP" --name "$AZ_CONTAINER_NAME" --query ipAddress.fqdn --output tsv)"
curl --fail --show-error --max-time 20 "http://${fqdn}:8000/api/health"

echo
echo "MySQL"
az mysql flexible-server show --resource-group "$AZ_RESOURCE_GROUP" --name "$AZ_MYSQL_SERVER" \
  --query '{Estado:state,FQDN:fullyQualifiedDomainName,Versao:version,BackupDias:backup.backupRetentionDays}' --output table

echo "Monitoramento"
az monitor log-analytics workspace show --resource-group "$AZ_RESOURCE_GROUP" --workspace-name "$AZ_LOG_WORKSPACE" \
  --query '{Nome:name,Estado:provisioningState,Retencao:retentionInDays}' --output table
az monitor app-insights component show --resource-group "$AZ_RESOURCE_GROUP" --app "$AZ_APP_INSIGHTS" \
  --query '{Nome:name,Estado:provisioningState,Tipo:applicationType}' --output table
