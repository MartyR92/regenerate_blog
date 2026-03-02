# Plan: Phase 8 - Diagram Rendering & Language Fixes

## 1. Fix Image Pathing
- [ ] Modify `scripts/image.py`:
    - Change `img_dir` base from `assets/images` to `static/images`.
    - Update directory creation logic to ensure `static/images/YYYY/slug/` exists.

## 2. Implement Language Detection
- [ ] Update `scripts/image.py` to:
    - Extract the `language` field from Front Matter (if present).
    - Fallback: Detect language by scanning for "Regenerative Wirtschaft" (DE) vs "Regenerative Economy" (EN) or using a simple keyword check.

## 3. Localize Captions & Alt-Text
- [ ] Refine the Gemini 1.5 Flash prompt in `scripts/image.py`:
    - Request a specific `caption` and `alt_text` in the detected language.
    - Explicitly forbid the mention of "agents" or "AI" in the reader-facing strings.
- [ ] Update the Markdown insertion logic to use these localized strings.

## 4. Brand Guidelines Adherence
- [ ] Ensure the prompt for SVG generation explicitly mentions the "Organic Precision" color palette and typography rules from the Guidelines.

## 5. Verification
- [ ] Run a local build and verify that the diagrams in `content/de/posts/` render correctly.
- [ ] Check that the captions are in German for German posts and English for English posts.
