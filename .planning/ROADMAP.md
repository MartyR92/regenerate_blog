# ROADMAP: Milestone v5.0 Visual Retrofit & Enrichment

## Phases
- [ ] **Phase 13: Agent Infrastructure for Retrofit** - Update `visual.py` and `image.py` to support multi-article processing and multi-visual generation.
- [ ] **Phase 14: Retrofit Execution & Validation** - Execute the retrofit on all 6 articles and verify rendering.

## Phase Details

### Phase 13: Agent Infrastructure for Retrofit
**Goal**: Agents are equipped to handle the visual enrichment of the entire archive.
**Depends on**: Milestone v4.0
**Requirements**: RET-01, RET-02, RET-03
**Success Criteria**:
  1. `visual.py` successfully identifies and processes all content files.
  2. `image.py` can generate a "chart" and a "diagram" based on specific instructions.
  3. `image.py` ensures WebP fallbacks are created for all new SVGs.
**Plans**: 2 plans
- [ ] 13-01-PLAN.md — Update `visual.py` for archive processing.
- [ ] 13-02-PLAN.md — Update `image.py` for multi-visual generation.

### Phase 14: Retrofit Execution & Validation
**Goal**: All existing articles meet the 3-visual standard.
**Depends on**: Phase 13
**Requirements**: VIS-03, VIS-04, VIS-05, VIS-06, RET-04, RET-05
**Success Criteria**:
  1. All 6 articles have a valid `featureImage` in front matter.
  2. All 6 articles have 3 working technical visuals in the body.
  3. All visuals render correctly in the Hugo preview with WebP fallbacks.
**Plans**: 1 plan
- [ ] 14-01-PLAN.md — Execute retrofit task and verify.

## Progress

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 13. Agent Infrastructure for Retrofit | 2/2 | Completed | 2026-03-03 |
| 14. Retrofit Execution & Validation | 1/1 | Completed | 2026-03-03 |
