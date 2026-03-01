# SOP 10: Memory Agent

## Role
Long-term context maintenance and knowledge persistence.

## Trigger
- **Workflow Run:** Completion of the Publish Agent.

## Inputs
- Final post slug and metadata.
- `context/blog-memory.json`: Post history.
- `context/series-registry.json`: Open series status.
- `context/ontology.json`: Tags and domains.

## Execution
1. Update `blog-memory.json` with the new post details (prepend to list).
2. Update the status of any ongoing series in `series-registry.json`.
3. Check for new tags and add them to the `proposed_tags` section of `ontology.json`.
4. Mark used items in `research-queue.json` as `used: true`.
5. Commit and push updated context files.

## Outputs
- Updated JSON context files in `context/`.

## Success Criteria
- [ ] `blog-memory.json` includes the latest post.
- [ ] `ontology.json` correctly reflects new tags.
- [ ] Context changes are committed back to the repository.
