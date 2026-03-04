# Fix Broken Visuals on Live Site PRD (v2 - Verification Heavy)

## HR Eng

| Fix Broken Visuals PRD |  | Resolving the "invisible visuals" issue on the live site by fixing root-relative pathing and ENSURING verification via browser. |
| :---- | :---- | :---- |
| **Author**: Pickle Rick **Contributors**: Morty **Intended audience**: Engineering, Design | **Status**: Draft **Created**: 2026-03-04 | **Self Link**: [Link] **Context**: [Link] 

## Introduction

The blog visuals (hero images and technical visuals) are currently reported as broken on the live site (`https://renatureforce.com/blog/`). Previous attempts focused on build output, but this version mandates LIVE verification via browser automation to prove visual visibility.

## Problem Statement

**Current Process:** Visuals are referenced in markdown as `/images/2026/...`. The image render hook was updated to use `absURL`.
**Primary Users:** Readers of the live blog.
**Pain Points:** Images fail to load (404) or are invisible, despite build-level green lights.
**Importance:** High. Visuals are the soul of the blog.

## Objective & Scope

**Objective:** Ensure all images render correctly on the live deployment.
**Ideal Outcome:** All 9 articles show their hero images and technical visuals when viewed in a real browser.

### In-scope or Goals
- Use `browserbase` to visit `https://renatureforce.com/blog/`.
- Take screenshots of multiple posts to visually confirm image loading.
- Audit the console logs of the browser for 404 errors.
- Fix any remaining discrepancies between build output and live server behavior.

### Not-in-scope or Non-Goals
- Generating new visuals.

## Product Requirements

1. **Live Browser Verification**: Use the browser tool to visit the live site and confirm image rendering.
2. **Path Finalization**: Ensure the server-side configuration (likely GitHub Pages or similar) isn't mangling paths.
3. **Build Validation**: The `hugo` command must produce HTML that matches the browser's expectations.

### Critical User Journeys (CUJs)
1. **Visual Load (Live)**: A user visits a live blog post and sees all images loading correctly in the browser.

### Functional Requirements

| Priority | Requirement | User Story |
| :---- | :---- | :---- |
| P0 | Browser Verification | As a user, I want to SEE the images on the actual website. |
| P0 | Audit Browser Logs | As a developer, I want to confirm zero 404s in the browser console. |
| P1 | Standardize Naming | As a developer, I want to ensure encoding-safe filenames throughout. |

## Assumptions

- The `baseURL` is `https://renatureforce.com/blog/`.
- The user can provide a recent screenshot of the "broken" state if my own browser check fails to reproduce.

## Risks & Mitigations

- **Risk**: Caching on the live site. -> **Mitigation**: Use cache-busting or force-reload in the browser check.

## Tradeoff

- **Manual vs Automated Check**: Automated browser check is faster and more objective for a genius like me.

## Business Benefits/Impact/Metrics

**Success Metrics:**
- 100% visual confirmation via browser screenshots.
- 0 404 errors in browser console.

## Stakeholders / Owners

| Name | Team/Org | Role | Note |
| :---- | :---- | :---- | :---- |
| Pickle Rick | Engineering | God-Tier Architect | Fixer of all things. |
| Morty | Engineering | Junior Assistant | Observer of greatness. |
