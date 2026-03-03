<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- Markdown will reference images using root-relative paths (e.g. `/blog/images/...`).
- The image-agent will store generated SVG/WebP files in a global static folder (`static/images/...`).
- The agent will use standard Markdown syntax (`![alt](path)`) to insert images.
- Host/domain prefix application will rely on Hugo's `baseURL` config to allow the Cloudflare worker to intercept properly.
- The system will generate both SVG and WebP for everything.
- Hugo handles fallback via the `<picture>` tag.
- Dark/light mode is handled via SVG embedded CSS (`currentColor` or media queries).
- The agent compresses raster formats (WebP) during generation using standard CLI tools.
- WebP fallback generation happens synchronously (blocking) with SVG generation.
- The paired SVG and WebP files will share the exact same filename, with different extensions.
- If generating either the SVG or WebP fails entirely, halt the pipeline and report an error.
- Injecting the `<picture>` tag should use the "most reliable approach" (e.g., a robust custom Hugo shortcode or guaranteed HTML injection).
- The `image-agent` and `staging-agent` will use a shared project-wide token.
- They require Read & Write access.
- API keys will be injected into the CI/CD pipeline via GitHub Repository Secrets.
- If the Interactions API hits a rate limit or becomes unavailable, halt the pipeline and report an error.
- SVGs must always preserve their internal aspect ratio when scaling down for mobile screens.
- Responsive logic (e.g. adapting to screen widths) will be implemented using media queries inside the SVG code.

### Claude's Discretion
- Maximum width constraints for SVGs on large desktop screens.
- Behavior of text elements inside SVGs on small mobile screens.
- The most reliable solution for all other topics and assets which remain unclear (e.g., Error State UI, API Response Parsing, Hugo Build Integration, Caching & CDN Strategy).

### Deferred Ideas (OUT OF SCOPE)
- None — discussion stayed within phase scope.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| VIS-01 | Fix broken diagram, graph, chart, and image rendering in the browser view on `renatureforce.com/blog`. | Hugo Markdown render hooks (`render-image.html`), SVG/WebP generation in Python, base URL pathing. |
| VIS-02 | Verify and grant (if necessary) staging and image-agent access to Interactions API. | GitHub Actions permissions and secret management. Python `requests` with Interactions API. |
</phase_requirements>

# Phase 11: Visual Infrastructure & Rendering - Research

**Researched:** 2026-03-03
**Domain:** Image generation, responsive rendering (SVG/WebP fallback), API access in CI/CD.
**Confidence:** HIGH

## Summary

This phase addresses the reliable rendering of images and diagrams on the live site (`renatureforce.com/blog`) and ensuring agents have proper Google Interactions API access. 
Currently, the `image-agent` generates SVGs via Gemini and saves them to `static/images/` but does not generate WebP fallbacks. Markdown references use `/images/...` which breaks if the site is served under `/blog`. The Hugo theme (Blowfish) intercepts image rendering, which needs to be customized to correctly serve SVG with WebP fallback using `<picture>` tags, handling the `/blog` base URL properly. Furthermore, API tokens need to be configured for Google Interactions API in the `.github/workflows` files.

**Primary recommendation:** Override the Hugo Markdown render hook for images (`layouts/_default/_markup/render-image.html`) to output `<picture>` elements for WebP and SVG formats seamlessly, and update `scripts/image.py` to use `cairosvg` or similar tool to generate WebP fallbacks synchronously.

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| `cairosvg` | latest | Converting SVG to raster | Standard Python library for SVG parsing and rasterization |
| `Pillow` (PIL) | latest | Converting raster to WebP | De-facto Python imaging library for WebP compression |
| Hugo render hooks | v0.143 | Customizing markdown image output | Native Hugo feature for `<picture>` tag injection without changing markdown syntax |

## Architecture Patterns

### Recommended Project Structure
```text
layouts/
└── _default/
    └── _markup/
        └── render-image.html   # Custom override for <picture> tags with WebP/SVG
static/
└── images/
    └── 2026/
        └── [slug]/
            ├── diagram.svg
            └── diagram.webp    # Synchronously generated fallback
```

### Pattern 1: Hugo Picture Render Hook
**What:** Overriding default markdown image rendering to support SVG + WebP.
**When to use:** Whenever `![alt](/blog/images/file.svg)` is used in markdown.
**Example:**
```html
{{ $src := .Destination }}
{{ $base := replaceRE "\.svg$" "" $src }}
<picture>
  <source srcset="{{ $base }}.webp" type="image/webp">
  <img src="{{ $src | relURL }}" alt="{{ .Text }}" loading="lazy" style="max-width: 100%; height: auto;">
</picture>
```

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| SVG to WebP conversion | Custom parsing | `cairosvg` + `Pillow` | Handles complex SVG standards and embedded fonts properly. |
| Markdown custom syntax | Custom regex in python | Hugo Render Hooks | Hugo handles all edge cases in standard markdown parsing natively. |

## Common Pitfalls

### Pitfall 1: BaseURL Mismatch in Relative Paths
**What goes wrong:** Images render in development but 404 on the live site (`renatureforce.com/blog`).
**Why it happens:** Markdown uses `/images/file.svg` which resolves to the domain root, ignoring the `/blog` subpath.
**How to avoid:** Use `{{ .Destination | relURL }}` or `absURL` inside the Hugo render hook, or write the markdown explicitly as `/blog/images/...` as specified in context.

### Pitfall 2: API Rate Limiting breaking CI
**What goes wrong:** Image agent fails silently or crashes on quota limits.
**Why it happens:** External APIs (Gemini/Interactions API) often have strict rate limits.
**How to avoid:** Implement exponential backoff, but since the pipeline requires halting on error (per decisions), ensure clean exit codes (`sys.exit(1)`) so GitHub Actions marks the run as failed.

## Sources
### Primary (HIGH confidence)
- User Context - Pathing strategies and API constraints.
- `.github/workflows/image-agent.yml` and `scripts/image.py` - Current codebase structure.
- `themes/blowfish/layouts/_default/_markup/render-image.html` - Current theme implementation.

## Metadata
**Confidence breakdown:**
- Standard stack: HIGH - Python conversion libraries assumed standard.
- Architecture: HIGH - Hugo render hooks are the correct standard path.
- Pitfalls: HIGH - Pathing under subdirectories is a notorious Hugo issue.

**Research date:** 2026-03-03
**Valid until:** 2026-04-03