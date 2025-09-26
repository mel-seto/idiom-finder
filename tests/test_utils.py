import pytest
from utils import utils


@pytest.mark.parametrize(
    "text, expected",
    [
        ("举棋不定", "jǔ qí bù dìng"),
        ("风", "fēng"),
        ("不怕慢，就怕站", "bù pà màn ， jiù pà zhàn"),
    ],
)
def test_get_pinyin_accent(text, expected):
    assert utils.get_pinyin(text) == expected
