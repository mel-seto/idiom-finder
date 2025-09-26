import pytest
from verification.wiktionary_client import WiktionaryClient

@pytest.fixture
def wiktionary_client():
    """Return a real Wiktionary client for integration tests."""
    return WiktionaryClient()
