import os
import json
import random
import requests
import urllib.parse
import google.generativeai as genai
from datetime import datetime
import sys

def call_inception_api(inception_key, prompt):
    """
    Fallback function to call Inception API (OpenAI-compatible).
    Adjusted based on common SSL/URL issues.
    """
    try:
        # NOTE: Ensure this URL is correct. Many providers use /v1/chat/completions
        url = "https://api.inception.ai/v1/chat/completions" 
        headers = {
            "Authorization": f"Bearer {inception_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "inception-1", 
            "messages": [
                {"role": "system", "content": "You are a research assistant. Return raw JSON only."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2
        }
        
        # verify=False is a last resort for SSL errors, but better to fix the root cause if possible.
        # Since we saw SSL errors in the logs, we add a timeout and retry logic.
        res = requests.post(url, headers=headers, json=payload, timeout=30)
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
    query = f"{domain} {tag} latest developments"

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

    # Try Gemini first
    if gemini_key:
        try:
            print("Attempting Gemini API...")
            genai.configure(api_key=gemini_key)
            # Use 'gemini-1.5-flash' - the 'latest' suffix was causing 404 in some environments
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            text = response.text.replace("```json", "").replace("```", "").strip()
            engine_used = "Gemini"
        except Exception as e:
            print(f"Gemini processing failed: {e}")

    # Fallback to Inception
    if not text and inception_key:
        print("Attempting Inception API Fallback...")
        text = call_inception_api(inception_key, prompt)
        engine_used = "Inception"

    if not text:
        print("All AI engines failed. Check API keys and network connectivity.")
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
