"""Gera a entrada corporativa da Sprint 3 sem modificar o MVP de referência."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPRINT = HERE.parent
SOURCE = SPRINT.parents[1] / "locaweb" / "data" / "processed" / "incidents_features.csv"
DESTINATION = HERE / "incidentes_predictfy.csv"
MANIFEST = HERE / "manifest.json"
RULES = HERE / "regras_ola.txt"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    if not SOURCE.is_file():
        raise FileNotFoundError(f"Fonte não encontrada: {SOURCE}")

    with SOURCE.open(newline="", encoding="utf-8") as source, DESTINATION.open(
        "w", newline="", encoding="utf-8"
    ) as destination:
        reader = csv.DictReader(source)
        if not reader.fieldnames:
            raise ValueError("CSV de origem sem cabeçalho")
        writer = csv.DictWriter(destination, fieldnames=["source_row_number", *reader.fieldnames])
        writer.writeheader()
        row_count = 0
        for row_count, row in enumerate(reader, start=1):
            writer.writerow({"source_row_number": row_count, **row})

    manifest = {
        "source_relative": "locaweb/data/processed/incidents_features.csv",
        "destination": DESTINATION.name,
        "rows": row_count,
        "columns": len(reader.fieldnames) + 1,
        "source_sha256": sha256(SOURCE),
        "destination_sha256": sha256(DESTINATION),
        "rules_file": RULES.name,
        "rules_sha256": sha256(RULES),
        "contains_personal_data": False,
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Amostra gerada: {row_count} linhas em {DESTINATION}")


if __name__ == "__main__":
    main()
