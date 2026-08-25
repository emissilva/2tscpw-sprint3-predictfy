# Reuso controlado da disciplina 01 — Cloud

Este documento é somente uma referência de integração. Nenhum arquivo, script ou recurso de `01_cloud` deve ser alterado durante o desenvolvimento do Data Warehouse.

## Registro histórico

Este arquivo preserva o alinhamento inicial entre as disciplinas. A execução final de Data Warehouse usou infraestrutura própria (`rg-predictfy-dw-sprint3-260823es`) e a execução final de Cloud usou `rg-predictfy-sprint3-260823es`; os recursos foram descartados após a coleta das evidências.

## Reaproveitado

- Convenções de nomes/tags e padrões de segurança documentados em Cloud.
- Região `eastus2` para ADF e Storage; o MySQL existente está em `chilecentral`.
- Banco lógico `predictfy` no MySQL para uma nova tabela de grão independente.
- TLS, segredo fora do Git, evidências reais antes de descarte e IaC parametrizada.

## Não reaproveitado

- A tabela `execucao_analitica`: seu grão é execução de previsão, diferente da matriz histórica de features.
- ACR, ACI, bridge FastAPI e imagens Docker: não são necessários para o ETL ADF.
- Capturas e métricas de Cloud: não comprovam Data Flow, pipeline ou sinks de Data Warehouse.
- Scripts de provisionamento/destruição do `01_cloud`: permanecem intocados.

## Regra operacional histórica

Os recursos Azure foram criados, evidenciados e descartados após confirmação dos artefatos. O pacote permanece reproduzível por IaC, JSONs publicados, scripts e guias locais; não depende de recursos ativos no momento da submissão.
