---
id: parent
title: "[Epic] Fix Broken Visuals on Live Site"
status: Backlog
priority: High
order: 0
created: 2026-03-04
updated: 2026-03-04
links:
  - url: ../../prd.md
    title: PRD
---

# Description

## Problem to solve
Visuals are broken on the live site because of incorrect root-relative paths that bypass the `/blog/` subpath.

## Solution
Update the render hook to use `relURL` and normalize all paths across the blog.

## Implementation Details
- Fix the render hook in `layouts/_default/_markup/render-image.html`.
- Normalize markdown and front matter paths.
- Verify the final build output in `public/`.
