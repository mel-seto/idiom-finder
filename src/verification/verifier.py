from typing import Optional
from singletons import CC_DICT, CHID_SET
from verification.wiktionary_client import WiktionaryClient


def verify_idiom_exists(idiom: str, wiktionary_client: Optional[WiktionaryClient] = None) -> bool:
    """Verify idiom exists via CHID Datatset, CC-CEDICT, or optional Wiktionary client."""
    if idiom in CHID_SET:
        return True
    
    if CC_DICT.get_definitions(idiom):
        return True

    client = wiktionary_client or WiktionaryClient()
    return client.exists(idiom)