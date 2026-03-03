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
import subprocess
import tempfile
try:
    import cairosvg
    CAIRO_AVAILABLE = True
except Exception:
    CAIRO_AVAILABLE = False
    print("Warning: cairosvg or cairo native library not found. WebP fallback will be skipped.")

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_all_articles():
    # Process all files in content/de/posts and content/en/posts
    return glob.glob("content/de/posts/*.md") + glob.glob("content/en/posts/*.md")

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
            elif res.status_code >= 500:
                print(f"Server Error ({res.status_code}). Retrying in 10s...")
                time.sleep(10)
            else:
                print(f"Critical API Error: {res.status_code} - {res.text}")
                return None
        except requests.exceptions.Timeout:
            print(f"Timeout occurred. Retrying... (Attempt {i+1}/{max_retries})")
            time.sleep(10)
    return None

def get_best_model(api_key):
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
        res = requests.get(url, timeout=10)
        if res.status_code == 200:
            models = [m['name'] for m in res.json().get('models', [])]
            # Preference order
            for target in ["gemini-2.5-flash", "gemini-1.5-flash"]:
                for m in models:
                    if target in m:
                        return m
            if models: return models[0]
    except:
        pass
    return "models/gemini-2.5-flash" # Fallback

def generate_procedural_svg(visual_type, title, lang):
    # A clean, Organic Precision styled placeholder
    color_primary = "#0F1A15"
    color_secondary = "#C5B388"
    color_accent = "#2C3330"
    
    svg = f"""<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
    <rect width="800" height="400" fill="{color_primary}"/>
    <path d="M 50 350 L 750 350" stroke="{color_accent}" stroke-width="2"/>
    <path d="M 50 50 L 50 350" stroke="{color_accent}" stroke-width="2"/>
    <text x="400" y="200" font-family="JetBrains Mono, monospace" font-size="24" fill="{color_secondary}" text-anchor="middle">
        {visual_type}
    </text>
    <text x="400" y="240" font-family="JetBrains Mono, monospace" font-size="16" fill="{color_accent}" text-anchor="middle">
        {title}
    </text>
    <circle cx="100" cy="300" r="5" fill="{color_secondary}"/>
    <circle cx="200" cy="250" r="5" fill="{color_secondary}"/>
    <circle cx="300" cy="280" r="5" fill="{color_secondary}"/>
    <circle cx="400" cy="150" r="5" fill="{color_secondary}"/>
    <path d="M 100 300 L 200 250 L 300 280 L 400 150" fill="none" stroke="{color_secondary}" stroke-width="2" stroke-dasharray="5,5"/>
</svg>"""
    caption = f"Visual representation: {visual_type} regarding {title}"
    if lang == "de":
        caption = f"Visuelle Darstellung: {visual_type} zu {title}"
    return svg, caption

