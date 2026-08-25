# Checklist de evidências reais

## 1. Arquitetura

- [x] Arquivo Draw.io editável.
- [x] Representação legível no PDF.
- [x] Legenda de componentes e fluxo explicado.

## 2. Provisionamento IaC

- [x] Execução sem persistir ou exibir segredos.
- [x] Execução bem-sucedida dos scripts.
- [x] Resource Group com todos os recursos coletado pela API/CLI Azure.
- [x] Lista de recursos via Azure CLI.

## 3. Container

- [x] Builds concluídos no ACR.
- [x] Imagens e tags no repositório privado.
- [x] Dois ACIs em estado `Running`.
- [x] FQDN e resposta do endpoint `/api/health`.
- [x] Limitação HTTPS → HTTP declarada; o frontend publicado não foi reconfigurado.

## 4. Machine Learning e produto atual

- [x] Endpoint de captura retornando previsão de artefato real.
- [x] Origem e SHA-256 do artefato registrados.
- [x] Produto atual, telas e chatbot contextualizados sem ampliar o escopo formal de Cloud.

## 5. MySQL

- [x] Banco e tabela criados.
- [x] Inserção efetuada pela aplicação.
- [x] Consulta mostrando a nova execução.
- [x] Processamento agregado por modelo/horizonte/segmento.

## 6. Monitoramento

- [x] Logs do ACI consultados no Log Analytics por KQL.
- [x] Métricas de CPU/memória e comandos MySQL.
- [x] Telemetria OpenTelemetry comprovada no Application Insights.
- [x] Evidência de chamadas saudáveis e falha controlada 401.

## 7. Qualidade do PDF

- [x] Integrantes em ordem alfabética e RMs corretos.
- [x] Seções sequenciais com título, fonte e explicação.
- [x] Segredos, e-mails e IDs sensíveis não são exibidos no PDF.
- [x] Texto diferencia implementado, evidenciado e evolução futura.
- [x] Links, comandos e PDF revisados.
