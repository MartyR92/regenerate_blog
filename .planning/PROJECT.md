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

### Milestone 3: Build Verification & E2E Validation
- [x] Define and document SOPs for all 10 agents.
- [x] Implement en/de language toggle in the header.
- [x] Refine the latest post and conduct E2E verification by triggering a new one.
- [x] Verify link accessibility and full feature integration on GitHub Pages.

### Milestone v5.0: Visual Retrofit & Enrichment
**Goal:** Retrofit all 6 existing articles with a complete visual set (1 Unsplash hero image, 1 existing technical diagram, and 2 new technical visuals - 1 chart and 1 diagram).

**Target features:**
- Enhance `visual.py` to retrofit all existing articles with Unsplash hero images.
- Enhance `image.py` to generate multiple technical visuals (1 chart, 1 diagram) per article with WebP fallbacks.
- Implement a one-time automated retrofit task to ensure all 6 articles meet the "3 visuals" standard.
