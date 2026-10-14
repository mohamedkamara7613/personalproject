# -*- coding: utf-8 -*-
import os
import re
import unicodedata
import shutil
from translit_map import TRANSLIT_MAP
from v1 import normalize, similarity

# ======================================================
# CONFIG
# ======================================================

AUDIO_ROOT = "audios"
UNCLASSIFIED_DIR = "_UNCLASSIFIED"
AMBIGUOUS_DIR = "_AMBIGUOUS"

MATCH_THRESHOLD = 4        # seuil minimal de confiance
AMBIGUOUS_MARGIN = 1       # écart max entre 1er et 2e score


# ======================================================
# MATCHING & DECISION
# ======================================================

def match_audio(audio_title, khassidas):
    norm = normalize(audio_title)

    scores = []
    for k in khassidas:
        score = similarity(norm, k["canonical_norm"])
        scores.append((k, score))

    scores.sort(key=lambda x: x[1], reverse=True)

    best, best_score = scores[0]
    second_score = scores[1][1] if len(scores) > 1 else 0

    return best, best_score, second_score

def decide_folder(audio_title, khassidas):
    best, best_score, second_score = match_audio(audio_title, khassidas)

    if best_score < MATCH_THRESHOLD:
        return UNCLASSIFIED_DIR, best_score

    if second_score >= best_score - AMBIGUOUS_MARGIN:
        return AMBIGUOUS_DIR, best_score

    folder = best["canonical_norm"].replace(" ", "_")[:80]
    return folder, best_score

# ======================================================
# FILE SYSTEM ACTION
# ======================================================

def organize_audio(audio_path, folder_name):
    dest_dir = os.path.join(AUDIO_ROOT, folder_name)
    os.makedirs(dest_dir, exist_ok=True)

    dest_path = os.path.join(dest_dir, os.path.basename(audio_path))
    shutil.move(audio_path, dest_path)

# ======================================================
# EXAMPLE USAGE
# ======================================================

import json

if __name__ == "__main__":
    # Load khassidas from JSON
    json_path = os.path.join(os.path.dirname(__file__), "khassidas.json")
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            khassidas = json.load(f)
        print(f"✅ Loaded {len(khassidas)} khassidas from {json_path}")
    except FileNotFoundError:
        print(f"❌ Error: {json_path} not found.")
        exit(1)

    # Example titles to verify classification logic
    test_titles = [
        "Tawbatun Nasuh Al Jalibatu Lil An Wari Wal Futuh",
        "Subhana Rabina In Kana Wahdu Rabina Lamafhulan",
        "Adjabani Khayrouba",
        "Adjabani Rabousama",
        "Tawbat Nasuh Jalibatu Nur", # Imperfect match
        "Unknown Title Test" # Should contain low score
    ]

    print("\n--- Verifying Classification Logic ---")
    for audio_title in test_titles:
        folder, score = decide_folder(audio_title, khassidas)
        print(f"Audio: '{audio_title}'")
        print(f"  -> Folder: {folder}")
        print(f"  -> Score: {score}")
        
    print("\n✅ Verification complete. 'decide_folder' and 'match_audio' are working.")
    # organize_audio(audio_path, folder_name) is ready to be used on real files.
