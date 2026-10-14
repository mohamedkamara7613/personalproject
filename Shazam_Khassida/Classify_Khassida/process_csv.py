import csv
import re

input_file = "liste_khassida.csv"
output_file = "liste_khassida_processed.txt"

def clean_title(text):
    # Split by comma to take the first column (CSV behavior)
    # But since the file is mixed (some real CSV, some just lines), manual split might be better 
    # or just use csv module which handles quotes.
    # actually, some lines are just "Title" (no comma). 
    # If we use string split on first comma, it usually works for "Title,Traduction".
    # For lines without comma, it takes the whole line.
    
    parts = text.split(',', 1)
    title = parts[0].strip()
    
    # Remove HTML artifacts like <= /p> or similar
    # Found in inspection: "Alquraan<= /p>", "Haama Saxidnaa bikaram < /p>"
    title = re.sub(r'<=?\s*/\s*p>', '', title)
    title = re.sub(r'<\s*/\s*p>', '', title)
    
    # Remove content in parentheses, e.g. (Traduction), (arabe), (Wolof)
    # The user wants "seulement les titres".
    title = re.sub(r'\s*\(.*?\)', '', title)
    
    # Remove special characters or noise if any
    # normalize whitespace
    title = re.sub(r'\s+', ' ', title).strip()
    
    return title

def process():
    titles = set()
    cleaned_titles = []
    
    encoding = 'utf-8'
    
    with open(input_file, 'r', encoding=encoding, errors='replace') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            # Skip header lines
            if line.startswith("Titre") or "Translittération" in line or "Source principale" in line:
                continue
                
            # Basic CSV parsing logic: if line has comma, take first part.
            # Use csv module for reliable parsing of quotes?
            # The file seems to have simple structure mostly.
            # Let's try simple split first to avoid issues with appended plain text lines.
            
            # If the line is quoted like "Title, Part 2", csv reader handles it.
            # If I just split by comma, I might break "Title with comma".
            # Does the file contain titles with commas?
            # Looking at file snippet: none obvious.
            # Let's use csv.reader for the line to be safe.
            pass
            
            
    # Re-reading with csv module for proper handling
    final_list = []
    
    with open(input_file, 'r', encoding=encoding, errors='replace') as f:
        # We allow somewhat loose CSV parsing because of the appended text lines
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            
            first_col = row[0].strip()
            
            # filtering headers
            if first_col.startswith("Titre") and ("Translittération" in first_col or "variations" in first_col):
                continue
            
            cleaned = clean_title(first_col)
            
            # Filter distinctively invalid or empty titles
            if not cleaned or cleaned == "." or cleaned == "-":
                continue
            
            if cleaned not in titles:
                titles.add(cleaned)
                final_list.append(cleaned)
    
    final_list.sort()
    
    with open(output_file, 'w', encoding='utf-8') as out:
        for t in final_list:
            out.write(t + "\n")
            
    print(f"Processed {len(final_list)} unique titles to {output_file}")

if __name__ == "__main__":
    process()
