# Phase 9 State: Mandatory Bilingual Core

## Summary
Refactor the `writer-agent` to ensure that every generation cycle results in a matched pair of German and English articles. This involves script logic changes and system prompt updates to maintain 100% content parity.

## Current Phase
[x] 1. Research
[x] 2. Planning
[x] 3. Verification

## Tasks
- [x] Research optimal generation strategy (Sequential Pass).
- [x] Update `scripts/writer.py` to handle dual-file output (DE + EN).
- [x] Refine `context/agent-prompts/writer-v1.md` for bilingual instructions and mandatory `language` key.
- [x] Refactor `scripts/image.py` to process all drafts and generate localized JSON captions.
- [x] Refactor `scripts/designer.py` to audit multiple files and aggregate results.
- [x] Locally verify bilingual pair generation and localized visual integration.
