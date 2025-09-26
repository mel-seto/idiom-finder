from pycccedict.cccedict import CcCedict
import json
from pathlib import Path

CC_DICT = CcCedict()

# source: https://github.com/chujiezheng/ChID-Dataset
CHID_FILE = Path(__file__).parent.parent / "data/chid_idiom_reference.json"
with open(CHID_FILE, "r", encoding="utf-8") as f:
    chid_data = json.load(f) 
CHID_SET = set(chid_data)  # O(1) lookup