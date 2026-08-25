# Referência de entrega — 01_cloud

## Estado do item

O item `01_cloud` está encerrado e pronto para entrega. Não alterar seus artefatos finais sem solicitação explícita do usuário.

Documento oficial:

- `Cloud_Locaweb_Sprint3_Predictfy.pdf`

Fontes reproduzíveis:

- `gerar_entrega.py`: gera relatório HTML, arquitetura SVG, métricas e Draw.io.
- `gerar_pdf_final.py`: gera capa independente e PDF com cabeçalho, rodapé e paginação nas páginas internas.
- `arquitetura_predictfy_azure.drawio`: arquitetura editável.
- `evidencias/entrega_final/`: HTML, SVGs, marcas e gráficos finais.
- `evidencias/reexecucao_2026-08-23/`: capturas, logs e JSONs da execução real.

O ambiente Azure foi removido após a coleta das evidências. A confirmação `az group exists = false` está registrada no relatório e nos arquivos de evidência.

## Padrão mínimo para as próximas disciplinas

Utilizar esta entrega como referência de qualidade documental, não como modelo de conteúdo a ser copiado literalmente. Cada disciplina deve continuar obedecendo ao seu próprio enunciado.

1. Ler primeiro o trecho da disciplina no enunciado oficial e construir uma matriz de cobertura.
2. Produzir evidências reais. Não criar prints, resultados, métricas ou telas simuladas.
3. Registrar comandos executados, respostas relevantes e telas do serviço utilizado.
4. Explicar em cada imagem o que deve ser observado e qual parte da solução ela comprova.
5. Preservar arquivos brutos de evidência, como JSON, logs e saídas do terminal.
6. Nunca incluir senhas, tokens, chaves, connection strings ou credenciais nas capturas e documentos.
7. Se forem usados recursos pagos ou efêmeros, coletar e validar todas as evidências antes do descarte; depois registrar a confirmação da remoção.

## Padrão visual do relatório

- Nome do grupo: `Predictfy`.
- Capa limpa, sem cabeçalho, rodapé ou número.
- Cabeçalho somente nas páginas internas, com marca Predictfy, disciplina/Sprint e FIAP.
- Rodapé somente nas páginas internas, com identificação do Challenge e paginação.
- A primeira página após a capa inicia em `Página 1`.
- Títulos únicos por seção, com hierarquia visual consistente.
- Evitar páginas com uma única imagem pequena e grandes áreas vazias.
- Permitir fluxo entre páginas, mas manter juntos tabelas, blocos de código, imagens e respectivas legendas.
- Prints devem ser legíveis e acompanhados de contexto técnico; não usar imagens como decoração.
- Remover do documento entregue checklists internos, rastreabilidade de produção, pendências editoriais e instruções para a equipe.
- O nome do arquivo deve começar pela disciplina e permanecer descritivo, seguindo o exemplo `Cloud_Locaweb_Sprint3_Predictfy.pdf`, salvo convenção específica do enunciado.

## Padrão de arquitetura e diagramas

- Entregar a fonte editável quando solicitada, especialmente `.drawio`.
- Preferir ícones oficiais do provedor utilizado.
- Manter caixas alinhadas, dimensões consistentes e textos integralmente contidos.
- Usar conectores ortogonais, apenas com ângulos de 90 graus.
- Centralizar entradas e saídas nas extremidades das caixas.
- Unificar trechos de conectores quando compartilharem a mesma origem ou destino e isso não alterar a semântica.
- Diferenciar visualmente fluxos de dados, implantação, logs, telemetria e métricas.
- Toda seta deve representar uma integração realmente executada ou uma relação exigida e claramente identificada.
- Revisar se todos os componentes citados no texto aparecem no desenho e se todos os componentes desenhados fazem parte da entrega.

## Validação antes de encerrar outra disciplina

- Conferir todos os requisitos e o bloco “Como será a entrega?” do enunciado.
- Validar o formato e o nome do arquivo.
- Extrair o texto do PDF e procurar itens obrigatórios e termos internos que não devem aparecer.
- Renderizar todas as páginas em miniaturas e revisar cortes, sobreposições, espaços excessivos e legibilidade.
- Confirmar que cabeçalhos, rodapés e números não cobrem o conteúdo.
- Conferir quantidade de páginas, tamanho A4 e abertura do PDF final.
- Validar arquivos XML/SVG/Draw.io quando aplicável.
- Manter uma única versão claramente identificada como documento oficial de entrega.

