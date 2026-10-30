import math
import pytest
from tokentax import metrics as m


def test_clean_collapses_csv_doubled_quotes():
    assert m.clean('""""""hello"""" he said') == '"hello" he said'
    assert m.clean('"plain" text') == '"plain" text'


def test_count_words_and_chars():
    s = "the cat  sat\non mats"
    assert m.count_words(s) == 5
    assert m.count_chars(s) == 15  # whitespace excluded
    assert m.count_chars("తెలుగు") == 6  # code points, NFC


def test_premium_is_ratio_to_english():
    assert m.premium(300, 100) == 3.0
    assert m.premium(100, 100) == 1.0
    with pytest.raises(ValueError):
        m.premium(10, 0)


def test_tokens_per_word_and_char():
    assert m.per_unit(150, 100) == 1.5
    assert m.per_unit(10, 0) is None


def test_cost_per_million_english_words():
    # English: 1.3 tokens/word at $2/Mtok -> 1M words = 1.3M tokens = $2.60
    assert m.cost_per_m_en_words(tokens=1300, en_words=1000, usd_per_mtok=2.0) == pytest.approx(2.60)
    # Same content in a language that needs 3x the tokens costs 3x
    assert m.cost_per_m_en_words(3900, 1000, 2.0) == pytest.approx(7.80)


def test_cost_scales_linearly_with_premium():
    en = m.cost_per_m_en_words(1000, 800, 1.25)
    xx = m.cost_per_m_en_words(4200, 800, 1.25)
    assert xx / en == pytest.approx(m.premium(4200, 1000))


def test_context_window_in_words():
    # 200k window, English 1000 words -> 1300 tokens => ~153,846 English words fit
    assert m.context_words(200_000, tokens=1300, words=1000) == pytest.approx(153_846.15, rel=1e-6)
    # a 4x language fits 1/4 of the content
    en = m.context_words(128_000, 1000, 750)
    xx = m.context_words(128_000, 4000, 750)
    assert en / xx == pytest.approx(4.0)


def test_geomean_and_summary():
    assert m.geomean([1, 4]) == pytest.approx(2.0)
    assert m.geomean([2, 2, 2]) == pytest.approx(2.0)
    with pytest.raises(ValueError):
        m.geomean([])


def test_paragraph_cost_headline():
    # English paragraph normalised to $1.00; language at premium 7.2 -> $7.20
    assert m.paragraph_cost(7.2, base=1.0) == pytest.approx(7.2)
    assert math.isclose(m.paragraph_cost(1.0), 1.0)
