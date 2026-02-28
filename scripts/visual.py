import os
import sys
import glob
import requests
import json
import re
import urllib3
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def main():
    gemini_key = os.environ.get("GEMINI_API_KEY")
    unsplash_key = os.environ.get("UNSPLASH_ACCESS_KEY")
    
    if not gemini_key:
        print("Missing GEMINI_API_KEY")
        sys.exit(1)
        
    # Get the latest modified draft file
    drafts = glob.glob("_drafts/*.md")
    if not drafts:
        print("No drafts found to process.")
        sys.exit(0)
        
    target_file = max(drafts, key=os.path.getctime)
    print(f"Processing visuals for: {target_file}")
    
    with open(target_file, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Simple check if featureImage already exists
    if "featureImage:" in content or "thumbnail:" in content:
        print("Image already defined in front matter. Skipping.")
        sys.exit(0)
        
    # 1. Ask Gemini for a search query based on the content
    prompt = f"""
    Based on the following blog post, provide a 1-3 word search query in English 
    that would find a good cover image on Unsplash (representing nature, economy, solarpunk, etc.).
    Respond ONLY with the search query, nothing else.
    
    POST CONTENT:
    {content[:2000]}
    """
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_key}"
    res = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=60)
    
    if res.status_code != 200:
        print(f"Failed to get search query from Gemini: {res.status_code} - {res.text}")
        sys.exit(1)
        
    search_query = res.json()['candidates'][0]['content']['parts'][0]['text'].strip()
    print(f"Generated Unsplash search query: {search_query}")
    
    # 2. Search Unsplash
    if not unsplash_key:
        print("Missing UNSPLASH_ACCESS_KEY. Skipping image download.")
        sys.exit(0)
        
    unsplash_url = f"https://api.unsplash.com/search/photos?query={search_query}&per_page=1&orientation=landscape"
    headers = {"Authorization": f"Client-ID {unsplash_key}"}
    u_res = requests.get(unsplash_url, headers=headers)
    
    if u_res.status_code != 200 or not u_res.json().get('results'):
        print(f"Unsplash search failed or returned no results for: {search_query}")
        sys.exit(0)
        
    img_data = u_res.json()['results'][0]
    img_url = img_data['urls']['regular']
    author_name = img_data['user']['name']
    
    print(f"Found image by {author_name}")
    
    # 3. Download the image
    img_response = requests.get(img_url)
    
    slug = os.path.basename(target_file).replace('.md', '')
    year = datetime.now().strftime("%Y")
    
    # Define paths
    img_dir = f"assets/images/{year}/{slug}"
    os.makedirs(img_dir, exist_ok=True)
    img_path = f"{img_dir}/cover.jpg"
    
    with open(img_path, "wb") as f:
        f.write(img_response.content)
        
    print(f"Saved image to {img_path}")
    
    # 4. Ask Gemini for an alt-text
    alt_prompt = f"Write a short, descriptive alt-text (max 15 words) for an article cover image about: {search_query}"
    alt_res = requests.post(url, json={"contents": [{"parts": [{"text": alt_prompt}]}]})
    alt_text = alt_res.json()['candidates'][0]['content']['parts'][0]['text'].strip().replace('"', "'")
    
    # 5. Update front matter
    new_fm = f'featureImage: "/images/{year}/{slug}/cover.jpg"\\nfeatureImageAlt: "{alt_text}"\\n'
    content = content.replace("---\\n", f"---\\n{new_fm}", 1)
    
    # Append attribution at the end
    attribution = f'\\n\\n*Cover image by {author_name} on Unsplash*\\n'
    content += attribution
    
    with open(target_file, "w", encoding="utf-8") as f:
        f.write(content)
        
    print("Successfully updated post with visual assets.")

if __name__ == "__main__":
    main()
