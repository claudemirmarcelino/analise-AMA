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

A consolidação AMAWeb das Ouvidorias fica como próxima etapa porque os resultados do AMAWeb estão distribuídos em JSONs por run, sem um CSV consolidado equivalente ao MT.

## Regra de qualidade
Resultados identificados como Cloudflare/Access Denied/Just a Moment permanecem nos dados, mas não contam como avaliação utilizável para indicadores de nota.