def process_file(target_file, gemini_key, research_data):
    print(f"Processing visuals for: {target_file}")
    
    # Dynamic model discovery
    model_name = get_best_model(gemini_key)
    print(f"Using model: {model_name}")
    
    with open(target_file, "r", encoding="utf-8") as f:
        full_text = f.read()

    # Detect Language
    fm_match = re.search(r'^---\s*\n(.*?)\n---\s*\n', full_text, re.DOTALL | re.MULTILINE)
    lang = "de" 
    if fm_match:
        try:
            fm = yaml.safe_load(fm_match.group(1))
            if "language" in fm:
                lang = fm["language"]
        except:
            pass
    
    if ".en.md" in target_file:
        lang = "en"
    elif ".de.md" in target_file:
        lang = "de"

    top_research = research_data[0] if research_data else {"summary": "Regenerative economy and ecology."}
    metrics = top_research.get("summary", "")
    
    # 1. Define Visual Types and Filenames
    visual_tasks = [
        {"type": "Technical Chart", "id": 2, "focus": "Data focus, e.g., trends, comparisons, metrics."},
        {"type": "Technical Diagram", "id": 3, "focus": "System focus, e.g., flows, structures, conceptual architecture."}
    ]

    # Standardize slug
    base_name = os.path.basename(target_file).replace('.md', '')
    slug = re.sub(r'\.(de|en)$', '', base_name)
    year = datetime.now().strftime("%Y")
    img_dir = f"static/images/{year}/{slug}"
    os.makedirs(img_dir, exist_ok=True)

    updated_content = full_text

    for task in visual_tasks:
        img_filename = f"technical_visual_{task['id']}_{lang}.svg"
        img_path = f"{img_dir}/{img_filename}"
        
        # Skip if already exists
        if f"/blog/images/{year}/{slug}/{img_filename}" in updated_content:
            print(f"Visual {task['id']} already referenced in {target_file}. Skipping.")
            continue

        print(f"Generating {task['type']} for {target_file}...")
        
        # Construction of Prompt
        prompt = f"""
        Based on the following data, generate a clean, modern SVG code for a {task['type']} and a matching caption in {lang.upper()}.
        
        DATA: {metrics}
        FOCUS: {task['focus']}
        
        AESTHETIC: 'Organic Precision' (Micro Arm).
        PALETTE: Primary #0F1A15, Secondary #C5B388, Accent #2C3330.
        TYPOGRAPHY: JetBrains Mono for data labels.
        
        REQUIREMENTS:
        1. Return a JSON object with two fields: 'svg' and 'caption'.
        2. 'svg': The raw <svg>...</svg> code.
           - Use embedded CSS inside the SVG for responsiveness.
           - Use 'currentColor' or '@media (prefers-color-scheme: dark)' for dark/light mode compatibility.
           - Use '@media (max-width: 600px)' for mobile text resizing.
           - Enforce a maximum width constraint (e.g., max-width: 800px).
           - Ensure a scalable 'viewBox' attribute is present.
        3. 'caption': A professional, reader-facing description of the visual data in {lang.upper()}.
        4. NO mentions of 'AI', 'agents', or 'image-agent'.
        5. Ensure high-contrast and precision.
        """

        url = f"https://generativelanguage.googleapis.com/v1beta/{model_name}:generateContent?key={gemini_key}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.2,
                "response_mime_type": "application/json"
            }
        }

        res = call_gemini_with_retry(url, payload)
        
        svg_text = ""
        caption = ""
        
        if res:
            try:
                res_json = res.json()
                data = json.loads(res_json['candidates'][0]['content']['parts'][0]['text'])
                svg_text = data.get('svg', "").strip()
                caption = data.get('caption', "").strip()
            except:
                print("Failed to parse Gemini response for visual. Using procedural fallback.")
                svg_text, caption = generate_procedural_svg(task['type'], base_name, lang)
        else:
            print(f"Gemini API unavailable for {task['type']}. Using procedural fallback.")
            svg_text, caption = generate_procedural_svg(task['type'], base_name, lang)
            
        if not svg_text.startswith("<svg"):
            print("Invalid SVG output structure.")
            continue

        with open(img_path, "w", encoding="utf-8") as f:
            f.write(svg_text)
            
        # Synchronous WebP Fallback (Optional)
        if CAIRO_AVAILABLE:
            try:
                webp_filename = img_filename.replace(".svg", ".webp")
                webp_path = f"{img_dir}/{webp_filename}"
                with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_png:
                    temp_png_path = tmp_png.name
                cairosvg.svg2png(bytestring=svg_text.encode('utf-8'), write_to=temp_png_path)
                try:
                    subprocess.run(['cwebp', '-q', '80', temp_png_path, '-o', webp_path], check=True, capture_output=True)
                    print(f"Saved WebP fallback to: {webp_path}")
                except FileNotFoundError:
                    print("Warning: cwebp not found. Skipping WebP conversion.")
                except Exception as e:
                    print(f"Warning: WebP conversion failed: {e}")
                if os.path.exists(temp_png_path): os.remove(temp_png_path)
            except Exception as e:
                print(f"Warning: SVG to PNG conversion failed: {e}")
        else:
            print("Skipping WebP fallback (Cairo missing).")

        # Smart Placement Logic
        markdown_ref = f"\n\n![{caption}](/blog/images/{year}/{slug}/{img_filename})\n*{caption}*\n"
        
        sections = updated_content.split("\n## ")
        if len(sections) > task['id']:
            # Place after the Nth H2 section
            sections[task['id']] = sections[task['id']] + markdown_ref
            updated_content = "\n## ".join(sections)
        else:
            updated_content += markdown_ref

        print(f"Successfully integrated {task['type']} ({task['id']}).")
        time.sleep(5)

    with open(target_file, "w", encoding="utf-8") as f:
        f.write(updated_content)

def main():
    gemini_key = os.environ.get("GEMINI_API_KEY")
    if not gemini_key:
        print("Missing GEMINI_API_KEY")
        sys.exit(1)

    targets = get_all_articles()
    if not targets:
        print("No articles found.")
        sys.exit(0)

    research_data = parse_research_data()
    
    print(f"Found {len(targets)} articles to process.")
    for target in targets:
        process_file(target, gemini_key, research_data)
        time.sleep(2)

if __name__ == "__main__":
    main()
