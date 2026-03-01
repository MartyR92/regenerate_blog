# Plan: Phase 6 - E2E Verification & Refinement

## 1. Refinement of "Algorithmic Symbiosis"
- [ ] Edit `content/de/posts/2026-02-26-algorithmische-symbiose-...md`:
    - Insert `[DIAGRAM: Myzel-Netzwerk von Kapital und Wissen Flowchart]` at line 100.
    - Insert `[DIAGRAM: Vergleich Ernteerträge vs. Ressourceneffizienz Balkendiagramm]` at line 130.
- [ ] Move the refined file back to `_drafts/` to trigger a "re-run" of the pipeline (Editor -> Visual -> Staging).

## 2. Trigger E2E Run for a New Post
- [ ] Construct a `gh issue create` command:
    - **Title:** `[POST] Tokenomics of Soil: Integrating Carbon Credits into ReFi`
    - **Label:** `write:`
    - **Body:** Follow the `new-post.yml` structure (Angle, Sources, Language: `de+en`).
- [ ] Monitor GitHub Actions (via `gh run list`).

## 3. Implementation of en/de Switch Validation
- [ ] Once the `Staging Agent` opens a PR for the new post:
    - Review the **Designer Agent Audit** in the PR comment.
    - Specifically verify that the language switcher is detected/validated.

## 4. Final Deployment Audit
- [ ] After merging the PR:
    - Use `dev-browser` to visit `https://martyr92.github.io/regenerate_blog/`.
    - Click the language flag/toggle.
    - Verify that the technical diagrams are rendered correctly in the new post.

## 5. Verification
- [ ] Live link is working and bilingual.
- [ ] SOPs are confirmed as "passed" by the build results.
