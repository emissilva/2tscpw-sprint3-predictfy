# Matriz de requisitos — Machine Learning

| Requisito oficial | Implementação inicial | Evidência no notebook |
|---|---|---|
| Nome oficial do notebook | `EC_Sprint_3_Predictfy_Predictfy_ML.ipynb` | Arquivo executado e validado |
| Identificar nulos e missing values | Perfil por coluna, quantidade e percentual | Tabela de qualidade e gráfico |
| Identificar dados inválidos | Datas, duração, chaves e domínios de rótulos | Auditoria programática |
| Tratar outliers | IQR da duração e do alvo diário calculado somente no treino; picos reais preservados | Resumos, distribuição e datas extremas |
| Avaliar imputação | Decisão por semântica e ausência MNAR | Justificativa documentada |
| Analisar distribuições | Prioridade, duração, volume mensal, diário e por dia da semana | Tabelas e gráficos |
| Investigar correlações | Matriz numérica e correlação com o alvo | Heatmap e ranking |
| Engenharia de features temporais | Calendário, ciclos, lags totais, participação P2, janelas e mudança de regime encerradas em D−1 | Código reproduzível |
| Vantagens e limitações | Quadro por família de features | Seção 4 |
| Modelo simples e interpretável | Regressão linear e Ridge com coeficientes, VIF, OLS e resíduos | Validação e backtest |
| Preservar ordem temporal | Treino, validação e backtest cronológicos | Datas e assertivas |
| Atenção máxima a leakage | `shift(1)`, campos bloqueados e scaler no treino | Auditoria explícita |
| Série temporal e estacionariedade | Cobertura, decomposição, ADF/ACF, lags e diferenças semanais; tendência anual excluída da seleção | Diagnóstico e tratamento temporal |
| Métricas adequadas | MAE, RMSE, WAPE e R² contra baseline sazonal | Mesmas datas em validação/backtest |
| ZIP do representante | `EmersonRM562033_Machine_Learning_Sprint3.zip` | ZIP contendo somente o notebook |
