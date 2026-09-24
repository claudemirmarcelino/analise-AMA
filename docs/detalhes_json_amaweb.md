## Dados derivados dos JSONs

Além dos CSVs consolidados, o projeto agora possui uma rotina para transformar os JSONs individuais do AMAWeb em tabelas analíticas:

- `dados/amaweb_praticas_detalhe.csv`: uma linha por prática avaliada em cada JSON.
- `dados/amaweb_resumo_praticas.csv`: consolidação por site, prática e veredito.
- `dados/amaweb_elementos_detalhe.csv`: elementos individuais retornados pela avaliação.

A rotina também trata `warning` e `cantTell` como "Verificar manualmente" e preserva o código de resultado (`resultCode`).

O workflow `.github/workflows/atualizar_amaweb.yml` executa essa extração usando diretamente uma cópia pública do repositório-fonte, sem modificar o repositório de origem.