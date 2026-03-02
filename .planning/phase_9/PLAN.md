# Plan: Phase 9 - Mandatory Bilingual Core

## 1. Update System Prompt (`context/agent-prompts/writer-v1.md`)
- [ ] Add instructions for "Translation Pass" mode.
- [ ] Mandate the inclusion of `language` key in Front Matter.
- [ ] Define tone preservation rules for English (maintaining 'Avantgarde Prestige').

## 2. Refactor Writer Script (`scripts/writer.py`)
- [ ] **Dual-Generation Logic:**
    - Step 1: Generate German article based on research.
    - Step 2: Generate English article based on the German article output.
- [ ] **Path Management:**
    - Derive a single `slug` from the German title.
    - Save DE to `content/de/posts/{slug}.md`.
    - Save EN to `content/en/posts/{slug}.md`.
    - *Note:* Since the agents work in `_drafts/`, the initial pair should be saved to `_drafts/de/{slug}.md` and `_drafts/en/{slug}.md` or similar, but since the current pipeline expects files in `_drafts/`, I might need to adjust the directory structure of drafts or the publish script.
    - *Decision:* Save as `{slug}.de.md` and `{slug}.en.md` in `_drafts/`, then let the publish script move them to the correct `content/` subfolder.

## 3. Workflow Updates (Optional)
- [ ] Verify if `editor-agent.yml` and `visual-agent.yml` can handle multiple files in a single push. (They already use `_drafts/**` globs, so it should work).

## 4. Verification
- [ ] Run `scripts/writer.py` locally.
- [ ] Verify that two files are created with identical slugs.
- [ ] Check that Front Matter contains `language: de` and `language: en`.
