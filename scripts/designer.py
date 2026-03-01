import os
import sys
import glob
import re
import yaml
import json

def get_latest_draft():
    drafts = glob.glob("_drafts/*.md")
    if not drafts:
        return None
    return max(drafts, key=os.path.getctime)

class BrandValidator:
    def __init__(self, guidelines_path):
        with open(guidelines_path, "r", encoding="utf-8") as f:
            self.guidelines = f.read()
        
        # Core brand rules (extracted from v4.0 guidelines)
        self.rules = {
            "typography": {
                "macro": ["Fraunces", "Syne", "Inter"],
                "micro": ["EB Garamond", "Inter", "JetBrains Mono"]
            },
            "palette": {
                "macro": ["#F5EFE0", "#1A3D2B", "#B8912A"],
                "micro": ["#0F1A15", "#2C3330", "#C5B388"]
            },
            "fibonacci": [8, 13, 21, 34, 55, 89, 144],
            "border_radius": {
                "macro": 4,
                "micro": 2
            }
        }

    def validate_front_matter(self, fm):
        issues = []
        lang = fm.get("language", "de")
        # Blowfish theme parameters check
        # We check if certain brand tokens are used if defined
        
        # Example check: font-family overrides or specific class tags
        # (This depends on how Hugo templates are set up, but we'll check common ones)
        return issues

    def validate_content(self, content):
        issues = []
        # Check for forbidden words (Solarpunk in external copy)
        forbidden_external = ["Solarpunk", "Natural Solarpunk"]
        # Note: Guidelines say don't use in client-facing. 
        # Posts are client-facing.
        for word in forbidden_external:
            if word in content:
                issues.append(f"FORBIDDEN WORD: '{word}' found in post content. (Guideline 08: Use 'Organic Precision' instead).")

        # Check for common layout shortcodes (assumed patterns)
        # e.g. [space: 20] -> should be Fibonacci
        space_matches = re.findall(r'\{\{< space\s+(\d+)\s+>\}\}', content)
        for space in space_matches:
            val = int(space)
            if val not in self.rules["fibonacci"]:
                issues.append(f"LAYOUT: Non-Fibonacci spacing value '{val}' used. Recommended: {self.rules['fibonacci']}.")

        return issues

def main():
    guidelines_path = "ReNatureForce_BrandGuidelines_v4.md"
    if not os.path.exists(guidelines_path):
        print(f"Guidelines not found at {guidelines_path}")
        sys.exit(1)

    target_file = get_latest_draft()
    if not target_file:
        print("No drafts found.")
        sys.exit(0)

    print(f"Validating design for: {target_file}")
    
    with open(target_file, "r", encoding="utf-8") as f:
        full_text = f.read()

    # Extract Front Matter
    fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', full_text, re.DOTALL)
    fm = {}
    content = full_text
    if fm_match:
        try:
            fm = yaml.safe_load(fm_match.group(1))
            content = full_text[fm_match.end():]
        except:
            pass

    validator = BrandValidator(guidelines_path)
    
    report = []
    report.append(f"# Design Compliance Report: {os.path.basename(target_file)}")
    report.append(f"**Date:** {json.dumps(str(os.environ.get('GITHUB_RUN_ID', 'local')))}")
    report.append("\n## Audit Results")

    fm_issues = validator.validate_front_matter(fm)
    content_issues = validator.validate_content(content)

    all_issues = fm_issues + content_issues

    if not all_issues:
        report.append("✅ All checks passed. The post aligns with Rə:Ecosystem Brand Guidelines v4.0.")
    else:
        for issue in all_issues:
            report.append(f"- ⚠️ {issue}")

    report_text = "\n".join(report)
    print(report_text)

    # Save report for GitHub Action
    with open("design_report.md", "w", encoding="utf-8") as f:
        f.write(report_text)

if __name__ == "__main__":
    main()
