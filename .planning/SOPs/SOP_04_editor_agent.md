# SOP 04: Editor Agent

## Role
Editorial review and consistency check.

## Trigger
- **Push:** New or updated file in `_drafts/`.
- **Manual:** `workflow_dispatch`.

## Inputs
- `_drafts/*.md`: The article draft.
- `context/system-identity.md`: For tone verification.
- `context/ontology.json`: For tag validation.

## Execution
1. Perform tone and consistency checks against brand persona.
2. Identify all `[VERIFY]` tags and provide guidance for factual verification.
3. Validate metadata (Front Matter) and categories.
4. Create a Pull Request (PR) from `editor/` branch to `main`.
5. Add review comments directly to the PR.

## Outputs
- GitHub Pull Request.
- PR Inline Comments.

## Success Criteria
- [ ] PR is successfully opened with the `editor-review` label.
- [ ] At least one editorial comment is provided.
- [ ] Tone aligns with the 'Regenerative Avantgarde'.
