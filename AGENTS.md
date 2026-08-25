# Guia de contexto para agentes — Predictfy Sprint 3

## Finalidade e escopo

Este repositório contém as entregas acadêmicas da Sprint 3 do projeto Predictfy para o Challenge Locaweb. O conteúdo disponível está organizado em quatro disciplinas concluídas ou em estado avançado: Cloud, Data Warehouse, Deep Learning e Machine Learning.

Este arquivo é a entrada operacional para agentes. O `README.md` da raiz é intencionalmente curto e voltado ao público. Antes de alterar qualquer área, leia também o `README.md`, a `MATRIZ_REQUISITOS.md` e, quando existir, o `CONTINUIDADE.md` da disciplina correspondente.

As instruções mais específicas têm precedência dentro de seu diretório. Em especial, `01_cloud/AGENTS.md` rege todo o conteúdo de `01_cloud/`.

## Contexto do produto

Predictfy é uma solução acadêmica de AIOps voltada à operação da Locaweb. Sua linha de base funcional inclui:

- dashboard React com visões de Gestão, Monitoramento, Técnico, Modelos, Operações e Administração;
- API FastAPI para contexto, previsões, risco, clusters, KPIs, modelos, operações, chat e administração;
- chatbot híbrido, contextual e somente leitura, com histórico, feedback, cache, rate limit e métricas de uso;
- autenticação Microsoft Entra e controle persistente de acesso;
- previsão de volume, classificação de risco de violação de OLA e segmentação operacional;
- comparação, registro e validação de contratos dos modelos;
- ciclo de feedback operacional e governança;
- persistência configurável e implantação atual documentada em Vercel/Render;
- arquiteturas Azure desenvolvidas como evolução acadêmica da Sprint 3.

O produto-base foi desenvolvido em outro repositório, chamado `locaweb`, que não está incluído aqui. Em alguns ambientes locais ele pode existir como diretório irmão em `../locaweb`; em clones isolados, essa referência estará ausente. Nunca invente conteúdo, código, dataset ou estado do produto-base para compensar essa ausência. Use `00_gestao/LINHA_BASE_PRODUTO_ATUAL.md` como resumo interno e peça acesso ao repositório ou dataset original quando a tarefa exigir verificação direta.

## Ordem recomendada de leitura

1. Este `AGENTS.md`.
2. `00_gestao/LINHA_BASE_PRODUTO_ATUAL.md` para compreender o produto representado.
3. `00_gestao/PLANO_MESTRE.md` para compreender requisitos e critérios transversais.
4. `00_gestao/DUVIDAS_E_PENDENCIAS.md` para conhecer limitações históricas; valide se continuam atuais antes de tratá-las como pendências abertas.
5. O `README.md` e a `MATRIZ_REQUISITOS.md` da disciplina em alteração.
6. O `CONTINUIDADE.md`, a revisão final e as evidências da disciplina, quando disponíveis.
7. Em `01_cloud/`, leia obrigatoriamente `01_cloud/AGENTS.md` antes de agir.

## Estrutura real do repositório

- `00_gestao/`: linha de base, plano mestre e registro histórico de dúvidas.
- `01_cloud/`: infraestrutura Azure, FastAPI/MySQL, IaC, arquitetura, evidências reais e relatório final.
- `02_data_warehouse/`: Azure Data Factory, Data Flow, MySQL, Blob/TXT, SQL, IaC, evidências e relatório final.
- `03_deep_learning/`: notebook PyTorch, gerador, validação, artefatos serializados e ZIP de entrega.
- `04_machine_learning/`: notebook de EDA/engenharia temporal, gerador, validação e ZIP de entrega.

O plano mestre também descreve Data Protection e Data Visualization, mas essas pastas não existem neste repositório. Não afirme que essas duas entregas foram implementadas aqui e não crie sua estrutura sem solicitação explícita.

## Estado por disciplina

### 01 — Cloud Solutions & Scalable Infrastructure

Estado: encerrado e pronto para entrega. Não altere artefatos finais sem solicitação explícita.

Implementação comprovada:

- Azure Container Registry e dois Azure Container Instances;
- Azure Database for MySQL Flexible Server;
- Log Analytics e Application Insights;
- bridge de integração analítica com MySQL;
- scripts Azure CLI e Bicep reproduzíveis;
- execução real coletada em 20 e 23/08/2026;
- descarte posterior do Resource Group efêmero.

