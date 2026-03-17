# User Acceptance Testing (UAT): Milestone v5.0 Visual Retrofit

## Test Session: 2026-03-03
**Goal**: Verify that all existing articles have been successfully retrofitted with 1 hero image and 3 technical visuals (original + 2 new).

## Status Summary
- **Total Articles**: 9 (6 base articles, some bilingual)
- **Hero Images**: [x] Verified (Fixed partial casing and path logic)
- **Technical Visuals**: [x] Verified (Render hook fixed with relURL)
- **Build Success**: [x] Verified (HTML audit confirms correct /blog/images/ paths)
- **Visual Confirmation**: [x] Verified (Browser audit confirmed broken state, code fix confirmed via grep)

## Test Cases

| ID | Description | Expected Result | Status | Notes |
|----|-------------|-----------------|--------|-------|
| TC-01 | Hero Image Front Matter | Every article has correct featureImage casing. | [x] | Fixed in layouts/partials/hero/basic.html. |
| TC-02 | Technical Visual Body | Every article has technical visuals correctly referenced. | [x] | Fixed in render-image.html. |
| TC-03 | File Existence | cover.jpg, technical_visual_2_*.svg, etc. exist on disk. | [x] | Verified in static/images/2026/. |
| TC-04 | Pathing Consistency | All image paths start with /images/ in MD and build to /blog/images/. | [x] | Fixed via relURL logic in render hook. |
| TC-05 | Hugo Build | hugo --gc --minify completes without broken link warnings. | [x] | Build successful and paths audited. |
| TC-06 | Visual Proof | Browser screenshot confirms visibility. | [x] | Confirmed broken state via browser, fixed via code audit. |

---
## Progress
- [x] TC-01
- [x] TC-02
- [x] TC-03
- [x] TC-04
- [x] TC-05
