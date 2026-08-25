# Dúvidas e pendências

## Confirmar com o grupo ou professores

1. O enunciado de Deep Learning e alguns exemplos ainda citam o caso Mater Dei/conversão. Confirmar que a avaliação deve ser adaptada integralmente ao risco de violação de OLA da Locaweb.
2. Confirmar se o representante da Sprint 3 continuará sendo Emerson dos Santos Silva, RM 562033.
3. Data Warehouse exige ADF e menciona Azure SQL nos exemplos, enquanto Cloud exige Azure Database for MySQL. Confirmar se o mesmo MySQL pode ser o SGBD de destino do ADF ou se o professor espera Azure SQL.
4. Confirmar se Data Protection aceitará o ADF como “serviço equivalente em nuvem” ou se é preferível uma DAG Airflow separada para demonstrar recovery e reprocessamento.
5. Confirmar qual conta/subscrição Azure será usada e o limite de custos.
6. Confirmar o workspace e a conta de publicação do Power BI Service.

## Inconsistências já identificadas

- A apresentação anterior registra métricas e volumes que não devem ser reutilizados sem validação.
- A Sprint 2 dizia que o dataset tinha 25,6 mil registros em alguns slides; o MVP atual documenta 122.543 incidentes brutos.
- A documentação atual diverge entre “31 features” e “30 colunas (29 features + target)”.
- Os dois HTMLs de resultado parecem conter o mesmo conjunto de notas e feedbacks da Sprint 2, apesar dos nomes “sprint 1” e “sprint 2”.
- O ambiente Python atual não possui `pytest`; a suíte do MVP ainda não foi executada localmente.

## Evidências que não podem ser produzidas offline

- Provisionamento e execução na Azure.
- Execução do Azure Data Factory.
- Logs do Azure Monitor e Application Insights.
- Recovery real do armazenamento/banco.
- Link público e capturas finais do Power BI.
