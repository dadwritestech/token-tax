"""token-tax feed for herald: a weekly language fact, plus one post per newly measured tokenizer."""
import datetime as dt
import json
import os
import sys

ROOT = os.path.join(os.path.dirname(__file__), "..")
REPO = "https://github.com/dadwritestech/token-tax"
CALC = "https://dadwritestech.github.io/token-tax/calculator.html"


def ratios(tok, langs):
    eng = tok["tokens"]["eng_Latn"]
    return {k: v / eng for k, v in tok["tokens"].items() if k != "eng_Latn" and k in langs}


def main(today=None):
    s = json.load(open(os.path.join(ROOT, "results", "summary.json"), encoding="utf-8"))
    langs = s["languages"]
    toks = {t["id"]: t for t in s["tokenizers"]}
    out = []

    # One fact a week: rotate through languages, show the spread across tokenizers.
    today = today or dt.date.today()
    year, week, _ = today.isocalendar()
    others = sorted(k for k in langs if k != "eng_Latn")
    lang = others[(year * 53 + week) % len(others)]
    per = sorted(((ratios(t, langs).get(lang), t["label"]) for t in toks.values()
                  if lang in t["tokens"]), key=lambda x: x[0])
    if per:
        name = langs[lang]["name"]
        (lo, lo_t), (hi, hi_t) = per[0], per[-1]
        out.append({
            "id": f"token-tax/weekly/{year}-W{week:02d}",
            "text": (f"{name} costs {hi:.2f}x the tokens of the same English text on {hi_t}, "
                     f"and {lo:.2f}x on {lo_t}.\n\nSame meaning, same price per token, "
                     f"different bill. Measured on FLORES-200."),
            "link": CALC,
        })

    # A new tokenizer in the data gets its own post (baseline marks existing ones as done).
    for t in toks.values():
        r = ratios(t, langs)
        if not r:
            continue
        worst = max(r, key=r.get)
        avg = sum(r.values()) / len(r)
        tel = r.get("tel_Telu")
        out.append({
            "id": f"token-tax/tokenizer/{t['id']}",
            "text": (f"New in token-tax: {t['label']} ({t.get('vendor', '')}). Across {len(r)} languages "
                     f"it averages {avg:.2f}x the English token count; worst is "
                     f"{langs[worst]['name']} at {r[worst]:.2f}x"
                     + (f", Telugu {tel:.2f}x." if tel else ".")),
            "link": REPO,
            "priority": 5,
        })
    for e in out:
        print(json.dumps(e, ensure_ascii=False))


if __name__ == "__main__":
    main()
