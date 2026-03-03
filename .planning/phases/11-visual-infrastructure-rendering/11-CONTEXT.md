# Phase 11: Visual Infrastructure & Rendering - Context

**Gathered:** 2026-03-03
**Status:** Ready for planning

<domain>
## Phase Boundary

Fixing the rendering of diagrams, graphs, charts, and images (SVG/WebP paths) on the live site (`renatureforce.com/blog`) and ensuring the `staging-agent` and `image-agent` have the correct API permissions to the Google Interactions API.
</domain>

<decisions>
## Implementation Decisions

### Asset Pathing Strategy
- Markdown will reference images using root-relative paths (e.g. `/blog/images/...`).
- The image-agent will store generated SVG/WebP files in a global static folder (`static/images/...`).
- The agent will use standard Markdown syntax (`![alt](path)`) to insert images.
- Host/domain prefix application will rely on Hugo's `baseURL` config to allow the Cloudflare worker to intercept properly.

### Image Format & Fallbacks
- The system will generate both SVG and WebP for everything.
- Hugo handles fallback via the `<picture>` tag.
- Dark/light mode is handled via SVG embedded CSS (`currentColor` or media queries).
- The agent compresses raster formats (WebP) during generation using standard CLI tools.
- WebP fallback generation happens synchronously (blocking) with SVG generation.
- The paired SVG and WebP files will share the exact same filename, with different extensions.
- If generating either the SVG or WebP fails entirely, halt the pipeline and report an error.
- Injecting the `<picture>` tag should use the "most reliable approach" (e.g., a robust custom Hugo shortcode or guaranteed HTML injection).

### Interactions API Scoping
- The `image-agent` and `staging-agent` will use a shared project-wide token.
- They require Read & Write access.
- API keys will be injected into the CI/CD pipeline via GitHub Repository Secrets.
- If the Interactions API hits a rate limit or becomes unavailable, halt the pipeline and report an error.

### Responsive Behavior (SVG)
- SVGs must always preserve their internal aspect ratio when scaling down for mobile screens.
- Responsive logic (e.g. adapting to screen widths) will be implemented using media queries inside the SVG code.

### Claude's Discretion
- Maximum width constraints for SVGs on large desktop screens.
- Behavior of text elements inside SVGs on small mobile screens.
- The most reliable solution for all other topics and assets which remain unclear (e.g., Error State UI, API Response Parsing, Hugo Build Integration, Caching & CDN Strategy).
</decisions>

<specifics>
## Specific Ideas

- Focus on maximum reliability across the board. Whenever an edge case arises, choose the most robust and failure-proof approach.

</specifics>

<deferred>
## Deferred Ideas

- None — discussion stayed within phase scope.

</deferred>

---

*Phase: 11-visual-infrastructure-rendering*
*Context gathered: 2026-03-03*