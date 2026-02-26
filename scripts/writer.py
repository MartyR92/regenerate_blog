import os
import json
import requests
from datetime import datetime
import sys
import re

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
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    text = re.sub(r'^-+|-+$', '', text)
    return text

def main():
    gemini_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not gemini_key:
        print("GEMINI_API_KEY missing")
        sys.exit(1)

    # 1. Load Context
    identity = get_context_file("context/system-identity.md")
    memory = get_context_file("context/blog-memory.json")
    series = get_context_file("context/series-registry.json")
    
    # 2. Load Research Queue (Top 3 relevant)
    research_data = []
    if os.path.exists("context/research-queue.json"):
        with open("context/research-queue.json", "r", encoding="utf-8") as f:
            try:
                queue = json.load(f)
                # Sort by relevance score descending
                queue.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)
                research_data = queue[:3]
            except:
                pass

    # 3. Dynamic Model Discovery
    print("Discovering available Pro models...")
    target_model = "models/gemini-1.5-pro" # Default
    try:
        diag = requests.get(f"https://generativelanguage.googleapis.com/v1beta/models?key={gemini_key}")
        if diag.status_code == 200:
            model_list = [m['name'] for m in diag.json().get('models', [])]
            pro_models = [m for m in model_list if "pro" in m and "1.5" in m]
            if pro_models:
                target_model = pro_models[0]
                print(f"Using discovered Pro model: {target_model}")
            else:
                print(f"No specific 1.5 Pro found, using first available: {model_list[0]}")
                target_model = model_list[0]
    except Exception as e:
        print(f"Discovery failed, falling back to default: {e}")

    # 4. Construct Prompt
    prompt = f"""
    SYSTEM IDENTITY:
    {identity}

    BLOG MEMORY (Established Theses):
    {memory}

    SERIES REGISTRY:
    {series}

    RESEARCH INPUT (Top Items):
    {json.dumps(research_data, indent=2)}

    TASK:
    Write a 1.500 - 3.000 word deep-dive blog post based on the research input. 
    Follow the 'Natural Solarpunk x Avantgarde Prestige' style guide.
    Use [VERIFY] tags for any factual claims not backed by the research input.
    Provide the output in Markdown format with Hugo Front Matter.
    The Front Matter MUST include:
    - title
    - date (current: {datetime.now().isoformat()})
    - draft: true
    - ai_assisted: true
    - ai_model: {target_model}
    - author: "Martin Reiter"
    - categories and tags from the ontology.
    """

    # 5. Call Gemini REST API
    url = f"https://generativelanguage.googleapis.com/v1beta/{target_model}:generateContent?key={gemini_key}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 8192 # Sufficient for long-form content
        }
    }
    
    try:
        res = requests.post(url, json=payload, timeout=120)
        if res.status_code == 200:
            content = res.json()['candidates'][0]['content']['parts'][0]['text']
            
            # 6. Save to _drafts
            title_match = re.search(r'^title:\s*"(.*)"', content, re.MULTILINE)
            title = title_match.group(1) if title_match else "generated-post"
            date_str = datetime.now().strftime("%Y-%m-%d")
            filename = f"_drafts/{date_str}-{slugify(title)}.md"
            
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
            
            print(f"Successfully generated post: {filename}")
        else:
            print(f"Gemini API error: {res.status_code} - {res.text}")
            sys.exit(1)
    except Exception as e:
        print(f"Execution error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
