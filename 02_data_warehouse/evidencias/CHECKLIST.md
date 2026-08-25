# Checklist de evidências reais

Não inserir imagens simuladas. Em cada captura, ocultar usuário, subscription ID, host, senha, connection string e tokens.

- [ ] Resource Group mostrando ADF, Storage Account e o Azure Database for MySQL reaproveitado.
- [ ] Query Editor/cliente SQL executando `001_schema.sql` e exibindo a tabela criada.
- [ ] Container `landing` com `incidentes_predictfy.csv`, `regras_ola.txt` e tamanhos visíveis.
- [ ] Canvas do Data Flow mostrando duas sources, select, filter, join, derive, Alter Row e os dois sinks.
- [ ] Derived Column com as expressões visíveis.
- [ ] Pipeline publicado e execução `Succeeded` no ADF Monitor.
- [ ] Detalhes da atividade com quantidade de linhas lidas/escritas e duração.
- [ ] Resultado das consultas de `002_validacao.sql` no Azure Database for MySQL.
- [ ] Container `curated` com o TXT e uma prévia do conteúdo.
- [ ] Documento final em sequência, com legenda e explicação em cada figura.

Nome sugerido das capturas: `01_recursos_paas.png` até `09_txt_curated.png`.
