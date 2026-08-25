# Revisão final local — Cloud

Data da revisão: 19/08/2026.

## Resultado

O pacote local da disciplina Cloud está completo e aderente à seção da Sprint 3 do documento `Regras_Gerais_Challenge_Locaweb_Fev_2026_2TSCP_F_V_W_X_Sprint_1_2_3_4_v6.pdf`.

## Artefatos concluídos

- Arquitetura lógica e arquivo Draw.io editável.
- Matriz de rastreabilidade dos requisitos.
- Sete scripts shell, um Bicep auxiliar e dois containers para provisionamento, verificação, evidências e descarte.
- Reuso da API e do Dockerfile atuais sem alterar o repositório online.
- Bridge FastAPI isolado com autenticação por chave, TLS para MySQL, schema InnoDB, inserção, consulta e agregação.
- Proveniência por nome e SHA-256 do artefato.
- Instrumentação OpenTelemetry para Application Insights.
- Relatório sequencial final com evidências reais coletadas.
- Guia de execução e checklist de capturas.
- Validador local automatizado.

## Testes executados

- XML Draw.io analisado com sucesso: 1 diagrama e componentes obrigatórios presentes.
- Sintaxe dos sete scripts validada com `bash -n`.
- Sintaxe Python do bridge validada.
- Contexto Docker verificado: todos os arquivos referenciados existem.
- Artefato atual `previsoes_baseline.json` validado nos horizontes D+1 a D+7 para Total, P2 e P3.
- Relatório verificado quanto aos temas obrigatórios e às funcionalidades atuais.
- Estado Git do repositório `locaweb` conferido: nenhuma alteração versionada causada por esta entrega.

## Correções realizadas durante a revisão

- O extrator inicial assumia organização por segmento; foi ajustado ao contrato real `serie` do baseline atual.
- A arquitetura passou a mostrar o bridge como container separado, evitando afirmar que o backend atual suporta MySQL.
- Application Insights deixou de ser apenas um recurso criado e passou a receber telemetria real do bridge via OpenTelemetry.
- Foi acrescentado controle `X-Bridge-Key` nas rotas de banco.
- Foi documentado que o ACI público usa HTTP e não deve ser ligado diretamente ao frontend HTTPS sem terminação TLS.
- Dependências foram atualizadas após conferência nos registros oficiais em 19/08/2026.
- Foi incluído `99_destroy.sh` com prefixo permitido e marcador obrigatório de evidências.

## Validação Azure posterior

Em 20/08/2026, Azure CLI 2.89.1, Docker/OrbStack e a assinatura Azure for Students foram validados. A execução real criou ACR, dois ACIs, MySQL B1ms, Log Analytics e Application Insights. Health checks, previsão 44,0, inserção, consulta, agregação, KQL e métricas passaram. As evidências foram coletadas antes da exclusão integral do Resource Group.

## Parecer

O desenvolvimento, a execução Azure e o PDF final estão aprovados. O Resource Group foi removido e a verificação independente `az group exists` retornou `false`.
