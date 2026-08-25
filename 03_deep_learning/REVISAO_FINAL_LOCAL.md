# Revisão final local — Deep Learning

## Ambiente

- micromamba: `deep`
- Python: 3.12
- framework: PyTorch 2.8
- dataset bruto: 122.543 linhas e 19 colunas
- fonte: XLSX canônico com SHA-256 já validado no projeto `locaweb`
- rótulos de todas as janelas de treino, seleção e backtest filtrados por `data_resultado` anterior ao respectivo corte temporal

## Resultado executado

- Arquitetura selecionada: MLP compacta, camadas ocultas 64 e 32
- Camada de entrada: 349 features após transformação
- K-Means escolhido no treino: K=4
- Delta médio de PR-AUC ao adicionar cluster: -0,00204
- Decisão: cluster rejeitado como feature da ANN
- PR-AUC no backtest Q4: 0,12880
- ROC-AUC no backtest Q4: 0,72183
- Recall na política Top-5%: 36,0%
- Precisão na política Top-5%: 5,75%
- F1 na política Top-5%: 0,09917
- Taxa efetiva de alertas no Q4: 6,04%
- Lift na política Top-5%: 5,96×
- Revisões por acerto: 17,4
- Delta pareado de PR-AUC ANN−XGBoost: mediana -0,07146; IC95% bootstrap [-0,15374; +0,00038]

## EDA ampliada

- Diagnóstico de missing, cardinalidade e duplicatas do arquivo canônico
- Risco por prioridade, produto, categoria, subcategoria e período, estimado somente no treino
- Drift temporal por PSI e cobertura de categorias inéditas nos períodos futuros
- Duração pós-incidente analisada apenas como diagnóstico, nunca como feature
- Perfil e estabilidade temporal dos clusters
- Curvas de aprendizagem e estabilidade das três seeds
- Sensibilidade operacional Top-1%, Top-3%, Top-5% e Top-10%
- Intervalos de confiança bootstrap para PR-AUC, precisão, recall e F1
- Falsos positivos e falsos negativos por segmento no Q4
- Curva de calibração, mantendo o resultado definido como score de ranking

### Novas evidências observadas

- O maior drift operacional no Q4 apareceu em `rolling_7d` (PSI 6,363), indicando mudança forte no regime recente de volume.
- A maior taxa de categoria inédita no Q4 foi 1,25%; portanto, o drift é mais de distribuição/volume do que simples surgimento de rótulos categóricos novos.
- PR-AUC do backtest apresentou IC95% bootstrap amplo: [0,05823; 0,25080], refletindo a pequena quantidade de violações.
- Na sensibilidade retrospectiva, Top-1% teve o maior F1 (0,23158), mas não substitui a política Top-5% previamente congelada.
- O ensemble esconde variação relevante entre seeds: PR-AUC individual no Q4 de 0,07882 a 0,14558.
- Violações apresentaram duração posterior muito superior às não violações, confirmando valor descritivo e, simultaneamente, o risco grave de leakage se duração ou resolução fossem usadas como entrada.

## Otimização controlada

- Cinco conjuntos de features foram comparados em dois folds temporais anteriores a julho.
- `sem_contexto_volume` obteve a melhor PR-AUC média nos folds (`0,14240` contra `0,11777` do baseline).
- Na confirmação de julho–agosto, entretanto, o ganho médio caiu para apenas `+0,00121`, abaixo do critério mínimo de `+0,002`; portanto, as features originais foram preservadas.
- O threshold escolhido exclusivamente em setembro correspondeu à capacidade nominal de `1,5%`; a nova execução point-in-time publicou o threshold Top-5% `0,470483` no manifesto.
- No Q4 retrospectivo, essa política alcançou precisão `21,67%`, recall `26,0%` e F1 `0,23636`, contra F1 `0,09917` da política Top-5%.
- A carga caiu de 313 para 60 alertas e de 17,4 para 4,6 revisões por acerto.
- A capacidade de 1,5% venceu em apenas `43,2%` dos bootstraps de setembro. É uma hipótese promissora, mas instável e ainda não deve substituir a política oficial sem validação prospectiva.

## Tratamento adicional da classe rara

- BCE ponderada continuou sendo a melhor estratégia pré-julho, com PR-AUC média `0,11777`.
- Focal loss obteve `0,09102`; batches balanceados, `0,07255`; ranking pareado, `0,06391`; frequência categórica com contexto operacional, `0,02328`.
- Na confirmação julho–agosto, o novo treinamento com BCE ponderada teve ganho médio `-0,00023`; nenhuma estratégia foi promovida.
- O backtest do re-treino BCE apresentou PR-AUC `0,12930`, praticamente igual ao baseline `0,12880`; a diferença não representa melhoria validada.
- Threshold por prioridade produziu F1 retrospectivo `0,24074`, contra `0,23636` do threshold global; setembro tinha somente 2 positivos P2 e 9 P3, tornando a segmentação insuficientemente suportada.
- Top-1 diário obteve precisão `11,96%`, recall `22,0%` e F1 `0,15493`, inferior ao threshold global de 1,5%.
- SMOTE foi deliberadamente evitado por risco de criar combinações temporais/categóricas artificiais.

## Decisão de governança

A ANN permanece como candidata acadêmica em `shadow mode`. A comparação pareada não demonstrou superioridade sobre o XGBoost: o intervalo de confiança inclui zero e favorece majoritariamente o baseline. A rede não deve substituir automaticamente o modelo ativo. O resultado da clusterização foi mantido como evidência negativa válida: nesse protocolo, adicionar o cluster prejudicou a métrica primária.

## Checklist

- [x] Notebook com nome oficial
- [x] Dataset oficial carregado
- [x] Split temporal e prevenção de leakage
- [x] Três arquiteturas comparadas
- [x] Clusterização avaliada sem consultar o teste
- [x] Thresholds escolhidos na validação
- [x] Q4 tratado explicitamente como backtest retrospectivo, não como teste prospectivo inédito
- [x] ANN avaliada em três seeds e comparada ao XGBoost nas mesmas linhas e features
- [x] Política Top-5% calibrada em setembro, separada da seleção da arquitetura
- [x] MVP `prever_risco(caso)` executado
- [x] Casos inválidos e categoria desconhecida testados
- [x] Preprocessor, ensemble ANN, XGBoost pareado e manifesto serializados localmente
- [x] Ausência de erros nas células
- [x] Rótulos point-in-time maduros em treino, validação de arquitetura, threshold e backtest
- [x] ZIP contém somente o notebook
