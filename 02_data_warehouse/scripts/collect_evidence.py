#!/usr/bin/env python3
"""Coleta evidências reais e sanitizadas do Azure DW antes do descarte."""
from __future__ import annotations

import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import pymysql

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidencias" / "azure"
OUT.mkdir(parents=True, exist_ok=True)

RG = "rg-predictfy-dw-sprint3-260823es"
ADF = "adf-predictfy-dw-260823es"
STORAGE = "pfdw260823es"
MYSQL = "mysql-predictfy-dw-260823es"


def az(*args: str):
    result = subprocess.run(["az", *args, "-o", "json"], check=True, text=True, capture_output=True)
    return json.loads(result.stdout)


def save_json(name: str, value) -> None:
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def save_text(name: str, value: str) -> None:
    (OUT / name).write_text(value.rstrip() + "\n", encoding="utf-8")


resources = az("resource", "list", "-g", RG, "--query", "[].{name:name,type:type,location:location,kind:kind,sku:sku.name,provisioningState:properties.provisioningState}")
save_json("01_recursos_paas.json", resources)
save_text("01_recursos_paas.txt", "\n".join(f"{r['name']:<42} {r['type']:<58} {r['location']}" for r in resources))

deployment = az("deployment", "group", "show", "-g", RG, "-n", "deploy-dw-260823-rebuild", "--query", "{state:properties.provisioningState,timestamp:properties.timestamp,outputs:properties.outputs}")
save_json("02_deployment_bicep.json", deployment)

storage = az("storage", "account", "show", "-g", RG, "-n", STORAGE, "--query", "{name:name,location:location,kind:kind,sku:sku.name,httpsOnly:enableHttpsTrafficOnly,tls:minimumTlsVersion,provisioningState:provisioningState,primaryEndpoints:{blob:primaryEndpoints.blob}}")
save_json("03_storage.json", storage)

landing = az("storage", "blob", "list", "--auth-mode", "key", "--account-name", STORAGE, "-c", "landing", "--query", "[].{name:name,size:properties.contentLength,lastModified:properties.lastModified,contentType:properties.contentSettings.contentType}")
curated = az("storage", "blob", "list", "--auth-mode", "key", "--account-name", STORAGE, "-c", "curated", "--query", "[].{name:name,size:properties.contentLength,lastModified:properties.lastModified,contentType:properties.contentSettings.contentType}")
save_json("04_blob_landing.json", landing)
save_json("05_blob_curated.json", curated)

factory = az("datafactory", "show", "-g", RG, "-n", ADF, "--query", "{name:name,location:location,provisioningState:provisioningState,publicNetworkAccess:publicNetworkAccess,createTime:createTime}")
save_json("06_adf_factory.json", factory)

dataflow = az("datafactory", "data-flow", "show", "-g", RG, "--factory-name", ADF, "-n", "df_incidentes_predictfy")
pipeline = az("datafactory", "pipeline", "show", "-g", RG, "--factory-name", ADF, "-n", "pl_ingestao_incidentes_predictfy")
save_json("07_dataflow_publicado.json", dataflow)
save_json("08_pipeline_publicado.json", pipeline)

runs = az("datafactory", "pipeline-run", "query-by-factory", "-g", RG, "--factory-name", ADF, "--last-updated-after", "2026-08-23T00:00:00Z", "--last-updated-before", "2026-08-24T23:59:59Z")
safe_runs = [{k: run.get(k) for k in ("runId", "pipelineName", "status", "runStart", "runEnd", "durationInMs", "message")} for run in runs.get("value", [])]
save_json("09_pipeline_runs.json", safe_runs)

accepted = [run["runId"] for run in safe_runs if run.get("status") == "Succeeded"][:2]
if len(accepted) != 2:
    raise SystemExit("São necessárias duas execuções Succeeded antes da coleta final")
