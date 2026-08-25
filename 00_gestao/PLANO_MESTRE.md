# Plano mestre da Sprint 3

Prazo oficial: **30/08/2026**.

## Linha de base obrigatória

Todas as disciplinas devem representar a versão atual do Predictfy, consultada no repositório `locaweb` atualizado. As entregas anteriores não são a arquitetura de referência da Sprint 3. Elas servem somente para preservar a evolução histórica e aplicar os feedbacks recebidos.

A solução atual inclui, no mínimo:

- dashboard React reorganizado por perfil e contexto operacional;
- telas de Gestão, Monitoramento, Técnico, Modelos, Operações e Administração;
- chatbot híbrido com respostas determinísticas e análise por LLM;
- histórico de conversas, contexto do dashboard, feedback, cache, rate limit e métricas de tokens;
- autenticação Microsoft Entra e controle de acesso persistente;
- FastAPI com rotas de previsões, risco, clusters, KPIs, modelos, operações, chat e administração;
- modelos de volume, risco e segmentação, com comparação, registro e gates de validação;
- fila/ciclo de feedback operacional para governança e evolução dos modelos;
- persistência local ou PostgreSQL para recursos do chatbot e administração;
- deploy atual Vercel/Render, tratado como implementação existente, e arquitetura Azure exigida como evolução acadêmica da Sprint 3.

## Cloud Solutions & Scalable Infrastructure

- Diagrama Draw.io com Resource Group, compute Azure, rede quando aplicável, Docker, Azure Database for MySQL e Azure Monitor/Application Insights.
- IaC em Azure CLI ou Terraform.
- Aplicação containerizada consumindo a lógica/modelo do MVP.
- Arquitetura deve representar também frontend, API, autenticação, chatbot, persistência, modelos e fluxo operacional atuais.
- Inserção, consulta e processamento no MySQL.
- Evidências reais de provisionamento, execução e monitoramento.
- PDF sequencial da entrega.

## Data Warehousing & Advanced Data Integration

- Arquitetura e descrição do processo de ingestão.
- Infraestrutura PaaS na Azure.
- Azure Data Factory com transformação, limpeza, enriquecimento e coluna derivada.
- Entrada significativa em pelo menos um formato corporativo.
- Persistência em SGBD e TXT.
- `colunas_derivadas.txt`, evidências de execução e comentários finais.

## Artificial Intelligence & Deep Learning Application

- Notebook `EC_Sprint_3_Predictfy_Predictfy_DeepL.ipynb`.
- Pré-processamento para ANN aproveitando a EDA.
- Avaliação da utilidade da clusterização.
- Explicação da camada de entrada e arquitetura da rede.
- Testes de parametrização e avaliação por métricas adequadas ao desbalanceamento.
- MVP local capaz de carregar dados e produzir previsão real.
- Demonstrar como a ANN se integra ao produto atual e como seu resultado pode ser exposto pela API/telas, sem fingir que uma integração ainda não implementada já existe.
- ZIP final no padrão do representante.

## Machine Learning & Artificial Intelligence

- Notebook `EC_Sprint_3_Predictfy_Predictfy_ML.ipynb`.
- EDA: nulos, inválidos, outliers, imputação, distribuições e correlações.
- Engenharia de features temporais com vantagens e limitações.
- Split estritamente temporal e análise explícita de data leakage.
- Modelo simples e interpretável para avaliar as features.
- ZIP final no padrão do representante.

## Data Protection & Ingestion

- Estratégia de backup full e incremental, periodicidade, retenção e armazenamento.
- Justificativa ligada à continuidade do AIOps.
- Pipeline orquestrado com extração, limpeza, validação e carga analítica.
- Simulação documentada de falha, recovery e reprocessamento.
- Logs, capturas e PDF `evidencias-sprint3-rm562033.pdf`.

## Data Visualization, Business Analytics & AI Integration

- KPIs documentados e justificados para o contexto operacional da Locaweb.
- Dashboard interativo com filtros, segmentação e drill-down.
- Documentar e evidenciar as telas atuais; o Power BI deve complementar a experiência analítica, não substituir nem ignorar o dashboard React existente.
- Fontes, tratamentos e modelagem documentados.
- Insights ligados a ações estratégicas.
- Link publicado e PDF `Locaweb_Sprint3_Predictfy.pdf`.

## Critérios transversais de revisão

- Usar os cinco integrantes e RMs em ordem alfabética.
- Priorizar evidências visuais reais, conforme feedback das Sprints anteriores.
- Reduzir texto excessivamente técnico em slides e relatórios executivos.
- Manter coerência de números entre notebooks, dashboard, PDFs e MVP.
- Capturar evidências das telas e funcionalidades atuais, especialmente chatbot, Operações, Administração e governança de modelos.
- Diferenciar claramente resultado histórico, previsão, cenário e hipótese.
