import pytest
from verification.verifier import verify_idiom_exists
from singletons import CC_DICT


@pytest.mark.integration
def test_real_idiom_in_cc_cedict():
    """Verify a known idiom exists in CC-CEDICT."""
    idiom = "山珍海味"  # pick a real idiom in your CC_DICT
    assert verify_idiom_exists(idiom) is True

@pytest.mark.integration
def test_fake_idiom_not_in_cc_cedict():
    """Verify a non-existent idiom returns False."""
    idiom = "不存在的成语"
    assert verify_idiom_exists(idiom) is False

@pytest.mark.integration
def test_real_idiom_wiktionary(wiktionary_client):
    """Verify that a known idiom exists on Wiktionary."""
    idiom = "成语"
    assert verify_idiom_exists(idiom, wiktionary_client=wiktionary_client) is True

@pytest.mark.integration
def test_fake_idiom_wiktionary(wiktionary_client):
    """Verify that a made-up idiom does not exist on Wiktionary."""
    idiom = "不存在的成语"
    assert verify_idiom_exists(idiom, wiktionary_client=wiktionary_client) is False
