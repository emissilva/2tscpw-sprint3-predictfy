# Adaptador MySQL da Sprint 3

Componente isolado que comprova os três requisitos de banco da disciplina:

1. consome um artefato real de previsão do Predictfy;
2. insere a execução no Azure Database for MySQL;
3. consulta e processa o histórico por agregação.

## Rotas

- `GET /health`: saúde do artefato e da conexão.
- `POST /executions/capture`: extrai uma previsão D+1..D+7 e persiste sua proveniência.
- `GET /executions`: consulta registros recentes.
- `GET /executions/summary`: processa agregados por modelo, horizonte e segmento.

As rotas de dados exigem `X-Bridge-Key`. O health check não revela configurações sensíveis.

## Build

O contexto deve ser a pasta `predictfy-locaweb`, pois o Dockerfile inclui snapshots governados diretamente de `locaweb/outputs` sem alterar o MVP:

```bash
docker build -f "Sprint 3/01_cloud/app_mysql/Dockerfile" -t predictfy-mysql-bridge:sprint3 .
```

## Variáveis

- `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DATABASE`.
- `BRIDGE_API_KEY`: segredo usado somente para a demonstração.
- `PREDICTFY_OUTPUT_DIR` e `PREDICTFY_SCHEMA_FILE`: opcionais para testes.
