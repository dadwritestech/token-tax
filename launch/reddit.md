# Reddit posts

Reddit was not reachable from the build machine, so **the rule notes below come from memory and were not freshly read.** Before posting, open each sub's rules page and use the flair it requires. Post in the account's own voice, space the four posts out (not all within one hour), and reply to comments.

---

## r/MachineLearning

Rules to verify: titles need a tag ([P] for projects), self-promotion is allowed only for substantive work, and low-effort or beginner posts are removed. Make it a self-post with the link inside.

**Title:** [P] token-tax: per-language token premium for 21 tokenizers × 48 languages on FLORES-200, converted to $ and effective context

**Body:**

Petrov et al. (NeurIPS 2023) showed that tokenizers treat languages unequally. I wanted the same measurement for the tokenizers people actually pay for in 2026, expressed in dollars.

Setup: FLORES-200 devtest (1,012 parallel sentences), 48 languages, 21 public tokenizers (tiktoken o200k/cl100k, Llama 3/4, Gemma 3/4, Qwen 3/3.5, DeepSeek V3/V4, Mistral ×4, GLM-5, Phi-4, Granite 3.3, Falcon 3, OLMo 2, BLOOM, Sarvam-1). Premium = tokens(lang) / tokens(same English content). Byte-identical tokenizers are collapsed into one row (Phi-4 and OLMo 2 = cl100k). Prices come per model from a dated sheet. Costs are reported per 1M *English-equivalent* words, which avoids word segmentation for Thai, Burmese and Chinese.

Findings:
- Gemma 3/4 has the lowest geomean premium (1.69×), and its worst language is Odia at 3.4×. Every other tokenizer's worst language is at 5× or more.
- Llama 3 matches cl100k to two decimals on Telugu, Tamil, Amharic and Burmese. The vocabulary extension helped only Hindi (4.78× → 2.53×).
- Sarvam-1 (Indic-first) is about 1.15× on Indic languages but 14.2× on Burmese and 3.65× on Chinese. Specialisation moves the tax rather than removing it.
- Chinese is *cheaper* than English (0.91–0.95×) on Qwen 3.5, BLOOM, GLM-5 and DeepSeek.

Limits: formal translated text only (no code-mixed or romanised data); the headline is input-side; tokens are not quality. Claude and Gemini are left empty because they need API counting; PRs welcome.

Code (Apache-2.0) and data (CC BY 4.0): https://github.com/dadwritestech/token-tax

---

## r/LocalLLaMA

Rules to verify: limits on self-promotion (most of the account's activity should not be self-promo), and posts must be about local or open models. Flair: "Resources" or "Discussion".

**Title:** Measured the "language tax" of open-weight tokenizers: Telugu costs 8.3× English on Llama 3, 2.8× on Llama 4, 1.75× on Gemma

**Body:**

If you run models locally in a language other than English, the tokenizer decides how much of your context window you actually get. I measured 21 tokenizers on the same 1,012 FLORES-200 sentences in 48 languages.

How many English-equivalent words fit in the context window:
- Llama 3.3 70B, 131k ctx: ~106k words of English, ~13k of Telugu
- Qwen3-235B, 262k ctx: ~208k English, ~30k Telugu
- Gemma 4 31B, 262k ctx: ~204k English, ~117k Telugu

Gemma has the most even tokenizer of everything I measured (its worst language is Odia, at 3.4×). Llama 3's tokenizer is cl100k plus extra tokens, and for Telugu and Tamil those extra tokens did nothing. Llama 4 fixed most of it.

There's an in-browser calculator that runs the real tokenizer files (transformers.js), so you can paste your own prompts: https://dadwritestech.github.io/token-tax/calculator.html

Repo with all the numbers: https://github.com/dadwritestech/token-tax

---

## r/india

Rules to verify: the required post flair (probably "Science/Technology"), limits on self-promotion, and whether links to your own GitHub are allowed in a normal post. Keep the post focused on the finding, not on selling anything.

**Title:** AI models charge Indian languages more for the same sentence. Telugu costs up to 8× English on some models. I measured 21 of them.

**Body:**

AI APIs bill by "tokens", which are small pieces of text. The catch is that the same sentence in Telugu, Tamil or Hindi gets split into many more tokens than it does in English. So Indian-language users and startups pay more for the same content, and less of it fits in the model's memory.

I measured this on a standard set of 1,012 sentences translated into 48 languages:
- On Llama 3, Telugu costs 8.29× English, Tamil 7.65×, Hindi 2.53×.
- On GPT-5.x (the tokenizer behind current ChatGPT models), Telugu is 1.93× and Hindi 1.57×.
- Google's Gemma is the fairest: Telugu 1.75×, Hindi 1.30×.
- Sarvam AI's Indian tokenizer brings Telugu down to 1.15×, almost equal to English.

Llama 3 improved Hindi, but the South Indian languages were left behind until Llama 4.

You can paste your own text into the calculator. It runs in your browser and nothing is uploaded: https://dadwritestech.github.io/token-tax/calculator.html

Open-source data: https://github.com/dadwritestech/token-tax

---

## r/developersIndia

Rules to verify: project posts may be limited to a showcase flair (such as "I Made This") or a weekly thread, and there may be minimum-karma rules. If a showcase thread exists, post there.

**Title:** I built an open dataset + calculator showing how much more Indian languages cost on LLM APIs (Telugu 8.3× on Llama 3, 1.9× on GPT-5.x)

**Body:**

If you're building anything for Indian users on top of an LLM API, your token bill depends on the language, not just the model. I measured 21 tokenizers on the same 1,012 sentences in 48 languages (FLORES-200) and priced them.

Input cost per 1M English-equivalent words:
- gpt-5-mini: English $0.31, Hindi $0.48, Telugu $0.59, Tamil $0.61
- llama-3.3-70b: English $0.12, Hindi $0.31, Tamil $0.95, Telugu $1.03
- gemma-4-31b: English $0.26, Hindi $0.33, Tamil $0.37, Telugu $0.45

Practical takeaways:
- If your users write in Dravidian languages, avoid Llama 3-era tokenizers and GLM-5.
- Measure your real traffic. The calculator runs the tokenizers in your browser.
- Hinglish and Tenglish in Roman script behave differently from native script. I haven't measured them yet; it's an open issue if anyone wants to help.

Repo (Python, Apache-2.0): https://github.com/dadwritestech/token-tax
Calculator: https://dadwritestech.github.io/token-tax/calculator.html
