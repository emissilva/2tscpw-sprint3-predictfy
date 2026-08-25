# Guia de execução e coleta de evidências

## Pré-requisitos

1. Assinatura acadêmica Azure ativa e permissão de Contributor.
2. Azure CLI atual ou Azure Cloud Shell.
3. Limite de custo definido pelo grupo.
4. Registros atuais da SPA e API no Microsoft Entra.
5. Execução a partir da raiz `predictfy-locaweb`.

## 1. Configurar sem persistir segredos

Use a seção 5 de `PASSO_A_PASSO_EXECUCAO.md` como lista de variáveis. Exporte os valores na sessão do terminal e informe os segredos com `read -s`. Não grave segredos em arquivo versionado.

Gere sufixos globais curtos para ACR, MySQL e DNS. O nome do ACR aceita somente letras e números minúsculos.

## 2. Entrar e conferir assinatura

```bash
az login
az account list --output table
az account set --subscription "NOME-OU-ID-DA-ASSINATURA"
az account show --output table
```

Capture apenas a tabela necessária e oculte IDs sensíveis no relatório.

## 3. Provisionar

Execute individualmente os comandos Azure CLI da seção 7 de `PASSO_A_PASSO_EXECUCAO.md`: Resource Group, Log Analytics, Application Insights, ACR, MySQL, banco e firewall. Pare se algum comando retornar erro.

Revise no portal: Resource Group, Log Analytics, Application Insights, ACR e MySQL.

## 4. Construir e implantar a API atual

Execute individualmente os comandos das seções 8 e 9 de `PASSO_A_PASSO_EXECUCAO.md`: `az acr build`, obtenção temporária das credenciais, `az container create`, inventário e health check.

Capture o build do ACR, estado do ACI, tag da imagem e resposta do health check.

## 5. Implantar e exercitar o bridge MySQL

Execute individualmente os comandos das seções 10 e 11 de `PASSO_A_PASSO_EXECUCAO.md`: build, deploy e as quatro chamadas `curl` do bridge.

Capture separadamente:

- health com banco conectado;
- inserção D+1 Total;
- consulta do registro persistido;
- agregação por modelo/horizonte/segmento.

## 6. Monitoramento

Execute individualmente todos os comandos da seção 13 de `PASSO_A_PASSO_EXECUCAO.md`. Eles consultam o Log Analytics por KQL, coletam CPU/memória dos ACIs, métricas do MySQL e telemetria do Application Insights. A instrumentação OpenTelemetry é habilitada quando `APPLICATIONINSIGHTS_CONNECTION_STRING` é injetada.

Produza uma chamada válida e uma chamada sem `X-Bridge-Key` para demonstrar, respectivamente, sucesso e bloqueio 401. Não provoque indisponibilidade do ambiente.

## 7. Integração com as telas atuais

Use o produto online para capturar as telas atuais: Gestão, Monitoramento, Técnico, Modelos, Operações, Administração e Chatbot. Explique que o frontend publicado permanece no Vercel, enquanto a Sprint 3 comprova a portabilidade da API e a integração analítica em Azure.

O ACI expõe HTTP por padrão. Navegadores bloqueiam chamadas de uma página HTTPS para uma API HTTP. Não altere a URL do frontend publicado para apontar diretamente ao ACI sem uma camada HTTPS adequada.

## 8. Encerramento e custo

Após confirmar que as evidências estão completas, crie o marcador indicado na seção 15 de `PASSO_A_PASSO_EXECUCAO.md`. Depois, execute manualmente a validação do prefixo do Resource Group e o comando `az group delete` apresentados na seção 16.

Confirme ao final com `az group exists --name "$AZ_RESOURCE_GROUP"`; o resultado esperado é `false`.
