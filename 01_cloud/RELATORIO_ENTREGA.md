# Predictfy AIOps — Cloud Solutions & Scalable Infrastructure

## Sprint 3 — Challenge Locaweb 2026

### Integrantes

| Integrante | RM |
|---|---:|
| Elton Vinicios Almeida de Oliveira | 562187 |
| Emerson dos Santos Silva | 562033 |
| Kelvin Douglas Ribeiro Rabelo | 561538 |
| Pedro Henrique Simão Soares | 562283 |
| Vitor Lucas Mattos de Brito Mariano | 562116 |

> Nome final: `Locaweb_Sprint3_Predictfy.pdf`, seguindo o padrão oficial `Locaweb_Sprint3_Nome_do_Grupo.pdf`.

---

## 1. Contexto da solução atual

A Predictfy é uma solução de AIOps criada para transformar o histórico de incidentes da Locaweb em apoio preditivo à operação. O produto atual combina previsão de volume, classificação de risco de violação de OLA, segmentação de padrões operacionais, explicabilidade, governança de modelos e um ciclo de feedback das ações tomadas.

O sistema não se limita aos modelos. O dashboard possui visões de Gestão, Monitoramento, Técnico, Modelos, Operações e Administração. Um chatbot contextual combina respostas determinísticas com análises por LLM, respeitando autenticação Microsoft Entra, papéis de acesso, histórico, limites de uso, cache e rastreabilidade das fontes.

**Evidência 1 — produto atual:** inserir uma composição legível das telas de Gestão, Modelos, Operações, Administração e Chatbot.

**Explicação da evidência:** as telas comprovam que a implantação em nuvem suporta um produto integrado e não apenas um endpoint isolado de Machine Learning.

---

## 2. Desenho da arquitetura

A arquitetura da Sprint 3 preserva o frontend React publicado e transfere a execução containerizada da API para o Microsoft Azure. O Azure Container Registry armazena a imagem privada, enquanto o Azure Container Instances executa a API FastAPI com os artefatos analíticos governados. O Azure Database for MySQL registra as execuções analíticas previstas para a disciplina. Log Analytics e Application Insights centralizam logs, disponibilidade e desempenho.

O Microsoft Entra ID continua responsável pela identidade. O provedor de LLM permanece desacoplado, permitindo consultas analíticas sem misturar credenciais com os artefatos de modelo.

**Figura 1 — arquitetura da solução:** inserir exportação do arquivo Draw.io.

**Descrição:** explicar o fluxo numerado desde o login e a interação nas telas até a API, modelos, MySQL e observabilidade.

### Justificativa dos componentes

| Componente | Papel | Justificativa |
|---|---|---|
| Resource Group | Isolar recursos da entrega | Simplifica governança, custos e ciclo de vida |
| ACR | Guardar imagens privadas | Versionamento, rastreabilidade e integração nativa com ACI |
| ACI | Executar a API FastAPI | Atende ao enunciado sem administração de VM |
| MySQL Flexible Server | Persistência DBaaS | Serviço gerenciado exigido na disciplina |
| Log Analytics | Centralizar logs | Permite investigação por consultas e correlação temporal |
| Application Insights | Disponibilidade e APM | Evidencia saúde, falhas e desempenho da aplicação |
| Entra ID | Identidade | Mantém a segurança já implementada no produto atual |

---

## 3. Provisionamento com infraestrutura como código

O provisionamento foi automatizado em Azure CLI, com Bicep auxiliar para o MySQL mínimo. Os scripts verificam variáveis obrigatórias e usam nomes parametrizados. Segredos não são armazenados nos arquivos; senha do banco e chaves efêmeras são fornecidas apenas no momento da execução.

Arquivos:

- `iac/01_provision.sh`: Resource Group, Log Analytics, Application Insights, ACR e MySQL.
- `iac/02_build_and_deploy.sh`: build remoto da imagem e implantação no ACI.
- `iac/03_verify.sh`: inventário, estado, health check e verificações dos serviços.
- `iac/04_deploy_mysql_bridge.sh`: build e implantação do adaptador MySQL com telemetria.
- `iac/05_exercise_mysql.sh`: inserção, consulta e processamento usados nas evidências.
- `iac/06_collect_cli_evidence.sh`: inventário, logs, consultas e métricas em arquivos reproduzíveis.
- `iac/99_destroy.sh`: exclusão protegida do Resource Group após validação das evidências.
- `iac/mysql_ephemeral.bicep`: MySQL B1ms, 32 GB, retenção de 1 dia e sem alta disponibilidade.

**Figura 2 — execução do IaC:** inserir terminal com provisionamento concluído, ocultando IDs e segredos quando necessário.

**Figura 3 — Resource Group:** inserir portal Azure mostrando os recursos provisionados.

**Descrição:** destacar repetibilidade, parametrização e separação entre código e configuração sensível.

---

## 4. Execução da aplicação com containers

A API atual já possui Dockerfile baseado em Python 3.11. O ACR executa o build remoto usando esse Dockerfile e publica uma imagem versionada. O ACI obtém a imagem do registro privado, expõe a porta 8000 e inicia o Uvicorn/FastAPI.

