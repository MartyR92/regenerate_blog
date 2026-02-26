import os
import json
import random
import requests
import urllib.parse
import google.generativeai as genai
from datetime import datetime
import sys

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
    # Strip whitespace/newlines from keys to prevent header errors
    serper_key = os.environ.get("SERPER_API_KEY", "").strip()
    gemini_key = os.environ.get("GEMINI_API_KEY", "").strip()

    if serper_key:
        try:
            res = requests.post(
                "https://google.serper.dev/search", 
                headers={"X-API-KEY": serper_key, "Content-Type": "application/json"},
                json={"q": query, "num": 5}
            )
            if res.status_code == 200:
                serper_results = res.json().get("organic", [])
            else:
                print(f"Serper API error status: {res.status_code}, body: {res.text}")
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

    if not gemini_key: 
        print("GEMINI_API_KEY is empty or missing after stripping.")
        sys.exit(1)
    
    try:
        genai.configure(api_key=gemini_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"Analyze the data and return a raw JSON object (no markdown formatting, no code blocks) with keys: title, summary, relevance_score (1-100), sources (list of strings). Data:\\n{context_str}"
        
        response = model.generate_content(prompt)
        text = response.text.replace("```json", "").replace("```", "").strip()
        
        data = json.loads(text)
        data["timestamp"] = datetime.utcnow().isoformat()
        data["query"] = query
        
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
            
        print(f"Successfully added research entry for query: {query}")
    except Exception as e:
        print(f"Error during Gemini processing or file write: {e}")
        if 'text' in locals():
            print(f"Raw response was: {text}")
        sys.exit(1)

if __name__ == "__main__":
    main()
