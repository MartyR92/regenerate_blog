import os
import json
import requests
import sys
import glob

# Disable SSL warnings
import urllib3
requests.packages.urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_context_file(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def main():
    gemini_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not gemini_key:
        print("GEMINI_API_KEY missing")
        sys.exit(1)

    # 1. Identify file to review
    # We look for the newest file in _drafts/
    drafts = glob.glob("_drafts/*.md")
    if not drafts:
        print("No drafts found to review.")
        sys.exit(0)
    
    # Sort by modification time to get the latest
    latest_draft = max(drafts, key=os.path.getmtime)
    print(f"Reviewing latest draft: {latest_draft}")
    
    with open(latest_draft, "r", encoding="utf-8") as f:
        article_content = f.read()

    # 2. Load Context
    identity = get_context_file("context/system-identity.md")
    memory = get_context_file("context/blog-memory.json")
    ontology = get_context_file("context/ontology.json")
    editor_prompt_template = get_context_file("context/agent-prompts/editor-v1.md")

    # 3. Dynamic Model Discovery (Gemini 2.5)
    target_model = "models/gemini-2.5-flash"
    try:
        diag = requests.get(f"https://generativelanguage.googleapis.com/v1beta/models?key={gemini_key}")
        if diag.status_code == 200:
            model_list = [m['name'] for m in diag.json().get('models', [])]
            gemini_25 = [m for m in model_list if "2.5" in m]
            if gemini_25:
                target_model = gemini_25[0]
    except:
        pass

    # 4. Construct Final Prompt
    prompt = f"""
    {editor_prompt_template}

    --- CONTEXT DATA ---
    SYSTEM IDENTITY:
    {identity}

    BLOG MEMORY:
    {memory}

    ONTOLOGY (Tags/Categories):
    {ontology}

    --- ARTICLE TO REVIEW ---
    FILE: {latest_draft}
    CONTENT:
    {article_content}
    """

    # 5. Call Gemini REST API
    url = f"https://generativelanguage.googleapis.com/v1beta/{target_model}:generateContent?key={gemini_key}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    try:
        res = requests.post(url, json=payload, timeout=120)
        if res.status_code == 200:
            review_output = res.json()['candidates'][0]['content']['parts'][0]['text']
            
            # 6. Output handling
            # In a real GH Action, we write to GITHUB_STEP_SUMMARY
            summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
            if summary_file:
                with open(summary_file, "a", encoding="utf-8") as f:
                    f.write(f"
## Editor Review for `{os.path.basename(latest_draft)}`
")
                    f.write(review_output)
            
            print("Successfully generated editor review.")
            print(review_output)
        else:
            print(f"Gemini API error: {res.status_code} - {res.text}")
            sys.exit(1)
    except Exception as e:
        print(f"Execution error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
