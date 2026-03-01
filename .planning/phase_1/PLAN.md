# Plan: Phase 1 - Core Logic & Scripting

## 1. Environment Setup
- [ ] Verify `google-genai` and `requests` are available in the GitHub Actions environment (already implied by existing scripts, but `google-genai` might need adding to a `requirements.txt` if it exists).
- [ ] Check if `requirements.txt` exists.

## 2. Image Agent (`scripts/image.py`)
- [ ] **Data Extraction:**
    - Parse `context/research-queue.json` for technical metrics.
    - Identify the latest post in `_drafts/`.
- [ ] **Prompt Engineering:**
    - Construct a prompt for `gemini-3.1-flash-image-preview` that includes:
        - "Organic Precision" or "Terrain Depth" style guides.
        - High `thinking_level`.
        - Specific data labels and diagram type (Flowchart, Mycelium Network, etc.).
- [ ] **Execution & Integration:**
    - Call Gemini API.
    - Download generated image to `assets/images/YYYY/slug/diagram_N.webp`.
    - Insert `![Caption](/images/YYYY/slug/diagram_N.webp)` into the Markdown file.

## 3. Designer Agent (`scripts/designer.py`)
- [ ] **Rule Implementation:**
    - Create a Python class/function to validate:
        - Font pairings in Front Matter.
        - 60/30/10 color ratios (if defined in Front Matter).
        - Fibonacci spacing in layout shortcodes.
- [ ] **Integration:**
    - Script should output a JSON or Markdown report for the GitHub Action to consume.

## 4. Prompt Engineering (`context/agent-prompts/`)
- [ ] Create `context/agent-prompts/image-v1.md`.
- [ ] Create `context/agent-prompts/designer-v1.md`.

## 5. Verification
- [ ] Local syntax check of Python scripts.
- [ ] Verify file path logic for image storage.
