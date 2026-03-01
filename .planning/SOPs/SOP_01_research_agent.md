# SOP 01: Research Agent

## Role
Automated information sourcing and synthesis for the regenerative economy niche.

## Trigger
- **Schedule:** Monday and Thursday at 06:00 UTC.
- **Manual:** `workflow_dispatch` in GitHub Actions.

## Inputs
- `context/ontology.json`: Domain definitions and tags.
- Serper.dev API: For web search.
- OpenAlex API: For academic sources.

## Execution
1. Pick a random domain/tag from the ontology.
2. Query APIs for latest developments.
3. Use Gemini (or Inception fallback) to analyze and summarize findings.
4. Filter for sources with verifiable IDs (DOI, URL).

## Outputs
- `context/research-queue.json`: Updated list of research items.

## Success Criteria
- [ ] `research-queue.json` contains valid JSON.
- [ ] At least one new item with `relevance_score > 0` is appended.
- [ ] Sources are clearly listed for each item.
