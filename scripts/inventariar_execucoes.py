#!/usr/bin/env python3
"""
Inventaria as rodadas e artefatos existentes no repositório-fonte.

O horário da pasta é tratado como identificador da rodada, não como duração.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
import re


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--source-dir", type=Path, required=True)
    p.add_argument("--output", type=Path, default=Path("dados/inventario_execucoes.csv"))
    args = p.parse_args()

    root = args.source_dir
    targets = [
        ("AMAWeb", "MT", root / "webscrap_amaweb" / "saida_mt"),
        ("AMAWeb", "Ouvidorias", root / "webscrap_amaweb" / "saida_ouvidorias_mt"),
        ("AMAWeb", "MT HTML/Cloudflare", root / "webscrap_amaweb" / "saida_mt_html_cloudflare"),
        ("AMAWeb", "MT HTML/Cloudflare retry", root / "webscrap_amaweb" / "saida_mt_html_cloudflare_retry"),
        ("AMAWeb", "MT HTML/Cloudflare retry 2", root / "webscrap_amaweb" / "saida_mt_html_cloudflare_retry2"),
        ("AMAWeb", "MT HTML/Cloudflare retry 3", root / "webscrap_amaweb" / "saida_mt_html_cloudflare_retry3"),
        ("AccessMonitor", "MT", root / "webscrap_accessmonitor" / "saida_mt"),
        ("AccessMonitor", "Ouvidorias", root / "webscrap_accessmonitor" / "saida_ouvidorias_mt"),
        ("AccessMonitor", "HTML individual", root / "webscrap_accessmonitor" / "teste_html"),
        ("AccessMonitor", "HTML lote", root / "webscrap_accessmonitor" / "teste_html_lote"),
    ]

    rows = []
    for tool, context, base in targets:
        if not base.exists():
            continue
        for day in sorted(base.iterdir()):
            if not day.is_dir() or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", day.name):
                continue
            for run in sorted(day.iterdir()):
                if not run.is_dir():
                    continue
                files = [x for x in run.iterdir() if x.is_file()]
                rows.append({
                    "ferramenta": tool,
                    "contexto": context,
                    "data": day.name,
                    "hora_rodada": run.name,
                    "fonte": str(run.relative_to(root)).replace("\\", "/"),
                    "arquivos": len(files),
                    "json": sum(x.suffix.lower() == ".json" for x in files),
                    "pdf": sum(x.suffix.lower() == ".pdf" for x in files),
                    "html": sum(x.suffix.lower() == ".html" for x in files),
                    "csv": sum(x.suffix.lower() == ".csv" for x in files),
                    "duracao_status": "duracao_nao_observavel",
                })

    args.output.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0]) if rows else [
        "ferramenta","contexto","data","hora_rodada","fonte",
        "arquivos","json","pdf","html","csv","duracao_status"
    ]
    with args.output.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    print(f"Rodadas inventariadas: {len(rows)}")


if __name__ == "__main__":
    main()
