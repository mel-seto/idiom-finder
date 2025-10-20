import requests


_WIKTIONARY_CACHE = {}

class WiktionaryClient:
    """Simple wrapper for Wiktionary API queries."""
    BASE_URL = "https://en.wiktionary.org/w/api.php"
    HEADERS = {"User-Agent": "MyChineseIdiomApp/1.0 (email@example.com)"}

    def exists(self, term: str) -> bool:
        import requests

        if term in _WIKTIONARY_CACHE:
            return _WIKTIONARY_CACHE[term]

        try:
            params = {"action": "query", "titles": term, "format": "json"}
            response = requests.get(self.BASE_URL, params=params, headers=self.HEADERS, timeout=5)
            response.raise_for_status()
            data = response.json()
            print(f'data: {data}')
            pages = data.get("query", {}).get("pages", {})
            exists = "-1" not in pages
        except Exception:
            exists = False

        _WIKTIONARY_CACHE[term] = exists
        return exists
