# Research: Phase 9 - Mandatory Bilingual Core

## 1. Bilingual Content Strategy
- **Option A (Simultaneous):** Ask Gemini to output both versions in one response.
    - *Risk:* Exceeding token limits, inconsistent quality, mixed language errors.
- **Option B (Sequential):** Generate DE first, then use it as a source for EN translation.
    - *Pros:* Highest consistency, semantic parity, full utilization of 8k output tokens for each version.
    - *Choice:* Option B is preferred for professional quality.

## 2. Hugo Multilingual Mechanics
- **Linkage:** Hugo uses the relative path under the language directory to link translations.
- **Requirement:** 
    - `content/de/posts/my-slug.md`
    - `content/en/posts/my-slug.md`
- **Slug Management:** The writer script must generate a slug based on the *primary* title (usually German) and reuse it for the English filename.

## 3. Metadata Parity
- **Front Matter:** Must include a `language` key (`de` or `en`).
- **Translations:** Titles, descriptions, and categories should be localized. Tags can remain consistent (English is common in ontology) or be localized.

## 4. Prompt Engineering Requirements
- `writer-v1.md` needs a new section detailing the "Translation Pass" logic.
- Instructions must emphasize that the English version is a *semantic mirror*, not a literal translation, ensuring the "Avantgarde Prestige" tone is maintained in both.
