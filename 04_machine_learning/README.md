# Predictfy — Sprint 3 — Machine Learning

Desenvolvimento da disciplina **Machine Learning & Artificial Intelligence** do Challenge Locaweb 2026.

## Artefatos

- `EC_Sprint_3_Predictfy_Predictfy_ML.ipynb`: notebook oficial.
- `generate_notebook.py`: fonte reproduzível do notebook.
- `validate_notebook.py`: valida execução, conteúdo e gera o ZIP.
- `MATRIZ_REQUISITOS.md`: cobertura do enunciado oficial.
- `CONTINUIDADE.md`: decisões e ponto de retomada.
- `requirements-machine-learning.txt`: dependências mínimas.

## Escopo inicial

O notebook analisa o XLSX canônico e estuda engenharia de features para previsão D+1 do volume diário de incidentes que entraram no KPI. O protocolo usa somente dados reais de 2025, ordem estritamente temporal, referência sazonal pela mediana das três semanas anteriores e regressão linear/Ridge interpretável. A cobertura esparsa de 2023–2024 é documentada, mas não usada como treino principal. Campos posteriores à abertura ficam restritos à EDA e não entram no modelo.

O modelo é um baseline acadêmico para interpretação. Ele não substitui automaticamente os modelos registrados no produto atual.

## Resultado principal

A regressão linear com calendário semanal e lags venceu a validação julho–setembro, mas perdeu para a mediana das três semanas anteriores no backtest Q4 (MAE `13,612` contra `12,696`). O notebook preserva esse resultado negativo e conclui pela não promoção do modelo.

## Execução

```bash
cd "Sprint 3/04_machine_learning"
/Users/emersonsilva/micromamba/envs/deep/bin/python generate_notebook.py
/Users/emersonsilva/micromamba/envs/deep/bin/jupyter execute EC_Sprint_3_Predictfy_Predictfy_ML.ipynb --inplace
/Users/emersonsilva/micromamba/envs/deep/bin/python validate_notebook.py
```

Se o dataset não estiver em um dos caminhos relativos conhecidos, defina `PREDICTFY_DATASET` com o caminho do `LW-DATASET.xlsx` oficial.
