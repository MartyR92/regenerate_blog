# User Acceptance Testing (UAT): Milestone v5.0 Visual Retrofit

## Test Session: 2026-03-03
**Goal**: Verify that all existing articles have been successfully retrofitted with 1 hero image and 3 technical visuals (original + 2 new).

## Status Summary
- **Total Articles**: 9 (6 base articles, some bilingual)
- **Hero Images**: [x] Verified (All have `featureImage`)
- **Technical Visuals**: [x] Verified (3 per article)
- **Build Success**: [x] Verified (`hugo` success)

## Test Cases

| ID | Description | Expected Result | Status | Notes |
|----|-------------|-----------------|--------|-------|
| TC-01 | Hero Image Front Matter | Every article has `featureImage: "/blog/images/2026/.../cover.jpg"`. | [x] | Verified via grep. |
| TC-02 | Technical Visual Body | Every article has `technical_visual_2` and `technical_visual_3` referenced. | [x] | Verified via grep. |
| TC-03 | File Existence | `cover.jpg`, `technical_visual_2_*.svg`, and `technical_visual_3_*.svg` exist on disk. | [x] | Verified via ls -R. Some duplicates due to fallback. |
| TC-04 | Pathing Consistency | All image paths start with `/blog/images/`. | [x] | Verified in markdown files. |
| TC-05 | Hugo Build | `hugo --gc --minify` completes without broken link warnings. | [x] | Build successful. |

---
## Progress
- [x] TC-01
- [x] TC-02
- [x] TC-03
- [x] TC-04
- [x] TC-05
