import requests
from pypinyin import Style, pinyin

from singletons import CC_DICT

def get_pinyin(text: str):
    """Convert Chinese characters to pinyin with tones."""
    py_list = pinyin(text, style=Style.TONE, heteronym=False)
    return " ".join([syllable[0] for syllable in py_list])


def verify_idiom_exists(idiom: str) -> bool:
    """Verify idiom first via CC-CEDICT, then Wiktionary API."""
    # Step 1: Local CC-CEDICT lookup
    if CC_DICT.get_definitions(idiom):
        return True

    # Step 2: Wiktionary fallback
    try:
        url = "https://zh.wiktionary.org/w/api.php"
        params = {"action": "query", "titles": idiom, "format": "json"}
        response = requests.get(url, params=params, timeout=3)
        data = response.json()
        pages = data.get("query", {}).get("pages", {})
        return not ("-1" in pages)
    except Exception:
        # Network or API failure — assume unknown
        return False
    