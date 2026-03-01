# Research: Image & Designer Agent Core Logic

## 1. Gemini 3.1 Flash Image Preview (Nano Banana 2)
### Technical Capabilities
- **Model ID:** `models/gemini-3.1-flash-image-preview`
- **Optimal Modality:** High-precision text rendering and technical diagramming.
- **Thinking Level:** Setting `thinking_level: "HIGH"` enables spatial reasoning for node/connector placement.
- **Resolution:** Supports up to 4K (4096x4096).
- **Text Accuracy:** ~94% for rendered labels.

### Implementation Strategy (Python)
- Use the `google-genai` library or the REST API (consistent with existing scripts).
- Modality must include `IMAGE` in `response_modalities`.
- Diagrams should be prompted with specific label lists and "clean vector style" or "Organic Precision" descriptors.

## 2. Agent Positioning & Data Flow
### Existing Pipeline
1. `research.py` -> `context/research-queue.json`
2. `writer.py` -> `_drafts/YYYY-MM-DD-slug.md`
3. `visual.py` -> Adds hero image to `_drafts/` post.

### Proposed New Flow
1. `writer.py` (Draft Text)
2. **`image.py`** (Technical Visuals)
   - Reads `_drafts/latest.md` and `research-queue.json`.
   - Identifies data points (e.g., ROI percentages, growth rates).
   - Generates diagrams using Gemini 3.1.
   - Appends/Inserts image markdown into the post.
3. `editor.py` (Review)
4. `visual.py` (Hero Visuals)
5. **`designer.py`** (Validation)
   - Runs during `staging-agent.yml`.
   - Validates Front Matter (typography, color ratios) and layout.

## 3. Brand Guidelines Consistency
### "Organic Precision" (Micro)
- **Palette:** `#0F1A15` (Void), `#2C3330` (Slate), `#C5B388` (Brass).
- **Typography:** EB Garamond, Inter, JetBrains Mono (Data).
- **Geometry:** 1-2px border radius, Fibonacci spacing (8, 13, 21, 34, 55...).
- **Patterns:** Botanical radial grids (not square).

### "Terrain Depth" (Macro)
- **Palette:** `#F5EFE0` (Cream), `#1A3D2B` (Forest), `#B8912A` (Gold).
- **Typography:** Fraunces, Syne, Inter.
- **Geometry:** 4px max border radius, layered color fields.

## 4. Automation & Scripts
- **`scripts/image.py`**: Needs to handle image downloading, path generation (`assets/images/YYYY/slug/diagram_N.webp`), and Markdown insertion.
- **`scripts/designer.py`**: Needs a rule-based engine to check Hugo Front Matter strings and potentially scan the rendered HTML/Markdown for Brand Guideline violations.
