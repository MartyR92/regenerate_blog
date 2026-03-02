# Phase 8 State: Diagram Rendering & Language Fixes

## Summary
Investigate and resolve issues with technical diagram rendering and ensure that image descriptions are localized to the post's language without internal agent metadata.

## Current Phase
[x] 1. Research
[x] 2. Planning
[x] 3. Verification

## Tasks
- [x] Investigate SVG/WebP rendering failure (pathing vs structure).
- [x] Research language detection methods for `image.py`.
- [x] Update `image.py` to generate reader-facing, localized captions.
- [x] Relocate diagram output to `static/images/` for Hugo compatibility.
- [x] Verify localized caption generation (DE detected for German posts).
