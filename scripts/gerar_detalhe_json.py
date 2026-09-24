#!/usr/bin/env python3
"""
Extrai dados analíticos dos JSONs do AMAWeb.

Uso:
  python scripts/gerar_detalhe_json.py --source-dir ../analize_sites_Egov

Saídas:
  dados/amaweb_praticas_detalhe.csv
  dados/amaweb_resumo_praticas.csv
  dados/amaweb_elementos_detalhe.csv
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--source-dir", type=Path, required=True)
    p.add_argument("--output-dir", type=Path, default=Path("dados"))
    return p.parse_args()


def safe_url(host: str | None) -> str:
    if not host:
        return ""
    try:
        u = urlsplit(host.strip())
        h = u.hostname or ""
        h = h.lower().removeprefix("www.")
        path = u.path.rstrip("/")
        return f"{h}{path}{u.query}"
    except Exception:
        return host.strip().lower()


def verdict_label(verdict: str) -> str:
    return {
        "passed": "Aceitável",
        "failed": "Não aceitável",
        "warning": "Verificar manualmente",
        "cantTell": "Verificar manualmente",
        "inapplicable": "Não aplicável",
    }.get(verdict, verdict or "")


def iter_json_files(source_dir: Path):
    roots = [
        source_dir / "webscrap_amaweb" / "saida_mt",
        source_dir / "webscrap_amaweb" / "saida_ouvidorias_mt",
    ]
    for root in roots:
        if root.exists():
            yield from sorted(root.rglob("*.json"))


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    practice_rows: list[dict[str, str]] = []
    element_rows: list[dict[str, str]] = []
    summary_counter: Counter[tuple[str, str, str, str, str]] = Counter()
    files_read = 0

    for path in iter_json_files(args.source_dir):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            data = payload.get("result", {}).get("data", {})
            if not isinstance(data, dict):
                continue
        except Exception:
            continue

        files_read += 1
        raw_url = str(data.get("rawUrl") or "")
        title = str(data.get("title") or "")
        score = str(data.get("score") or "")
        context = (
            "ouvidorias"
            if "saida_ouvidorias_mt" in path.as_posix()
            else "mt"
        )

        nodes = data.get("nodes") or {}
        if not isinstance(nodes, dict):
            continue

        for practice, items in nodes.items():
            if not isinstance(items, list):
                continue

            for item in items:
                if not isinstance(item, dict):
                    continue

                verdict = str(item.get("verdict") or "")
                label = verdict_label(verdict)
                code = str(item.get("resultCode") or item.get("code") or "")
                description = str(item.get("description") or "")
                elements = item.get("elements")
                if not isinstance(elements, list):
                    elements = []

                row = {
                    "contexto": context,
                    "arquivo_json": path.as_posix(),
                    "url": raw_url,
                    "url_chave": safe_url(raw_url),
                    "titulo": title,
                    "nota": score,
                    "practice": str(practice),
                    "verdict": verdict,
                    "veredito": label,
                    "result_code": code,
                    "description": description,
                    "element_count": str(len(elements)),
                }
                practice_rows.append(row)
                summary_counter[(context, safe_url(raw_url), str(practice), verdict, label)] += 1

                for pos, element in enumerate(elements, start=1):
                    if isinstance(element, dict):
                        element_rows.append({
                            "contexto": context,
                            "arquivo_json": path.as_posix(),
                            "url": raw_url,
                            "url_chave": safe_url(raw_url),
                            "titulo": title,
                            "nota": score,
                            "practice": str(practice),
                            "verdict": verdict,
                            "veredito": label,
                            "result_code": code,
                            "element_ordem": str(pos),
                            "element_json": json.dumps(element, ensure_ascii=False),
                        })
                    else:
                        element_rows.append({
                            "contexto": context,
                            "arquivo_json": path.as_posix(),
                            "url": raw_url,
                            "url_chave": safe_url(raw_url),
                            "titulo": title,
                            "nota": score,
                            "practice": str(practice),
                            "verdict": verdict,
                            "veredito": label,
                            "result_code": code,
                            "element_ordem": str(pos),
                            "element_json": json.dumps(element, ensure_ascii=False),
                        })

    with (args.output_dir / "amaweb_praticas_detalhe.csv").open("w", encoding="utf-8", newline="") as f:
        fields = ["contexto","arquivo_json","url","url_chave","titulo","nota","practice","verdict","veredito","result_code","description","element_count"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(practice_rows)

    summary_rows = []
    for (context, url_key, practice, verdict, label), count in sorted(summary_counter.items()):
        summary_rows.append({
            "contexto": context,
            "url_chave": url_key,
            "practice": practice,
            "verdict": verdict,
            "veredito": label,
            "quantidade": count,
        })

    with (args.output_dir / "amaweb_resumo_praticas.csv").open("w", encoding="utf-8", newline="") as f:
        fields = ["contexto","url_chave","practice","verdict","veredito","quantidade"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(summary_rows)

    with (args.output_dir / "amaweb_elementos_detalhe.csv").open("w", encoding="utf-8", newline="") as f:
        fields = ["contexto","arquivo_json","url","url_chave","titulo","nota","practice","verdict","veredito","result_code","element_ordem","element_json"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(element_rows)

    print(f"JSONs lidos: {files_read}")
    print(f"Linhas de práticas: {len(practice_rows)}")
    print(f"Linhas de elementos: {len(element_rows)}")
    print(f"Linhas de resumo: {len(summary_rows)}")


if __name__ == "__main__":
    main()
