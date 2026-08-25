# Predictfy — Sprint 3 — Deep Learning

Entrega da disciplina **Artificial Intelligence & Deep Learning Application** do Challenge Locaweb 2026.

## Artefato oficial

- `EC_Sprint_3_Predictfy_Predictfy_DeepL.ipynb`
- ZIP para envio: `EmersonRM562033_Deep_Learning_Sprint3.zip`
- Registro para retomada: `CONTINUIDADE.md`

O notebook implementa uma rede neural artificial para triagem de risco de violação de OLA. A ANN é avaliada como candidata em *shadow mode*: ela não substitui o XGBoost ativo nem altera o projeto `locaweb`.

Além da modelagem, o artefato contém EDA ampliada inspirada nos materiais das aulas 03, 04, 09, 11 e 14: qualidade e duplicatas, padrões do alvo calculados no treino, drift numérico, categorias inéditas, análise pós-incidente isolada das features, estabilidade dos clusters, curvas por seed, erros por segmento, calibração, sensibilidade de capacidade e intervalos de confiança por bootstrap.

Uma seção adicional de otimização controlada compara cinco conjuntos de features em duas janelas temporais anteriores a julho, confirma o vencedor em julho–agosto e pesquisa thresholds somente em setembro. O Q4 permanece como diagnóstico retrospectivo e não participa de nenhuma escolha.

O estudo de classe rara compara BCE ponderada, focal loss, batches balanceados, ranking pareado e um candidato com frequência categórica/contexto operacional D−1. Também avalia threshold por prioridade e Top-1 diário, sem gerar amostras sintéticas.

## Execução

O ambiente utilizado é o micromamba `deep` (Python 3.12).

```bash
micromamba activate deep
jupyter lab
```

O notebook procura o dataset nesta ordem:

1. variável de ambiente `PREDICTFY_DATASET`;
2. `../../locaweb/data/raw/LW-DATASET.xlsx` a partir desta pasta;
3. `data/raw/LW-DATASET.xlsx` a partir do diretório atual.

## Princípios de modelagem

- `KPI Violado?` é o ground truth.
- Campos posteriores ao incidente não entram como features.
- A série diária é reindexada em calendário completo antes dos lags.
- Encoders, scaler e K-Means são ajustados somente no treino.
- Treino: até junho; arquitetura/cluster: julho-agosto; política: setembro; Q4 é backtest retrospectivo.
- Três seeds avaliam a estabilidade da ANN.
- ANN e XGBoost são comparados nas mesmas linhas e features.
- A política principal limita a fila aos 5% maiores scores.
- PR-AUC é a métrica primária; acurácia não é usada para seleção.
- O Q4 não é chamado de evidência prospectiva inédita porque já foi analisado pelo projeto.

## Validação local

```bash
/Users/emersonsilva/micromamba/envs/deep/bin/python validate_notebook.py
unzip -l EmersonRM562033_Deep_Learning_Sprint3.zip
```
