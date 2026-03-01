# Research: Phase 6 - E2E Verification & Refinement

## 1. Quality Audit: "Algorithmic Symbiosis" Post
- **Status:** Already published in `content/de/posts/`.
- **Gaps:** 
    - Lacks `[DIAGRAM]` tags introduced in Milestone 2.
    - Contains several `[VERIFY]` tags that should be resolved or formatted according to SOP.
    - Language: German only. Needs an English counterpart to test the en/de switch.
- **Refinement Strategy:** 
    - Insert `[DIAGRAM]` placeholders at key data points (ROI, Yield metrics).
    - Trigger a manual translation or create a translated version.

## 2. Trigger Mechanism
- **Tool:** GitHub CLI (`gh`) is installed and available.
- **Action:** `gh issue create` with the `write:` label will trigger the `Writer Agent`.
- **Template:** Use fields from `.github/ISSUE_TEMPLATE/new-post.yml`.

## 3. Production Environment
- **URL:** `https://martyr92.github.io/regenerate_blog/`
- **Verification Target:** 
    - Language switcher visibility in the header.
    - Successful navigation between `de/posts/slug` and `en/posts/slug`.
    - Correct rendering of technical diagrams (from `image-agent`).
    - Presence of the Designer Agent report in the final PR before merge.
