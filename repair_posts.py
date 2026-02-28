import glob, re, os

fixes = {
    'Ã¤': 'ä', 'Ã¶': 'ö', 'Ã¼': 'ü',
    'Ã„': 'Ä', 'Ã–': 'Ö', 'Ãœ': 'Ü',
    'ÃŸ': 'ß', 'â€“': '–', 'â€”': '—',
    'â€ž': '„', 'â€œ': '“', 'â€™': '’'
}

for f in glob.glob('content/de/posts/*.md'):
    try:
        if os.path.getsize(f) == 0:
            continue
            
        with open(f, 'rb') as file:
            raw = file.read()
        
        if raw.startswith(b'\xef\xbb\xbf'):
            raw = raw[3:]
            
        content = raw.decode('utf-8', errors='ignore')
        
        # Strip code blocks
        content = re.sub(r'^```markdown\s*', '', content)
        content = re.sub(r'\s*```$', '', content)
        content = content.strip()
        
        for k, v in fixes.items():
            content = content.replace(k, v)
            
        # Ensure it starts with exactly ---
        if not content.startswith('---'):
            # Maybe there is garbage at the start?
            idx = content.find('---')
            if idx != -1:
                content = content[idx:]
        
        with open(f, 'w', encoding='utf-8', newline='') as file:
            file.write(content)
        print(f'Repaired {f}')
    except Exception as e:
        print(f'Error repairing {f}: {e}')
