# Matriz de requisitos — Deep Learning

| Requisito oficial | Implementação | Evidência esperada |
|---|---|---|
| Notebook com nome oficial | `EC_Sprint_3_Predictfy_Predictfy_DeepL.ipynb` | Arquivo executado e validado |
| Pré-processamento para ANN | Calendário completo, lags D−1/D−7 reais, one-hot e padronização ajustados no treino | Dimensões, períodos e auditoria anti-leakage |
| Aproveitamento da EDA | Qualidade, desbalanceamento e distribuição temporal do target | Tabelas e gráficos executados |
| Avaliação de clusterização | K-Means ajustado no treino; ANN com e sem cluster | Métricas de cluster e delta de PR-AUC |
| Camada de entrada | Quantidade de features após transformação e explicação das famílias | Resumo da arquitetura |
| Montagem da ANN | PyTorch MLP, ReLU, dropout, BCE ponderada e early stopping | Código, diagrama textual e curvas |
| Testes de parametrização | Três arquiteturas × três seeds comparadas em julho-agosto | Média, desvio e pior seed |
| Métricas adequadas | PR-AUC, ROC-AUC, recall, precisão, F1, lift e matriz de confusão | Validação e teste temporal |
| MVP funcional local | Função `prever_risco(caso)` e artefatos serializados | Previsão real e manifesto versionado |
| Integração com o produto | Candidata `ann_ola_risk` em shadow mode | Contrato proposto, sem alegar implantação |
| ZIP do representante | `EmersonRM562033_Deep_Learning_Sprint3.zip` | ZIP contendo somente o notebook |
