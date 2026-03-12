import os
import json
import requests
import sys
import subprocess
from datetime import datetime
import re
import glob

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
    github_token = os.environ.get("GITHUB_TOKEN", "").strip()
    repo = os.environ.get("GITHUB_REPOSITORY")
    
    if not gemini_key or not github_token:
        print("Missing API Keys")
        sys.exit(1)

    # 1. Identify files to review
    target_files = []
    
    # Try git diff first (for push/pr triggers)
    try:
        changed_files = subprocess.check_output(['git', 'diff', '--name-only', 'HEAD^', 'HEAD']).decode('utf-8').splitlines()
        target_files = [f for f in changed_files if f.startswith('_drafts/') and f.endswith('.md')]
    except:
        pass

    # Fallback to all files in _drafts (for manual triggers or first commit)
    if not target_files:
        target_files = glob.glob("_drafts/*.md")
    
    if not target_files:
        print("No drafts found to review.")
        sys.exit(0)

    base_file = target_files[0]
    slug = os.path.basename(base_file).replace('.md', '').replace('.de', '').replace('.en', '')
    
    # Discovery available model
    target_model = "models/gemini-1.5-pro"
    try:
        diag = requests.get(f"https://generativelanguage.googleapis.com/v1beta/models?key={gemini_key}")
        if diag.status_code == 200:
            m_list = [m['name'] for m in diag.json().get('models', [])]
            gemini_25 = [m for m in m_list if "2.5" in m]
            if gemini_25: target_model = gemini_25[0]
    except: pass

    review_outputs = []

    for target_file in target_files:
        print(f"Reviewing: {target_file}")
        with open(target_file, "r", encoding="utf-8") as f:
            content = f.read()

        # 2. Check & Fix ai_assisted Flag
        if "ai_assisted:" not in content:
            content = content.replace("---", "---\nai_assisted: true", 1)
            with open(target_file, "w", encoding="utf-8") as f:
                f.write(content)
            print("Added missing ai_assisted flag.")

        # 3. Call Gemini 2.5 Pro for Review
        editor_prompt = get_context_file("context/agent-prompts/editor-v1.md")
        memory = get_context_file("context/blog-memory.json")
        identity = get_context_file("context/system-identity.md")
        ontology = get_context_file("context/ontology.json")
        
        final_prompt = f"""
        {editor_prompt}
        
        --- CONTEXT ---
        SYSTEM IDENTITY: {identity}
        BLOG MEMORY: {memory}
        ONTOLOGY: {ontology}
        
        --- ARTICLE ---
        FILE: {target_file}
        CONTENT:
        {content}
        """

        print(f"Requesting review from {target_model}...")
        url = f"https://generativelanguage.googleapis.com/v1beta/{target_model}:generateContent?key={gemini_key}"
        res = requests.post(url, json={"contents": [{"parts": [{"text": final_prompt}]}]}, timeout=180)
        
        if res.status_code != 200:
            print(f"Gemini Error: {res.text}")
            sys.exit(1)
        
        review_output = res.json()['candidates'][0]['content']['parts'][0]['text']
        review_outputs.append(f"### Review for {os.path.basename(target_file)}\n\n{review_output}")

    # 4. Create Branch & PR
    date_tag = datetime.now().strftime('%Y%m%d')
    branch_name = f"editor/{slug[:20]}-{date_tag}"
    
    subprocess.run(['git', 'config', 'user.name', 'github-actions[bot]'])
    subprocess.run(['git', 'config', 'user.email', 'github-actions[bot]@users.noreply.github.com'])
    
    # Check if branch exists
    subprocess.run(['git', 'checkout', '-b', branch_name])
    for tf in target_files:
        subprocess.run(['git', 'add', tf])
        
    # Always create a commit so the PR can be opened (differs from base)
    subprocess.run(['git', 'commit', '--allow-empty', '-m', f"Editor: Review for {slug}"])
    subprocess.run(['git', 'push', 'origin', branch_name, '--force'])

    # 5. Create PR via API
    pr_headers = {"Authorization": f"token {github_token}", "Accept": "application/vnd.github.v3+json"}
    combined_review = "\n\n---\n\n".join(review_outputs)
    pr_payload = {
        "title": f"Editor Review: {slug}",
        "body": f"## Automated Review by Editor Agent\n\n{combined_review}",
        "head": branch_name,
        "base": "main"
    }
    
    pr_res = requests.post(f"https://api.github.com/repos/{repo}/pulls", headers=pr_headers, json=pr_payload)
    if pr_res.status_code == 201:
        pr_num = pr_res.json()['number']
        print(f"SUCCESS: PR #{pr_num} created.")
        # Add Label
        requests.post(f"https://api.github.com/repos/{repo}/issues/{pr_num}/labels", 
                      headers=pr_headers, json={"labels": ["editor-review"]})
    elif pr_res.status_code == 422:
        print("PR already exists or no changes.")
    else:
        print(f"PR Error: {pr_res.text}")

if __name__ == "__main__":
    main()
