import pytest
from tokentax import report

LANGS = {
    "eng_Latn": {"name": "English", "words": 1000, "chars": 5000, "spaced": True},
    "tel_Telu": {"name": "Telugu", "words": 800, "chars": 5200, "spaced": True},
    "zho_Hans": {"name": "Chinese", "words": 90, "chars": 1600, "spaced": False},
}
COUNTS = {
    "openai-o200k": {"eng_Latn": 1300, "tel_Telu": 2600, "zho_Hans": 1560},
    "phi-4": {"eng_Latn": 1300, "tel_Telu": 2600, "zho_Hans": 1560},  # identical vector
    "llama-3": {"eng_Latn": 1250, "tel_Telu": 10000, "zho_Hans": 1500},
}
PRICES = {"checked": "2026-10-30", "models": [
    {"id": "m1", "tokenizer": "openai-o200k", "input": 2.0, "output": 8.0, "context": 200_000},
    {"id": "claude", "tokenizer": "anthropic-claude", "input": None, "output": None, "context": None},
]}


def summary():
    return report.build_summary({"meta": {}, "languages": LANGS, "counts": COUNTS}, PRICES)


def test_identical_tokenizers_collapse():
    s = summary()
    ids = [r["id"] for r in s["tokenizers"]]
    assert ids == ["openai-o200k", "llama-3"]  # sorted by geomean premium, phi-4 folded in
    assert s["tokenizers"][0]["same_as"] == ["phi-4"]


def test_premium_worst_and_geomean():
    r = summary()["tokenizers"][0]
    assert r["premium"]["tel_Telu"] == pytest.approx(2.0)
    assert r["worst"] == {"lang": "tel_Telu", "premium": pytest.approx(2.0)}
    assert r["geomean_premium"] == pytest.approx((2.0 * 1.2) ** 0.5)
    assert r["tokens_per_word"]["tel_Telu"] == pytest.approx(2600 / 800)
    assert r["tokens_per_char"]["zho_Hans"] == pytest.approx(1560 / 1600)


def test_model_costs_and_context():
    m1 = summary()["models"][0]
    # 1.3 tok per English word * $2/Mtok
    assert m1["usd_in_per_m_en_words"]["eng_Latn"] == pytest.approx(2.6)
    assert m1["usd_in_per_m_en_words"]["tel_Telu"] == pytest.approx(5.2)
    assert m1["usd_out_per_m_en_words"]["tel_Telu"] == pytest.approx(20.8)
    assert m1["context_en_words"]["tel_Telu"] == pytest.approx(200_000 * 1000 / 2600)
    # native words only for spaced scripts
    assert "zho_Hans" not in m1["context_native_words"]
    assert m1["context_native_words"]["tel_Telu"] == pytest.approx(200_000 * 800 / 2600)


def test_api_only_slots_are_not_estimated():
    s = summary()
    claude = s["models"][1]
    assert claude["measured"] is False
    assert "usd_in_per_m_en_words" not in claude
    assert set(s["pending"]) == {"anthropic-claude", "google-gemini"}
