#!/usr/bin/env bash
set -euo pipefail

: "${AZ_RESOURCE_GROUP:?Variável AZ_RESOURCE_GROUP obrigatória}"
evidence_marker="${EVIDENCE_MARKER:-Sprint 3/01_cloud/evidencias/azure/EVIDENCIAS_COLETADAS.ok}"

case "$AZ_RESOURCE_GROUP" in
  rg-predictfy-sprint3-*) ;;
  *) echo "Recusa: Resource Group fora do padrão seguro." >&2; exit 2 ;;
esac

[[ -f "$evidence_marker" ]] || {
  echo "Recusa: marcador de evidências ausente: $evidence_marker" >&2
  exit 2
}

az resource list --resource-group "$AZ_RESOURCE_GROUP" \
  --query '[].{Nome:name,Tipo:type,Regiao:location}' --output table
az group delete --name "$AZ_RESOURCE_GROUP" --yes

if [[ "$(az group exists --name "$AZ_RESOURCE_GROUP")" == "false" ]]; then
  echo "CONFIRMADO: Resource Group removido e recursos encerrados."
else
  echo "Falha: Resource Group ainda existe." >&2
  exit 1
fi
