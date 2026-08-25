# Registro de decisões e ponto de retomada

Última atualização: 25/08/2026  
Projeto: Predictfy × Locaweb — Sprint 3 — Machine Learning

## Decisões iniciais

- O problema modelado é o volume diário de incidentes que entraram no KPI, alinhado às telas de Gestão/Monitoramento e à cadeia de previsão do Predictfy.
- O alvo é `volume_dia`; o notebook não reaproveita métricas históricas como se fossem novas.
- A EDA cobre o arquivo bruto completo. Campos de duração e resolução são apenas diagnósticos.
- O calendário completo é criado antes dos lags.
- Lags e janelas são encerrados em D−1.
- 2023–2024 são somente diagnóstico de cobertura. Treino usa 29/01–30/06/2025, validação usa julho–setembro e o Q4 é backtest retrospectivo.
- A referência é a mediana dos volumes observados em D−7, D−14 e D−21.
- Regressão linear e Ridge avaliam a utilidade incremental das features.
- O notebook é gerado por `generate_notebook.py`; alterações diretas no `.ipynb` serão perdidas ao regenerar.

## Resultado executado

- Dataset oficial: 122.543 linhas, SHA-256 `87bab6e0625093ad4833a768d671fbac0405f08609103685fc6a0bccbee44959`.
- Série modelada: 25.156 incidentes KPI em 2025; 5.159 P2 e 19.997 P3.
- ADF: p-valor `0,6330`; a série em nível não rejeitou raiz unitária.
- Configuração congelada: regressão linear com calendário semanal + lags totais.
- Validação julho–setembro: MAE `11,444`, contra `12,967` do baseline sazonal; ganho de `11,75%`.
- Backtest Q4: MAE `13,612`, contra `12,696` do baseline; piora de `7,21%`.
- Durbin–Watson dos resíduos: `1,065`, indicando autocorrelação positiva remanescente.
- Decisão: não promover a Ridge; manter o baseline sazonal como referência.
- A primeira formulação com lags simultâneos de total, P2 e P3 foi corrigida porque `total = P2 + P3` gerava VIF infinito. A composição passou a ser representada pela participação histórica de P2 nos candidatos completos.
- Tendência linear e ciclo anual foram retirados da seleção principal: existe somente um ciclo anual com cobertura suficiente, tornando a extrapolação frágil. Foram adicionadas diferenças semanais encerradas em D−1 ao candidato completo.

## Antes de encerrar a entrega

1. Conferir as métricas executadas e interpretar os maiores erros operacionais.
2. Avaliar estabilidade em janelas temporais adicionais sem consultar o backtest para seleção.
3. Congelar o pipeline e validar prospectivamente com dados de 2026, se forem disponibilizados.
4. Executar `validate_notebook.py` e conferir que o ZIP contém somente o notebook oficial.

## Restrições preservadas

- Não modificar o repositório de referência `locaweb`.
- Não afirmar que o baseline acadêmico foi integrado ou promovido no produto.
- Não usar duração, resolução, encerramento, solução, código de fechamento ou target OLA como features.
- Não usar o segundo semestre de 2025 para escolher features ou hiperparâmetros.
