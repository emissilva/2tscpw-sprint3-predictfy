"""Bridge acadêmico: lê um artefato governado do Predictfy e audita a execução no MySQL.

Este serviço é isolado do MVP para preservar o repositório online. Ele não armazena
prompts, tokens Entra, chaves da OpenAI ou dados pessoais.
"""

from __future__ import annotations

import hashlib
import json
import os
import secrets
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

import mysql.connector
from fastapi import Depends, FastAPI, Header, HTTPException, Query, status
from pydantic import BaseModel, Field

if os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING"):
    from azure.monitor.opentelemetry import configure_azure_monitor

    configure_azure_monitor()

OUTPUT_DIR = Path(os.getenv("PREDICTFY_OUTPUT_DIR", "/app/outputs"))
BASELINE_FILE = OUTPUT_DIR / "previsoes_baseline.json"
SCHEMA_FILE = Path(os.getenv("PREDICTFY_SCHEMA_FILE", "/app/schema.sql"))

app = FastAPI(
    title="Predictfy Cloud Evidence Bridge",
    version="1.0.0",
    description="Demonstra consumo de artefato ML e persistência no Azure MySQL.",
)


class CaptureRequest(BaseModel):
    horizonte: int = Field(default=1, ge=1, le=7)
    segmento: str = Field(default="total", pattern="^(total|p2|p3)$")


class CaptureResponse(BaseModel):
    correlation_id: str
    modelo: str
    horizonte: str
    segmento: str
    valor_previsto: float
    origem_artefato: str
    artefato_sha256: str
    executado_em_utc: datetime


def require_bridge_key(x_bridge_key: str | None = Header(default=None)) -> None:
    expected = os.getenv("BRIDGE_API_KEY", "")
    if not expected:
        raise HTTPException(status_code=503, detail="BRIDGE_API_KEY não configurada.")
    if not x_bridge_key or not secrets.compare_digest(x_bridge_key, expected):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Chave inválida.")


def mysql_config() -> dict[str, Any]:
    required = {
        "host": os.getenv("MYSQL_HOST"),
        "user": os.getenv("MYSQL_USER"),
        "password": os.getenv("MYSQL_PASSWORD"),
        "database": os.getenv("MYSQL_DATABASE", "predictfy"),
    }
    missing = [key for key, value in required.items() if not value]
    if missing:
        raise RuntimeError(f"Configuração MySQL ausente: {', '.join(missing)}")
    return {
        **required,
        "port": int(os.getenv("MYSQL_PORT", "3306")),
        "ssl_disabled": False,
        "connection_timeout": 10,
        "autocommit": False,
    }


@contextmanager
def db_connection() -> Iterator[Any]:
    connection = mysql.connector.connect(**mysql_config())
    try:
        yield connection
    finally:
        connection.close()


def load_baseline(path: Path = BASELINE_FILE) -> tuple[dict[str, Any], str]:
    raw = path.read_bytes()
    return json.loads(raw), hashlib.sha256(raw).hexdigest()


def extract_forecast(payload: dict[str, Any], segmento: str, horizonte: int) -> tuple[str, float]:
    """Normaliza o snapshot sem assumir apenas uma única versão de chave."""
    # Contrato atual do baseline: `serie` contém D+1..D+7 e colunas total/P2/P3.
    current_series = payload.get("serie")
    if isinstance(current_series, list) and len(current_series) >= horizonte:
        point = current_series[horizonte - 1]
        segment_key = segmento if segmento == "total" else segmento.upper()
        if isinstance(point, dict) and segment_key in point:
            return str(payload.get("modelo", "baseline_sazonal_7d")), float(point[segment_key])

    # Compatibilidade defensiva com snapshots estruturados por segmento.
    series = payload.get(segmento) or payload.get(segmento.upper())
    if not isinstance(series, dict):
        raise ValueError(f"Segmento ausente no artefato: {segmento}")

    predictions = series.get("previsoes") or series.get("forecast") or series.get("valores")
    if isinstance(predictions, list) and len(predictions) >= horizonte:
        point = predictions[horizonte - 1]
        if isinstance(point, dict):
            for key in ("yhat", "previsao", "valor", "total"):
                if key in point:
                    return str(payload.get("modelo", "baseline_sazonal_7d")), float(point[key])
        return str(payload.get("modelo", "baseline_sazonal_7d")), float(point)

    for key in (f"d{horizonte}", f"D+{horizonte}", str(horizonte)):
        if key in series:
            point = series[key]
            if isinstance(point, dict):
                point = point.get("previsao", point.get("yhat", point.get("valor")))
            return str(payload.get("modelo", "baseline_sazonal_7d")), float(point)

    raise ValueError(f"Horizonte D+{horizonte} ausente no artefato.")


