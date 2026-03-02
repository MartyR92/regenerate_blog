import os
import sys
import glob
import re
import yaml
import json

def get_drafts():
    return glob.glob("_drafts/*.md")

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

    def validate_content(self, content, lang):
        issues = []
        # Check for forbidden words (Solarpunk in external copy)
        # Note: Guidelines say don't use in client-facing. 
        # Posts are client-facing.
        forbidden_external = ["Solarpunk", "Natural Solarpunk"]
        for word in forbidden_external:
            if word in content:
                issues.append(f"FORBIDDEN WORD: '{word}' found in {lang.upper()} content. (Guideline 08: Use 'Regenerative Avantgarde' instead).")

        # Check for common layout shortcodes
        space_matches = re.findall(r'\{\{< space\s+(\d+)\s+>\}\}', content)
        for space in space_matches:
            val = int(space)
            if val not in self.rules["fibonacci"]:
                issues.append(f"LAYOUT ({lang.upper()}): Non-Fibonacci spacing value '{val}' used. Recommended: {self.rules['fibonacci']}.")

        return issues

def main():
    guidelines_path = "ReNatureForce_BrandGuidelines_v4.md"
    if not os.path.exists(guidelines_path):
        print(f"Guidelines not found at {guidelines_path}")
        sys.exit(1)

    targets = get_drafts()
    if not targets:
        print("No drafts found.")
        sys.exit(0)

    validator = BrandValidator(guidelines_path)
    report = []
    report.append("# Multi-Post Design Compliance Report")
    report.append(f"**Run ID:** {os.environ.get('GITHUB_RUN_ID', 'local')}")
    
    for target_file in targets:
        print(f"Validating design for: {target_file}")
        with open(target_file, "r", encoding="utf-8") as f:
            full_text = f.read()

        # Extract Front Matter
        fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', full_text, re.DOTALL)
        fm = {}
        content = full_text
        lang = "de"
        if fm_match:
            try:
                fm = yaml.safe_load(fm_match.group(1))
                content = full_text[fm_match.end():]
                lang = fm.get("language", "de")
            except:
                pass

        report.append(f"\n### Audit: {os.path.basename(target_file)} ({lang.upper()})")
        issues = validator.validate_content(content, lang)

        if not issues:
            report.append("✅ All checks passed.")
        else:
            for issue in issues:
                report.append(f"- ⚠️ {issue}")

    report_text = "\n".join(report)
    print(report_text)

    # Save report for GitHub Action
    with open("design_report.md", "w", encoding="utf-8") as f:
        f.write(report_text)

if __name__ == "__main__":
    main()
