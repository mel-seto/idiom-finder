import pytest
from unittest.mock import MagicMock
import verification.verifier as verifier_module
from verification.wiktionary_client import WiktionaryClient

class FakeClient:
    def __init__(self, return_value: bool):
        self.return_value = return_value
        self.called_with = None

    def exists(self, idiom: str) -> bool:
        self.called_with = idiom
        return self.return_value
    
def test_returns_true_if_in_cc_cedict(monkeypatch):
    """Return True if CC-CEDICT has definitions."""
    mock_CC_DICT = MagicMock()
    mock_CC_DICT.get_definitions.return_value = ["dummy definition"]

    # Patch CC_DICT inside verifier module
    monkeypatch.setattr(verifier_module, "CC_DICT", mock_CC_DICT)

    result = verifier_module.verify_idiom_exists("山珍海味")
    assert result is True
    mock_CC_DICT.get_definitions.assert_called_once_with("山珍海味")


def test_returns_false_if_not_in_cc_cedict(monkeypatch):
    """Return False if CC-CEDICT has no definitions and no Wiktionary client."""
    mock_CC_DICT = MagicMock()
    mock_CC_DICT.get_definitions.return_value = []

    monkeypatch.setattr(verifier_module, "CC_DICT", mock_CC_DICT)

    result = verifier_module.verify_idiom_exists("不存在的成语")
    assert result is False
    mock_CC_DICT.get_definitions.assert_called_once_with("不存在的成语")


def test_returns_true_with_wiktionary_fallback(monkeypatch):
    """Return True if Wiktionary client finds the idiom."""
    mock_CC_DICT = MagicMock()
    mock_CC_DICT.get_definitions.return_value = []

    monkeypatch.setattr(verifier_module, "CC_DICT", mock_CC_DICT)
    wik_client = FakeClient(True)

    result = verifier_module.verify_idiom_exists("非数据集成语", wik_client)
    assert result is True
