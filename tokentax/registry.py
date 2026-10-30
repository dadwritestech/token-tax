"""Languages and tokenizers measured. Tokenizers are loaded only from public, ungated
sources (tiktoken BPE files or Hugging Face tokenizer.json). Where the official repo is
gated, an ungated mirror with the identical tokenizer.json is used and named here."""

LANGUAGES = {
    # code: (name, script, spaced)  spaced=False -> no whitespace between words
    "eng_Latn": ("English", "Latin", True),
    "tel_Telu": ("Telugu", "Telugu", True),
    "hin_Deva": ("Hindi", "Devanagari", True),
    "tam_Taml": ("Tamil", "Tamil", True),
    "ben_Beng": ("Bengali", "Bengali", True),
    "urd_Arab": ("Urdu", "Arabic", True),
    "mar_Deva": ("Marathi", "Devanagari", True),
    "guj_Gujr": ("Gujarati", "Gujarati", True),
    "kan_Knda": ("Kannada", "Kannada", True),
    "mal_Mlym": ("Malayalam", "Malayalam", True),
    "pan_Guru": ("Punjabi", "Gurmukhi", True),
    "ory_Orya": ("Odia", "Odia", True),
    "sin_Sinh": ("Sinhala", "Sinhala", True),
    "npi_Deva": ("Nepali", "Devanagari", True),
    "amh_Ethi": ("Amharic", "Ge'ez", True),
    "tir_Ethi": ("Tigrinya", "Ge'ez", True),
    "swh_Latn": ("Swahili", "Latin", True),
    "yor_Latn": ("Yoruba", "Latin", True),
    "hau_Latn": ("Hausa", "Latin", True),
    "zul_Latn": ("Zulu", "Latin", True),
    "ibo_Latn": ("Igbo", "Latin", True),
    "som_Latn": ("Somali", "Latin", True),
    "arb_Arab": ("Arabic", "Arabic", True),
    "pes_Arab": ("Persian", "Arabic", True),
    "heb_Hebr": ("Hebrew", "Hebrew", True),
    "tha_Thai": ("Thai", "Thai", False),
    "mya_Mymr": ("Burmese", "Myanmar", False),
    "khm_Khmr": ("Khmer", "Khmer", False),
    "lao_Laoo": ("Lao", "Lao", False),
    "vie_Latn": ("Vietnamese", "Latin", True),
    "ind_Latn": ("Indonesian", "Latin", True),
    "tgl_Latn": ("Tagalog", "Latin", True),
    "zho_Hans": ("Chinese (Simplified)", "Han", False),
    "jpn_Jpan": ("Japanese", "Kana/Kanji", False),
    "kor_Hang": ("Korean", "Hangul", True),
    "deu_Latn": ("German", "Latin", True),
    "fra_Latn": ("French", "Latin", True),
    "spa_Latn": ("Spanish", "Latin", True),
    "por_Latn": ("Portuguese", "Latin", True),
    "ita_Latn": ("Italian", "Latin", True),
    "nld_Latn": ("Dutch", "Latin", True),
    "pol_Latn": ("Polish", "Latin", True),
    "rus_Cyrl": ("Russian", "Cyrillic", True),
    "ukr_Cyrl": ("Ukrainian", "Cyrillic", True),
    "tur_Latn": ("Turkish", "Latin", True),
    "ell_Grek": ("Greek", "Greek", True),
    "kat_Geor": ("Georgian", "Georgian", True),
    "hye_Armn": ("Armenian", "Armenian", True),
}