O endpoint `/api/health` comprova a execução e informa quais artefatos analíticos estão disponíveis dentro da imagem. As demais rotas permanecem protegidas pela sessão do Predictfy.

**Figura 4 — build no ACR:** inserir log final e lista de tags do repositório `predictfy-api`.

**Figura 5 — ACI em execução:** inserir estado `Running`, imagem, FQDN e configuração de recursos.

**Figura 6 — health check:** inserir chamada e resposta JSON de `/api/health`.

---

## 5. Integração com dados e Machine Learning

A imagem contém os artefatos governados produzidos pelo pipeline atual. A API seleciona os modelos de previsão com base em comparação no mesmo holdout temporal e expõe previsões normalizadas ao dashboard. Outros endpoints fornecem risco de OLA, explicabilidade, clusters, KPIs e registro dos modelos.

As telas atuais transformam esses resultados em decisões: Gestão acompanha impacto executivo; Monitoramento observa tendências e alertas; Técnico investiga explicabilidade; Modelos compara qualidade e limitações; Operações registra ações e resultados; o Chatbot combina fontes para responder perguntas contextuais.

**Figura 7 — modelo consumido pela API:** inserir resposta autenticada de uma rota de previsão e a tela correspondente.

**Figura 8 — governança:** inserir tela de Modelos e evidência do registro/validação dos artefatos.

**Figura 9 — operação assistida:** inserir tela de Operações e exemplo do ciclo de feedback.

---

## 6. Banco de Dados em Nuvem

O Azure Database for MySQL Flexible Server é utilizado para demonstrar persistência das execuções analíticas da Sprint 3. A integração registra metadados mínimos: correlação, modelo, horizonte, segmento, valor previsto, origem e SHA-256 do artefato e instante UTC.

Essa tabela permite:

- inserir uma nova execução após o processamento;
- consultar o histórico por modelo ou período;
- agregar quantidade e média de resultados;
- rastrear qual artefato originou a informação.

Prompts, tokens de autenticação, segredos e dados pessoais não são armazenados.

**Figura 10 — banco e estrutura:** inserir servidor, banco e criação da tabela.

**Figura 11 — inserção:** inserir execução pela aplicação e linha persistida.

**Figura 12 — consulta e processamento:** inserir consulta agregada por modelo/horizonte.

> Execução Azure validada em 20/08/2026: previsão D+1 Total = 44,0; inserção, consulta e agregação concluídas no MySQL `Ready`.

---

## 7. Monitoramento da aplicação

O ACI envia stdout, stderr e eventos ao Log Analytics Workspace. O bridge envia telemetria OpenTelemetry ao Application Insights. A evidência inclui consulta KQL, métricas reais de CPU/memória e tráfego 200/401 controlado.

O monitoramento deve responder três perguntas operacionais:

1. A API está disponível?
2. Houve erros ou degradação no período?
3. Qual evento de infraestrutura ou aplicação explica a anomalia?

**Figura 13 — logs:** inserir consulta dos logs do container.

**Figura 14 — métricas:** inserir gráfico de CPU/memória ou volume de requisições.

**Figura 15 — Application Insights:** inserir teste de disponibilidade e painel de falhas/desempenho.

---

## 8. Segurança, escalabilidade e custos

O projeto separa identidade, aplicação, dados e observabilidade. Tokens Entra e autorização por papel protegem as rotas. Segredos são injetados no ambiente e nunca incluídos na imagem. O ACR é privado e o MySQL deve ter acesso reduzido ao mínimo necessário.

ACI e MySQL foram dimensionados para demonstração acadêmica: ACI com 1 vCPU, ACR Basic e MySQL B1ms/32 GB, retenção de 1 dia, sem alta disponibilidade ou geobackup. O Resource Group foi removido após a coleta para interromper custos. Para uma evolução produtiva, a arquitetura pode adotar HTTPS gerenciado, rede privada, Key Vault, identidade gerenciada e autoscaling.

---

## 9. Conclusão

A Sprint 3 materializa o Predictfy atual em uma arquitetura Azure reproduzível. O uso de ACR e ACI demonstra a portabilidade da API; MySQL comprova persistência e processamento em DBaaS; Azure Monitor e Application Insights tornam a execução observável. A solução preserva autenticação, chatbot, telas e governança, conectando modelos preditivos a decisões operacionais reais.

---

## Referências técnicas

- Documento oficial do Challenge Locaweb — Sprint 3.
- Materiais da disciplina Cloud Solutions & Scalable Infrastructure.
- Microsoft Learn — [Azure Container Registry](https://learn.microsoft.com/cli/azure/acr), [logs do Azure Container Instances](https://learn.microsoft.com/azure/container-instances/container-instances-log-analytics), [Azure Database for MySQL Flexible Server](https://learn.microsoft.com/azure/mysql/flexible-server/quickstart-create-server-cli), [Log Analytics](https://learn.microsoft.com/azure/azure-monitor/logs/quick-create-workspace) e [Application Insights](https://learn.microsoft.com/azure/azure-monitor/app/create-workspace-resource).
- Documentação técnica do MVP Predictfy AIOps.
