# Fix Invisible Visuals PRD

## HR Eng

| Fix Invisible Visuals PRD |  | Addressing the "invisible visuals" problem caused by redundant path prefixes and encoding-sensitive folder names in the blog archive. |
| :---- | :---- | :---- |
| **Author**: Pickle Rick **Contributors**: Morty **Intended audience**: Engineering, Design | **Status**: Draft **Created**: 2026-03-04 | **Self Link**: [Link] **Context**: [Link] 

## Introduction

The current blog archive features "invisible visuals" due to a combination of redundant path prefixes (`/blog/blog/`) and encoding issues with folder names on the live site. This PRD outlines the steps to normalize these paths and folder names for deployment-readiness.

## Problem Statement

**Current Process:** Visuals are retrofitted using `scripts/visual.py` and `scripts/image.py` using root-relative paths like `/blog/images/...`.
**Primary Users:** Readers of the RenatureForce blog.
**Pain Points:** Images do not load on the live site, resulting in a broken visual experience.
**Importance:** Visuals are a core part of the "Natural Solarpunk" aesthetic. A blog without its visuals is like a Morty without his stammer—pointless.

## Objective & Scope

**Objective:** Ensure all hero and technical visuals are correctly rendered on the live site.
**Ideal Outcome:** All 9 articles display their 1 hero image and 3 technical visuals correctly.

### In-scope or Goals
- Fix the redundant `/blog/` prefix in `featureImage` and body markdown references.
- Sanitize image folder names to remove non-ASCII characters that cause issues with Hugo and some web servers.
- Update `scripts/image.py` and `scripts/visual.py` to use relative paths or correct site-relative paths.

### Not-in-scope or Non-Goals
- Generating new visuals (the ones we have are fine, they just aren't visible).

## Product Requirements

1. **Path Correction**: All `featureImage` and body image paths must be updated from `/blog/images/...` to `/images/...` or correct relative paths, depending on the final deployment structure.
2. **Folder Sanitization**: Rename all folders in `static/images/2026/` to use slug-safe, ASCII-only names.
3. **Agent Retrofit**: Update the generation scripts to ensure future visuals are created with the correct pathing and naming conventions.

### Critical User Journeys (CUJs)
1. **Visual Load**: A user visits a blog post and immediately sees the high-quality hero image and technical visuals.

### Functional Requirements

| Priority | Requirement | User Story |
| :---- | :---- | :---- |
| P0 | Fix Image Path Prefix | As a user, I want the images to load correctly so the blog isn't ugly. |
| P0 | Sanitize Folder Names | As a developer, I want my folder names to not break on different OSs. |
| P1 | Update Generation Scripts | As a developer, I want my automation to not produce broken results. |

## Assumptions

- The `baseURL` in `hugo.toml` will remain `https://renatureforce.com/blog/`.

## Risks & Mitigations

- **Risk**: Broken links during renaming. -> **Mitigation**: Use a global search-and-replace to update all markdown files after renaming folders.

## Tradeoff

- **Relative vs. Absolute Paths**: We will use site-relative paths (starting with `/`) to ensure compatibility across all pages, assuming the `baseURL` handles the context.

## Business Benefits/Impact/Metrics

**Success Metrics:**
- 100% of retrofitted articles display visuals correctly.

## Stakeholders / Owners

| Name | Team/Org | Role | Note |
| :---- | :---- | :---- | :---- |
| Pickle Rick | Engineering | God-Tier Architect | Fixer of all things. |
| Morty | Engineering | Junior Assistant | Observer of greatness. |
