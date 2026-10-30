# LinkedIn post

The same paragraph costs $1.00 in English and $8.29 in Telugu.

That isn't a separate price list. LLM APIs charge per token, and tokenizers split Indian languages into far more tokens than English for the same meaning.

I measured 21 tokenizers across 48 languages on the same 1,012 translated sentences (FLORES-200), then priced them per model:

→ Llama 3: Telugu costs 8.29×, Tamil 7.65× and Hindi 2.53× the English price
→ GPT-5.x: Telugu 1.93×, Hindi 1.57×
→ Gemma: the most even; no language is above 3.4×
→ Sarvam-1 (built for Indic languages): Telugu 1.15×, close to parity

It shrinks the context window too. A 131k-token Llama 3.3 holds about 106k words of English, but only about 13k words' worth of Telugu.

If you're building AI products for India, the tokenizer is a cost line. Test your real traffic before you pick a model.

Open data, the method, and an in-browser calculator (your text never leaves the page):
https://github.com/dadwritestech/token-tax

#AI #LLM #India #Multilingual #Telugu #Hindi
