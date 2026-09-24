# Metodologia

A URL é normalizada removendo protocolo, `www.`, barra final e fragmento, mantendo caminho e query. A correspondência entre AMAWeb e AccessMonitor tenta primeiro a URL normalizada e, na falta dela, o mesmo hostname; o campo `correspondencia` registra qual regra foi usada.

Os quatro runs do AccessMonitor MT de 21/09/2026 são consolidados e deduplicados por URL, mantendo a ocorrência do run mais recente em que a URL aparece.

Notas exibidas em páginas de bloqueio Cloudflare não são consideradas avaliações utilizáveis. A validação funcional das Ouvidorias permanece separada da avaliação de acessibilidade.