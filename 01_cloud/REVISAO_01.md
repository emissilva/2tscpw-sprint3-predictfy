# Revisão 01 — entrega Cloud

## Aderência já atendida no material

- Arquitetura contém Resource Group, ACI, Docker, MySQL, Azure Monitor e Application Insights.
- Fluxo mostra entrada do usuário até previsões/resultados.
- IaC usa Azure CLI, conforme conteúdo da disciplina.
- Build usa o Dockerfile real do produto atual.
- Relatório segue a sequência pedida no enunciado.
- Telas, chatbot, autenticação, administração, operações e governança atuais aparecem na narrativa e no checklist.

## Correções aplicadas

- Entregas antigas deixaram de ser referência arquitetural.
- Métricas antigas não foram reutilizadas.
- MySQL foi tratado como integração nova, sem fingir suporte no backend atual.
- Evidências externas foram marcadas como pendentes, sem imagens simuladas.
- Segredos foram removidos dos exemplos de configuração.

## Pendências da próxima revisão

- Criar arquivo Draw.io editável e validar legibilidade da exportação.
- Finalizar e testar o adaptador MySQL.
- Validar comandos com uma assinatura Azure antes da coleta de evidências.
- Definir HTTPS para integração direta com o frontend publicado; o endpoint público padrão do ACI não deve ser apresentado como arquitetura produtiva.
- Instrumentar telemetria real ou configurar teste de disponibilidade no Application Insights.
- Converter o relatório revisado para PDF somente após inserir evidências reais.
