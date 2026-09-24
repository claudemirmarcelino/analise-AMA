# analise-AMA

Repositório independente para análise integrada de acessibilidade de portais públicos de Mato Grosso com AMAWeb e AccessMonitor.

## Fonte
Dados transformados a partir de `Giuseph66/analize_sites_Egov`, sem alterar o repositório de origem.

## Conteúdo
- `dados/fato_amaweb_mt.csv`: consolidado AMAWeb dos sites MT.
- `dados/fato_accessmonitor_mt.csv`: quatro runs do AccessMonitor MT de 21/09/2026, unidos e deduplicados pela URL normalizada.
- `dados/base_integrada_mt.csv`: comparação dos dois instrumentos.
- `dados/fato_accessmonitor_ouvidorias.csv`: AccessMonitor da rodada de Ouvidorias de 21/09/2026.
- `dados/validacao_ouvidorias.csv`: validação funcional das Ouvidorias.
- `scripts/gerar_detalhe_json.py`: extrator dos JSONs individuais do AMAWeb.
- `dados/amaweb_praticas_detalhe.csv`: saída do extrator, com uma linha por prática.
- `dados/amaweb_resumo_praticas.csv`: saída resumida por site, prática e veredito.
- `dados/amaweb_elementos_detalhe.csv`: saída detalhada dos elementos avaliados.

## JSONs do AMAWeb
Os JSONs individuais não serão ignorados. Eles são a fonte dos detalhes de prática, veredito, código de resultado e elementos.

O workflow `.github/workflows/atualizar_amaweb.yml` baixa uma cópia do repositório público de origem e executa a transformação automaticamente. Ele pode ser executado em **Actions > Atualizar detalhes AMAWeb > Run workflow**.

## Regra de qualidade
Resultados identificados como Cloudflare/Access Denied/Just a Moment permanecem nos dados, mas não contam como avaliação utilizável para indicadores de nota.

## Importante
O repositório de origem permanece intacto. Toda transformação acontece somente neste repositório.