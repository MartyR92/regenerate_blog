# SOP 05: Visual Agent

## Role
Artistic image sourcing and automated attribution.

## Trigger
- **Workflow Run:** PR creation by Editor Agent.
- **Manual:** `workflow_dispatch`.

## Inputs
- `_drafts/latest.md`: The article draft.
- Unsplash API: For stock photos.
- Gemini API: For search query generation and alt-texts.

## Execution
1. Ask Gemini for an Unsplash search query based on post content.
2. Search Unsplash for high-quality, landscape-oriented images.
3. Download image to `assets/images/YYYY/slug/cover.jpg`.
4. Generate descriptive alt-text using Gemini.
5. Update Hugo Front Matter with `featureImage` and `featureImageAlt`.
6. Append photographer attribution to the end of the post.

## Outputs
- `assets/images/YYYY/slug/cover.jpg`: Hero image asset.
- Updated Markdown file in `_drafts/`.

## Success Criteria
- [ ] Cover image exists in the correct asset folder.
- [ ] Front Matter includes correctly formatted image parameters.
- [ ] Attribution is present at the end of the article.
