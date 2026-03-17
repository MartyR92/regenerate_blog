# PydanticAI Hybrid Orchestrator Implementation Plan

## Overview
Replace the fragile, 10-workflow GitHub Actions setup with a PydanticAI-powered Stateful Orchestrator. It will utilize a multi-provider fallback router cycling through 9 available API keys (1x Claude, 3x Gemini, 5x OpenRouter) to provide 100% resilience against rate limits and ensure maximum execution speed and reliability.

## Scope Definition (CRITICAL)
### In Scope
- Create `scripts/orchestrator.py` using PydanticAI.
- Implement the "Hydra" Fallback Router logic to handle API limits (429s) and model fallbacks (Tier 1 -> Tier 2).
- Integrate Mercury 2, Claude 4.6, Gemini 3.1, and Nemotron 3 APIs.
- Set up OpenRouter fallback targets (Llama 4, Mistral Large 3, Cohere Command R+).
- Define Pydantic models for strict state and schema validation between agents.
- Replace `writer-agent.yml`, `editor-agent.yml`, etc. with `publish-pipeline.yml` and `local-sync.yml`.

### Out of Scope (DO NOT TOUCH)
- Changing the underlying Hugo static site generation mechanics.
- Modifying the visual aesthetic constraints (Organic Precision).
- Altering the fundamental structure of `content/` directories.

## Current State Analysis
- 10 distinct GitHub Action YAML files causing race conditions, slow execution times, and complex Git-based state passing.
- Hardcoded API calls in individual Python scripts (`scripts/writer.py`, `scripts/editor.py`, etc.) vulnerable to rate limits.
- No unified schema validation or automatic error correction loop between agents.

## Implementation Phases

### Phase 1: Core Orchestrator & Router Setup
- **Goal**: Establish the PydanticAI foundation and the Tiered Fallback Router.
- **Steps**:
  1. [ ] Install PydanticAI and dependencies (`pip install pydantic-ai openai anthropic google-genai`).
  2. [ ] Create `scripts/orchestrator.py` and define the `FallbackRouter` class to handle key cycling and retries.
  3. [ ] Configure the Tier 1 and Tier 2 model mappings (Mercury 2, Claude 4.6, Gemini 3.1, Nemotron 3, Llama 4, Mistral, Cohere).
- **Verification**: Write a simple unit test to trigger an artificial 429 error and verify the router successfully falls back to a secondary OpenRouter model.

### Phase 2: Agent Definition & Schema Design
- **Goal**: Recreate the 10 agents as PydanticAI `Agent` objects with strict input/output schemas and inject specific, high-end `.gemini/skills` prompts into their system definitions.
- **Steps**:
  1. [ ] Define Pydantic `BaseModel` classes for each agent's output (e.g., `DraftState`, `EditorialFeedback`, `VisualAssets`).
  2. [ ] Map and inject relevant `.gemini/skills` as core system prompts for each agent:
     - **Research Agent**: `deep-research`, `research-engineer`, `citation-management`, `scientific-writing`
     - **Writer Agent**: `beautiful-prose`, `avoid-ai-writing`, `copywriting`, `seo-content-writer`, `content-creator`
     - **Editor Agent**: `professional-proofreader`, `seo-content-auditor`, `research-reviewer`, `brand-guidelines`
     - **Image/Visual Agents**: `ui-ux-pro-max`, `frontend-design`, `canvas-design`, `data-visualization`
     - **Designer/Staging Agents**: `web-design-guidelines`, `baseline-ui`, `accessibility-compliance-accessibility-audit`, `ui-ux-pro-max`
     - **Distribution Agent**: `social-orchestrator`, `seo-meta-optimizer`, `email-sequence`
  3. [ ] Initialize PydanticAI agents (Research, Writer, Editor, Image, Visual, Designer, Staging, Publish) injecting the router and the mapped skill prompts.
  4. [ ] Implement the in-memory state graph to pass the `Context` seamlessly between agents.
- **Verification**: Run a mock state-passing test locally. Ensure the Editor agent receives the exact Pydantic schema output by the Writer agent without Git commits, and verifies the response aligns with the injected skill guidelines.

### Phase 3: Hybrid Workflow & CI/CD Consolidation
- **Goal**: Bridge the local drafting process with the cloud execution and clean up old GitHub Actions.
- **Steps**:
  1. [ ] Add CLI arguments to `orchestrator.py` (`--draft` for local Mercury 2 execution, `--publish` for full cloud execution).
  2. [ ] Create `.github/workflows/publish-pipeline.yml` to trigger the cloud execution upon pushing to `_drafts/`.
  3. [ ] Delete the deprecated individual agent YAML files.
- **Verification**: Trigger the `publish-pipeline.yml` in GitHub Actions. Monitor the logs to verify the orchestrator completes the full lifecycle and pushes the final article to the `main` branch.

### Phase 4: Security-Audit and implementation
- **Goal**: Ensure the API keys, context handling, and network requests are securely managed, utilizing the `secrets-management` patterns.
- **Steps**:
  1. [ ] Audit `.github/workflows/publish-pipeline.yml` for exposed environment variables. Ensure all keys (Anthropic, Gemini, OpenRouter) are strictly injected via GitHub Secrets without being echo'd to logs.
  2. [ ] Audit `scripts/orchestrator.py` to prevent payload leakage of API keys during logging/exception handling.
  3. [ ] Implement validation around data fetched by the Research Agent to prevent prompt injection or execution of malicious payloads.
- **Verification**: Review execution logs to ensure keys are masked, and attempt a dummy prompt injection through a mock RSS feed/source to verify the system's resilience.

### Phase 5: Test, Verify and Deploy
- **Goal**: Perform End-to-End (E2E) testing of the entire hybrid workflow and merge to production.
- **Steps**:
  1. [ ] Run a local test with `python scripts/orchestrator.py --draft` to ensure Mercury 2 accurately drafts a blog post into `_drafts/`.
  2. [ ] Push the draft to trigger `publish-pipeline.yml` in a staging environment.
  3. [ ] Monitor the PydanticAI execution loop in the Actions runner for accurate agent handoffs and model fallback triggering (e.g., simulating a 429).
  4. [ ] Verify the final generated markdown, visual assets, and site build on the staging branch.
- **Verification**: If all tests pass and the generated site is flawless, merge the PydanticAI orchestrator into `main` and fully deprecate the legacy pipeline.
