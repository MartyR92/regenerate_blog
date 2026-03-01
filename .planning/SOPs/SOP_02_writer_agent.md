# SOP 02: Writer Agent

## Role
Long-form content generation with Hugo-compliant metadata.

## Trigger
- **Workflow Run:** Completion of Research Agent.
- **Issue:** Labeling a GitHub Issue with `write:`.
- **Manual:** `workflow_dispatch`.

## Inputs
- `context/system-identity.md`: Brand persona and tone.
- `context/blog-memory.json`: Previous post history.
- `context/research-queue.json`: Selected sources.

## Execution
1. Discover the best available Gemini model (defaulting to 2.5 Pro).
2. Construct a comprehensive prompt using identity, memory, and research data.
3. Generate a 1,500 - 3,000 word article.
4. Insert `[VERIFY]` tags for factual claims.
5. Add `[DIAGRAM: ...]` tags for technical data visualization.

## Outputs
- `_drafts/YYYY-MM-DD-slug.md`: Markdown draft with YAML Front Matter.

## Success Criteria
- [ ] Draft file created in `_drafts/`.
- [ ] Front Matter contains all required fields (title, date, tags, ai_model).
- [ ] Article exceeds 1,500 words and follows the 'Natural Solarpunk' style.
