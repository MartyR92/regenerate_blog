# Plan: Phase 10 - Content Cleanup & E2E Validation

## 1. Content Purge
- [ ] Delete `content/de/posts/2026-02-28-die-symbiose-des-überflusses-wie-präzisionsagrartechnologie-die-regenerative-ökonomie-katalysiert.md`.
- [ ] Delete `content/de/posts/hello-world.md`.
- [ ] Delete `content/en/posts/hello-world.md`.

## 2. Deploy Refined Bilingual Pair
- [ ] Move `_drafts/2026-03-02-praezision-im-feld-*.de.md` to `content/de/posts/`.
- [ ] Move `_drafts/2026-03-02-praezision-im-feld-*.en.md` to `content/en/posts/`.
- [ ] Commit and Push these changes to `main`.

## 3. Mandatory E2E Pipeline Verification
- [ ] Create a GitHub Issue with the `write:` label.
- [ ] **Title:** `[POST] Mycelial Networks: The Biological Internet of the Regenerative Economy`
- [ ] **Body:** Request `de+en` versions with a focus on "Living Systems" and "Mycology".
- [ ] Verify that the pipeline produces:
    - A German post in `_drafts/`.
    - An English post in `_drafts/`.
    - Localized technical diagrams for both.
    - A Designer Agent audit in the PR.

## 4. Live Site Final Audit
- [ ] Visit `https://martyr92.github.io/regenerate_blog/`.
- [ ] Confirm the homepage looks professional (Background/Card layout).
- [ ] Test the language toggle on the "Precision in the Field" post.
- [ ] Ensure the SVG diagram is visible and the caption is localized.

## 5. Verification
- [ ] All 10 agents confirmed as functional and SOP-compliant.
- [ ] Site contains only high-quality, bilingual content.
