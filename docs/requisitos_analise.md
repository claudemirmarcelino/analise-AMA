# Requisitos da análise — definidos a partir das orientações enviadas

## 1. Organização do experimento

A análise deve preservar a organização original das duas ferramentas:

- **AMAWeb**
  - MT: análise de prefeituras, câmaras e demais sites do lote MT.
  - Ouvidorias: análise específica das páginas/serviços de Ouvidoria.
  - Rodadas especiais de HTML/Cloudflare e respectivos retries.
- **AccessMonitor**
  - MT.
  - Ouvidorias.
  - testes de HTML individual.
  - testes de HTML em lote.

## 2. Não misturar os experimentos

Cada resultado deve carregar, no mínimo:

- ferramenta;
- contexto;
- tipo de experimento;
- data;
- horário/identificador da rodada;
- URL de entrada;
- URL efetivamente avaliada;
- método de avaliação;
- arquivo JSON;
- arquivo PDF;
- arquivo HTML, quando existir;
- status da coleta;
- erro/falha, quando existir.

Assim será possível comparar AMAWeb × AccessMonitor sem misturar uma execução normal com uma execução de fallback por HTML.

## 3. Dados de entrada

A pasta `dados_entradas` é parte da evidência da pesquisa.

Ela deve ser analisada para identificar:

- URLs inicialmente previstas;
- município/entidade;
- URL informada;
- URL final ou tentada;
- validação funcional das Ouvidorias;
- eventuais diferenças entre a URL original e a URL realmente avaliada.

## 4. Dados de falhas

A pasta `dados_falhas` também deve entrar na análise.

Não deve ser tratada simplesmente como "dados ausentes". As falhas precisam ser classificadas, por exemplo:

- DNS;
- HTTP;
- timeout;
- bloqueio;
- Cloudflare;
- URL inválida;
- página sem resultado;
- outro erro técnico.

A quantidade e o tipo de falhas fazem parte da avaliação da qualidade da coleta.

## 5. HTMLs colocados manualmente

Os HTMLs usados nos experimentos de fallback/teste devem ser preservados como uma dimensão metodológica própria.

A pergunta analítica é:

> Quando a avaliação por URL não funciona, o uso do HTML baixado muda a possibilidade de obter uma avaliação?

Por isso, devem ser comparados:

- avaliação direta por URL;
- avaliação a partir do HTML;
- primeira tentativa;
- retries;
- mudança de nota;
- mudança no status;
- tempo/rodada de execução.

## 6. JSONs do AMAWeb

Os JSONs não são apenas evidência de auditoria.

Eles são uma fonte analítica detalhada e devem alimentar:

- prática;
- veredito;
- código de resultado;
- descrição;
- quantidade de elementos;
- elementos avaliados;
- resumo por site;
- resumo por prática;
- comparação de práticas entre ferramentas, quando houver correspondência possível.

## 7. Tempo de execução

O horário `HH-MM-SS` da pasta deve ser usado como identificador da rodada.

Não assumir que esse horário representa a duração.

A duração somente deve ser calculada quando houver:

- horário de início e fim;
- log de execução;
- ou outra evidência temporal equivalente.

Quando não houver essa evidência, registrar `duracao_nao_observavel`, em vez de inventar uma duração.

## 8. Perguntas que a base deve permitir responder

1. Quantos sites foram previstos?
2. Quantos foram efetivamente avaliados?
3. Quantos falharam e por quê?
4. Quais sites tiveram avaliação nas duas ferramentas?
5. Quando as duas ferramentas avaliaram o mesmo site, quais foram as notas e as diferenças?
6. Quais práticas aparecem como problema com maior frequência?
7. O resultado muda quando se usa HTML em vez da URL?
8. Quantas tentativas foram necessárias?
9. Quais rodadas foram retries?
10. Qual foi a cobertura de cada experimento?
11. Qual é o impacto de Cloudflare/bloqueios sobre a cobertura?
12. Em Ouvidorias, a avaliação de acessibilidade deve ser analisada separadamente da confirmação funcional da página.

## 9. Regra de rastreabilidade

Toda linha analítica relevante deve permitir voltar à evidência de origem por:

`fonte -> rodada -> arquivo -> URL -> resultado`

O objetivo é que nenhum indicador do dashboard dependa de uma classificação que não possa ser auditada posteriormente.
