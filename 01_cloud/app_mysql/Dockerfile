FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY ["Sprint 3/01_cloud/app_mysql/requirements.txt", "/app/requirements.txt"]
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY ["Sprint 3/01_cloud/app_mysql/main.py", "/app/main.py"]
COPY ["Sprint 3/01_cloud/app_mysql/schema.sql", "/app/schema.sql"]
COPY ["locaweb/outputs/previsoes_baseline.json", "/app/outputs/previsoes_baseline.json"]
COPY ["locaweb/outputs/comparacao_modelos.json", "/app/outputs/comparacao_modelos.json"]
COPY ["locaweb/outputs/model_registry.json", "/app/outputs/model_registry.json"]

RUN useradd --create-home --uid 10001 predictfy && chown -R predictfy:predictfy /app
USER predictfy

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/health')"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
