---
id: f17b1
title: Fix Image Render Hook
status: Todo
priority: High
order: 10
created: 2026-03-04
updated: 2026-03-04
links:
  - url: ../linear_ticket_parent.md
    title: Parent Ticket
---

# Description

## Problem to solve
The `layouts/_default/_markup/render-image.html` hook outputs absolute paths like `/images/...` which fail on the live site's `/blog/` subpath.

## Solution
Use Hugo's `relURL` function to ensure paths are correctly prefixed with the site's subpath.

## Implementation Details
- Edit `layouts/_default/_markup/render-image.html`.
- Wrap the `$src` and `$webp` variables in `relURL` before passing them to `safeURL`.
- Verify that the generated HTML in a test build uses the correct prefix.
