# Requirements: Visual Integrity & Bilingual Content Parity

## 1. Goal
Achieve professional visual standards for technical diagrams and ensure 100% bilingual content parity (DE+EN) for every blog post.

## 2. Diagram Fixes & Consistency
### 2.1 Technical Rendering
- Debug and fix the SVG/WebP rendering issue identified in the screenshot.
- Ensure diagrams use the "Organic Precision" aesthetic (Micro) or "Terrain Depth" (Macro) as per Brand Guidelines v4.0.
### 2.2 Language-Aware Descriptions
- The `image-agent` must detect the primary language of the post and output the description/caption in the matching language.
- Descriptions must be "Reader-Facing" (describing the data/visuals).
- **Prohibited:** Never include internal metadata like "created by image-agent" in reader-facing captions.

## 3. Mandatory Bilingual Workflow
### 3.1 Content Parity
- The `writer-agent` must be reconfigured to ALWAYS output a pair of files: one in German (`content/de/posts/`) and one in English (`content/en/posts/`).
- The translations must be of equal quality and depth (1,500 - 3,000 words each).
### 3.2 Automated Linkage
- Ensure Hugo's relative path matching correctly links the DE and EN versions for the language switcher.

## 4. Content Cleanup & Quality
### 4.1 Post Repair
- Identify and replace low-quality/placeholder posts (e.g., `2026-02-28-...md` and `hello-world.md` if necessary).
- Ensure all published posts meet the 1,500+ word count requirement.
### 4.2 Title Uniqueness
- Implement strict title uniqueness rules to prevent keyword recurrence (e.g., avoiding "Algorithmisch" in every title).

## 5. Deployment Success
- **Success Criteria:** A single production deployment that contains identical DE and EN versions of the same new article, with functional SVG diagrams and a working language switch.
