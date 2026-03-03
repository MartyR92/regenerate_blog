import os
import sys
import glob
import requests
import json
import re
from datetime import datetime
import urllib3
import time
import yaml

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_drafts():
    # Process all files in _drafts
    return glob.glob("_drafts/*.md")

def parse_research_data():
    path = "context/research-queue.json"
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return []

def call_gemini_with_retry(url, payload, max_retries=3):
    for i in range(max_retries):
        try:
            res = requests.post(url, json=payload, timeout=120)
            if res.status_code == 200:
                return res
            elif res.status_code == 429:
                print(f"Quota exceeded. Retrying in 60s... (Attempt {i+1}/{max_retries})")
                time.sleep(60)
            else:
                print(f"API Error: {res.status_code} - {res.text}")
                break
        except requests.exceptions.Timeout:
            print(f"Timeout occurred. Retrying... (Attempt {i+1}/{max_retries})")
            time.sleep(10)
    return None

def process_file(target_file, gemini_key, research_data):
    print(f"Processing visuals for: {target_file}")
    
    with open(target_file, "r", encoding="utf-8") as f:
        full_text = f.read()

    # Detect Language and extract Front Matter
    # Be more robust with whitespace and potential code block wrappers (which shouldn't be there anymore)
    fm_match = re.search(r'^---\s*\n(.*?)\n---\s*\n', full_text, re.DOTALL | re.MULTILINE)
    lang = "de" # Default
    if fm_match:
        try:
            fm = yaml.safe_load(fm_match.group(1))
            if "language" in fm:
                lang = fm["language"]
        except:
            pass
    
    # Second pass if FM match failed or language still de and file has .en.md
    if ".en.md" in target_file:
        lang = "en"
    elif ".de.md" in target_file:
        lang = "de"

    top_research = research_data[0]
    metrics = top_research.get("summary", "")
    
    # Construction of SVG & Caption Prompt
    prompt = f"""
    Based on the following data, generate a clean, modern SVG code for a technical diagram and a matching caption in {lang.upper()}.
    
    DATA: {metrics}
    
    AESTHETIC: 'Organic Precision' (Micro Arm).
    PALETTE: Primary #0F1A15, Secondary #C5B388, Accent #2C3330.
    TYPOGRAPHY: JetBrains Mono for data labels.
    
    REQUIREMENTS:
    1. Return a JSON object with two fields: 'svg' and 'caption'.
    2. 'svg': The raw <svg>...</svg> code (width 800).
    3. 'caption': A professional, reader-facing description of the visual data in {lang.upper()}.
    4. NO mentions of 'AI', 'agents', or 'image-agent'.
    5. Ensure high-contrast and precision.
    """

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_key}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.2,
            "response_mime_type": "application/json"
        }
    }

    print(f"Calling Gemini 2.5 Flash for localized SVG generation ({lang})...")
    res = call_gemini_with_retry(url, payload)
    
    if not res:
        print(f"Failed to get response for {target_file}")
        return
        
    try:
        res_json = res.json()
        data = json.loads(res_json['candidates'][0]['content']['parts'][0]['text'])
        svg_text = data.get('svg', "").strip()
        caption = data.get('caption', "").strip()
        
        if not svg_text.startswith("<svg"):
            print("Invalid SVG output structure.")
            return

        # 4. Save SVG to STATIC directory
        # Standardize slug: strip lang suffix if present for the folder name
        base_name = os.path.basename(target_file).replace('.md', '')
        slug = re.sub(r'\.(de|en)$', '', base_name)
        year = datetime.now().strftime("%Y")
        img_dir = f"static/images/{year}/{slug}"
        os.makedirs(img_dir, exist_ok=True)
        img_filename = f"technical_diagram_1_{lang}.svg"
        img_path = f"{img_dir}/{img_filename}"
        
        with open(img_path, "w", encoding="utf-8") as f:
            f.write(svg_text)
            
        print(f"Saved SVG diagram to: {img_path}")

        # 5. Update Markdown with localized caption
        markdown_ref = f"\n\n![{caption}](/images/{year}/{slug}/{img_filename})\n*{caption}*\n"
        
        if f"/images/{year}/{slug}/{img_filename}" in full_text:
            print("Diagram already referenced. Skipping.")
        else:
            if "##" in full_text:
                parts = full_text.split("##", 2)
                if len(parts) > 2:
                    new_content = parts[0] + "##" + parts[1] + markdown_ref + "##" + parts[2]
                else:
                    new_content = full_text + markdown_ref
            else:
                new_content = full_text + markdown_ref

            with open(target_file, "w", encoding="utf-8") as f:
                f.write(new_content)
            
            print("Successfully integrated visuals.")

    except Exception as e:
        print(f"Processing failed for {target_file}: {e}")

def main():
    gemini_key = os.environ.get("GEMINI_API_KEY")
    if not gemini_key:
        print("Missing GEMINI_API_KEY")
        sys.exit(1)

    targets = get_drafts()
    if not targets:
        print("No drafts found in _drafts/")
        sys.exit(0)

    research_data = parse_research_data()
    if not research_data:
        print("No research data found.")
        sys.exit(0)

    for target in targets:
        process_file(target, gemini_key, research_data)
        # Small sleep to avoid quota issues between files
        time.sleep(2)

if __name__ == "__main__":
    main()
