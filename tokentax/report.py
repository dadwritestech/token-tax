"""Join token counts with prices.yaml and emit everything the README and site need.

  python -m tokentax.report   ->  results/summary.json, site/data.js, results/tables.md
"""
from __future__ import annotations

import json
import pathlib

import yaml

from . import metrics as m
from .registry import API_ONLY, TOKENIZERS

ROOT = pathlib.Path(__file__).resolve().parent.parent
EN = "eng_Latn"


def group_identical(counts: dict) -> dict:
    """Map each tokenizer id to the first id with an identical count vector.
    Byte-identical tokenizers (e.g. Phi-4 reusing cl100k) collapse into one row."""
    canon, seen = {}, {}
    for tid, c in counts.items():
        key = tuple(sorted(c.items()))
        canon[tid] = seen.setdefault(key, tid)
    return canon


def tokenizer_rows(counts: dict, languages: dict) -> list[dict]:
    canon = group_identical(counts)
    rows = []
    for tid, c in counts.items():
        if canon[tid] != tid:
            continue
        spec = TOKENIZERS.get(tid) or API_ONLY.get(tid, {})
        en = c[EN]
        prem = {l: m.premium(n, en) for l, n in c.items()}
        others = {l: p for l, p in prem.items() if l != EN}
        worst = max(others, key=others.get)
        rows.append({
            "id": tid, "label": spec.get("label", tid), "vendor": spec.get("vendor", "?"),
            "source": spec.get("name"), "browser": spec.get("browser"),
            "same_as": [t for t in counts if canon[t] == tid and t != tid],
            "tokens": c,
            "premium": prem,
            "tokens_per_word": {l: m.per_unit(n, languages[l]["words"]) for l, n in c.items()},
            "tokens_per_char": {l: m.per_unit(n, languages[l]["chars"]) for l, n in c.items()},
            "geomean_premium": m.geomean(others.values()),
            "worst": {"lang": worst, "premium": others[worst]},
        })
    rows.sort(key=lambda r: r["geomean_premium"])
    return rows


def model_rows(prices: dict, counts: dict, languages: dict) -> list[dict]:
    en_words = languages[EN]["words"]
    out = []
    for p in prices["models"]:
        tid = p.get("tokenizer")
        row = dict(p)
        c = counts.get(tid) if tid else None
        row["measured"] = c is not None
        if c and p.get("input") is not None:
            row["usd_in_per_m_en_words"] = {l: m.cost_per_m_en_words(n, en_words, p["input"]) for l, n in c.items()}
            row["usd_out_per_m_en_words"] = {l: m.cost_per_m_en_words(n, en_words, p["output"]) for l, n in c.items()}
        if c and p.get("context"):
            row["context_en_words"] = {l: m.context_words(p["context"], n, en_words) for l, n in c.items()}
            row["context_native_words"] = {l: m.context_words(p["context"], n, languages[l]["words"])
                                           for l, n in c.items() if languages[l]["spaced"]}
        out.append(row)
    return out


def build_summary(counts_doc: dict, prices: dict) -> dict:
    counts, languages = counts_doc["counts"], counts_doc["languages"]
    return {
        "meta": {**counts_doc["meta"], "prices_checked": str(prices["checked"])},
        "languages": languages,
        "tokenizers": tokenizer_rows(counts, languages),
        "models": model_rows(prices, counts, languages),
        "pending": [k for k in API_ONLY if k not in counts],
    }


def _fmt_table(summary: dict, langs: list[str]) -> str:
    L = summary["languages"]
    head = "| tokenizer | " + " | ".join(L[l]["name"] for l in langs) + " | geomean (47 langs) | worst |"
    sep = "|---" * (len(langs) + 3) + "|"
    lines = [head, sep]
    for r in summary["tokenizers"]:
        label = r["label"] + (f" (= {', '.join(r['same_as'])})" if r["same_as"] else "")
        cells = [f"{r['premium'][l]:.2f}×" for l in langs]
        w = r["worst"]
        lines.append(f"| {label} | " + " | ".join(cells) +
                     f" | {r['geomean_premium']:.2f}× | {L[w['lang']]['name']} {w['premium']:.1f}× |")
    return "\n".join(lines)


def _fmt_cost(summary: dict, langs: list[str]) -> str:
    L = summary["languages"]
    head = "| model | " + " | ".join(L[l]["name"] for l in langs) + " | context window holds (Telugu content, English-equivalent words) |"
    lines = [head, "|---" * (len(langs) + 2) + "|"]
    for r in summary["models"]:
        if "usd_in_per_m_en_words" not in r:
            continue
        cost = r["usd_in_per_m_en_words"]
        ctx = r.get("context_en_words", {})
        ctx_cell = f"{r['context']:,} tok → {ctx['tel_Telu']:,.0f} (vs {ctx[EN]:,.0f} English)" if ctx else ""
        lines.append(f"| {r['id']} | " + " | ".join(f"${cost[l]:.2f}" for l in langs) + f" | {ctx_cell} |")
    return "\n".join(lines)


def main():
    counts_doc = json.loads((ROOT / "results" / "counts.json").read_text(encoding="utf-8"))
    prices = yaml.safe_load((ROOT / "prices.yaml").read_text(encoding="utf-8"))
    s = build_summary(counts_doc, prices)
    # A few parallel FLORES sentences (CC BY-SA 4.0) as calculator samples.
    # Without the (gitignored) FLORES download, reuse the samples already in summary.json.
    from .measure import load_corpus
    try:
        s["samples"] = {l: "\n".join(load_corpus(l).splitlines()[1:4])
                        for l in ["eng_Latn", "tel_Telu", "hin_Deva", "tam_Taml", "amh_Ethi", "mya_Mymr", "zho_Hans"]}
    except FileNotFoundError:
        s["samples"] = json.loads((ROOT / "results" / "summary.json").read_text(encoding="utf-8"))["samples"]
    (ROOT / "results" / "summary.json").write_text(json.dumps(s, indent=1, ensure_ascii=False), encoding="utf-8")
    (ROOT / "site" / "data.js").write_text("window.TOKEN_TAX = " + json.dumps(s, ensure_ascii=False) + ";\n",
                                           encoding="utf-8")
    key = ["tel_Telu", "hin_Deva", "tam_Taml", "amh_Ethi", "yor_Latn", "mya_Mymr", "arb_Arab", "zho_Hans", "deu_Latn"]
    md = ["## Token premium vs English (same FLORES content)\n", _fmt_table(s, key),
          "\n\n## Input $ per 1M English-equivalent words\n", _fmt_cost(s, ["eng_Latn"] + key)]
    (ROOT / "results" / "tables.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("wrote results/summary.json, site/data.js, results/tables.md")


if __name__ == "__main__":
    main()
