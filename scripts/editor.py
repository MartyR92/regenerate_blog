import os
import json
import requests
import sys
import subprocess
from datetime import datetime
import re

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
    github_token = os.environ.get("GITHUB_TOKEN", "").strip()
    if not gemini_key or not github_token:
        print("Missing API Keys")
        sys.exit(1)

    # 1. Identify changed file in _drafts/
    try:
        changed_files = subprocess.check_output(['git', 'diff', '--name-only', 'HEAD^', 'HEAD']).decode('utf-8').splitlines()
        draft_files = [f for f in changed_files if f.startswith('_drafts/') and f.endswith('.md')]
    except:
        # Fallback if git diff fails (e.g. initial commit)
        draft_files = [f for f in os.listdir('_drafts') if f.endswith('.md')]
        draft_files = [os.path.join('_drafts', f) for f in draft_files]

    if not draft_files:
        print("No changed drafts found.")
        sys.exit(0)

    target_file = draft_files[0]
    print(f"Editing/Reviewing: {target_file}")

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
    
    prompt = f"{editor_prompt}\n\nMEMORY:\n{memory}\n\nARTICLE:\n{content}"
    
    # Use direct REST for reliability
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={gemini_key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    res = requests.post(url, json=payload, timeout=120)
    if res.status_code != 200:
        print(f"Gemini Error: {res.text}")
        sys.exit(1)
    
    review_output = res.json()['candidates'][0]['content']['parts'][0]['text']

    # 4. Git Operations: Create Branch & PR
    slug = os.path.basename(target_file).replace('.md', '')
    branch_name = f"editor/{slug}-{datetime.now().strftime('%Y%m%d')}"
    
    subprocess.run(['git', 'config', 'user.name', 'github-actions[bot]'])
    subprocess.run(['git', 'config', 'user.email', 'github-actions[bot]@users.noreply.github.com'])
    subprocess.run(['git', 'checkout', '-b', branch_name])
    subprocess.run(['git', 'add', target_file])
    subprocess.run(['git', 'commit', '-m', f"Editor review for {slug}"])
    subprocess.run(['git', 'push', 'origin', branch_name, '--force'])

    # 5. Create Pull Request via GitHub API
    repo = os.environ.get("GITHUB_REPOSITORY")
    pr_url = f"https://api.github.com/repos/{repo}/pulls"
    headers = {"Authorization": f"token {github_token}", "Accept": "application/vnd.github.v3+json"}
    
    pr_data = {
        "title": f"Editor Review: {slug}",
        "body": review_output,
        "head": branch_name,
        "base": "main"
    }
    
    pr_res = requests.post(pr_url, headers=headers, json=pr_data)
    if pr_res.status_code == 201:
        pr_number = pr_res.json()['number']
        print(f"PR Created: #{pr_number}")
        
        # Add Label
        label_url = f"https://api.api.github.com/repos/{repo}/issues/{pr_number}/labels"
        requests.post(label_url, headers=headers, json={"labels": ["editor-review"]})
    else:
        print(f"PR Creation failed: {pr_res.text}")

if __name__ == "__main__":
    main()
