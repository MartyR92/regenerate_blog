# Requirements: Milestone v5.0 Visual Retrofit & Enrichment

## 1. Visual Standards
- **VIS-03**: Every article MUST have 1 hero image fetched from Unsplash.
- **VIS-04**: Every article MUST have 3 technical visuals: 1 existing diagram (kept), 1 new diagram, and 1 new chart.
- **VIS-05**: All new technical visuals MUST follow the "Organic Precision" aesthetic and have WebP fallbacks.
- **VIS-06**: All visuals MUST use root-relative paths (`/blog/images/...`) for deployment compatibility.

## 2. Agent Enhancements
- **RET-01**: `visual.py` must be capable of processing all articles in `content/de/posts` and `content/en/posts`.
- **RET-02**: `image.py` must be capable of generating a specific mix of visuals (1 chart + 1 diagram) per article.
- **RET-03**: `image.py` must correctly detect existing visuals to avoid duplicates and ensure placement is logical.

## 3. Automation & Deployment
- **RET-04**: The retrofit must be executable as a standalone task.
- **RET-05**: Updated visuals must be automatically staged and committed to the repository.
