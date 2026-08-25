# 01 — Cloud Solutions & Scalable Infrastructure

Entrega da Sprint 3 baseada no produto Predictfy. O repositório `../../locaweb` é somente leitura.

## Objetivo

Demonstrar a execução da camada de aplicação e da lógica analítica em Microsoft Azure, com infraestrutura reproduzível, container, banco gerenciado e monitoramento.

## Arquitetura escolhida

- **Resource Group:** ciclo de vida isolado da Sprint 3.
- **Azure Container Registry:** armazenamento privado da imagem da API.
- **Azure Container Instances:** execução do container FastAPI.
- **Azure Database for MySQL Flexible Server:** persistência exigida pela disciplina.
- **Log Analytics Workspace:** centralização de logs do container.
- **Application Insights:** disponibilidade e telemetria da aplicação.
- **Microsoft Entra ID:** autenticação já usada pelo produto.
- **Vercel:** hospedagem atual do frontend React; permanece representada como serviço externo.
- **OpenAI:** provedor analítico do chatbot; permanece externo e configurável.

## Conteúdo desta entrega

- `ARQUITETURA.md`: desenho lógico, fluxo e justificativas.
- `MATRIZ_REQUISITOS.md`: rastreabilidade item a item do enunciado.
- `iac/`: provisionamento Azure CLI idempotente e parametrizado.
- `app_mysql/`: integração mínima com MySQL para registrar e consultar execuções analíticas.
- `RELATORIO_ENTREGA.md`: texto-base do PDF e pontos de inserção das evidências reais.
- `CHECKLIST_EVIDENCIAS.md`: capturas e testes necessários após o deploy.
- `EXECUCAO_AZURE_2026-08-20.md`: resultado consolidado da execução real.
- `PASSO_A_PASSO_EXECUCAO.md`: roteiro completo para reproduzir a implantação, validar, coletar evidências e descartar os recursos (exceto Draw.io).
- `evidencias/azure/`: inventário, logs, métricas e consultas coletados pela Azure CLI.
- `evidencias/reexecucao_2026-08-23/capturas_reais/`: capturas reais do Terminal e Portal Azure.
- `evidencias/entrega_final/`: relatório HTML, arquitetura, gráficos e marcas usadas no documento.
- `gerar_entrega.py`: gerador dos artefatos visuais e do relatório.
- `gerar_pdf_final.py`: gerador do PDF com capa independente, cabeçalho, rodapé e paginação.
- `Cloud_Locaweb_Sprint3_Predictfy.pdf`: documento oficial para entrega.
- `AGENTS.md`: padrão de referência para as demais disciplinas.

## Estado

**Encerrado e pronto para entrega.**

Execução Azure, ML → MySQL, logs, métricas e Application Insights foram validados em 23/08/2026. O PDF final possui uma capa sem cabeçalho ou numeração e 14 páginas internas numeradas. O ambiente efêmero foi removido integralmente após a coleta, e a verificação independente confirmou que o Resource Group não existe mais.
