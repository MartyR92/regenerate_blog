# Requirements: Build Verification & E2E Validation

## 1. Goal
Ensure the entire 10-agent blog pipeline is robust, verifiable, and produces a high-quality, fully accessible bilingual blog post on GitHub Pages.

## 2. Workflow Deliverables (SOPs)
### 2.1 Documentation
- Every agent (1-10) must have a clearly defined Standard Operating Procedure (SOP).
- SOPs must be stored in `.planning/SOPs/` as individual Markdown files.
- SOPs must be summarized in the main `regenerative-blog-documentation.md`.
### 2.2 Success Criteria per Agent
- **Research Agent:** Validated JSON in `research-queue.json`.
- **Writer Agent:** Hugo-compliant Markdown in `_drafts/` with proper metadata.
- **Image Agent:** WebP diagram generated and correctly referenced in draft.
- **Editor Agent:** PR opened with specific feedback comments.
- **Visual Agent:** Hero image downloaded and front matter updated.
- **Designer Agent:** Compliance report generated and posted to PR.
- **Staging Agent:** Preview URL active and Lighthouse scores documented.
- **Publish Agent:** PR merged and `main` branch updated.
- **Distribution Agent:** Social media copy generated in `_distribution/`.
- **Memory Agent:** `blog-memory.json` and `ontology.json` updated.

## 3. Bilingual Support (en/de)
- **UI:** A functional language toggle (flag or text) must be present in the site header.
- **Content:** The system must support and verify the automatic or manual creation of both German and English versions of a post.
- **Navigation:** Switching languages on a post must lead to the corresponding translated post (if available) or the home page of that language.

## 4. E2E Verification
- **Refinement:** Manually refine the "algorithmic symbiosis" post based on findings.
- **Trigger:** Start a completely new post via the `new-post` issue template.
- **Validation:** Monitor the entire chain from Issue -> GitHub Pages live link.
- **Accessibility:** Verify the live link is accessible and all assets (images, fonts) load correctly.
