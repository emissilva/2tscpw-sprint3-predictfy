# Guia de execução e coleta de evidências — Data Warehouse

Este guia é o índice operacional. Os comandos completos e suas explicações estão em `PASSO_A_PASSO_EXECUCAO.md`.

## Pré-requisitos

1. Assinatura Azure ativa com permissão de Contributor.
2. Azure CLI/Bicep, `jq`, MySQL 8 e Python 3.
3. Execução a partir de `predictfy-locaweb/Sprint 3/02_data_warehouse`.
4. Tempo para concluir duas cargas e coletar evidências antes de remover recursos.

## 1. Preparar e validar

Use as seções iniciais do passo a passo para selecionar a assinatura, definir um sufixo globalmente único e informar a senha com `read -s`. Não grave senha ou connection string no projeto.

Execute `validate_local.py`, compile `iac/main.bicep` e valide os nove JSONs antes de gerar custo.

## 2. Provisionar a infraestrutura

Execute individualmente os comandos da seção 4 do passo a passo. Eles criam Resource Group exclusivo, ADF e Storage em East US 2 e MySQL em uma região aceita pela assinatura.

Confira pelo terminal:

```bash
az resource list --resource-group "$AZURE_RESOURCE_GROUP" --output table
```

## 3. Preparar MySQL e landing

Execute as seções 5 e 6: crie `fato_incidente_predictfy` com TLS, envie `incidentes_predictfy.csv` e `regras_ola.txt` e confirme os dois arquivos no container `landing`.

## 4. Publicar o ADF manualmente

Execute, na ordem, as seções 7 a 10:

1. linked services Blob e MySQL;
2. quatro datasets;
3. `df_incidentes_predictfy`;
4. `pl_ingestao_incidentes_predictfy`.

Cada artefato possui seu próprio comando `az rest`; o roteiro não depende de `scripts/publish_adf.sh`.

No ADF Studio, confira que `selectDestino` segue diretamente para o TXT e passa por Alter Row somente no ramo MySQL.

## 5. Executar duas vezes

Use as seções 11 e 12 para criar a primeira e a segunda execução. Consulte cada `runId` até `Succeeded` e colete as métricas de atividade. Não execute as cargas em paralelo.

## 6. Validar os dois destinos

Execute as consultas da seção 13. O esperado é:

- 25.588 registros;
- 25.588 chaves distintas;
- zero prioridades sem regra;
- colunas derivadas e de linhagem preenchidas.

Depois execute a seção 14 para confirmar o TXT, contar as linhas e inspecionar o cabeçalho delimitado por `|`.

## 7. Coletar evidências

Capture janelas reais e legíveis, sem segredos:

- inventário do Resource Group;
- blobs de landing e curated;
- canvas e Derived Column no ADF Studio;
- duas execuções `Succeeded` e métricas;
- consultas MySQL;
- TXT curated e amostra.

Preserve os retornos JSON/TXT em uma pasta nova. Não reutilize evidências antigas como se fossem da nova execução.

## 8. Encerrar com segurança

Remova os segredos da sessão. Se o ambiente for efêmero, siga a seção 17: crie o marcador de evidências, valide o prefixo `rg-predictfy-dw-sprint3-*`, mostre o inventário e somente então remova o Resource Group.

```bash
az group exists --name "$AZURE_RESOURCE_GROUP"
```

O retorno final esperado é `false`.
