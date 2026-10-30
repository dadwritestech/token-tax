# Hacker News

**Title** (no superlatives, per HN guidelines):

    Show HN: Token-tax – what the same text costs in 48 languages on 21 tokenizers

**URL:** https://github.com/dadwritestech/token-tax

**First comment** (post right after submitting):

> LLM APIs charge per token, but a tokenizer turns the same meaning into very different token counts depending on the language. I measured 21 public tokenizers on FLORES-200, where the same 1,012 sentences exist in every language, and priced the result with a dated price sheet (sources and check dates are in prices.yaml). The headline: content that costs $1.00 in English costs $8.29 in Telugu on Llama 3, $1.93 on GPT-5.x, and $1.75 on Gemma. Llama 3 kept GPT-4's cl100k weakness for Telugu and Tamil almost to the decimal; Meta fixed Hindi in that release but not the Dravidian languages. A specialist Indic tokenizer (Sarvam-1) gets Telugu to 1.15× but charges 14.2× for Burmese. The context window shrinks by the same factor: GLM-5's 204,800 tokens hold about 165k words of English but only about 20k English-equivalent words of Telugu.
>
> No model inference anywhere, only tokenizers, so everything reproduces on a laptop. There's an in-browser calculator for your own text (js-tiktoken plus transformers.js; the text stays local). Caveats: FLORES is formal translated text, so chat and romanised Hinglish/Tenglish will differ. Claude and Gemini are blank because their tokenizers are only reachable through their APIs, and I didn't want to estimate them. If you have a key, the count-tokens run is free and PRs are welcome. This builds on Petrov et al. (NeurIPS 2023), updated with dollar figures and 2026 models. Code is Apache-2.0; numbers and charts are CC BY 4.0.
