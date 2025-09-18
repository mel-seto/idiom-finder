#!/usr/bin/env python3
"""
add_chid_definitions.py

Full workflow:
1. Load ChiD dataset (chid_idiom_reference.json)
2. Augment with English definitions using pycccedict
3. Save augmented dataset (chid_augmented.json)
4. Filter out entries missing definitions → chid_valid.json
5. Save report of missing definitions → chid_missing.json
"""

import json
import os

from pycccedict.cccedict import CcCedict

# --- CONFIG ---
DIRECTORY = "./idiom_dataset"
INPUT_FILE = f"{DIRECTORY}/chid_idiom_reference.json"  # input ChiD dataset
AUGMENTED_FILE = f"{DIRECTORY}/chid_augmented.json"  # augmented dataset
VALID_FILE = f"{DIRECTORY}/chid_valid.json"  # filtered dataset for RAG
MISSING_FILE = f"{DIRECTORY}/chid_missing.json"  # report of missing definitions


def main():
    # Check input file exists
    if not os.path.exists(INPUT_FILE):
        raise FileNotFoundError(f"Input file '{INPUT_FILE}' not found.")

    # Load ChiD dataset
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        chid_data = json.load(f)

    # Initialize pycccedict
    cc_dict = CcCedict()

    # --- Step 1: Augment ChiD with English definitions ---
    for entry in chid_data:
        idiom = entry["idiom"]
        definitions = cc_dict.get_definitions(idiom)
        entry["meaning"] = definitions if definitions else None

    # Save augmented dataset
    with open(AUGMENTED_FILE, "w", encoding="utf-8") as f:
        json.dump(chid_data, f, ensure_ascii=False, indent=2)

    # --- Step 2: Filter valid idioms ---
    valid_idioms = [entry for entry in chid_data if entry.get("meaning")]

    with open(VALID_FILE, "w", encoding="utf-8") as f:
        json.dump(valid_idioms, f, ensure_ascii=False, indent=2)

    # --- Step 3: Save report of missing definitions ---
    missing_idioms = [entry for entry in chid_data if not entry.get("meaning")]

    with open(MISSING_FILE, "w", encoding="utf-8") as f:
        json.dump(missing_idioms, f, ensure_ascii=False, indent=2)

    # --- Summary ---
    print(f"Total idioms loaded: {len(chid_data)}")
    print(f"Augmented dataset saved: {AUGMENTED_FILE}")
    print(f"Valid idioms saved: {len(valid_idioms)} → {VALID_FILE}")
    print(f"Missing definitions: {len(missing_idioms)} → {MISSING_FILE}")


if __name__ == "__main__":
    main()
