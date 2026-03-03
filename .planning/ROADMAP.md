# ROADMAP: Milestone v4.0 Visuals Fixes & Deep Research

## Phases
- [x] **Phase 11: Visual Infrastructure & Rendering** - Fix visual rendering on the live blog and ensure API access for image agents.
- [x] **Phase 12: Deep Research & Citations** - Implement verifiable citations and quotes powered by Interactions API.

## Phase Details

### Phase 11: Visual Infrastructure & Rendering
**Goal**: Users experience flawlessly rendered visuals and agents have proper API access for future capability.
**Depends on**: None
**Requirements**: VIS-01, VIS-02
**Success Criteria**:
  1. User can view all diagrams, graphs, and images correctly rendered on the live blog without broken paths.
  2. The automated pipeline successfully generates images without permission errors regarding the Interactions API.
  3. Users can inspect SVG/WebP visuals clearly across different viewport sizes.
**Plans**: 2 plans
- [x] 11-01-PLAN.md — Update CI/CD pipelines and generate WebP fallbacks
- [x] 11-02-PLAN.md — Implement custom Hugo picture render hook

### Phase 12: Deep Research & Citations
**Goal**: Users can read blog posts with verifiable facts, evident citations, and quotes sourced via deep research.
**Depends on**: Phase 11
**Requirements**: RES-01, RES-02
**Success Criteria**:
  1. User can see explicit citations and source quotes integrated naturally within the blog post content.
  2. User can click or reference the provided citations to verify factual claims made in the articles.
  3. The automated pipeline successfully produces heavily researched articles utilizing the Interactions API for deep searching.
**Plans**: 1 plan
- [x] 12-01-PLAN.md — Enhance research agent and writer prompt for citations

## Progress

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 11. Visual Infrastructure & Rendering | 2/2 | Completed | 2026-03-03 |
| 12. Deep Research & Citations | 1/1 | Completed | 2026-03-03 |