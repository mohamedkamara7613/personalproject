import re
import unicodedata
import difflib

input_file = "1-liste_khassida_processed.txt"
output_file = "2-liste_khassida_processed.txt"

def remove_accents(input_str):
    # Normalize unicode characters to decompose combined characters (like 'é' to 'e' + '´')
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    # Filter out non-spacing mark characters
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

def normalize_text(text):
    # 1. Lowercase
    text = text.lower()
    
    # 2. Remove accents
    text = remove_accents(text)
    
    # 3. Remove parentheses and their content
    text = re.sub(r'\s*\([^)]*\)', '', text)
    
    # 4. Replace dashes and underscores with spaces
    text = re.sub(r'[-_]', ' ', text)
    
    # 5. Remove HTML artifacts if any remaining (sanity check)
    text = re.sub(r'<[^>]+>', '', text)
    
    # 6. Replace double letters with single letter (aa -> a, mm -> m)
    # This matches any character captured in group 1, followed by one or more of the same character
    text = re.sub(r'(.)\1+', r'\1', text)
    
    # 7. Collapse multiple spaces and trim
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def get_similarity(s1, s2):
    return difflib.SequenceMatcher(None, s1, s2).ratio()

def process():
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            raw_titles = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: {input_file} not found.")
        return

    # Store tuples of (original_title, normalized_key)
    # We want to preserve the original title for the final list if possible, 
    # OR the user wants "tout mettre ... en lower-case". 
    # The prompt says: "fait moi ... où il faudrait tout mettre ... en lower-case, remplacer les doubles lettres..."
    # This implies the OUTPUT titles should be the normalized versions.
    # "Choix du titre canonique... choisir automatiquement une version 'standard' : e.g., la plus longue"
    # Wait, if we transform everything to normalized form, they naturally collide.
    # BUT, fuzzy matching implies we group things that are SIMILAR but NOT IDENTICAL in normalized form.
    # E.g. "bouchera lana" vs "buchra lana". These normalize differently ("buchera lana" vs "buchra lana").
    # So we need to group based on the normalized version.
    
    # Let's create a list of objects {'original': t, 'normalized': normalize_text(t)}
    items = []
    for t in raw_titles:
        norm = normalize_text(t)
        if norm:
            items.append({'original': t, 'normalized': norm})
            
    # Deduplicate exact matches on normalized string first to reduce work
    # We keep the "longest" original title as representative for the exact normalized group?
    # Or strict adherence to "tout mettre en lower-case...".
    # User said: "Output: 2-liste... où il faudrait tout mettre ... en lower-case"
    # So the output text MUST be the normalized version.
    # But later "Choix du titre canonique... choisir automatiquement une version 'standard' : e.g., la plus longue"
    # Use the normalized version that is longest? Or the original version converted to normalized?
    # If "aa" -> "a", then "baakh" becomes "bakh". match "bakh" and "baakh". 
    # If the output must have single letters, then "bakh" is the target.
    # So, the canon is effectively the normalized string.
    # BUT, "Bouchera-Lana" (norm: bouchera lana) vs "Buchra lanâ" (norm: buchra lana).
    # These are fuzzy match, not exact.
    # We need to pick one normalized form to represent the group.
    
    # Strategy:
    # 1. Start with list of unique normalized strings.
    # 2. Group them by fuzzy similarity.
    # 3. For each group, pick a representative (e.g. longest, or most frequent if we tracked counts).
    
    unique_normalized = list(set(i['normalized'] for i in items))
    unique_normalized.sort() # sort for stability
    
    groups = [] # List of lists of strings
    
    processed = set()
    
    print(f"Clustering {len(unique_normalized)} unique normalized titles...")
    
    # Simple greedy clustering
    for i, title in enumerate(unique_normalized):
        if title in processed:
            continue
            
        current_group = [title]
        processed.add(title)
        
        for j in range(i + 1, len(unique_normalized)):
            other = unique_normalized[j]
            if other in processed:
                continue
            
            if get_similarity(title, other) > 0.9:
                current_group.append(other)
                processed.add(other)
        
        groups.append(current_group)

    canons = []
    for group in groups:
        # User: "choisir automatiquement une version 'standard' : e.g., la plus longue"
        # Since these are all normalized forms, they should be relatively similar.
        # Length is a decent heuristic for completeness, though sometimes shorter is cleaner.
        # Let's stick to "longest" as suggested.
        canon = max(group, key=len)
        canons.append(canon)
        
    canons.sort()
    
    print(f"Reduced to {len(canons)} canonical titles.")
    
    with open(output_file, 'w', encoding='utf-8') as out:
        for c in canons:
            out.write(c + "\n")
            
    print(f"Written to {output_file}")

if __name__ == "__main__":
    process()