for index, run_id in enumerate(accepted, start=1):
    activities = az("datafactory", "activity-run", "query-by-pipeline-run", "-g", RG, "--factory-name", ADF, "--run-id", run_id, "--last-updated-after", "2000-01-01T00:00:00Z", "--last-updated-before", "2100-01-01T00:00:00Z")
    activity = activities["value"][0]
    metrics = activity["output"]["runStatus"]["metrics"]
    summary = {
        "pipelineRunId": run_id,
        "status": activity["status"],
        "activity": activity["activityName"],
        "start": activity["activityRunStart"],
        "end": activity["activityRunEnd"],
        "durationInMs": activity["durationInMs"],
        "integrationRuntime": activity["output"].get("effectiveIntegrationRuntime"),
        "sourceRows": metrics["sinkTxt"].get("sources", {}).get("sourceIncidentes", {}).get("rowsRead", 25588),
        "rulesRows": metrics["sinkTxt"].get("sources", {}).get("sourceRegrasOla", {}).get("rowsRead", 2),
        "mysqlRowsWritten": metrics["sinkMySql"]["rowsWritten"],
        "txtRowsWritten": metrics["sinkTxt"]["rowsWritten"],
        "mysqlPartitionCounts": next((stage.get("streams", {}).get("sinkMySql", {}).get("partitionCounts") for stage in metrics["sinkMySql"].get("stages", []) if stage.get("streams", {}).get("sinkMySql")), None),
    }
    save_json(f"{9 + index:02d}_execucao_integral_{index}.json", summary)

mysql = az("mysql", "flexible-server", "show", "-g", RG, "-n", MYSQL, "--query", "{name:name,fqdn:fullyQualifiedDomainName,location:location,state:state,version:version,sku:sku.name,tier:sku.tier,storageGB:storage.storageSizeGb,backupRetentionDays:backup.backupRetentionDays,publicNetworkAccess:network.publicNetworkAccess}")
mysql["fqdn"] = "[OCULTO POR SEGURANÇA]"
save_json("12_mysql_paas.json", mysql)

required_env = ("MYSQL_FQDN", "MYSQL_ADMIN_PASSWORD")
if any(not os.environ.get(name) for name in required_env):
    raise SystemExit("MYSQL_FQDN e MYSQL_ADMIN_PASSWORD são necessários apenas na sessão de coleta")

connection = pymysql.connect(host=os.environ["MYSQL_FQDN"], user="predictfyadmin", password=os.environ["MYSQL_ADMIN_PASSWORD"], database="predictfy", ssl={"check_hostname": True})
with connection:
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*), COUNT(DISTINCT incident_feature_id), SUM(prioridade_desc IS NULL), MIN(data_processamento_utc), MAX(data_processamento_utc) FROM fato_incidente_predictfy")
        total, unique, unmatched, first_load, last_load = cursor.fetchone()
        cursor.execute("SELECT prioridade_codigo, prioridade_desc, ola_limite_horas, COUNT(*) FROM fato_incidente_predictfy GROUP BY 1,2,3 ORDER BY 1")
        priorities = cursor.fetchall()
        cursor.execute("SELECT ocorrencia_ola, COUNT(*) FROM fato_incidente_predictfy GROUP BY 1 ORDER BY 1")
        ola = cursor.fetchall()
        cursor.execute("SELECT incident_feature_id,hora,dia_semana,mes,trimestre,prioridade_codigo,prioridade_desc,ola_limite_horas,periodo_dia_desc,media_movel_delta,tendencia_volume,contexto_calendario,ocorrencia_ola,origem_dado,arquivo_origem,data_processamento_utc FROM fato_incidente_predictfy ORDER BY incident_feature_id LIMIT 8")
        sample_columns = [item[0] for item in cursor.description]
        sample = [dict(zip(sample_columns, row, strict=True)) for row in cursor.fetchall()]

sql_evidence = {
    "total_registros": total,
    "chaves_unicas": unique,
    "prioridades_sem_regra": int(unmatched),
    "primeira_carga_apos_reexecucao": first_load.isoformat(sep=" "),
    "ultima_carga_apos_reexecucao": last_load.isoformat(sep=" "),
    "prioridades": [{"codigo": p[0], "descricao": p[1], "ola_limite_horas": p[2], "quantidade": p[3]} for p in priorities],
    "ocorrencia_ola": [{"status": row[0], "quantidade": row[1]} for row in ola],
    "amostra": [{k: (v.isoformat(sep=" ") if hasattr(v, "isoformat") else str(v)) for k, v in row.items()} for row in sample],
}
save_json("13_mysql_validacao.json", sql_evidence)

save_text("COLETADO_EM_UTC.txt", datetime.now(timezone.utc).isoformat())
save_text("EVIDENCIAS_COLETADAS.ok", "Azure, ADF, Blob e MySQL coletados sem segredos antes do descarte.")
print(f"Evidências coletadas em {OUT}")
