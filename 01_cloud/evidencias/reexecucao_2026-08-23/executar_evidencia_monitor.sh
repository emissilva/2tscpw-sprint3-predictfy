#!/usr/bin/env bash
set -euo pipefail

group="rg-predictfy-sprint3-260823es"
workspace="log-predictfy-sprint3"
appi="appi-predictfy-sprint3"
workspace_id="$(az monitor log-analytics workspace show -g "$group" -n "$workspace" --query customerId -o tsv)"

case "${1:-}" in
  logs)
    echo "PREDICTFY — LOG ANALYTICS / KQL"
    echo
    echo 'ContainerInstanceLog_CL | where TimeGenerated > ago(1h)'
    echo '| where Message has_any ("capture", "executions", "health")'
    echo '| project TimeGenerated, ContainerGroup_s, Message'
    echo
    az monitor log-analytics query -w "$workspace_id" \
      --analytics-query 'ContainerInstanceLog_CL | where TimeGenerated > ago(1h) | where Message has_any ("capture", "executions", "health") | project TimeGenerated, ContainerGroup_s, Message | order by TimeGenerated desc | take 15' \
      --query '[].{UTC:TimeGenerated,Container:ContainerGroup_s,Mensagem:Message}' -o table
    ;;
  appi)
    echo "PREDICTFY — APPLICATION INSIGHTS / OPENTELEMETRY"
    echo
    echo 'union withsource=Tabela requests, dependencies, exceptions, customMetrics'
    echo '| where timestamp > ago(1h) | summarize Registros=count() by Tabela'
    echo
    az monitor app-insights query -g "$group" --app "$appi" \
      --analytics-query 'union withsource=Tabela requests, dependencies, exceptions, customMetrics | where timestamp > ago(1h) | summarize Registros=count() by Tabela | order by Tabela asc' \
      --query 'tables[0].rows' -o table
    ;;
  *) echo "Uso: $0 logs|appi" >&2; exit 2 ;;
esac
