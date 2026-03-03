# Phase 13 Research: Agent Infrastructure for Retrofit

## Objective
Update the `visual-agent` (`visual.py`) and `image-agent` (`image.py`) to support the bulk processing and multi-visual generation required for the Milestone v5.0 retrofit.

## Current State Analysis
- **`visual.py`**:
    - Only processes the latest modified draft.
    - Hardcoded to save as `cover.jpg`.
    - No support for directory crawling or multiple articles.
- **`image.py`**:
    - Generates one `technical_diagram_1_{lang}.svg` per article.
    - Limited error handling for multiple calls per article.
    - No explicit logic for "Charts" vs "Diagrams" in the prompt.

## Proposed Changes
### 1. `visual.py` Enhancements
- Implement a `--all` flag or a function to iterate through `content/de/posts` and `content/en/posts`.
- Add a check to skip articles that already have `featureImage` (unless forced).
- Ensure Unsplash search query generation is robust for all archive content.

### 2. `image.py` Enhancements
- Implement logic to generate a specific number of visuals (target: 2 new per article).
- Diversify the prompt:
    - Visual 2: "Technical Chart" (Data focus).
    - Visual 3: "Technical Diagram" (System focus).
- Update filenames to `technical_visual_2_{lang}.svg` and `technical_visual_3_{lang}.svg`.
- Improve placement logic to ensure visuals are distributed through the post (e.g., after different H2 headers).

## Technical Risks
- **API Quotas**: Sequential calls to Gemini/Unsplash for 6 articles x 3 visuals might hit rate limits. Implementation must include pauses or batching.
- **Content Parsing**: Automated insertion into established markdown files must be cautious not to break structure.

## Next Steps
1. Create `13-01-PLAN.md` for `visual.py` updates.
2. Create `13-02-PLAN.md` for `image.py` updates.
