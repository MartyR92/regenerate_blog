# Regenerative Economy Blog: Automated Agent Pipeline

## Vision
A fully automated, GitHub-hosted blog for the "Regenerative Economy" niche, combining Natural Solarpunk aesthetics with Avantgarde Prestige. The system is designed to run on low-resource hardware (Intel Celeron, 512MB RAM) by offloading processing to GitHub Actions and Gemini API.

## Technical Stack
- **Framework:** Hugo (Blowfish Theme)
- **CI/CD:** GitHub Actions
- **AI Models:** Gemini 1.5 Pro, Gemini 1.5 Flash, Gemini Imagen
- **Infrastructure:** GitHub Pages, Unsplash API, Serper.dev

## Agent Architecture (Existing)
1. **research-agent:** Sources information from academic/web sources.
2. **writer-agent:** Generates long-form content and Hugo metadata.
3. **image-agent:** Generates technical diagrams/infographics.
4. **editor-agent:** Performs consistency checks and editorial review.
5. **visual-agent:** Generates hero and inline images.
6. **designer-agent:** Validates brand compliance.
7. **staging-agent:** Previews content and runs audits.
8. **publish-agent:** Merges and deploys to production.
9. **distribution-agent:** Creates social media teasers.
10. **memory-agent:** Updates the system's long-term memory and ontology.

## Milestones History
### Milestone 1: Core Pipeline Setup
- [x] Repository structure and Hugo initialization.
- [x] Implementation of the 8 core agents.
- [x] Automated deployment to GitHub Pages.
- [x] Context management (blog-memory, ontology).

### Milestone 2: Image & Designer Agent Integration
- [x] Specialized technical data-viz agent (`image-agent`).
- [x] Brand & Compliance guardian agent (`designer-agent`).
- [x] Pipeline extension to 10 agents.
- [x] Full documentation and system prompt updates.

## Current Milestone: Build Verification & E2E Validation
**Objective:** Test and verify the 10-agent build process, implement the missing language switch, and ensure a fully functional deployment on GitHub Pages.
- [ ] Define and document SOPs for all 10 agents.
- [ ] Implement en/de language toggle in the header.
- [ ] Refine the latest post and conduct E2E verification by triggering a new one.
- [ ] Verify link accessibility and full feature integration on GitHub Pages.
