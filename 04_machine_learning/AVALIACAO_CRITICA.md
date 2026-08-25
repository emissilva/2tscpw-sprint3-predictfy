# Avaliação crítica da entrega — Machine Learning

Data da auditoria: 25/08/2026  
Referência: páginas 37–38 do regulamento oficial e materiais da disciplina `04_machine_learning_ia`.

## Parecer

A entrega cobre integralmente os três blocos obrigatórios e respeita o formato oficial. O notebook está executado, apresenta evidências reais do XLSX canônico e não esconde o resultado desfavorável no backtest. Parecer técnico: **apto para entrega**, com limitações científicas explicitadas.

## Cobertura avaliada

| Critério | Situação | Evidência |
|---|---|---|
| AED: nulos e missing | Atendido | Perfil por coluna, percentual, gráfico e decisão de imputação |
| Dados inválidos | Atendido | IDs, duplicatas, domínios, datas incoerentes e duração negativa |
| Outliers | Atendido | IQR da duração e IQR do alvo calculado apenas no treino |
| Distribuições | Atendido | Prioridade, categorias KPI, duração e volumes mensal/diário/semanal |
| Correlações | Atendido | Pearson, Spearman e heatmap calculados antes do backtest |
| Features temporais | Atendido | Calendário, ciclos, lags, janelas, composição e mudança de regime D−1 |
| Vantagens e limitações | Atendido | Quadro explícito por família de features |
| Estacionariedade e ordem | Atendido | Cobertura, decomposição, ADF, ACF, diferenças semanais e split cronológico |
| Modelo interpretável | Atendido | Regressão linear, Ridge de sensibilidade, coeficientes, OLS, VIF e resíduos |
| Data leakage | Atendido | Campos proibidos, `shift(1)`, scaler no treino e assertivas |
| Avaliação | Atendido | Baseline comum, MAE, RMSE, WAPE, R², validação e Q4 isolado |
| Formato | Atendido | Notebook oficial e ZIP contendo somente o `.ipynb` |

## Melhorias implementadas nesta auditoria

1. Incluída distribuição das principais categorias do subset KPI e decisão explícita de imputação apenas descritiva.
2. Incluída auditoria de nulos após o feature engineering, comprovando que nenhuma imputação numérica silenciosa foi usada.
3. Incluído IQR do alvo usando somente o treino; o pico real foi preservado.
4. Criadas features de mudança semanal conhecidas em D−1 para responder à não estacionariedade observada pelo ADF.
5. Tendência linear e ciclo anual foram excluídos da seleção principal por haver apenas um ciclo anual com cobertura suficiente.
6. Removida multicolinearidade perfeita entre total, P2 e P3; composição passou a usar participação P2.
7. Drift de calendário foi separado de drift operacional.
8. Conclusão atualizada com decisão inequívoca de não promover o modelo.

## Resultado e risco residual

- A regressão linear ganhou do baseline na validação: MAE `11,444` contra `12,967`.
- No Q4, perdeu: MAE `13,612` contra `12,696`, piora de `7,21%`.
- O volume médio caiu de `73,70` na validação para `56,34` no Q4.
- Durbin–Watson `1,065` indica autocorrelação positiva residual.
- Só 2025 possui cobertura adequada; uma validação prospectiva em 2026 é necessária antes de qualquer promoção.

Esses riscos não impedem a entrega acadêmica. Ao contrário, demonstram aplicação correta de validação temporal e governança: o modelo interpretável cumpriu seu papel de avaliar features, mas não apresentou evidência suficiente para substituir o baseline operacional.
