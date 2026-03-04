import os
import sys
import glob
import requests
import json
import re
import unicodedata
import urllib3
import time
import random
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_all_articles():
    # Process all files in content/de/posts and content/en/posts
    return glob.glob("content/de/posts/*.md") + glob.glob("content/en/posts/*.md")

def call_gemini_with_retry(url, payload, max_retries=5):
    for i in range(max_retries):
        try:
            res = requests.post(url, json=payload, timeout=60)
            if res.status_code == 200:
                return res
            elif res.status_code == 429:
                wait_time = (2 ** i) * 10 + random.uniform(0, 5)
                print(f"Quota exceeded. Retrying in {wait_time:.1f}s... (Attempt {i+1}/{max_retries})")
                time.sleep(wait_time)
            elif res.status_code >= 500:
                print(f"Server Error ({res.status_code}). Retrying in 10s...")
                time.sleep(10)
            else:
                print(f"Critical API Error: {res.status_code} - {res.text}")
                return None
        except requests.exceptions.Timeout:
            print(f"Timeout occurred. Retrying... (Attempt {i+1}/{max_retries})")
            time.sleep(10)
    print("Maximum retries reached.")
    return None

def slugify(text):
    text = text.lower().replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('ß', 'ss')
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return re.sub(r'^-+|-+$', '', text)

def process_file(target_file, gemini_key, unsplash_key):
    print(f"Processing visuals for: {target_file}")
    
    with open(target_file, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Simple check if featureImage already exists
    if "featureImage:" in content or "thumbnail:" in content:
        print(f"Image already defined in {target_file}. Skipping.")
        return
        
    # 1. Ask Gemini for a search query based on the content
    prompt = f"""
    Based on the following blog post, provide a 1-3 word search query in English 
    that would find a good cover image on Unsplash (representing nature, economy, solarpunk, etc.).
    Respond ONLY with the search query, nothing else.
    
    POST CONTENT:
    {content[:2000]}
    """
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    res = call_gemini_with_retry(url, payload)
    
    search_query = "Solarpunk Nature" # Default fallback
    if res:
        try:
            res_json = res.json()
            search_query = res_json['candidates'][0]['content']['parts'][0]['text'].strip()
            print(f"Generated Unsplash search query: {search_query}")
        except:
            print("Failed to parse Gemini response. Using fallback search query.")
    else:
        print("Gemini API unavailable. Using local fallback search query.")
    
    # 2. Search Unsplash
    if not unsplash_key:
        print("Missing UNSPLASH_ACCESS_KEY. Skipping image download for now.")
        return
        
    unsplash_url = f"https://api.unsplash.com/search/photos?query={search_query}&per_page=1&orientation=landscape"
    headers = {"Authorization": f"Client-ID {unsplash_key}"}
    u_res = requests.get(unsplash_url, headers=headers)
    
    if u_res.status_code != 200 or not u_res.json().get('results'):
        print(f"Unsplash search failed or returned no results for: {search_query}")
        return
        
    img_data = u_res.json()['results'][0]
    img_url = img_data['urls']['regular']
    author_name = img_data['user']['name']
    
    print(f"Found image by {author_name}")
    
    # 3. Download the image
    img_response = requests.get(img_url)
    
    # Standardize slug
    base_name = os.path.basename(target_file).replace('.md', '')
    slug = slugify(re.sub(r'\.(de|en)$', '', base_name))
    year = datetime.now().strftime("%Y")
    
    # Define paths
    img_dir = f"static/images/{year}/{slug}"
    os.makedirs(img_dir, exist_ok=True)
    img_path_full = f"{img_dir}/cover.jpg"
    
    with open(img_path_full, "wb") as f:
        f.write(img_response.content)
        
    print(f"Saved image to {img_path_full}")
    
    # 4. Ask Gemini for an alt-text
    alt_text = f"Cover image for article about {search_query}"
    alt_prompt = f"Write a short, descriptive alt-text (max 15 words) for an article cover image about: {search_query}"
    alt_res = call_gemini_with_retry(url, {"contents": [{"parts": [{"text": alt_prompt}]}]})
    if alt_res:
        try:
            alt_text = alt_res.json()['candidates'][0]['content']['parts'][0]['text'].strip().replace('"', "'")
        except: pass
    
    # 5. Update front matter
    new_fm = f'featureImage: "/images/{year}/{slug}/cover.jpg"\nfeatureImageAlt: "{alt_text}"\n'
    content = content.replace("---\n", f"---\n{new_fm}", 1)
    
    # Append attribution at the end
    attribution = f"\n\n*Cover image by {author_name} on Unsplash*\n"
    content += attribution
    
    with open(target_file, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"Successfully updated {target_file} with visual assets.")

def main():
    gemini_key = os.environ.get("GEMINI_API_KEY")
    unsplash_key = os.environ.get("UNSPLASH_ACCESS_KEY")
    
    if not gemini_key:
        print("Missing GEMINI_API_KEY")
        sys.exit(1)
        
    articles = get_all_articles()
    if not articles:
        print("No articles found to process.")
        sys.exit(0)
        
    print(f"Found {len(articles)} articles to process.")
    
    for article in articles:
        process_file(article, gemini_key, unsplash_key)
        time.sleep(2)

if __name__ == "__main__":
    main()
