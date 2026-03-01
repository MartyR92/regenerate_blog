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
                queue.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)
                research_data = queue[:3]
            except:
                pass

    # 3. Dynamic Model Discovery (Prioritizing 2.5)
    print("Discovering available models (Prioritizing Gemini 2.5)...")
    target_model = "models/gemini-2.5-flash" # Default based on last successful run
    try:
        diag = requests.get(f"https://generativelanguage.googleapis.com/v1beta/models?key={gemini_key}")
        if diag.status_code == 200:
            model_list = [m['name'] for m in diag.json().get('models', [])]
            # Try to find exactly 2.5 models
            gemini_25_models = [m for m in model_list if "2.5" in m]
            if gemini_25_models:
                target_model = gemini_25_models[0]
                print(f"Using discovered Gemini 2.5 model: {target_model}")
            else:
                print(f"No Gemini 2.5 found, available: {model_list[:3]}")
                # Fallback to the first one in the list if no 2.5 found
                target_model = model_list[0]
    except Exception as e:
        print(f"Discovery failed, falling back to default: {e}")

    # 4. Construct Prompt
    prompt = f"""
    SYSTEM IDENTITY:
    {identity}

    BLOG MEMORY (Previously published titles and concepts):
    {memory}

    SERIES REGISTRY:
    {series}

    RESEARCH INPUT (Top Items):
    {json.dumps(research_data, indent=2)}

    TASK:
    Write a 1.500 - 3.000 word deep-dive blog post based on the research input. 
    Follow the 'Natural Solarpunk x Avantgarde Prestige' style guide.
    
    IMPORTANT: 
    - Ensure the TITLE and CONTENT are unique compared to the BLOG MEMORY.
    - DO NOT use overused keywords like 'Algorithmic', 'Symbiosis', or 'Precision' in the title unless strictly necessary for the technical context.
    - Prefer evocative, biological, or architectural metaphors.
    
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
            "temperature": 0.9,
            "maxOutputTokens": 8192,
            "topP": 0.95
        }
    }
    
    try:
        res = requests.post(url, json=payload, timeout=180) # Increased timeout for Gemini 2.5
        if res.status_code == 200:
            content = res.json()['candidates'][0]['content']['parts'][0]['text']
            
            # 6. Save to _drafts
            # Try to extract title from Front Matter
            title_match = re.search(r'title:\s*"(.*)"', content)
            if not title_match:
                title_match = re.search(r'title:\s*(.*)', content)
                
            title = title_match.group(1).strip() if title_match else "generated-post"
            title = title.replace('"', '')
            
            date_str = datetime.now().strftime("%Y-%m-%d")
            filename = f"_drafts/{date_str}-{slugify(title)}.md"
            
            # Ensure _drafts exists
            os.makedirs("_drafts", exist_ok=True)
            
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
            
            print(f"Successfully generated post using {target_model}: {filename}")
        else:
            print(f"Gemini API error: {res.status_code} - {res.text}")
            sys.exit(1)
    except Exception as e:
        print(f"Execution error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
