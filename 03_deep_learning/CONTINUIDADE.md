# Registro de decisões e ponto de retomada

Última atualização: 25/08/2026  
Projeto: Predictfy × Locaweb — Sprint 3 — Deep Learning

## Estado atual

- Notebook oficial: `EC_Sprint_3_Predictfy_Predictfy_DeepL.ipynb`
- ZIP de entrega: `EmersonRM562033_Deep_Learning_Sprint3.zip`
- Ambiente de execução: micromamba `deep`, Python 3.12, PyTorch 2.8
- Notebook validado com 47 células, sendo 29 células de código executadas e sem erros salvos.
- O ZIP contém exclusivamente o notebook oficial.
- O projeto de referência `locaweb` permaneceu sem alterações.
- Decisão de produto: ANN em `shadow mode`; não promover automaticamente.

## Pergunta e target

- Objetivo: ordenar incidentes P2/P3 pelo risco de violação de OLA no momento da abertura.
- Ground truth: `KPI Violado?`.
- PR-AUC é a métrica primária por causa do forte desbalanceamento.
- O score da ANN é usado para ranking e não deve ser comunicado como probabilidade calibrada.
- Acurácia não é usada para selecionar modelos.

## Decisões contra leakage

- Features devem existir na abertura ou ser agregações encerradas em D−1.
- Campos proibidos: duração, resolução, encerramento, solução, código de fechamento, target e `Aberto por`.
- `Aberto por` foi removido por privacidade, alta cardinalidade e risco de memorização.
- A série diária foi reindexada em calendário completo antes do cálculo dos lags.
- Encoders, scalers, K-Means e frequências categóricas são ajustados somente no treino correspondente.
- Labels de treino precisam ter resultado conhecido antes do corte temporal.
- Campos posteriores ao incidente aparecem somente em análise descritiva.
- SMOTE foi deliberadamente evitado por poder gerar combinações temporais e categóricas artificiais.
- O Q4 já havia sido analisado e é chamado somente de backtest retrospectivo, nunca de teste inédito.

## Cortes temporais

- Treino principal: aberturas anteriores a 01/07/2025, com resultado conhecido antes desse corte.
- Validação de arquitetura/cluster: julho e agosto de 2025, somente com resultados conhecidos até 01/09/2025.
- Validação de threshold: setembro de 2025, somente com resultados conhecidos até 01/10/2025.
- Backtest retrospectivo: outubro a dezembro de 2025.
- Ablação e estratégias de classe rara: folds março–abril e maio–junho, sempre com treino anterior e label conhecido.

## Pipeline escolhido

- Modelo: MLP PyTorch compacta, camadas ocultas 64 e 32, dropout 0,20.
- Entrada baseline: 349 features após transformação.
- Categóricas: prioridade, produto, categoria, subcategoria e período do dia.
- Numéricas: calendário, horário, feriado e contexto agregado de volume.
- Treinamento: BCEWithLogitsLoss com `pos_weight`, Adam, weight decay e early stopping.
- Avaliação de estabilidade: seeds 11, 42 e 101; predição final por média do ensemble.
- K-Means: K=4 escolhido por silhouette somente no treino.
- Cluster rejeitado como feature; delta médio de PR-AUC `-0,002038`.

## Resultado baseline no Q4

- PR-AUC: `0,128803`.
- ROC-AUC: `0,721833`.
- Política Top-5% calibrada em setembro: threshold `0,470483` na execução point-in-time.
- Precisão: `5,7508%`.
- Recall: `36,0%`.
- F1: `0,099174`.
- Taxa efetiva de alertas: `6,039%`.
- Lift: `5,961×`.
- Revisões por acerto: `17,4`.
- IC95% bootstrap da PR-AUC: `[0,058228; 0,250801]`.

## Comparação com XGBoost

- O XGBoost pareado foi treinado nas mesmas linhas e features transformadas da ANN.
- Delta PR-AUC ANN−XGBoost: mediana `-0,07146`.
- IC95% bootstrap do delta: `[-0,153739; +0,000377]`.
- Não existe evidência de superioridade da ANN sobre o XGBoost.

## EDA ampliada

- Foram produzidos gráficos de target, evolução mensal, volume versus prevalência, risco por segmentos, clusterização, curvas de aprendizagem, Precision–Recall, matriz de confusão e calibração.
- Foram produzidas tabelas de missing, cardinalidade, duplicatas, PSI, categorias inéditas, sensibilidade operacional, erros por segmento e intervalos de confiança.
- Maior drift operacional no Q4: `rolling_7d`, PSI `6,363`.
- Maior taxa de categoria inédita no Q4: `1,25%`.
- A mudança parece estar mais no regime de volume/distribuição do que no surgimento de categorias novas.
- PR-AUC individual das seeds no Q4 variou de `0,07882` a `0,14558`.
- Duração posterior foi muito maior nos casos violados, mas continua proibida como feature.

## Ablação de features

Conjuntos testados:

