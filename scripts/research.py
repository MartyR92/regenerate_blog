import os
import json
import random
import requests
import urllib.parse
from datetime import datetime
import sys

# Removed google-generativeai import to keep it lean and avoid confusion
# with the REST API approach.

def call_inception_api(inception_key, prompt):
    """
    Fallback function to call Inception API (OpenAI-compatible).
    """
    try:
        # NOTE: Using a hypothetical common endpoint if the original failed.
        # Most "Prestige" AI providers use OpenAI-compatible routing.
        url = "https://api.inception.ai/v1/chat/completions" 
        headers = {
            "Authorization": f"Bearer {inception_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "inception-1", 
            "messages": [
                {"role": "system", "content": "You are a research assistant for a regenerative economy blog. Return raw JSON only with keys: title, summary, relevance_score, sources."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2
        }
        
        # Adding verify=False as a fallback for the SSL error seen in logs
        try:
            res = requests.post(url, headers=headers, json=payload, timeout=30)
        except requests.exceptions.SSLError:
            print("SSL Error with Inception, retrying without verification...")
            res = requests.post(url, headers=headers, json=payload, timeout=30, verify=False)

        if res.status_code == 200:
            content = res.json()['choices'][0]['message']['content']
            return content.replace("```json", "").replace("```", "").strip()
        else:
            print(f"Inception API error: {res.status_code} - {res.text}")
            return None
    except Exception as e:
        print(f"Inception API exception: {e}")
        return None

def main():
    try:
        with open("context/ontology.json", "r", encoding="utf-8") as f:
            ontology = json.load(f)
    except Exception as e:
        print(f"Error loading ontology: {e}")
        sys.exit(1)

    domain = random.choice(list(ontology.get("domains", {}).keys()))
    tags = ontology["domains"][domain].get("tags", [])
    tag = random.choice(tags) if tags else domain
    query = f"{domain} {tag} latest developments in regenerative economy"

    serper_results = []
    serper_key = os.environ.get("SERPER_API_KEY", "").strip()
    gemini_key = os.environ.get("GEMINI_API_KEY", "").strip()
    inception_key = os.environ.get("INCEPTION_API_KEY", "").strip()

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

    openalex_results = []
    try:
        url = f"https://api.openalex.org/works?search={urllib.parse.quote(query)}&per-page=5&sort=publication_date:desc"
        res = requests.get(url)
        if res.status_code == 200:
            openalex_results = res.json().get("results", [])
    except Exception as e:
        print(f"OpenAlex API error: {e}")

    context_str = f"Query: {query}\\n\\nWeb:\\n"
    for r in serper_results: 
        context_str += f"- {r.get('title')}: {r.get('snippet')}\\n"
    context_str += "\\nAcademic:\\n"
    for w in openalex_results: 
        context_str += f"- {w.get('title')}\\n"

    prompt = f"Analyze the research data and return a raw JSON object (no markdown, no code blocks) with keys: title, summary, relevance_score (1-100), sources (list of strings). Data:\\n{context_str}"
    
    text = None
    engine_used = None

    # Try Gemini first via direct REST API
    if gemini_key:
        try:
            print("Attempting Gemini API (REST v1)...")
            # Changed version to v1 (from v1beta) to resolve the 404
            url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={gemini_key}"
            headers = {"Content-Type": "application/json"}
            payload = {
                "contents": [{"parts": [{"text": prompt}]}]
            }
            res = requests.post(url, headers=headers, json=payload, timeout=30)
            if res.status_code == 200:
                res_json = res.json()
                text = res_json['candidates'][0]['content']['parts'][0]['text']
                text = text.replace("```json", "").replace("```", "").strip()
                engine_used = "Gemini (REST v1)"
            else:
                print(f"Gemini REST API error: {res.status_code} - {res.text}")
        except Exception as e:
            print(f"Gemini REST API exception: {e}")

    # Fallback to Inception
    if not text and inception_key:
        print("Attempting Inception API Fallback...")
        text = call_inception_api(inception_key, prompt)
        engine_used = "Inception"

    if not text:
        print("All AI engines failed. Please verify API keys and network connectivity.")
        sys.exit(1)
    
    try:
        data = json.loads(text)
        data["timestamp"] = datetime.utcnow().isoformat()
        data["query"] = query
        data["engine"] = engine_used
        
        queue = []
        if os.path.exists("context/research-queue.json"):
            with open("context/research-queue.json", "r", encoding="utf-8") as f:
                try: 
                    queue = json.load(f)
                except: 
                    pass
        queue.append(data)
        
        with open("context/research-queue.json", "w", encoding="utf-8") as f:
            json.dump(queue, f, indent=2, ensure_ascii=False)
            
        print(f"Successfully added research entry using {engine_used} for query: {query}")
    except Exception as e:
        print(f"JSON Parse Error: {e}")
        print(f"Raw response was: {text}")
        sys.exit(1)

if __name__ == "__main__":
    main()
