# SOP 09: Distribution Agent

## Role
Creation of platform-specific promotional copy.

## Trigger
- **Workflow Run:** Completion of the Publish Agent.

## Inputs
- The published Markdown article.
- System Identity (for platform-specific tone).

## Execution
1. Read the final version of the post.
2. Generate Mastodon copy (max 500 chars, academic/factual).
3. Generate LinkedIn copy (narrative, emphasis on ROI/Impact).
4. Generate a Newsletter teaser (curiosity-driven).
5. Format the output as a Markdown file.

## Outputs
- `_distribution/YYYY-MM-DD-slug.md`: Promotional text for manual copy-pasting.

## Success Criteria
- [ ] Distribution file is created.
- [ ] At least 3 platform-specific text versions are provided.
- [ ] Tone matches the specific social platform requirements.
