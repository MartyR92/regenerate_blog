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
    serper_key = os.environ.get("SERPER_API_KEY")
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
            print(f"Serper API error: {e}")

    openalex_results = []
    try:
        url = f"https://api.openalex.org/works?search={urllib.parse.quote(query)}&per-page=5&sort=publication_date:desc"
        res = requests.get(url)
        if res.status_code == 200:
            openalex_results = res.json().get("results", [])
    except Exception as e:
        print(f"OpenAlex API error: {e}")

    context_str = f"Query: {query}

Web:
"
    for r in serper_results: 
        context_str += f"- {r.get('title')}: {r.get('snippet')}
"
    context_str += "
Academic:
"
    for w in openalex_results: 
        context_str += f"- {w.get('title')}
"

    gemini_key = os.environ.get("GEMINI_API_KEY")
    if not gemini_key: 
        print("GEMINI_API_KEY missing")
        sys.exit(1)
    
    genai.configure(api_key=gemini_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"Analyze the data and return a raw JSON object (no markdown formatting, no code blocks) with keys: title, summary, relevance_score (1-100), sources (list of strings). Data:
{context_str}"
    
    response = model.generate_content(prompt)
    text = response.text.replace("```json", "").replace("```", "").strip()
    
    try:
        data = json.loads(text)
        data["timestamp"] = datetime.utcnow().isoformat()
        data["query"] = query
    except Exception as e:
        print(f"JSON Parse Error: {e}
Response was: {text}")
        sys.exit(1)

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

if __name__ == "__main__":
    main()
