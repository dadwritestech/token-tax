# Good first issues (open these right after the repo goes public)

Label each `good first issue` plus the label in brackets. Bodies are ready to paste.

---

## 1. Measure Claude with the count-tokens API  [tokenizer, help wanted]

Anthropic does not publish Claude's tokenizer, so the Claude rows in the README are empty on purpose. If you have an Anthropic API key, you can fill them: token counting is free and the run is 96 small requests.

```bash
export ANTHROPIC_API_KEY=...  ANTHROPIC_MODEL=claude-sonnet-5-5
python -m tokentax.measure --only --api && python -m tokentax.report
```

Please say which model id you counted against. Different Claude generations may use different tokenizers, so one row per tokenizer generation is ideal. Details in CONTRIBUTING.md.

---

## 2. Measure Gemini with countTokens  [tokenizer, help wanted]

Same as #1 for Google Gemini (`GEMINI_API_KEY`, `GEMINI_MODEL`). Gemma 4 is measured locally, but whether Gemini's production tokenizer is identical has not been verified. A measured Gemini row settles it.

---

## 3. Add GPT-6.x and GLM-5.x tokenizers  [tokenizer]

OpenRouter lists newer releases (gpt-6.1-*, glm-5.1/5.2/5.3) than v0 measured. For GLM, add the Hugging Face repo to `TOKENIZERS` if `tokenizer.json` is public. For GPT-6.x, check whether tiktoken's model map has an encoding for it. If it does not, leave it unmeasured; do not guess. Add the priced models to `prices.yaml` with their source URL.

---

## 4. Code-mixed and romanised corpus (Hinglish, Tenglish)  [corpus]

FLORES is formal, native-script text. Real chat in India is often romanised or code-mixed ("meeting ki late avtundi"). Proposal: a small, openly licensed parallel set (even 100 sentences) of English / native script / romanised / code-mixed. Then measure all tokenizers on it as a second table. Step one is finding or writing a corpus with a clear license; please discuss the source in the issue before collecting data.

---

## 5. Output-cost view in the calculator  [site]

The calculator prices input tokens. Output tokens cost 4–8× more per token, and answers in Telugu or Hindi carry the same premium. Add an "output" toggle to `site/calculator.html` using `usd_out_per_m_en_words`, which `results/summary.json` already contains. No new data needed.
