---
id: d5e83
title: Verify Build Output
status: Todo
priority: Medium
order: 30
created: 2026-03-04
updated: 2026-03-04
links:
  - url: ../linear_ticket_parent.md
    title: Parent Ticket
---

# Description

## Problem to solve
We need to ensure that the changes actually result in correct paths in the built HTML files in `public/`.

## Solution
Run a full Hugo build and grep the output HTML for correct image `src` and `srcset` attributes.

## Implementation Details
- Run `hugo --gc --minify`.
- Search `public/**/*.html` for `src="/blog/images/2026/..."`.
- Confirm that the hero images also show up correctly in the HTML.