- baseline completo;
- sem sazonalidade bruta;
- sem contexto global de volume;
- categorias compactas;
- conjunto enxuto sem variáveis brutas.

Resultados:

- `sem_contexto_volume` venceu nos folds anteriores a julho: PR-AUC média `0,14240` contra `0,11777` do baseline.
- Na confirmação julho–agosto, o ganho médio foi apenas `+0,001213`.
- Critério de confirmação: ganho mínimo de `+0,002`.
- Decisão: candidato não confirmado; features baseline preservadas.

## Otimização do threshold

- Busca realizada somente em setembro, entre capacidades nominais de 0,5% e 5%.
- Critério: maior F1 sob a restrição operacional.
- Política escolhida: capacidade nominal de 1,5%, threshold `0,693414`.
- Backtest retrospectivo da política de 1,5%:
  - precisão `21,6667%`;
  - recall `26,0%`;
  - F1 `0,236364`;
  - 60 alertas;
  - 4,6 revisões por acerto.
- Comparação: Top-5% gerou 313 alertas e 17,4 revisões por acerto.
- A capacidade de 1,5% venceu em apenas `43,2%` dos bootstraps de setembro.
- Decisão: hipótese operacional promissora, mas instável; não substituir a política oficial sem validação prospectiva.

## Estratégias para classe rara

PR-AUC média nos folds anteriores a julho:

- BCE ponderada: `0,11777`.
- Focal loss: `0,09102`.
- Batches balanceados: `0,07255`.
- Ranking pareado: `0,06391`.
- Frequência categórica + contexto operacional D−1: `0,02328`.

Confirmação:

- BCE ponderada permaneceu como melhor estratégia.
- Ganho médio do novo treinamento em julho–agosto: `-0,000225`.
- PR-AUC do re-treino no Q4: `0,129301`, praticamente igual ao baseline `0,128803`.
- Decisão: nenhuma estratégia nova foi confirmada ou promovida.

## Políticas segmentadas

- Threshold global de 1,5%: precisão `21,67%`, recall `26%`, F1 `0,23636`.
- Threshold por prioridade: precisão `22,41%`, recall `26%`, F1 `0,24074`.
- Top-1 diário em lote: precisão `11,96%`, recall `22%`, F1 `0,15493`.
- Setembro contém apenas 2 positivos P2 e 9 positivos P3.
- Decisão: ganho do threshold por prioridade é pequeno e sem suporte; não promover.
- Top-1 diário foi inferior ao threshold global e também não foi promovido.

## MVP e artefatos

- O MVP continua usando o baseline, não os candidatos retrospectivos.
- Os quatro campos de contexto temporal são obrigatórios; não há imputação silenciosa por mediana.
- Categorias desconhecidas são aceitas pelo encoder.
- Entradas ausentes, prioridade inválida e volumes negativos são rejeitados explicitamente.
- Artefatos locais:
  - `artifacts/preprocessor.pkl`;
  - `artifacts/ann_ensemble.pt`;
  - `artifacts/xgboost_pareado.pkl`;
  - `artifacts/manifest.json`.
- Os artefatos não entram no ZIP porque a entrega oficial exige somente o notebook.

## Decisões finais que não devem ser revertidas sem nova evidência

- Não usar Q4 para escolher features, arquitetura, loss ou threshold.
- Não chamar Q4 de teste inédito.
- Não usar campos pós-incidente ou identificadores pessoais.
- Não promover cluster, focal loss, batches balanceados, ranking, novas features ou thresholds segmentados com os resultados atuais.
- Não interpretar pequena diferença pontual no Q4 como melhoria validada.
- Não substituir XGBoost pela ANN neste estágio.
- Não produzir probabilidade ou automação sem calibração e validação prospectiva.
- Não incluir nas janelas de seleção ou backtest registros cujo `data_resultado` seja nulo ou posterior ao corte da decisão.

## Próxima retomada recomendada

1. Incorporar dados prospectivos de 2026 sem consultá-los durante o desenvolvimento.
2. Verificar qualidade e estabilidade do target e mudanças nas regras de OLA.
3. Aumentar o número de violações rotuladas, especialmente P2.
4. Congelar previamente os candidatos: baseline Top-5%, baseline threshold 1,5% e XGBoost pareado.
5. Compará-los no período prospectivo com PR-AUC, recall, precisão, F1, lift e revisões por acerto.
6. Usar bootstrap por blocos temporais e acompanhar pior mês, não apenas média global.
7. Só depois avaliar calibração, threshold por prioridade ou promoção do modelo.

## Comandos de retomada

```bash
cd "/Users/emersonsilva/fiap_ano2/predictfy-locaweb/Sprint 3/03_deep_learning"
micromamba run -n deep python generate_notebook.py
micromamba run -n deep python validate_notebook.py
```

Antes de regenerar, lembrar que `generate_notebook.py` é a fonte do notebook. Alterar apenas o `.ipynb` fará a mudança desaparecer na próxima geração.
