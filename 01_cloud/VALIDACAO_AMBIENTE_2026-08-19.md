# Validação do ambiente para a entrega Cloud

Data: 19/08/2026 (execução atravessou 20/08/2026 UTC).

## Azure

- Azure CLI 2.89.1 instalada e funcional.
- Assinatura `Azure for Students` ativa (`Enabled`) e selecionada como padrão.
- Usuário autenticado com papel `Owner` no escopo da assinatura.
- `Microsoft.ContainerRegistry`: registrado.
- `Microsoft.ContainerInstance`: registrado.
- `Microsoft.OperationalInsights`: registrado.
- `Microsoft.Insights`: registrado.
- `Microsoft.DBforMySQL`: registrado após autorização do responsável pela assinatura.

Nenhum recurso Azure foi criado durante esta validação.

## Docker

- Cliente e servidor Docker 29.4.0 ativos.
- Engine Linux ARM64 via OrbStack.
- Buildx 0.33.0 disponível.
- 10 CPUs e aproximadamente 8 GB disponíveis à VM Docker.
- Build real de `predictfy-mysql-bridge:local-test` concluído com sucesso.

## Teste ponta a ponta local

Foi criado um MySQL 8.0 descartável e o bridge foi executado contra ele.

- `GET /health`: `status=ok`, artefato e banco disponíveis.
- Requisição sem `X-Bridge-Key`: bloqueada com HTTP 401.
- Captura D+1 Total: modelo `baseline_sazonal_7d`, valor 44,0.
- Inserção MySQL: concluída com correlation ID e SHA-256 do artefato.
- Consulta: retornou o registro inserido.
- Processamento agregado: quantidade 1 e média prevista 44,00.

Os dois containers e a rede temporária foram removidos após o teste. A imagem local de teste foi preservada.

## Captura de tela

- `screencapture`, `open` e `osascript` disponíveis.
- Captura real autorizada e validada em 3420 × 2224 pixels.
- Arquivo de teste removido imediatamente, sem inspeção ou persistência.

## Estado para provisionamento

Todos os provedores necessários estão registrados. O ambiente está tecnicamente pronto para o provisionamento, que permanece separado desta validação porque a criação dos recursos pode consumir créditos da assinatura.
