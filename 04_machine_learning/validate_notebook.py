from __future__ import annotations

import json
import zipfile
from pathlib import Path

import nbformat


ROOT = Path(__file__).resolve().parent
NOTEBOOK = ROOT / "EC_Sprint_3_Predictfy_Predictfy_ML.ipynb"
ZIP_PATH = ROOT / "EmersonRM562033_Machine_Learning_Sprint3.zip"

required_terms = [
    "Análise Exploratória",
    "Engenharia de Features",
    "data leakage",
    "regressão",
    "validação",
    "Backtest",
    "vantagem",
    "Limitação",
    "ADF",
    "VIF",
    "baseline_mediana_3_semanas",
    "2025-10-01",
    "delta_semanal_d1",
    "outliers_do_alvo",
]

nb = nbformat.read(NOTEBOOK, as_version=4)
assert nb.cells, "Notebook vazio"
assert all(cell.cell_type in {"markdown", "code"} for cell in nb.cells)
assert not any(cell.cell_type == "code" and cell.get("outputs") is None for cell in nb.cells)

text = "\n".join(cell.source for cell in nb.cells)
for term in required_terms:
    assert term.lower() in text.lower(), f"Termo obrigatório ausente: {term}"

code_cells = [cell for cell in nb.cells if cell.cell_type == "code"]
assert all(cell.get("execution_count") is not None for cell in code_cells), "Há células de código não executadas"
errors = [
    output
    for cell in code_cells
    for output in cell.get("outputs", [])
    if output.get("output_type") == "error"
]
assert not errors, f"Notebook contém erros salvos: {errors}"
assert "train_test_split" not in text, "Split aleatório encontrado"
assert 'shift(1)' in text, "Janelas temporais sem evidência de shift(1)"
assert "não promover" in text.lower(), "Decisão de governança ausente"

with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED) as archive:
    archive.write(NOTEBOOK, NOTEBOOK.name)

with zipfile.ZipFile(ZIP_PATH) as archive:
    names = archive.namelist()
    assert names == [NOTEBOOK.name], f"Conteúdo inesperado no ZIP: {names}"
    archived = json.loads(archive.read(NOTEBOOK.name))
    assert archived["nbformat"] == 4

print(f"OK — {len(nb.cells)} células, {len(code_cells)} células de código executadas, sem erros")
print(f"OK — ZIP contém somente {NOTEBOOK.name}")
