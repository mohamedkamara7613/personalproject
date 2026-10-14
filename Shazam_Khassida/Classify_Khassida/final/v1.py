

import re
import unicodedata
import json
import os
from translit_map import TRANSLIT_MAP



def normalize(text):
    text = text.lower()
    
    # unicode → ascii
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode()
    
    for k, v in TRANSLIT_MAP.items():
        text = text.replace(k, v)
    
    # supprimer ponctuation
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    
    return text



def ngrams(tokens, n):
    return [" ".join(tokens[i:i+n]) for i in range(len(tokens)-n+1)]

def extract_features(text):
    tokens = text.split()
    
    return {
        "unigrams": set(tokens),
        "bigrams": set(ngrams(tokens, 2)),
        "trigrams": set(ngrams(tokens, 3)),
    }


def similarity(a, b):
    fa = extract_features(a)
    fb = extract_features(b)
    
    score = 0
    score += 3 * len(fa["trigrams"] & fb["trigrams"])
    score += 2 * len(fa["bigrams"] & fb["bigrams"])
    score += 1 * len(fa["unigrams"] & fb["unigrams"])
    
    return score

def adaptive_threshold(text):
    n = len(text.split())
    if n <= 3:
        return 2
    elif n <= 6:
        return 3
    else:
        return 4


def build_khassidas(titles, threshold=4):
    khassidas = []
    
    for title in titles:
        norm = normalize(title)
        matched = False

        threshold = adaptive_threshold(norm)
        
        for k in khassidas:
            if similarity(norm, k["canonical_norm"]) >= threshold:
                k["variants"].append(title)
                matched = True
                break
        
        if not matched:
            khassidas.append({
                "id": f"KH_{len(khassidas)+1:04d}",
                "canonical": title,
                "canonical_norm": norm,
                "variants": [title],
            })
    
    return khassidas





if __name__ == "__main__":
    final_list = []
    # Adjusted path to parent directory
    input_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "3-liste_khassida_processed.txt")
    
    if os.path.exists(input_file):
        with open(input_file, "r", encoding="utf-8") as f:
            for line in f:
                final_list.append(line.strip())

        khassidas = build_khassidas(final_list)

        print(f"{len(final_list)} titres → {len(khassidas)} khassidas réelles")

        with open("khassidas.json", "w", encoding="utf-8") as f:
            json.dump(khassidas, f, indent=4, ensure_ascii=False)
        print("Données exportées dans khassidas.json")

        for k in khassidas[:5]:
            print(k["id"], k["canonical"], "variants:", len(k["variants"]))
    else:
        print(f"Warning: {input_file} not found. Could not regenerate json.")

