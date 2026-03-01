# Plan: Phase 2 - Pipeline & Workflow Automation

## 1. Create Image Agent Workflow
- [ ] Create `.github/workflows/image-agent.yml`.
- [ ] Configure `on: workflow_run` for "Writer Agent".
- [ ] Steps:
    - Checkout repo.
    - Setup Python 3.11.
    - Install `requests`.
    - Run `python scripts/image.py` with `GEMINI_API_KEY`.
    - Git commit and push changes to `_drafts/` and `assets/images/`.
- [ ] **Verification:** Ensure it triggers only on `success` of the Writer Agent.

## 2. Integrate Designer Agent into Staging
- [ ] Modify `.github/workflows/staging-agent.yml`.
- [ ] **Step 2.1: Run Audit**
    - Insert a step after "Prepare Drafts for Preview".
    - Run `python scripts/designer.py`.
    - Upload `design_report.md` as an artifact (optional but good for debugging) or read it in the next step.
- [ ] **Step 2.2: Update PR Comment**
    - Modify the `Post PR Comment` step (github-script).
    - Read the content of `design_report.md`.
    - Append it to the `commentBody`.

## 3. General Workflow Hardening
- [ ] Verify permissions (`contents: write`, `pull-requests: write`) for all modified workflows.
- [ ] Check for model ID consistency (`gemini-3.1-flash-image-preview` vs what's in `image.py`).

## 4. Verification
- [ ] Validate YAML syntax for both files.
- [ ] Dry run logic check (ensuring `image-agent` push triggers `editor-agent`).
