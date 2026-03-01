# Research: Phase 5 - Workflow Deliverables & SOPs

## 1. Pipeline Analysis
The current 10-agent pipeline is structured as follows:

| # | Agent | Input | Deliverable (Output) | Success Criteria |
|---|---|---|---|---|
| 1 | Research | Ontology | `research-queue.json` | Valid JSON with relevance score > 0 |
| 2 | Writer | Research | `_drafts/*.md` | Front matter present, length > 1500 words |
| 3 | Image | Draft/Data | `assets/images/.../diagram.webp` | Image exists, Markdown reference added |
| 4 | Editor | Draft | GitHub PR + Comments | PR created, [VERIFY] tags reviewed |
| 5 | Visual | Draft | `cover.jpg` + Alt Text | Image downloaded, Front Matter updated |
| 6 | Designer | Draft/HTML | `design_report.md` in PR | Fibonacci and brand rules validated |
| 7 | Staging | Drafts | Live Preview URL | Build successful, Lighthouse score > 80 |
| 8 | Publish | PR | Production Site Live | Main branch updated, GPages deployed |
| 9 | Distribution| Published Post| `_distribution/*.md` | Text for 3+ platforms generated |
| 10| Memory | Post Metadata | Updated `blog-memory.json` | Slug added to history, tags updated |

## 2. SOP Template Structure
Each SOP should contain:
- **Title:** Agent Name
- **Role:** High-level purpose.
- **Trigger:** When it runs.
- **Inputs:** Data it consumes.
- **Execution:** Step-by-step logic.
- **Outputs:** Specific files or actions.
- **Success Criteria:** Definition of Done.

## 3. Findings
- Currently, documentation is high-level but lacks the specific "Success Criteria" per agent that the user requested.
- The `Image Agent` and `Designer Agent` are recently added and need their SOPs strictly aligned with the brand guidelines.
- The `Designer Agent` must explicitly check for the "en/de" switch existence in the final build during Phase 6.
