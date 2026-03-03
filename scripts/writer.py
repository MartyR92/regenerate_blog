import os
import json
import requests
from datetime import datetime
import sys
import re
import time

# Disable SSL warnings
import urllib3
requests.packages.urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_context_file(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def slugify(text):
    text = text.lower()
    # Handle German umlauts
    text = text.replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('ß', 'ss')
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    text = re.sub(r'^-+|-+$', '', text)
    return text

def call_gemini(url, payload):
    try:
        res = requests.post(url, json=payload, timeout=300)
        if res.status_code == 200:
            text = res.json()['candidates'][0]['content']['parts'][0]['text']
            # Strip triple backticks if present
            text = re.sub(r'^```markdown\n', '', text, flags=re.MULTILINE)
            text = re.sub(r'^```\n', '', text, flags=re.MULTILINE)
            text = re.sub(r'\n```$', '', text, flags=re.MULTILINE)
            return text.strip()
        else:
            print(f"Gemini API error: {res.status_code} - {res.text}")
            return None
    except Exception as e:
        print(f"Execution error: {e}")
        return None

def main():
    gemini_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not gemini_key:
        print("GEMINI_API_KEY missing")
        sys.exit(1)

    # 1. Load Context
    identity = get_context_file("context/system-identity.md")
    memory = get_context_file("context/blog-memory.json")
    series = get_context_file("context/series-registry.json")
    prompt_template = get_context_file("context/agent-prompts/writer-v1.md")
    
    # 2. Load Research Queue (Top Item)
    research_data = []
    if os.path.exists("context/research-queue.json"):
        with open("context/research-queue.json", "r", encoding="utf-8") as f:
            try:
                queue = json.load(f)
                # Filter out used items if field exists, otherwise take top
                unused = [x for x in queue if not x.get("used")]
                queue = unused if unused else queue
                queue.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)
                research_data = queue[:1]
            except:
                pass

    if not research_data:
        print("No research data found.")
        sys.exit(0)

    target_model = "models/gemini-2.5-flash"
    url = f"https://generativelanguage.googleapis.com/v1beta/{target_model}:generateContent?key={gemini_key}"

    # --- PASS 1: GERMAN GENERATION ---
    print("Generating German version (Pass 1)...")
    prompt_de = f"""
    {prompt_template}
    
    CONTEXT:
    IDENTITY: {identity}
    MEMORY: {memory}
    RESEARCH: {json.dumps(research_data, indent=2)}
    
    MODE: GENERATION
    LANGUAGE: DE
    """
    
    payload_de = {
        "contents": [{"parts": [{"text": prompt_de}]}],
        "generationConfig": {"temperature": 0.9, "maxOutputTokens": 8192}
    }
    
    content_de = call_gemini(url, payload_de)
    if not content_de:
        sys.exit(1)

    # --- PASS 2: ENGLISH TRANSLATION ---
    print("Generating English version (Pass 2)...")
    prompt_en = f"""
    {prompt_template}
    
    ORIGINAL ARTICLE (DE):
    {content_de}
    
    MODE: TRANSLATION
    LANGUAGE: EN
    INSTRUCTION: Create a semantic mirror of the DE article. Maintain all [VERIFY] and [DIAGRAM] tags.
    """
    
    payload_en = {
        "contents": [{"parts": [{"text": prompt_en}]}],
        "generationConfig": {"temperature": 0.4, "maxOutputTokens": 8192} # Lower temp for translation consistency
    }
    
    content_en = call_gemini(url, payload_en)
    if not content_en:
        sys.exit(1)

    # 3. Save Both Versions
    os.makedirs("_drafts", exist_ok=True)
    date_prefix = datetime.now().strftime("%Y-%m-%d")
    
    # Extract title from DE version for slug
    title_match = re.search(r'title:\s*"(.*)"', content_de)
    if not title_match:
        title_match = re.search(r'title:\s*(.*)', content_de)
    
    raw_title = title_match.group(1).strip() if title_match else "generated-post"
    slug = slugify(raw_title.replace('"', ''))
    
    # German File
    file_de = f"_drafts/{date_prefix}-{slug}.de.md"
    with open(file_de, "w", encoding="utf-8") as f:
        f.write(content_de)
    
    # English File
    file_en = f"_drafts/{date_prefix}-{slug}.en.md"
    with open(file_en, "w", encoding="utf-8") as f:
        f.write(content_en)

    print(f"Successfully generated bilingual pair:")
    print(f"  - DE: {file_de}")
    print(f"  - EN: {file_en}")

if __name__ == "__main__":
    main()
