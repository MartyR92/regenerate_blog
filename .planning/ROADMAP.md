# Roadmap: Visual Integrity & Bilingual Content Parity

## Phase 8: Diagram Rendering & Language Fixes
- [x] **Task 8.1: Debug SVG/WebP Logic**
    - Investigate why diagrams are failing to render (path issue vs. file format).
- [x] **Task 8.2: Implement Language-Aware Image Descriptions**
    - Update `scripts/image.py` to detect post language and translate captions.
    - Remove "agent-specific" mentions from captions.

## Phase 9: Mandatory Bilingual Core
- [x] **Task 9.1: Refactor `scripts/writer.py` for DE+EN Pairs**
    - Implement a two-pass generation or translation pass to ensure identical content in both languages.
- [x] **Task 9.2: Update System Prompts for Bilingual Content**
    - Refine `writer-v1.md` to enforce exact semantic parity between translations.

## Phase 10: Content Cleanup & E2E Validation
- [ ] **Task 10.1: Repair Low-Quality German Articles**
    - Delete or replace the "poorly written" 400-word and 0-byte placeholders with high-quality pairs.
- [ ] **Task 10.2: E2E Verification Run**
    - Trigger a new post generation.
    - Verify that both DE and EN files are created, diagrams are functional, and descriptions are localized.
- [ ] **Task 10.3: Final Site Audit**
    - Verify the live blog on GitHub Pages.
