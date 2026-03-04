---
id: a3c92
title: Standardize Front Matter and Markdown Pathing
status: Todo
priority: High
order: 20
created: 2026-03-04
updated: 2026-03-04
links:
  - url: ../linear_ticket_parent.md
    title: Parent Ticket
---

# Description

## Problem to solve
`featureImage` in front matter and some inline markdown references might still use inconsistent prefixes or redundant paths.

## Solution
Audit and normalize all `featureImage` and inline image paths to start with `/images/2026/` (site-relative) and rely on Hugo's processing.

## Implementation Details
- Scan all `content/**/*.md` for `featureImage` and `![]()` references.
- Ensure they all start with `/images/` (no `/blog/` prefix in the source markdown, as Hugo/theme should handle it).
- Verify consistency across languages (DE/EN).
