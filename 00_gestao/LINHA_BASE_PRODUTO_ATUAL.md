# Linha de base do produto atual

Este documento orienta todas as entregas da Sprint 3. Ele descreve o escopo que deve ser comprovado a partir do MVP atual, sem modificar o repositório de origem.

## Experiência do usuário

### Gestão

Visão executiva da saúde operacional, tendências, risco e impacto das previsões para decisão gerencial.

### Monitoramento

Visualização de volume, anomalias, sazonalidade e alertas operacionais.

### Técnico

Análise detalhada de clusters, risco de OLA, fatores explicativos e recortes operacionais.

### Modelos

Comparação de modelos, métricas, limitações, artefatos registrados e contexto para seleção/governança.

### Operações

Fila de oportunidades e ações operacionais, permitindo registrar o resultado da atuação e fechar o ciclo de feedback.

### Administração

Gestão de usuários, convites, papéis, ativação, revogação e acompanhamento de uso, com auditoria.

### Chatbot

Assistente contextual integrado ao dashboard, com consultas determinísticas e analíticas, ferramentas somente leitura, modos rápido/profundo, histórico, feedback, cache e metadados de uso.

## Backend e segurança

- API FastAPI organizada em rotas de contexto, previsões, risco, clusters, KPIs, modelos, operações, chat e administração.
- Autenticação Microsoft Entra, vínculo por tenant e object ID e sessão temporária assinada.
- Controle de acesso persistido e revogação de sessões após mudanças administrativas.
- Guardrails, limites de acesso, telemetria sem armazenamento de prompts e ferramentas analíticas somente leitura.
- Persistência configurável para SQLite/PostgreSQL e cache compartilhado opcional por Redis/Valkey.

## Inteligência analítica

- Previsão de volume com baseline sazonal, Prophet, Monte Carlo e LSTM.
- Classificação de risco de violação de OLA com XGBoost e explicabilidade.
- Segmentação operacional com K-Means.
- Comparação de modelos no mesmo holdout temporal.
- Registro de modelos e validação de contratos dos artefatos antes do deploy.
- Projeções de longo horizonte tratadas como cenários exploratórios fora do horizonte validado.

## Princípio para as entregas

Cada documento ou notebook da Sprint 3 deve responder:

1. Qual parte do produto atual esta disciplina sustenta?
2. Como os dados percorrem o sistema até chegar ao usuário?
3. Qual evidência real comprova o funcionamento?
4. Quais componentes existem hoje e quais são propostas acadêmicas ainda não implantadas?
5. Como a atividade contribui para disponibilidade, segurança, explicabilidade ou decisão operacional?

Não apresentar como existente qualquer recurso Azure, ADF, MySQL, Airflow ou Power BI que ainda não tenha sido realmente implementado e evidenciado.
