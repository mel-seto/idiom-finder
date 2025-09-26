from typing import Optional
from singletons import CC_DICT
from verification.wiktionary_client import WiktionaryClient


def verify_idiom_exists(idiom: str, wiktionary_client: Optional[WiktionaryClient] = None) -> bool:
    """Verify idiom exists via CC-CEDICT or optional Wiktionary client."""
    # Step 1: Local CC-CEDICT lookup
    if CC_DICT.get_definitions(idiom):
        return True

    # Step 2: Wiktionary fallback
    client = wiktionary_client or WiktionaryClient()
    return client.exists(idiom)