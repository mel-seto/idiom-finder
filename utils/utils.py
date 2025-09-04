from pypinyin import pinyin, Style

def get_pinyin(text: str):
    """Convert Chinese characters to pinyin with tones."""
    py_list = pinyin(text, style=Style.TONE, heteronym=False)
    return " ".join([syllable[0] for syllable in py_list])
