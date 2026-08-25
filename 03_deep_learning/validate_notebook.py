from __future__ import annotations

import json
import zipfile
from pathlib import Path

import nbformat


ROOT = Path(__file__).resolve().parent
NOTEBOOK = ROOT / "EC_Sprint_3_Predictfy_Predictfy_DeepL.ipynb"
ZIP_PATH = ROOT / "EmersonRM562033_Deep_Learning_Sprint3.zip"
AUDIT_PATH = ROOT / "scientific_audit.json"
ARTIFACT_DIR = ROOT / "artifacts"

REQUIRED_TERMS = [
    "Pré-processamento para ANN",
    "Avaliação da clusterização",
    "Implementação e treinamento",
    "Avaliação de desempenho",
    "prever_risco",
    "shadow mode",
    "PR-AUC",
    "EDA ampliada e descoberta de padrões",
    "Diagnóstico ampliado do modelo",
    "taxa_categoria_inedita",
    "bootstrap_metrics",
    "Otimização retrospectiva controlada",
    "rolling_folds",
    "threshold_search_df",
    "Estratégias para classe rara",
    "FocalLoss",
    "train_pairwise_ranker",
    "Políticas por prioridade e fila diária",
]


def main() -> None:
    notebook = nbformat.read(NOTEBOOK, as_version=4)
    nbformat.validate(notebook)
    text = "\n".join("".join(cell.get("source", "")) for cell in notebook.cells)
    missing = [term for term in REQUIRED_TERMS if term not in text]
    if missing:
        raise AssertionError(f"Termos obrigatórios ausentes: {missing}")

    code_cells = [cell for cell in notebook.cells if cell.cell_type == "code"]
    not_executed = [i for i, cell in enumerate(code_cells) if cell.execution_count is None]
    errors = [
        output
        for cell in code_cells
        for output in cell.get("outputs", [])
        if output.get("output_type") == "error"
    ]
    if not_executed:
        raise AssertionError(f"Células de código não executadas: {not_executed}")
    if errors:
        raise AssertionError(f"Notebook contém {len(errors)} erro(s) salvo(s)")
    saved_outputs = "\n".join(
        str(output.get("text", "")) + str(output.get("data", {}).get("text/plain", ""))
        for cell in code_cells
        for output in cell.get("outputs", [])
    )
    if "FALHOU: deveria rejeitar" in saved_outputs:
        raise AssertionError("Um teste negativo do contrato do MVP não rejeitou a entrada")

    audit = json.loads(AUDIT_PATH.read_text(encoding="utf-8"))
    checks = {key: value for key, value in audit.items() if key != "artifact_files"}
    failed_checks = [key for key, value in checks.items() if value is not True]
    if failed_checks:
        raise AssertionError(f"Auditorias científicas falharam: {failed_checks}")
    required_artifacts = {"ann_ensemble.pt", "manifest.json", "preprocessor.pkl", "xgboost_pareado.pkl"}
    actual_artifacts = {path.name for path in ARTIFACT_DIR.iterdir() if path.is_file()}
    if not required_artifacts <= actual_artifacts:
        raise AssertionError(f"Artefatos ausentes: {sorted(required_artifacts - actual_artifacts)}")

    with zipfile.ZipFile(ZIP_PATH) as archive:
        names = archive.namelist()
    if names != [NOTEBOOK.name]:
        raise AssertionError(f"Conteúdo inválido do ZIP: {names}")

    json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    print(
        f"OK — notebook válido, {len(notebook.cells)} células, "
        f"{len(code_cells)} células executadas, auditorias científicas aprovadas "
        "e ZIP com arquivo único."
    )


if __name__ == "__main__":
    main()
