import pytest
from utils.utils import get_pinyin

@pytest.mark.parametrize("text, expected", [
    ("举棋不定", "jǔ qí bù dìng"),
    ("风", "fēng"),
    ("不怕慢，就怕站", "bù pà màn ， jiù pà zhàn"),
])
def test_get_pinyin_accent(text, expected):
    assert get_pinyin(text) == expected
