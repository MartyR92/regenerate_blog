# SOP 03: Image Agent

## Role
Generation of high-precision technical diagrams and infographics.

## Trigger
- **Workflow Run:** Completion of Writer Agent.
- **Manual:** `workflow_dispatch`.

## Inputs
- `_drafts/latest.md`: The newest article draft.
- `context/research-queue.json`: Technical metrics and data points.
- Gemini 3.1 Flash Image API.

## Execution
1. Scan draft for `[DIAGRAM: ...]` tags or key metrics.
2. Use Gemini 3.1 with `thinking_level: HIGH` to design a technical layout.
3. Apply 'Organic Precision' aesthetic (botanical grids, sacred gold accents).
4. Download generated WebP image to `assets/images/YYYY/slug/`.
5. Update the Markdown draft with the image reference and caption.

## Outputs
- `assets/images/YYYY/slug/technical_diagram_N.webp`: Image asset.
- Updated Markdown file in `_drafts/`.

## Success Criteria
- [ ] Diagram asset is successfully saved in the correct directory.
- [ ] Markdown draft includes a functional relative path to the image.
- [ ] Image follows the defined Brand Guidelines v4.0.