# id -> spec. kind: "tiktoken" (name = encoding) or "hf" (name = HF repo with tokenizer.json).
# browser: what the in-page calculator loads ("tiktoken:<enc>" via js-tiktoken,
# "hf:<repo>" via transformers.js), or None if too heavy for a browser.
TOKENIZERS = {
    "openai-o200k": {"label": "OpenAI o200k (GPT-4o … GPT-5.x)", "vendor": "OpenAI", "kind": "tiktoken", "name": "o200k_base"},
    "openai-cl100k": {"label": "OpenAI cl100k (GPT-4, GPT-3.5)", "vendor": "OpenAI", "kind": "tiktoken", "name": "cl100k_base"},
    "llama-3": {"label": "Llama 3.x", "vendor": "Meta", "kind": "hf", "name": "unsloth/Meta-Llama-3.1-8B", "mirror_of": "meta-llama/Llama-3.1-8B"},
    "llama-4": {"label": "Llama 4", "vendor": "Meta", "kind": "hf", "name": "unsloth/Llama-4-Scout-17B-16E-Instruct", "mirror_of": "meta-llama/Llama-4-Scout-17B-16E-Instruct"},
    "qwen-3": {"label": "Qwen 3", "vendor": "Alibaba", "kind": "hf", "name": "Qwen/Qwen3-8B"},
    "qwen-3.5": {"label": "Qwen 3.5", "vendor": "Alibaba", "kind": "hf", "name": "Qwen/Qwen3.5-9B"},
    "gemma-3": {"label": "Gemma 3", "vendor": "Google", "kind": "hf", "name": "unsloth/gemma-3-1b-it", "mirror_of": "google/gemma-3-1b-it"},
    "gemma-4": {"label": "Gemma 4", "vendor": "Google", "kind": "hf", "name": "google/gemma-4-12B-it"},
    "deepseek-v3": {"label": "DeepSeek V3", "vendor": "DeepSeek", "kind": "hf", "name": "deepseek-ai/DeepSeek-V3"},
    "deepseek-v4": {"label": "DeepSeek V4", "vendor": "DeepSeek", "kind": "hf", "name": "deepseek-ai/DeepSeek-V4-Pro"},
    "mistral-7b": {"label": "Mistral 7B (2023 SentencePiece)", "vendor": "Mistral", "kind": "hf", "name": "mistralai/Mistral-7B-v0.1"},
    "mistral-tekken": {"label": "Mistral Tekken (Nemo)", "vendor": "Mistral", "kind": "hf", "name": "mistralai/Mistral-Nemo-Instruct-2407"},
    "mistral-large-3": {"label": "Mistral Large 3", "vendor": "Mistral", "kind": "hf", "name": "mistralai/Mistral-Large-3-675B-Instruct-2512"},
    "mistral-medium-3.5": {"label": "Mistral Medium 3.5", "vendor": "Mistral", "kind": "hf", "name": "mistralai/Mistral-Medium-3.5-128B"},
    "glm-5": {"label": "GLM-5", "vendor": "Z.ai", "kind": "hf", "name": "zai-org/GLM-5"},
    "phi-4": {"label": "Phi-4", "vendor": "Microsoft", "kind": "hf", "name": "microsoft/phi-4"},
    "granite-3.3": {"label": "Granite 3.3", "vendor": "IBM", "kind": "hf", "name": "ibm-granite/granite-3.3-8b-instruct"},
    "falcon-3": {"label": "Falcon 3", "vendor": "TII", "kind": "hf", "name": "tiiuae/Falcon3-7B-Base"},
    "olmo-2": {"label": "OLMo 2", "vendor": "Ai2", "kind": "hf", "name": "allenai/OLMo-2-1124-7B"},
    "bloom": {"label": "BLOOM (2022, multilingual)", "vendor": "BigScience", "kind": "hf", "name": "bigscience/bloom"},
    "sarvam-1": {"label": "Sarvam-1 (Indic-first)", "vendor": "Sarvam AI", "kind": "hf", "name": "sarvamai/sarvam-1"},
}
for _spec in TOKENIZERS.values():
    _spec.setdefault("browser", f"{_spec['kind']}:{_spec['name']}")

# Vendors whose tokenizers are only reachable through an authenticated count-tokens API.
# Deliberately NOT estimated. Fill these with `python -m tokentax.measure --api`.
API_ONLY = {
    "anthropic-claude": {"label": "Anthropic Claude", "vendor": "Anthropic", "env": "ANTHROPIC_API_KEY",
                         "endpoint": "https://api.anthropic.com/v1/messages/count_tokens"},
    "google-gemini": {"label": "Google Gemini", "vendor": "Google", "env": "GEMINI_API_KEY",
                      "endpoint": "https://generativelanguage.googleapis.com/v1beta/models/{model}:countTokens"},
}
