import pytest
from unittest.mock import MagicMock
import singletons
from verification.verifier import verify_idiom_exists, WiktionaryClient


class FakeWiktionaryClient:
    def __init__(self, return_value: bool):
        self.return_value = return_value
        self.called_with = None

    def exists(self, idiom: str) -> bool:
        self.called_with = idiom
        return self.return_value
    

def test_returns_true_if_in_chid():
    # Pick an idiom guaranteed to be in CHID_SET
    idiom = next(iter(singletons.CHID_SET))
    fake_client = FakeWiktionaryClient(False)  # should not be called
    result = verify_idiom_exists(idiom, wiktionary_client=fake_client)
    assert result is True
    assert fake_client.called_with is None  # Wiktionary not used

def test_returns_true_if_in_cc_dict(monkeypatch):
    idiom = "临危不乱"  # example idiom not in CHID_SET
    monkeypatch.setattr("singletons.CC_DICT.get_definitions", lambda x: ["fake def"])
    fake_client = FakeWiktionaryClient(False)  # should not be called
    result = verify_idiom_exists(idiom, wiktionary_client=fake_client)
    assert result is True
    assert fake_client.called_with is None  # Wiktionary not used

def test_returns_true_if_only_in_wiktionary():
    idiom = "不存在的成语"
    fake_client = FakeWiktionaryClient(True)
    result = verify_idiom_exists(idiom, wiktionary_client=fake_client)
    assert result is True
    assert fake_client.called_with == idiom

def test_returns_false_if_nowhere():
    idiom = "完全不存在的成语"
    fake_client = FakeWiktionaryClient(False)
    result = verify_idiom_exists(idiom, wiktionary_client=fake_client)
    assert result is False
    assert fake_client.called_with == idiom
