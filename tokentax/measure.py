"""Tokenise the FLORES-200 devtest corpus for every language x tokenizer.

Output: results/counts.json  {meta, languages: {code: {words, chars, ...}}, counts: {tok: {lang: n}}}

Each language's 1012 sentences are joined with "\\n" and tokenised as one document
(no BOS/EOS/special tokens), which is how a paragraph actually reaches an API.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import pathlib
import sys

from . import metrics as m
from .registry import API_ONLY, LANGUAGES, TOKENIZERS

ROOT = pathlib.Path(__file__).resolve().parent.parent
FLORES = ROOT / "data" / "raw" / "flores200_dataset" / "devtest"
CACHE = ROOT / ".hfcache"


def load_corpus(code: str, raw: bool = False) -> str:
    lines = (FLORES / f"{code}.devtest").read_text(encoding="utf-8").splitlines()
    text = "\n".join(lines)
    return text if raw else m.clean(text)


def load_tokenizer(spec):
    if spec["kind"] == "tiktoken":
        import tiktoken
        enc = tiktoken.get_encoding(spec["name"])
        return lambda s: len(enc.encode(s, disallowed_special=()))
    from huggingface_hub import hf_hub_download
    from tokenizers import Tokenizer
    tok = Tokenizer.from_file(hf_hub_download(spec["name"], "tokenizer.json", cache_dir=str(CACHE)))
    return lambda s: len(tok.encode(s, add_special_tokens=False).ids)


def count_via_api(key: str, text: str) -> int:  # pragma: no cover - needs keys
    """Anthropic / Gemini count-tokens. Subtracts a one-character message so per-request
    overhead (role markers etc.) does not leak into the language comparison."""
    import urllib.request
    spec = API_ONLY[key]
    api_key = os.environ[spec["env"]]

    def call(body_text):
        if key == "anthropic-claude":
            body = {"model": os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5-5"),
                    "messages": [{"role": "user", "content": body_text}]}
            req = urllib.request.Request(spec["endpoint"], json.dumps(body).encode(), {
                "x-api-key": api_key, "anthropic-version": "2023-06-01", "content-type": "application/json"})
            return json.load(urllib.request.urlopen(req))["input_tokens"]
        model = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
        body = {"contents": [{"parts": [{"text": body_text}]}]}
        req = urllib.request.Request(spec["endpoint"].format(model=model), json.dumps(body).encode(), {
            "x-goog-api-key": api_key, "content-type": "application/json"})
        return json.load(urllib.request.urlopen(req))["totalTokens"]

    return call(text) - call(".") + 1


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*", help="tokenizer ids to (re)measure")
    ap.add_argument("--api", action="store_true", help="also measure API-only vendors whose key env var is set")
    ap.add_argument("--raw", action="store_true", help="skip quote cleaning (to measure the FLORES artifact)")
    ap.add_argument("--out", default=str(ROOT / "results" / "counts.json"))
    args = ap.parse_args(argv)

    out = pathlib.Path(args.out)
    data = json.loads(out.read_text(encoding="utf-8")) if out.exists() else {"counts": {}}
    corpora = {c: load_corpus(c, raw=args.raw) for c in LANGUAGES}
    data["languages"] = {c: {"name": n, "script": s, "spaced": sp,
                             "words": m.count_words(corpora[c]), "chars": m.count_chars(corpora[c])}
                         for c, (n, s, sp) in LANGUAGES.items()}
    data["meta"] = {"corpus": "FLORES-200 devtest (1012 sentences)", "cleaned": not args.raw,
                    "measured": dt.date.today().isoformat()}

    for tid in args.only or list(TOKENIZERS):
        spec = TOKENIZERS[tid]
        print(f"{tid:20s} {spec['name']}", file=sys.stderr, flush=True)
        n = load_tokenizer(spec)
        data["counts"][tid] = {c: n(t) for c, t in corpora.items()}
    if args.api:
        for key, spec in API_ONLY.items():
            if os.environ.get(spec["env"]):
                data["counts"][key] = {c: count_via_api(key, t) for c, t in corpora.items()}
            else:
                print(f"skip {key}: {spec['env']} not set (left empty, not estimated)", file=sys.stderr)

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"wrote {out}", file=sys.stderr)


if __name__ == "__main__":
    main()
