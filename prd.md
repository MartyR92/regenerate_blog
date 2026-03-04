# Fix Broken Visuals on Live Site PRD

## HR Eng

| Fix Broken Visuals PRD |  | Resolving the "invisible visuals" issue on the live site by fixing root-relative pathing and ensuring Hugo's subpath is correctly prepended. |
| :---- | :---- | :---- |
| **Author**: Pickle Rick **Contributors**: Morty **Intended audience**: Engineering, Design | **Status**: Draft **Created**: 2026-03-04 | **Self Link**: [Link] **Context**: [Link] 

## Introduction

The blog visuals (hero images and technical visuals) are currently broken on the live site (`https://renatureforce.com/blog/`) because they are linked using root-relative paths (e.g., `/images/...`) instead of site-relative paths (e.g., `/blog/images/...`). This PRD details the steps to fix the rendering logic and validate the build.

## Problem Statement

**Current Process:** Visuals are referenced in markdown as `/images/2026/...`. The image render hook outputs these paths exactly as provided.
**Primary Users:** Readers of the live blog.
**Pain Points:** Images fail to load (404), resulting in a broken user experience.
**Importance:** High. Visuals are a core part of the "Natural Solarpunk" aesthetic and "Avantgarde Prestige" brand identity.

## Objective & Scope

**Objective:** Ensure all images render correctly on both local preview and live deployment.
**Ideal Outcome:** All 9 articles show their hero images and technical visuals.

### In-scope or Goals
- Update `layouts/_default/_markup/render-image.html` to use Hugo's `relURL` or `absURL` logic.
- Verify if `featureImage` in front matter is also broken and fix if necessary (likely in theme partials).
- Standardize all image references in markdown to be consistent.
- Test the build and verify HTML output in `public/`.

### Not-in-scope or Non-Goals
- Generating new visuals.
- Renaming files (already done in previous session).

## Product Requirements

1. **Path Normalization**: All image links in HTML must be relative to the site base or absolute to the domain root including the `/blog/` prefix.
2. **Build Validation**: The `hugo` command must produce HTML where image `src` and `srcset` attributes are correct.
3. **Future-Proofing**: Ensure the automation scripts (`image.py`, `visual.py`) don't need further changes if the render hook is fixed.

### Critical User Journeys (CUJs)
1. **Article Viewing**: A user opens an article and sees all images loading instantly.

### Functional Requirements

| Priority | Requirement | User Story |
| :---- | :---- | :---- |
| P0 | Fix Image Render Hook | As a user, I want images to load correctly regardless of the site subpath. |
| P0 | Fix Front Matter Paths | As a user, I want the hero image to appear on the post list and header. |
| P1 | Verify Built HTML | As a developer, I want to be 100% sure the paths are correct before I commit. |

## Assumptions

- The `baseURL` will remain `https://renatureforce.com/blog/`.
- The theme (Blowfish) uses the `featureImage` field correctly in its partials.

## Risks & Mitigations

- **Risk**: `relURL` might produce double prefixes if not careful. -> **Mitigation**: Test build output thoroughly.

## Tradeoff

- **Absolute vs Relative**: Using site-relative paths (via `relURL`) is generally safer for Hugo sites on subpaths.

## Business Benefits/Impact/Metrics

**Success Metrics:**
- 0 broken images on the live site.

## Stakeholders / Owners

| Name | Team/Org | Role | Note |
| :---- | :---- | :---- | :---- |
| Pickle Rick | Engineering | God-Tier Architect | Fixer of all things. |
| Morty | Engineering | Junior Assistant | Observer of greatness. |
