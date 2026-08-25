"""Validação local sem Azure, Docker daemon ou dependências do bridge."""

from __future__ import annotations

import ast
import json
import subprocess
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[1]


def check_drawio() -> None:
    root = ET.parse(ROOT / "arquitetura_predictfy_azure.drawio").getroot()
    assert root.tag == "mxfile"
    text = " ".join(cell.attrib.get("value", "") for cell in root.findall(".//mxCell"))
    for term in ("Resource Group", "Container Registry", "MySQL", "Log Analytics", "Application Insights"):
        assert term in text, f"Componente ausente no Draw.io: {term}"
    assert "ACI" in text or "Container Instances" in text, "Componente ACI/Container Instances ausente no Draw.io"


def check_shell() -> None:
    scripts = sorted((ROOT / "iac").glob("*.sh"))
    assert len(scripts) >= 5
    subprocess.run(["bash", "-n", *map(str, scripts)], check=True)


def check_docker_context() -> None:
    dockerfile = (ROOT / "app_mysql" / "Dockerfile").read_text()
    referenced = [
        "Sprint 3/01_cloud/app_mysql/requirements.txt",
        "Sprint 3/01_cloud/app_mysql/main.py",
        "Sprint 3/01_cloud/app_mysql/schema.sql",
        "locaweb/outputs/previsoes_baseline.json",
        "locaweb/outputs/comparacao_modelos.json",
        "locaweb/outputs/model_registry.json",
    ]
    for relative in referenced:
        assert relative in dockerfile
        assert (PROJECT / relative).is_file(), f"Arquivo do build ausente: {relative}"


def load_extract_forecast():
    source = (ROOT / "app_mysql" / "main.py").read_text()
    tree = ast.parse(source)
    function = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "extract_forecast")
    namespace: dict = {}
    exec(compile(ast.Module(body=[function], type_ignores=[]), "extract_forecast", "exec"), namespace)
    return namespace["extract_forecast"]


def check_current_artifact() -> None:
    artifact = PROJECT / "locaweb" / "outputs" / "previsoes_baseline.json"
    payload = json.loads(artifact.read_text())
    extract = load_extract_forecast()
    for horizon in range(1, 8):
        values = [extract(payload, segment, horizon)[1] for segment in ("total", "p2", "p3")]
        assert all(isinstance(value, float) and value >= 0 for value in values)


def check_report_coverage() -> None:
    report = (ROOT / "RELATORIO_ENTREGA.md").read_text().lower()
    for term in ("arquitetura", "provisionamento", "container", "machine learning", "mysql", "monitoramento", "chatbot", "administração", "operações"):
        assert term in report, f"Seção/tema ausente no relatório: {term}"


def main() -> None:
    checks = [check_drawio, check_shell, check_docker_context, check_current_artifact, check_report_coverage]
    for check in checks:
        check()
        print(f"OK {check.__name__}")
    print("Pacote Cloud validado localmente.")


if __name__ == "__main__":
    main()