Documento oficial: `01_cloud/Cloud_Locaweb_Sprint3_Predictfy.pdf`.

Fontes principais: `01_cloud/gerar_entrega.py`, `01_cloud/gerar_pdf_final.py`, `01_cloud/arquitetura_predictfy_azure.drawio`, `01_cloud/iac/`, `01_cloud/app_mysql/` e `01_cloud/evidencias/reexecucao_2026-08-23/`.

### 02 — Data Warehousing & Advanced Data Integration

Estado: executado e documentado.

Implementação comprovada:

- Azure Data Factory e Storage em East US 2;
- MySQL Flexible Server em Chile Central;
- transformação e enriquecimento por Data Flow;
- duas execuções integrais em estado `Succeeded`;
- 25.588 registros persistidos de forma idempotente no MySQL e em TXT;
- zero prioridades P2/P3 sem regra OLA;
- descarte posterior da infraestrutura efêmera.

Documentos oficiais: `02_data_warehouse/DataWarehouse_Locaweb_Sprint3_Predictfy.pdf` e `02_data_warehouse/DataWarehouse_Locaweb_Sprint3_Predictfy.docx`.

Fontes principais: `02_data_warehouse/adf/`, `02_data_warehouse/iac/`, `02_data_warehouse/sql/`, `02_data_warehouse/scripts/`, `02_data_warehouse/arquitetura_ingestao.drawio`, `02_data_warehouse/gerar_entrega.py` e `02_data_warehouse/evidencias/`.

Validação local: execute `python3 02_data_warehouse/validate_local.py` a partir da raiz ou siga o README da disciplina.

### 03 — Artificial Intelligence & Deep Learning Application

Estado: notebook executado e validado; ZIP oficial contém somente o notebook.

Problema: ordenar incidentes P2/P3 pelo risco de violação de OLA no momento da abertura. O target é `KPI Violado?`; PR-AUC é a métrica primária. A ANN é uma candidata acadêmica em `shadow mode` e não substitui o XGBoost ativo.

Decisões preservadas:

- split e maturidade dos rótulos estritamente temporais;
- features disponíveis na abertura ou agregadas até D−1;
- proibição de duração, resolução, encerramento, solução, código de fechamento, target e identificadores pessoais como features;
- Q4/2025 é backtest retrospectivo, nunca teste prospectivo inédito;
- K-Means, focal loss, batches balanceados, ranking e novos thresholds não foram promovidos;
- não há evidência de superioridade da ANN sobre o XGBoost;
- scores não devem ser apresentados como probabilidades calibradas.

Artefato oficial: `03_deep_learning/EC_Sprint_3_Predictfy_Predictfy_DeepL.ipynb`.

ZIP oficial: `03_deep_learning/EmersonRM562033_Deep_Learning_Sprint3.zip`.

`03_deep_learning/generate_notebook.py` é a fonte do notebook. Alterações feitas apenas no `.ipynb` podem ser sobrescritas na regeneração. Consulte `03_deep_learning/CONTINUIDADE.md` antes de mudar modelagem, cortes, features, métricas ou decisões de governança.

Validação:

```bash
cd 03_deep_learning
micromamba run -n deep python generate_notebook.py
micromamba run -n deep python validate_notebook.py
```

### 04 — Machine Learning & Artificial Intelligence

Estado: notebook executado, auditado e apto para entrega; ZIP oficial contém somente o notebook.

Problema: previsão D+1 do volume diário de incidentes que entraram no KPI. A regressão linear serve como baseline interpretável para avaliar features e não foi promovida ao produto.

Resultado principal: o modelo venceu o baseline sazonal na validação julho–setembro de 2025, mas perdeu no backtest Q4. A decisão registrada é não promover a regressão/Ridge e manter a referência sazonal.

Decisões preservadas:

- calendário completo antes dos lags e janelas encerradas em D−1;
- ordem temporal estrita e transformações ajustadas somente no treino;
- campos pós-incidente não entram no modelo;
- 2023–2024 são diagnóstico de cobertura, não treino principal;
- Q4/2025 é backtest retrospectivo e não pode orientar seleção;
- não ocultar nem reinterpretar o resultado negativo de validação externa.

Artefato oficial: `04_machine_learning/EC_Sprint_3_Predictfy_Predictfy_ML.ipynb`.

ZIP oficial: `04_machine_learning/EmersonRM562033_Machine_Learning_Sprint3.zip`.

