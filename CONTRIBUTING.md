# Contributing to token-tax

Thanks for helping. The most useful contributions are **measured numbers**, not estimates. Every number in this repo comes from running a real tokenizer (or a vendor's official count-tokens API) on the same FLORES-200 text. Please keep it that way.

## Setup

```bash
git clone https://github.com/dadwritestech/token-tax && cd token-tax
pip install -r requirements.txt
pytest -q
```

Measuring needs the FLORES-200 corpus (not redistributed here):

```bash
mkdir -p data/raw && curl -L -o data/raw/flores200.tar.gz https://dl.fbaipublicfiles.com/nllb/flores200_dataset.tar.gz && tar -xzf data/raw/flores200.tar.gz -C data/raw
```

## Measure Claude or Gemini (needs your API key)

Anthropic and Google do not publish their tokenizers, so these rows are empty until someone with a key runs the official count-tokens endpoints. Counting tokens is free on both APIs; the run makes 96 small requests (48 languages × 2).

```bash
export ANTHROPIC_API_KEY=...        # and/or GEMINI_API_KEY=...
export ANTHROPIC_MODEL=claude-sonnet-5-5   # optional; GEMINI_MODEL defaults to gemini-2.5-flash
python -m tokentax.measure --only --api
python -m tokentax.report
```

`--only` with no ids skips the local tokenizers and keeps their committed counts. In the PR, say which model id you counted against and the date. **Never commit your key**; it is read from the environment only.

## Add a tokenizer

1. Add an entry to `TOKENIZERS` in [`tokentax/registry.py`](tokentax/registry.py):
   - `kind: "tiktoken"` with the encoding name, or `kind: "hf"` with a Hugging Face repo that has a `tokenizer.json`.
   - The source must be public and ungated. If the official repo is gated, use an ungated mirror with a byte-identical `tokenizer.json` and record the original in `mirror_of`.
2. `python -m tokentax.measure --only <id>` then `python -m tokentax.report`.
3. If a priced model uses it, point that model's `tokenizer:` field in `prices.yaml` at the new id.
4. Commit `tokentax/registry.py`, `results/`, `site/data.js` and, if the charts changed, the PNGs from `scripts/screenshot.py`.

Tokenizers that turn out byte-identical to an existing one are merged into one row automatically (for example Phi-4 = cl100k).

## Update a price

Edit [`prices.yaml`](prices.yaml): change `input` / `output` (USD per 1M tokens, standard tier), keep `source` pointing at the page you read, and bump `checked:` to today. Then `python -m tokentax.report` and commit. The git history is the dated price record, so one PR per price check is ideal.

## Add a language

Add the FLORES-200 code to `LANGUAGES` in `tokentax/registry.py`, then re-measure all tokenizers (`python -m tokentax.measure`). This downloads about 1 GB of tokenizer files on the first run.

## Checks before a PR

- `pytest -q` passes.
- `python -m tokentax.report` leaves no diff after your commit (CI checks this).
- No keys, tokens or `.env` files in the diff.

## Licensing of contributions

Code contributions are licensed Apache-2.0; data contributions (counts, prices) CC BY 4.0, matching [LICENSE](LICENSE) and [DATA_LICENSE](DATA_LICENSE).
