import os
import glob
import re

files = glob.glob('_drafts/*.md') + glob.glob('content/**/*.md', recursive=True)
for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Match the frontmatter block
    fm_match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if fm_match:
        fm = fm_match.group(1)
        new_fm = []
        changed = False
        for line in fm.split('\n'):
            if line.startswith('title:') and not line.startswith('title: "') and not line.startswith("title: '"):
                # Quote the title if it contains a colon
                val = line[6:].strip()
                if ':' in val:
                    line = f'title: "{val}"'
                    changed = True
            new_fm.append(line)
        
        if changed:
            new_fm_str = '\n'.join(new_fm)
            content = content.replace(fm, new_fm_str)
            with open(f, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f'Fixed {f}')
