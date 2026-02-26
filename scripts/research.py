import os
import json
import random
import requests
import urllib.parse
from datetime import datetime
import sys

# Disable SSL warnings
import urllib3
requests.packages.urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def main():
    try:
        with open("context/ontology.json", "r", encoding="utf-8") as f:
            ontology = json.load(f)
    except Exception as e:
        print(f"Error loading ontology: {e}")
        sys.exit(1)

    # Pick a random domain/tag for research
    domain = random.choice(list(ontology.get("domains", {}).keys()))
    tags = ontology["domains"][domain].get("tags", [])
    tag = random.choice(tags) if tags else domain
    query = f"{domain} {tag} latest developments in regenerative economy"

    # 1. Search Web (Serper)
    serper_results = []
    serper_key = os.environ.get("SERPER_API_KEY", "").strip()
    if serper_key:
        try:
            res = requests.post(
                "https://google.serper.dev/search", 
                headers={"X-API-KEY": serper_key, "Content-Type": "application/json"},
                json={"q": query, "num": 5}
            )
            if res.status_code == 200:
                serper_results = res.json().get("organic", [])
        except Exception as e:
            print(f"Serper API exception: {e}")

    # 2. Search Academic (OpenAlex)
    openalex_results = []
    try:
        url = f"https://api.openalex.org/works?search={urllib.parse.quote(query)}&per-page=5&sort=publication_date:desc"
        res = requests.get(url)
        if res.status_code == 200:
            openalex_results = res.json().get("results", [])
    except Exception as e:
        print(f"OpenAlex API error: {e}")

    # Prepare context for AI
    context_str = f"Query: {query}\\n\\nWeb:\\n"
    for r in serper_results: 
        context_str += f"- {r.get('title')}: {r.get('snippet')}\\n"
    context_str += "\\nAcademic:\\n"
    for w in openalex_results: 
        context_str += f"- {w.get('title')}\\n"

    prompt = f"Analyze the research data and return a raw JSON object (no markdown, no code blocks) with keys: title, summary, relevance_score (1-100), sources (list of strings). Data:\\n{context_str}"
    
    gemini_key = os.environ.get("GEMINI_API_KEY", "").strip()
    inception_key = os.environ.get("INCEPTION_API_KEY", "").strip()

    # DIAGNOSTIC: List models if 404 persists
    if gemini_key:
        print("Diagnostic: Fetching available models...")
        try:
            diag = requests.get(f"https://generativelanguage.googleapis.com/v1beta/models?key={gemini_key}")
            if diag.status_code == 200:
                model_list = [m['name'] for m in diag.json().get('models', [])]
                print(f"Found {len(model_list)} models. First 5: {model_list[:5]}")
                
                # Dynamic model selection from available list
                target_model = None
                for m in model_list:
                    if "gemini-1.5-flash" in m:
                        target_model = m
                        break
                if not target_model and model_list:
                    target_model = model_list[0]
                
                if target_model:
                    print(f"Attempting dynamically found model: {target_model}")
                    url = f"https://generativelanguage.googleapis.com/v1beta/{target_model}:generateContent?key={gemini_key}"
                    res = requests.post(url, headers={"Content-Type": "application/json"},
                                        json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=30)
                    
                    if res.status_code == 200:
                        text = res.json()['candidates'][0]['content']['parts'][0]['text']
                        text = text.replace("```json", "").replace("```", "").strip()
                        
                        data = json.loads(text)
                        data["timestamp"] = datetime.utcnow().isoformat()
                        data["query"] = query
                        data["engine"] = f"Gemini ({target_model})"
                        
                        queue = []
                        if os.path.exists("context/research-queue.json"):
                            with open("context/research-queue.json", "r", encoding="utf-8") as f:
                                try: queue = json.load(f)
                                except: pass
                        queue.append(data)
                        with open("context/research-queue.json", "w", encoding="utf-8") as f:
                            json.dump(queue, f, indent=2, ensure_ascii=False)
                        
                        print(f"SUCCESS with model {target_model}")
                        return
                    else:
                        print(f"Final Gemini attempt failed: {res.status_code} - {res.text}")
        except Exception as e:
            print(f"Diagnostic failed: {e}")

    # FALLBACK to Inception if Gemini failed
    if inception_key:
        print("Final Fallback: Inception API (verify=False)...")
        try:
            url = "https://api.inception.ai/v1/chat/completions" 
            payload = {
                "model": "inception-1", 
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.2
            }
            res = requests.post(url, headers={"Authorization": f"Bearer {inception_key}", "Content-Type": "application/json"},
                                json=payload, timeout=30, verify=False)
            
            if res.status_code == 200:
                text = res.json()['choices'][0]['message']['content'].replace("```json", "").replace("```", "").strip()
                data = json.loads(text)
                data["timestamp"] = datetime.utcnow().isoformat()
                data["query"] = query
                data["engine"] = "Inception"
                
                queue = []
                if os.path.exists("context/research-queue.json"):
                    with open("context/research-queue.json", "r", encoding="utf-8") as f:
                        try: queue = json.load(f)
                        except: pass
                queue.append(data)
                with open("context/research-queue.json", "w", encoding="utf-8") as f:
                    json.dump(queue, f, indent=2, ensure_ascii=False)
                print("SUCCESS with Inception")
                return
        except Exception as e:
            print(f"Inception fallback failed: {e}")

    print("All attempts failed.")
    sys.exit(1)

if __name__ == "__main__":
    main()
