# Infraestrutura PaaS

O template adiciona somente Data Factory e Storage Account com containers `landing`/`curated` ao Resource Group usado pelo `01_cloud`. A identidade gerenciada do ADF recebe acesso aos blobs. O MySQL não é recriado.

```bash
az deployment group create \
  --resource-group rg-predictfy-sprint3-260819es \
  --template-file "Sprint 3/02_data_warehouse/iac/main.bicep" \
  --parameters uniqueSuffix=260819es location=eastus2
```

Revise custos e confirme que o desenvolvimento de `01_cloud` terminou antes de executar. Não rode scripts de destruição enquanto qualquer disciplina estiver usando o Resource Group. O acesso ao MySQL deve usar TLS e segredo fornecido fora do Git.

Depois do provisionamento, execute `sql/001_schema.sql` no banco `predictfy`, envie `data/incidentes_predictfy.csv` e `data/regras_ola.txt` para `landing`, configure o segredo do linked service MySQL e publique os artefatos `adf/` no factory.