def ensure_schema() -> None:
    statements = [part.strip() for part in SCHEMA_FILE.read_text().split(";") if part.strip()]
    with db_connection() as connection:
        cursor = connection.cursor()
        try:
            for statement in statements:
                cursor.execute(statement)
            connection.commit()
        finally:
            cursor.close()


@app.get("/health")
def health() -> dict[str, Any]:
    artifact_ok = BASELINE_FILE.is_file()
    database_ok = False
    database_error = None
    try:
        with db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT 1")
            database_ok = cursor.fetchone() == (1,)
            cursor.close()
    except Exception as exc:  # health expõe somente o tipo, nunca credenciais
        database_error = type(exc).__name__
    return {
        "status": "ok" if artifact_ok and database_ok else "degraded",
        "artifact": artifact_ok,
        "database": database_ok,
        "database_error_type": database_error,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.post("/executions/capture", response_model=CaptureResponse, dependencies=[Depends(require_bridge_key)])
def capture(request: CaptureRequest) -> CaptureResponse:
    payload, digest = load_baseline()
    try:
        model, value = extract_forecast(payload, request.segmento, request.horizonte)
    except (KeyError, TypeError, ValueError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    record = CaptureResponse(
        correlation_id=str(uuid.uuid4()),
        modelo=model,
        horizonte=f"D+{request.horizonte}",
        segmento=request.segmento,
        valor_previsto=max(value, 0.0),
        origem_artefato=BASELINE_FILE.name,
        artefato_sha256=digest,
        executado_em_utc=datetime.now(timezone.utc),
    )

    with db_connection() as connection:
        cursor = connection.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO execucao_analitica
                    (correlation_id, modelo, horizonte, segmento, valor_previsto,
                     origem_artefato, artefato_sha256, executado_em_utc)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    record.correlation_id,
                    record.modelo,
                    record.horizonte,
                    record.segmento,
                    record.valor_previsto,
                    record.origem_artefato,
                    record.artefato_sha256,
                    record.executado_em_utc,
                ),
            )
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            cursor.close()
    return record


@app.get("/executions", dependencies=[Depends(require_bridge_key)])
def list_executions(limit: int = Query(default=20, ge=1, le=100)) -> dict[str, Any]:
    with db_connection() as connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT correlation_id, modelo, horizonte, segmento, valor_previsto,
                   origem_artefato, artefato_sha256, executado_em_utc
              FROM execucao_analitica
             ORDER BY executado_em_utc DESC
             LIMIT %s
            """,
            (limit,),
        )
        rows = cursor.fetchall()
        cursor.close()
    return {"total_retornado": len(rows), "items": rows}


@app.get("/executions/summary", dependencies=[Depends(require_bridge_key)])
def summary() -> dict[str, Any]:
    with db_connection() as connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT modelo, horizonte, segmento, COUNT(*) AS quantidade,
                   ROUND(AVG(valor_previsto), 2) AS media_prevista,
                   MAX(executado_em_utc) AS ultima_execucao_utc
              FROM execucao_analitica
             GROUP BY modelo, horizonte, segmento
             ORDER BY modelo, horizonte, segmento
            """
        )
        rows = cursor.fetchall()
        cursor.close()
    return {"grupos": rows}


@app.on_event("startup")
def startup() -> None:
    ensure_schema()
