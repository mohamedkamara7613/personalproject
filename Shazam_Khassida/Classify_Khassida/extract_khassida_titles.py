import email
from bs4 import BeautifulSoup
import sys

input_file = "Les khassaïdes en PDF.html"
output_file = "extracted_titles.txt"

import re
import quopri

def extract_titles(input_file, existing_titles):
    print(f"Reading {input_file} manually...")
    try:
        with open(input_file, 'rb') as fp:
            content = fp.read()
    except FileNotFoundError:
        print(f"File {input_file} not found.")
        return set()

    # Find the start of the HTML part
    # We look for Content-Type: text/html
    match = re.search(rb'Content-Type:\s*text/html', content)
    if not match:
        print("Could not find Content-Type: text/html")
        return set()

    start_idx = match.start()
    
    # Find the blank line after start_idx
    header_end_match = re.search(rb'\r?\n\r?\n', content[start_idx:])
    if not header_end_match:
        print("Could not find end of headers for HTML part.")
        return set()

    body_start_idx = start_idx + header_end_match.end()
    
    next_boundary = re.search(rb'\r?\n-{6,}MultipartBoundary', content[body_start_idx:])
    
    if next_boundary:
        html_payload = content[body_start_idx : body_start_idx + next_boundary.start()]
    else:
        # End of file
        html_payload = content[body_start_idx:]
        
    print(f"Extracted {len(html_payload)} bytes of payload. Decoding...")
    
    try:
        html_content = quopri.decodestring(html_payload)
    except Exception as e:
        print(f"Error decoding quoted-printable: {e}")
        return set()

    print("Parsing HTML...")
    soup = BeautifulSoup(html_content, 'html.parser')
    
    paragraphs = soup.find_all('p', class_=True)
    
    new_titles = set()
    found_count = 0
    
    # Heuristic keywords that must be present in the class string
    required_keywords = ["font-semibold", "text-lg", "line-clamp-1"]
    
    for p in paragraphs:
        classes = p.get('class')
        if not classes:
            continue
            
        # Join classes into a single string for fuzzy matching
        # Handle potential garbage from bad QP decoding (e.g. 3D"font-semibold)
        class_str = " ".join(classes)
        
        # Check if all required keywords are present (lenient matching)
        if all(keyword in class_str for keyword in required_keywords):
            text = p.get_text(separator=" ", strip=True)
            # Collapse multiple spaces including non-breaking spaces and newlines
            text = re.sub(r'\s+', ' ', text).strip()
            
            # Additional sanity check: title shouldn't be too long or empty
            if text and len(text) < 200:
                if text not in existing_titles and text not in new_titles:
                    new_titles.add(text)
                    found_count += 1
                    # DEBUG: Print found title
                    # print(f"Found new title: {text}")

    print(f"Found {found_count} new unique titles in {input_file}")
    return new_titles


if __name__ == "__main__":
    output_filename = "extracted_titles.txt"
    files_to_process = [
        "Les khassaïdes en PDF copy.html"
    ]
    
    # Load existing titles if file exists
    existing_titles = set()
    try:
        with open(output_filename, 'r', encoding='utf-8') as f:
            for line in f:
                existing_titles.add(line.strip())
        print(f"Loaded {len(existing_titles)} existing titles.")
    except FileNotFoundError:
        print("No existing extracted_titles.txt found.")

    all_new_titles = set()
    for fname in files_to_process:
        new_titles = extract_titles(fname, existing_titles)
        all_new_titles.update(new_titles)
        # Add to existing for next iteration/file check
        existing_titles.update(new_titles)
        
    if all_new_titles:
        print(f"Writing {len(all_new_titles)} new titles to {output_filename} (appending)...")
        with open(output_filename, 'a', encoding='utf-8') as out:
            for title in sorted(all_new_titles): # Sort just for nicer append order
                out.write(title + "\n")
    else:
        print("No new titles found to append.")