`04_machine_learning/generate_notebook.py` é a fonte do notebook. Consulte `04_machine_learning/CONTINUIDADE.md` e `04_machine_learning/AVALIACAO_CRITICA.md` antes de alterar metodologia ou conclusões.

Validação:

```bash
cd 04_machine_learning
micromamba run -n deep python generate_notebook.py
micromamba run -n deep jupyter execute EC_Sprint_3_Predictfy_Predictfy_ML.ipynb --inplace
micromamba run -n deep python validate_notebook.py
```

## Dados, métricas e interpretação

- O XLSX canônico do produto possui 122.543 registros brutos. Ele não está versionado neste repositório; os notebooks tentam localizá-lo por `PREDICTFY_DATASET` ou em caminhos relativos do repositório `locaweb`.
- Os 25.588 registros do Data Warehouse correspondem ao conjunto transformado daquela entrega.
- Os 25.156 incidentes citados em Machine Learning correspondem ao subconjunto KPI usado na série de 2025.
- Não trate esses números como intercambiáveis e não force sua igualdade: valide filtros, granularidade, período e regra de negócio.
- Diferencie sempre resultado histórico, previsão, cenário, hipótese e proposta ainda não implantada.
- Preserve números executados nos notebooks e evidências. Qualquer atualização deve ser reproduzível e refletida de forma coerente no notebook, README, relatório, matriz e artefatos finais afetados.

## Regras de evidência e integridade

- Não invente prints, logs, métricas, saídas de serviços, resultados de modelos ou telas.
- Não apresente como existente uma integração apenas proposta.
- Mantenha evidências brutas e explique o que cada captura comprova.
- Recursos Azure das entregas foram descartados. A ausência atual do recurso não invalida as evidências registradas e não autoriza reprovisionamento.
- Não provisione recursos pagos, não publique serviços e não execute operações externas com custo sem autorização explícita.
- Nunca versionar ou expor senhas, tokens, chaves, connection strings, cookies, dados pessoais ou arquivos `.env` reais.
- Antes de tornar um novo artefato público, revise também metadados, células de notebook, saídas, capturas e documentos binários em busca de segredos e dados pessoais.
- Não remova evidências, PDFs, notebooks, modelos ou ZIPs apenas por serem binários. Eles fazem parte do registro acadêmico, salvo decisão explícita em contrário.

## Regras de edição e geração

- Preserve o `README.md` da raiz curto e público; coloque orientação operacional neste arquivo ou na documentação interna apropriada.
- Faça alterações na fonte geradora quando o artefato for gerado. Não edite somente PDF, ZIP, notebook gerado, SVG ou HTML final.
- Após mudar uma fonte, regenere e valide todos os derivados relevantes.
- Não regenere documentos finais sem necessidade: ferramentas, versões e dados diferentes podem introduzir alterações extensas e não intencionais.
- Não modifique o repositório externo `locaweb` como efeito colateral de tarefas neste repositório.
- Preserve nomes oficiais de notebooks e pacotes de entrega.
- Mantenha uma única versão claramente identificada como oficial; arquivos históricos ou rascunhos não devem ser confundidos com a entrega final.
- Não reverta decisões científicas negativas para tornar resultados mais atraentes. Uma mudança exige nova evidência, protocolo válido e documentação da comparação.

## Padrão de revisão

Antes de encerrar uma alteração:

1. Confira a matriz de requisitos da disciplina.
2. Valide scripts, notebooks, IaC e formatos alterados.
3. Execute `git diff --check` e revise o diff completo.
4. Confirme que não foram incluídos caches, credenciais ou caminhos locais desnecessários.
5. Se houver PDF, revise abertura, tamanho A4, paginação, cortes, sobreposições e legibilidade.
6. Se houver ZIP, liste o conteúdo e confirme a convenção exigida.
7. Se houver notebook, confirme execução sem erros e coerência entre código, saídas e narrativa.
8. Atualize README, matriz, continuidade e relatório apenas quando a mudança realmente os afetar.
9. Registre limitações e itens não executados com linguagem explícita.

## Princípio de atuação

Cada alteração deve manter rastreabilidade entre requisito, implementação, evidência e conclusão. Quando faltarem o dataset, o repositório-base, uma conta de nuvem ou uma evidência externa, avance somente no que puder ser comprovado localmente e declare a limitação. Nunca preencha lacunas factuais por suposição.
