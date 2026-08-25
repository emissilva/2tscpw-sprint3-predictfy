"""Validação estática do pacote Data Warehouse da Sprint 3."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main() -> None:
    required = [
        "ARQUITETURA.md", "arquitetura_ingestao.drawio", "MAPEAMENTO_DADOS.md",
        "MATRIZ_REQUISITOS.md", "RELATORIO_ENTREGA.md", "REUSO_01_CLOUD.md",
        "colunas_derivadas.txt", "sql/001_schema.sql", "sql/002_validacao.sql",
        "iac/main.bicep", "adf/dataflow/df_incidentes_predictfy.json",
        "adf/pipeline/pl_ingestao_incidentes_predictfy.json",
        "data/incidentes_predictfy.csv", "data/regras_ola.txt", "data/manifest.json",
    ]
    missing = [name for name in required if not (ROOT / name).is_file()]
    if missing:
        raise AssertionError(f"Arquivos ausentes: {missing}")

    json_files = list((ROOT / "adf").rglob("*.json")) + [ROOT / "data/manifest.json"]
    for path in json_files:
        json.loads(path.read_text(encoding="utf-8"))

    manifest = json.loads((ROOT / "data/manifest.json").read_text(encoding="utf-8"))
    with (ROOT / "data/incidentes_predictfy.csv").open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        rows = sum(1 for _ in reader)
        columns = set(reader.fieldnames or [])
    expected = {"source_row_number", "hora", "dia_semana", "rolling_7d", "rolling_30d", "target_ola"}
    assert expected <= columns, f"Colunas ausentes: {expected - columns}"
    assert rows == manifest["rows"] and rows >= 1000, "Amostra ou manifesto inconsistente"
    csv_hash = hashlib.sha256((ROOT / "data/incidentes_predictfy.csv").read_bytes()).hexdigest()
    assert csv_hash == manifest["destination_sha256"], "SHA-256 da amostra diverge do manifesto"
    rules_hash = hashlib.sha256((ROOT / "data/regras_ola.txt").read_bytes()).hexdigest()
    assert rules_hash == manifest["rules_sha256"], "SHA-256 das regras diverge do manifesto"

    rules = list(csv.DictReader((ROOT / "data/regras_ola.txt").open(encoding="utf-8"), delimiter="|"))
    assert {row["prioridade_codigo"] for row in rules} == {"P2", "P3"}, "Regras OLA incompletas"
    assert {row["ola_limite_horas"] for row in rules} == {"4", "12"}, "Limites OLA incorretos"

    derivations = (ROOT / "colunas_derivadas.txt").read_text(encoding="utf-8")
    for name in ("incident_feature_id", "ocorrencia_ola", "tendencia_volume", "data_processamento_utc"):
        assert name in derivations

    dataflow = json.loads((ROOT / "adf/dataflow/df_incidentes_predictfy.json").read_text(encoding="utf-8"))
    script = "\n".join(dataflow["properties"]["typeProperties"]["scriptLines"])
    for token in ("joinType:'left'", "alterRow(upsertIf(true()))", "sinkMySql", "sinkTxt"):
        assert token in script, f"Contrato ausente no Data Flow: {token}"
    mysql_ls = (ROOT / "adf/linkedService/ls_mysql_predictfy.json").read_text(encoding="utf-8")
    publisher = (ROOT / "scripts/publish_adf.sh").read_text(encoding="utf-8")
    assert "SecureString" in mysql_ls and "__INJECTED_AT_PUBLISH__" in mysql_ls
    assert "MYSQL_CONNECTION_STRING" in publisher and "STORAGE_BLOB_ENDPOINT" in publisher

    import xml.etree.ElementTree as ET
    diagram = ET.parse(ROOT / "arquitetura_ingestao.drawio")
    assert diagram.getroot().tag == "mxfile", "Draw.io inválido"
    print(f"Pacote Data Warehouse validado localmente: {rows} registros, {len(json_files)} JSONs.")


if __name__ == "__main__":
    main()
