# X thread (attach docs/social.png to tweet 1 and docs/calculator.png to tweet 5)

1/
The same paragraph costs $1.00 in English and $8.29 in Telugu on Llama 3.

I measured the "token tax" for 21 tokenizers × 48 languages on identical text, and priced it. 🧵

2/
Why: LLM APIs bill per token, and a tokenizer splits the same meaning into far more tokens in some languages. The price per token is the same, so the bill is bigger and the usable context window is smaller.

3/
Llama 3 kept GPT-4's (cl100k) weakness for Telugu and Tamil almost to the decimal. Meta fixed Hindi (4.78× → 2.53×) but not the Dravidian languages. Llama 4 finally did: Telugu 2.83×.

4/
Most even tokenizer: Gemma, 1.69× on average, no language worse than 3.4×.
GPT-5.x: Telugu 1.93×, Amharic 5.81×.
Sarvam-1 (Indic-first): Telugu 1.15×, but Burmese 14.2×. Specialising moves the tax around.

5/
Paste your own text: the calculator runs the real tokenizers in your browser, and nothing is uploaded.
https://dadwritestech.github.io/token-tax/calculator.html

6/
Claude and Gemini are blank on purpose. Their tokenizers are API-only, and I didn't estimate. If you have a key, the count-tokens run is free and PRs are welcome.

Code Apache-2.0, data CC BY 4.0:
https://github.com/dadwritestech/token-tax
