#!/usr/bin/env bash
set -euo pipefail

required=(AZ_RESOURCE_GROUP AZ_CONTAINER_NAME AZ_BRIDGE_CONTAINER_NAME AZ_ACR_NAME AZ_MYSQL_SERVER AZ_LOG_WORKSPACE AZ_APP_INSIGHTS)
for name in "${required[@]}"; do
  [[ -n "${!name:-}" ]] || { echo "Variável obrigatória ausente: $name" >&2; exit 2; }
done

evidence_dir="${EVIDENCE_DIR:-Sprint 3/01_cloud/evidencias/azure}"
mkdir -p "$evidence_dir"

az resource list --resource-group "$AZ_RESOURCE_GROUP" \
  --query '[].{Nome:name,Tipo:type,Regiao:location}' --output json > "$evidence_dir/01_recursos.json"
az resource list --resource-group "$AZ_RESOURCE_GROUP" \
  --query '[].{Nome:name,Tipo:type,Regiao:location}' --output table > "$evidence_dir/01_recursos.txt"
az acr repository show-tags --name "$AZ_ACR_NAME" --repository predictfy-api --output json > "$evidence_dir/02_acr_api_tags.json"
az acr repository show-tags --name "$AZ_ACR_NAME" --repository predictfy-mysql-bridge --output json > "$evidence_dir/03_acr_bridge_tags.json"
az container show --resource-group "$AZ_RESOURCE_GROUP" --name "$AZ_CONTAINER_NAME" \
  --query '{Nome:name,Estado:instanceView.state,FQDN:ipAddress.fqdn,IP:ipAddress.ip,Imagem:containers[0].image,CPU:containers[0].resources.requests.cpu,MemoriaGB:containers[0].resources.requests.memoryInGb}' \
  --output json > "$evidence_dir/04_aci_api.json"
az container show --resource-group "$AZ_RESOURCE_GROUP" --name "$AZ_BRIDGE_CONTAINER_NAME" \
  --query '{Nome:name,Estado:instanceView.state,FQDN:ipAddress.fqdn,IP:ipAddress.ip,Imagem:containers[0].image,CPU:containers[0].resources.requests.cpu,MemoriaGB:containers[0].resources.requests.memoryInGb}' \
  --output json > "$evidence_dir/05_aci_bridge.json"
az mysql flexible-server show --resource-group "$AZ_RESOURCE_GROUP" --name "$AZ_MYSQL_SERVER" \
  --query '{Nome:name,Estado:state,FQDN:fullyQualifiedDomainName,Versao:version,Tier:sku.tier,SKU:sku.name,StorageGB:storage.storageSizeGb,RetencaoDias:backup.backupRetentionDays,GeoBackup:backup.geoRedundantBackup}' \
  --output json > "$evidence_dir/06_mysql.json"
az monitor log-analytics workspace show --resource-group "$AZ_RESOURCE_GROUP" --workspace-name "$AZ_LOG_WORKSPACE" \
  --query '{Nome:name,Estado:provisioningState,RetencaoDias:retentionInDays,Regiao:location}' --output json > "$evidence_dir/07_log_analytics.json"
az monitor app-insights component show --resource-group "$AZ_RESOURCE_GROUP" --app "$AZ_APP_INSIGHTS" \
  --query '{Nome:name,Estado:provisioningState,Tipo:applicationType,Regiao:location}' --output json > "$evidence_dir/08_application_insights.json"
az container logs --resource-group "$AZ_RESOURCE_GROUP" --name "$AZ_CONTAINER_NAME" > "$evidence_dir/09_api_logs.txt"
az container logs --resource-group "$AZ_RESOURCE_GROUP" --name "$AZ_BRIDGE_CONTAINER_NAME" > "$evidence_dir/10_bridge_logs.txt"
workspace_id="$(az monitor log-analytics workspace show --resource-group "$AZ_RESOURCE_GROUP" --workspace-name "$AZ_LOG_WORKSPACE" --query customerId --output tsv)"
az monitor log-analytics query --workspace "$workspace_id" \
  --analytics-query "ContainerInstanceLog_CL | where TimeGenerated > ago(2h) | project TimeGenerated, ContainerGroup_s, Message | order by TimeGenerated desc | take 100" \
  --output json > "$evidence_dir/11_log_analytics_query.json"

api_id="$(az container show --resource-group "$AZ_RESOURCE_GROUP" --name "$AZ_CONTAINER_NAME" --query id --output tsv)"
bridge_id="$(az container show --resource-group "$AZ_RESOURCE_GROUP" --name "$AZ_BRIDGE_CONTAINER_NAME" --query id --output tsv)"
mysql_id="$(az mysql flexible-server show --resource-group "$AZ_RESOURCE_GROUP" --name "$AZ_MYSQL_SERVER" --query id --output tsv)"
az monitor metrics list --resource "$api_id" --metric CpuUsage MemoryUsage \
  --interval PT1M --aggregation Average --output json > "$evidence_dir/12_metricas_aci_api.json"
az monitor metrics list --resource "$bridge_id" --metric CpuUsage MemoryUsage \
  --interval PT1M --aggregation Average --output json > "$evidence_dir/13_metricas_aci_bridge.json"
az monitor metrics list --resource "$mysql_id" --metric cpu_percent memory_percent active_connections Com_insert Com_select \
  --interval PT1M --aggregation Average --output json > "$evidence_dir/14_metricas_mysql.json"
az monitor app-insights query --resource-group "$AZ_RESOURCE_GROUP" --app "$AZ_APP_INSIGHTS" \
  --analytics-query "union withsource=Tabela dependencies, exceptions, customMetrics | where timestamp > ago(2h) | summarize Registros=count() by Tabela | order by Tabela asc" \
  --output json > "$evidence_dir/15_app_insights_telemetria.json"
date -u '+%Y-%m-%dT%H:%M:%SZ' > "$evidence_dir/COLETADO_EM_UTC.txt"
echo "Evidências CLI salvas em $evidence_dir"
